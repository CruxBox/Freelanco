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
	path('completed_orders/',show_completed_orders_freelancer,name='service_done'),
	path('add_item', add_item, name='add new item'),
	path('edit_item/<int:pk>/', edit_item, name='edit item'),
	path('place_order', place_order, name='place order'),
	path('accept_order/<int:pk>', accept_order_item, name='accept order'),
	path('reject_order/<int:pk>', reject_order_item, name='reject order'),
	path('start_order/<int:pk>', start_order_item, name = 'start order'),
	path('finished_order/<int:pk>', finished_order_item, name = 'finish order'),
	path('completed_order_users/', show_completed_orders_customer, name = 'user completed orders'),
	path('ongoing_order_users/', show_ongoing_orders_customer, name = 'user ongoing orders'),
]