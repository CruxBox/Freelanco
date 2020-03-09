from django.urls import path
from .views import (
    all_orders,
    display_cart_items,
    item_list
)

urlpatterns +=[
    path('',item_list, name='list view'),
    path()
]