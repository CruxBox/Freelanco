from django.shortcuts import render
from .models import Item, OrderItem, Order

def item_list(request):
    items = Item.objects.all()
    if items.exist():
        context = {
            'items': items,
            'items_exist': True
        }
    else:
        context = {
            'items_exist': False
        }
    render(request, "base.html", context)

def display_cart_items(request):
    order_objects = Order.objects.filter(user=request.user, ordered = False)
    if order_objects.exists():
        items = order_objects[0].items
        context = {
            'cart_items': items,
            'items_exist': True
        }
    else:
        context = {
            'items_exist': False
        }
    render(request, "base.html", context)

def all_orders(request):
    # This will give a list of orders that are now history
    order_objects = Order.objects.filter(user=request.user, ordered = True)
    if order_objects.exists():
        context={
            'order_exists':True,
            'orders':order_objects
        }
    else:
        context = {
            'order_exists':False
        }
    render(request, "base.html", context)

# Add item
# Delete item
# Place order
# Item detail view
