from django.urls import path
from .views import (
	all_orders,
	display_cart_items,
	item_list,
	remove_from_cart,
	add_to_cart,
	old_orders,
	display_cart_items
)

urlpatterns = [
	path('',item_list, name='item list'),
	path('service/<slug>',detail_view,name='detail view'),
	path('add_to_cart/<slug>', add_to_cart, name='add to cart'),
	path('remove_from_cart/<slug>', remove_from_cart, name='remove from cart'),
	path('old_orders/', old_orders, name='old orders'),
	path('show_cart/', display_cart_items, name='display cart items')
]