from django.db import models
from django.contrib.auth.models import User

from django.conf import settings
from django.shortcuts import reverse
from django.utils import timezone

import datetime
from django_countries.fields import CountryField

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)
ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)


def order_time():
    return timezone.now()


class Laundry(models.Model):  # this is to create a new model for retaurant
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='laundry')  # OneToOneField  is to ensure that one user have only one
    # restarant.
    name = models.CharField(max_length=500)
    phone = models.CharField(max_length=500)
    address = models.CharField(max_length=500)
    logo = models.ImageField(upload_to='laundry_logo/', blank=False)
    slug = models.SlugField(blank=True, null=True)

    def __str__(self):
        return self.address

    def getimage(self):
        if self.logo and hasattr(self.logo, 'url'):
            return self.logo.url

    def get_absolute_url(self):
        return reverse("core:menu", kwargs={
            'id': self.id
        })


class Customer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='customer')
    name = models.CharField(max_length=50, default="Customer")
    image = models.ImageField(upload_to="profile_images/",
                              blank=True)
    phone = models.CharField(max_length=500, blank=True)
    address = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.name

    def getimage(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return "https://www.w3schools.com/howto/img_avatar.png"


class Service(models.Model):
    laundry = models.ForeignKey(Laundry, on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    short_description = models.CharField(max_length=500)
    image = models.ImageField(upload_to='service_images/', blank=False)
    price = models.IntegerField(default=0)
    slug = models.SlugField(blank=True, null=True)

    def getimage(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

    def get_add_to_cart_url(self):
        return reverse(
            "core:add-to-cart",
            kwargs={
                'slug': self.slug
            }
        )

    def get_remove_from_cart_url(self):
        return reverse(
            "core:remove-from-cart",
            kwargs={
                'slug': self.slug
            }
        )

    def add_single_url(self):
        return reverse(
            "core:add-single-to-cart",
            kwargs={
                'slug': self.slug
            }
        )

    def remove_single_url(self):
        return reverse(
            "core:remove-single-from-cart",
            kwargs={
                'slug': self.slug
            }
        )

    def __str__(self):
        return self.name


class OrderItem(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 on_delete=models.CASCADE)
    item = models.ForeignKey(Service,
                             on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.name}"

    def get_final_price(self):
        return self.item.price * self.quantity


class Order(models.Model):
    CANCELLED_BY_CLIENT = "cancelled_by_client"
    NEW = "new"
    ORDER_STATUS = [(NEW, "New"), ("finalized", "Finalized"), ("rejected", "Rejected"),
                    (CANCELLED_BY_CLIENT, "Cancelled by client")]
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, null=True)
    items = models.ManyToManyField(OrderItem)
    laundry = models.ForeignKey(Laundry,
                                on_delete=models.CASCADE, null=True)
    name = models.CharField(null=True, max_length=100)
    ordered = models.BooleanField(default=False)

    order_time = models.DateTimeField(default=order_time)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=ORDER_STATUS,
                              default="new", max_length=100)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total

    def save(self, *args, **kwargs):
        ''' on Save update TimeStamp '''
        if not self.id:
            self.created = timezone.now()
        return super(Order, self).save(*args, **kwargs)


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    notification_text = models.CharField(max_length=500)
    notification_time = models.TimeField(auto_now_add=True)
    ordered_time = models.DateTimeField(auto_now_add=False)


class CouponUsed(models.Model):
    order = models.ForeignKey(Order, on_delete=False)
    laundry = models.ForeignKey(Laundry, on_delete=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'
