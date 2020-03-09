from django.shortcuts import render
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
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

def old_orders(request):
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
@login_required
def add_to_cart(request, slug):
	item = get_object_or_404(Item, slug=slug)
	orderItem, created = OrderItem.objects.get_or_create(
		item = item,
		user = request.user,
		ordered = False
	)

	cart = Order.objects.filter(user = request.user, ordered=False)
	if cart.exists():
		cart = cart[0]
		if cart.items.filter(items__slug = slug).exists():
#			orderItem.quantity+=1
#			orderItem.save()
			messages.info("Already in cart!")
		else:
#			orderItem.quantity = 1
#			orderItem.save()
			cart.items.add(orderItem)
	else:
		cart = Order.objects.create( user = request.user )
#		orderItem.quantity = 1
#		orderItem.save()
		cart.items.add(orderItem)

# Delete item
@login_required
def remove_from_cart(request,slug):
	item = get_object_or_404(Item, slug=slug)

	cart = Order.objects.filter(user = request.user, ordered=False)
	if cart.exists():
		cart = cart[0]
		if cart.items.filter(items__slug = slug).exists():
			orderItem = OrderItem.objects.filter(
											user = request.user,
											item = item
											)[0]
			cart.items.remove(orderItem)
		else:
			messages.info("This item wasn't present in your cart.")
	else:
		messages.info("You don't have an ongoing order.")

# Item detail view
def detail_view(request, slug):
	item = get_object_or_404(Item, slug = slug)

	context = {
		'item': item
		'provider': item.provider
	}

	render(request, 'base.html', context)


# Place order - Need to work on this
# Add notifications feature in this feature