from django.urls import path
from .views import *

urlpatterns = [
	path('',item_list, name='item list'),
	path('service/<int:pk>',detail_view,name='detail view'),
	path('add_to_cart/<int:pk>', add_to_cart, name='add to cart'),
	path('remove_from_cart/<int:pk>', remove_from_cart, name='remove from cart'),
	path('old_orders/', old_orders, name='old orders'),
	path('show_cart/', display_cart_items, name='display cart items'),
	path('my_services/',list_services,name='service_list'),
	path('current_orders/', current_requested_orders, name = 'service_curr'),
	path('add_item', add_item, name='add new item'),
	path('edit_item/<int:pk>/', edit_item, name='edit item'),
	path('place_order', place_order, name='place order'),
	path('acceptorder/<int:pk>', accept_order_item, name='accept order'),
	path('rejectorder/<int:pk>', reject_order_item, name='reject order')
]