from django.urls import path
from .views import (
	display_cart_items,
	item_list,
	remove_from_cart,
	add_to_cart,
	old_orders,
	detail_view,
	list_services,
	add_item,
	edit_item
)

urlpatterns = [
	path('',item_list, name='item list'),
	path('service/<int:pk>',detail_view,name='detail view'),
	path('add_to_cart/<int:pk>', add_to_cart, name='add to cart'),
	path('remove_from_cart/<int:pk>', remove_from_cart, name='remove from cart'),
	path('old_orders/', old_orders, name='old orders'),
	path('show_cart/', display_cart_items, name='display cart items'),
	path('my_services/',list_services,name='list_services'),
	path('add_item', add_item, name='add new item'),
	path('edit_item', edit_item, name='edit item')
]