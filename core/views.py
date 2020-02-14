
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)
from .models import (
    Laundry,
    Customer,
    Service,
    Order,
    OrderItem,
    Notification,
    CouponUsed,
    Address
)



class HomeView(ListView):
    model = Laundry
    paginate_by = 10
    template_name = "home.html"


def laundry_details(request, laundry_id):
    laundry = Laundry.objects.get(pk=laundry_id)
    context = dict()
    try:
        services = Service.objects.filter(laundry_id=laundry_id)
        print(services)
        context = {
            'exists': True,
            'services': services,
            'seller': laundry
        }
        print(context)
        print("here")
        return render(request, "menu.html", context)
    except ObjectDoesNotExist:
        context = {
            'exists': False,
            'seller': laundry
        }
        print(context)
        return render(request, "menu.html", context)


def get_laundry_object(obj):
    return obj.laundry_id


def add_to_cart(request, slug):
    print("Hello")
    item = get_object_or_404(Service, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item, customer=request.user)
    laundry = Laundry.objects.get(id=item.laundry_id)
    order_qs = Order.objects.filter(
        user=request.user, laundry=laundry, ordered=False)

    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
        else:
            order.items.add(order_item)
            order_item.save()
    else:

        order = Order.objects.create(
            user=request.user, laundry=laundry)
        order.items.add(order_item)
    return redirect("core:menu", laundry.id)


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.filter(user=self.request.user, ordered=False)
            context = {'object': order}
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("/")


def remove_from_cart(request, slug):
    item = get_object_or_404(Service, slug=slug)
    laundry = Laundry.objects.get(id=item.laundry_id)
    order_qs = Order.objects.filter(
        user=request.user, laundry=laundry, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                customer=request.user
            )[0]
            order.delete()
        else:
            return redirect("core:menu", laundry.id)
    else:
        messages.error(
            request, "This item has not been addded to cart yet")
        return redirect("core:menu", laundry.id)
    return redirect("core:menu", laundry.id)


def add_single_to_cart(request, slug):
    item = get_object_or_404(Service, slug=slug)
    laundry = Laundry.objects.get(id=item.laundry_id)
    order_qs = Order.objects.filter(
        user=request.user,
        laundry=laundry,
        ordered=False
    )

    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                customer=request.user
            )[0]
            order_item.quantity += 1
            order_item.save()
            messages.success(request, "Quantity updated successfully")
            return redirect("core:view-cart")
        else:
            messages.error(request, "No order found for this item")
            return redirect("core:menu", id=laundry.id)
    else:
        messages.error(request, "This item wasnt added to cart")
        return redirect("core:menu", id=laundry.id)
    return redirect("core:home")


def remove_single_from_cart(request, slug):
    item = get_object_or_404(Service, slug=slug)
    laundry = Laundry.objects.get(id=item.laundry_id)
    order_qs = Order.objects.filter(
        user=request.user,
        laundry=laundry,
        ordered=False
    )

    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                customer=request.user
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.success(request, "Quantity updated successfully")
            return redirect("core:view-cart")
        else:
            messages.error(request, "No order found for this item")
            return redirect("core:menu", laundry.id)
    else:
        messages.error(request, "This item wasnt added to cart")
        return redirect("core:menu", laundry.id)
    return redirect("core:home")

def user_profile(request):
    customer, created = Customer.objects.get_or_create(user=request.user)
    context = {
        'customer': customer
    }
    print(context)
    return render(request, "profile.html", context)


def laundry_dashboard(request):
    current_orders = Order.objects.filter(laundry=request.user.laundry)
    context = {
        'orders': current_orders
    }
    return render(request, 'seller/dashboard.html', context)





def laundry_profile_form(request):
    return render(request, "seller/profile.html")


def laundry_menu(request):
    return render(request, "seller/menu.html")