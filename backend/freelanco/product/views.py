from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from users.decorators import *
from datetime import datetime
from .models import Item, OrderItem, Order
from .forms import *
import logging

logger = logging.getLogger(__name__)

def item_list(request):
	name_filter=request.GET.get('search', '')
	if name_filter:
		items=Item.objects.filter(Q(title__icontains=name_filter) | Q(description__icontains=name_filter))
	else:
		items=Item.objects.all()
	if items.exists():
		context = {
			'items': items,
			'items_exist': True
		}
	else:
		context = {
			'items_exist': False
		}
	return render(request, "services_temp/service_providers.html", context)

@login_required
@only_customer
def display_cart_items(request):

	order_objects = Order.objects.filter(user=request.user.customer_profile , ordered = False)
	print(order_objects)
	if order_objects.exists() and len(order_objects[0].items.all()):

		order_items = order_objects[0].items.all()
		items = Item.objects.filter(orderitem__in = order_items)
		number_of_items = len(items)
		
		sub_total = 0

		for item in items:
			sub_total = item.discounted_cost

		context = {
			'cart_items': items,
			'items_exist': True,
			'number_of_items': number_of_items,
			'sub_total': sub_total,
			'tax':0
		}
	else:
		context = {
			'items_exist': False,
			'sub_total':0,
			'tax':0
		}
	return render(request, "services_temp/cart.html", context)

@login_required
@only_customer
def old_orders(request):
	# This will give a list of orders that are now history
	order_objects = Order.objects.filter(user=request.user.customer_profile , ordered = True)
	if order_objects.exists():
		context={
			'order_exists':True,
			'orders':order_objects
		}
	else:
		context = {
			'order_exists':False
		}
	return render(request, "base.html", context)

# Add item
@login_required
@only_customer
def add_to_cart(request, pk):
	item = get_object_or_404(Item, pk=pk)
	print(item.title)
	orderItem, created = OrderItem.objects.get_or_create(
		item = item,
		user = request.user.customer_profile,
		ordered = False
	)

	cart = Order.objects.filter(user = request.user.customer_profile, ordered=False)
	#print(cart.exists)
	#print(cart.items)
	if cart.exists():
		cart = cart[0]
		if cart.items.filter(item = item).exists():
			pass

		else:
			cart.items.add(orderItem)

	else:
		cart = Order.objects.create( user = request.user.customer_profile )
		cart.items.add(orderItem)

	return redirect("item list")

# Delete item
@login_required
@only_customer
def remove_from_cart(request,pk):
	item = get_object_or_404(Item, pk=pk)

	cart = Order.objects.filter(user = request.user.customer_profile, ordered=False)
	if cart.exists():
		cart = cart[0]
		orderItem = OrderItem.objects.filter(
										user = request.user.customer_profile,
										item = item
										)[0]
		cart.items.remove(orderItem)
		# else:
			# messages.info("This item wasn't present in your cart.")
	else:
		messages.info("You don't have an ongoing order.")
	return redirect("display cart items")

# Item detail view
def detail_view(request, pk):
	item = get_object_or_404(Item, pk = pk)

	context = {
		'item': item,
		'provider': item.provider
	}

	return render(request, 'base.html', context)


@login_required
@only_freelancer
def list_services(request):
	print(request.user)
	freelancer=request.user.freelancer_profile
	items=freelancer.items.all()
	print(items)
	context={
		'items':items
	}
	return render(request,'services_temp/seller_services_list.html',context)

# Place order - Need to work on this
# Add notifications feature in this feature


@login_required
@only_customer
def place_order(request):
	cust = request.user.customer_profile
	order = Order.objects.filter(user = cust, ordered = False)[0]
	order.setOrdered(True)
	orderItems = order.items.all()
	for orderItem in orderItems:
		#TODO: notify all providers
		orderItem.accepted = 0
		orderItem.save()

	order.ordered = True
	order.ordered_date = datetime.now()
	order.save()
	return HttpResponseRedirect(reverse("item list"))

@login_required
@only_freelancer
def show_completed_orders(request):
	provider = request.user.freelancer_profile
	items_provided = provider.items.all();
	ret_list = []
	for item in items_provided:
		orderItem = item.orderitem_set.all()
		if orderItem.exists() == False:
			continue
		print(orderItem[0].status)
		if orderItem[0].status == 2:
			ret_list += orderItem

	context = {'orders' : ret_list}
	return render(request, 'services_temp/seller_services_current.html', context)


@login_required
@only_freelancer
def current_requested_orders(request):
	provider = request.user.freelancer_profile
	items_provided = provider.items.all();
	# print(items_provided)
	ret_list = []
	for item in items_provided:
		orderItem = item.orderitem_set.all()
		if orderItem.exists() == False:
			continue
		print(orderItem,"lol")
		#orderItem = orderItem[0]
		print(orderItem[0].accepted)
		if orderItem[0].accepted == 0:
			ret_list += orderItem

	print(ret_list)
	context = {'orders' : ret_list}
	return render(request, 'services_temp/seller_services_current.html', context)


@login_required
@only_freelancer
def accept_order_item(request, pk):
	provider = request.user.freelancer_profile
	orderItem = OrderItem.objects.filter(pk=pk).first()
	orderItem.accepted = 1;
	orderItem.status = 2;
	orderItem.save()
	return HttpResponseRedirect(reverse("service_curr"))

@login_required
@only_freelancer
def reject_order_item(request, pk):
	provider = request.user.freelancer_profile
	orderItem = OrderItem.objects.filter(pk=pk).first()
	orderItem.accepted = 2;
	orderItem.status = 2;
	orderItem.save()

	return HttpResponseRedirect(reverse("service_curr"))

@login_required
@only_freelancer
def start_order_item(request, pk):
	provider = request.user.freelancer_profile
	orderItem = OrderItem.objects.filter(pk=pk).first()
	orderItem.accepted = 1;
	orderItem.status = 0;
	orderItem.save()

	return HttpResponseRedirect(reverse("service_curr"))


@login_required
@only_freelancer
def finished_order_item(request, pk):
	provider = request.user.freelancer_profile
	orderItem = OrderItem.objects.filter(pk=pk).first()
	orderItem.accepted = 1;
	orderItem.status = 2;
	orderItem.save()

	return HttpResponseRedirect(reverse("service_curr"))

@login_required
@only_freelancer
def edit_item(request, pk):
    if request.method=='POST':
        form=ItemEditForm(request.POST, instance=Item.objects.filter(pk = pk)[0])
        #print(form)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("service_list"))
    else:
        form3=ItemEditForm(instance=Item.objects.filter(pk = pk)[0])
        context={"form":form3}
        return render(request,'account/add_item.html',context)

@login_required
@only_freelancer
def add_item(request):
    if request.method=='POST':
        form=ItemEditForm(request.POST)
        if form.is_valid():
            item = form.save(commit = False)
            item.provider = request.user.freelancer_profile
            item.save();
            return HttpResponseRedirect(reverse("service_list"))
    else:
        form3=ItemEditForm()
        context={"form":form3}
        return render(request,'account/add_item.html',context)

@login_required
@only_freelancer
def delete_item(request, pk):
    item=Item.objects.get(pk = pk)
    if request.method=='POST':
        item.delete()
        return HttpResponseRedirect(reverse("service_list"))