from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import (
	HomeView,
	laundry_details,
	OrderSummaryView,
	add_single_to_cart,
	add_to_cart,
	remove_from_cart,
	remove_single_from_cart,
	user_profile,

laundry_dashboard,
laundry_menu,

)
app_name = 'core'
urlpatterns = [
	path('', HomeView.as_view(), name='home'),
	path('menu/<int:laundry_id>/', laundry_details, name='menu'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('view-cart/', OrderSummaryView.as_view(), name='view-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-single-item-from-cart/<slug>/',
         remove_single_from_cart, name='remove-single-from-cart'),
    path('add-single-to-cart/<slug>/',
         add_single_to_cart, name='add-single-to-cart'),
	path('profile',user_profile,name='user-profile'),

    path('seller/dashboard',laundry_dashboard, name="seller_dash"),

    path('seller/menu', laundry_menu, name="seller-menu")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)