from django.contrib import admin

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

admin.site.register(Laundry)
admin.site.register(Customer)
admin.site.register(Service)
admin.site.register(Order)
admin.site.register(OrderItem)
