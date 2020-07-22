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
from itertools import chain

logger = logging.getLogger(__name__)


enum_acc=["Pending Approval","Accepted","Rejected"]
enum_stat=["Ongoing","Done","Not Started"]

def item_list(request):
	"""
	This function is used to list all the items that are offered by all active freelancers
	"""
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
	"""
	This function is used to display all cart items of a customer. The user is supposed to be
	logged and should be a customer, else throw a 403 Forbidden error
	"""
	order_objects = Order.objects.filter(user=request.user.customer_profile , ordered = False)

	if order_objects.exists() and order_objects[0].items.count():
		order_items = order_objects[0].items.all()
		items = Item.objects.filter(orderitem__in = order_items)
		number_of_items = len(items)
		sub_total = 0

		for item in items:
			if item.discounted_cost !=-1:
				sub_total += item.discounted_cost
			else:
				sub_total += item.actual_cost
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
	"""
	This function is used to display list of orders that are now history for a customer.
	The user is supposed to be logged and should be a customer, else throw a 403 Forbidden error
	"""
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
	"""
	This function is used to add an item to the cart of a customer. Can be called when trying to REORDER.
	The user is supposed to be logged and should be a customer, else throw a 403 Forbidden error
	Parameters to be passed in: Primary Key of the Item
	"""
	item = get_object_or_404(Item, pk=pk)
	orderItem, created = OrderItem.objects.get_or_create(
		item = item,
		user = request.user.customer_profile,
		ordered = False,
		accepted = 3
	)
	print(orderItem)
	print(orderItem.accepted)
	print(orderItem.status)
	cart = Order.objects.filter(user = request.user.customer_profile, ordered=False)
	if cart.exists():
		cart = cart[0]
		if cart.items.filter(item = item).exists():
			pass

		else:
			cart.items.add(orderItem)
	else:
		cart = Order.objects.create( user = request.user.customer_profile )
		cart.items.add(orderItem)

	print(cart.items.all())
	return redirect(request.META.get('HTTP_REFERER'))

# Delete item
@login_required
@only_customer
def remove_from_cart(request,pk):
	"""
	This function is used to remove an item to the cart of a customer.
	The user is supposed to be logged and should be a customer, else throw a 403 Forbidden error
	Parameters to be passed in: Primary Key of the Item
	"""
	item = get_object_or_404(Item, pk=pk)
	cart = Order.objects.filter(user = request.user.customer_profile, ordered=False)
	if cart.exists():
		cart = cart[0]
		orderItem = OrderItem.objects.filter(
										user = request.user.customer_profile,
										item = item,
										ordered = False,
										accepted = 3
										)
		print("all items")
		print(orderItem)
		orderItem = orderItem[0]
		cart.items.remove(orderItem)
	else:
		messages.info("This item wasn't present in your cart.")
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
	"""
	This function is used list all active items published by a freelancer.
	The user is supposed to be logged and should be a freelancer, else throw a 403 Forbidden error
	"""
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
	"""
	This function is used to place an order (during checkout).
	The user is supposed to be logged and should be a customer, else throw a 403 Forbidden error
	"""
	cust = request.user.customer_profile
	order = Order.objects.filter(user = cust, ordered = False)[0]
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
def show_completed_orders_freelancer(request):
	"""
	This function is used to show all the completed orders of a freelancer.
	The orders that were rejected or accepted and completed are shown here.
	The user is supposed to be logged and should be a freelancer, else throw a 403 Forbidden error
	"""
	provider = request.user.freelancer_profile
	items_provided = provider.items.all()
	ret_list = []
	for item in items_provided:
		# if accepted and done, if rejected
		acceptedAndDone = OrderItem.objects.filter(item = item, accepted = 1, status = 1)
		rejected = OrderItem.objects.filter(item = item, accepted = 2)
		ret_list = chain(ret_list, acceptedAndDone, rejected)

	context = {'orders' : ret_list}
	return render(request, 'services_temp/seller_services_done.html', context)


@login_required
@only_freelancer
def current_requested_orders(request):
	"""
	This function is used to list all the ongoing and requested orders on the freelancer page.
	The orders that were accepted and need to start/finish or the ones that need approval.
	The user is supposed to be logged and should be a freelancer, else throw a 403 Forbidden error
	"""
	provider = request.user.freelancer_profile
	items_provided = provider.items.all()
	#accepted=1,status!=1 and accepted = 0
	ret_list = []
	for item in items_provided:
		acceptedAndOngoing = OrderItem.objects.filter(item = item, accepted = 1).exclude(status = 1)
		notAccepted = OrderItem.objects.filter(item = item, accepted = 0)
		ret_list = chain(ret_list, notAccepted, acceptedAndOngoing)

	# print(ret_list)
	context = {'orders' : ret_list}
	return render(request, 'services_temp/seller_services_current.html', context)


@login_required
@only_freelancer
def accept_order_item(request, pk):
	"""
	This function is used accept an order item that is shown on the freelancer approval page.
	The user is supposed to be logged and should be a freelancer, else throw a 403 Forbidden error
	Parameters: Primary key of the order item
	"""
	provider = request.user.freelancer_profile
	orderItem = OrderItem.objects.filter(pk=pk)[0]
	orderItem.accepted = 1
	orderItem.status = 2
	orderItem.save()
	return HttpResponseRedirect(reverse("service_curr"))

@login_required
@only_freelancer
def reject_order_item(request, pk):
	"""
	This function is used reject an order item that is shown on the freelancer approval page.
	The user is supposed to be logged and should be a freelancer, else throw a 403 Forbidden error
	Parameters: Primary key of the order item
	"""
	provider = request.user.freelancer_profile
	orderItem = OrderItem.objects.filter(pk=pk)[0]
	orderItem.accepted = 2
	orderItem.status = 2
	orderItem.save()

	return HttpResponseRedirect(reverse("service_curr"))

@login_required
@only_freelancer
def start_order_item(request, pk):
	"""
	This function is used start an order item that is shown on the freelancer current order page.
	The user is supposed to be logged and should be a freelancer, else throw a 403 Forbidden error
	Parameters: Primary key of the order item
	"""
	provider = request.user.freelancer_profile
	orderItem = OrderItem.objects.filter(pk=pk)[0]
	orderItem.status = 0
	orderItem.save()
	return HttpResponseRedirect(reverse("service_curr"))


@login_required
@only_freelancer
def finished_order_item(request, pk):
	"""
	This function is used to finish an order item that is shown on the freelancer current order page.
	The user is supposed to be logged and should be a freelancer, else throw a 403 Forbidden error
	Parameters: Primary key of the order item
	"""
	provider = request.user.freelancer_profile
	orderItem = OrderItem.objects.filter(pk=pk)[0]
	orderItem.status = 1
	orderItem.save()
	return HttpResponseRedirect(reverse("service_curr"))

@login_required
@only_freelancer
def edit_item(request, pk):
	"""
	This function is used to edit an item that is shown on the freelancer item list.
	The user is supposed to be logged and should be a freelancer, else throw a 403 Forbidden error
	Parameters: Primary key of the Item
	"""
    if request.method=='POST':
        form=ItemEditForm(request.POST,request.FILES,instance=Item.objects.filter(pk = pk)[0])
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
	"""
	This function is used to add an item that is shown on the freelancer item list.
	The user is supposed to be logged and should be a freelancer, else throw a 403 Forbidden error
	Parameters: Primary key of the Item
	"""
    if request.method=='POST':
        form=ItemEditForm(request.POST,request.FILES)
        if form.is_valid():
            item = form.save(commit = False)
            item.provider = request.user.freelancer_profile
            item.save()
            return HttpResponseRedirect(reverse("service_list"))
    else:
        form3=ItemEditForm()
        context={"form":form3}
        return render(request,'account/add_item.html',context)

@login_required
@only_freelancer
def delete_item(request, pk):
	"""
	This function is used to delete an item that is shown on the freelancer item list.
	The user is supposed to be logged and should be a freelancer, else throw a 403 Forbidden error
	Parameters: Primary key of the Item
	"""
    item=Item.objects.get(pk = pk)
    if request.method=='POST':
        item.delete()
        return HttpResponseRedirect(reverse("service_list"))


@login_required
@only_customer
def show_completed_orders_customer(request):
	"""
	This function is used to show all completed orders to the customer.
	The order items that are rejected or are accepted and completed are shown here.
	The user is supposed to be logged and should be a customer, else throw a 403 Forbidden error
	"""
	# rejected, (accepted and completed)
	cust = request.user.customer_profile
	finishedOrderItems = cust.orderitem_set.filter(accepted = 1, status = 1)
	rejectedOrderItems = cust.orderitem_set.filter(accepted = 2)
	retList = chain(finishedOrderItems, rejectedOrderItems)
	print(retList)
	context={
		"items":retList
	}
	return render(request,'services_temp/order_history.html',context)

@login_required
@only_customer
def show_ongoing_orders_customer(request):
	"""
	This function is used to show all ongoing orders to the customer.
	The order items that are pending an approval or are accepted and ongoing are shown here.
	The user is supposed to be logged and should be a customer, else throw a 403 Forbidden error
	"""
	#pending approval, (accepted and ongoing)
	cust = request.user.customer_profile
	ongoingOrderItems = cust.orderitem_set.filter(accepted = 1, status = 0)
	pendingApprovalOrderItems = cust.orderitem_set.filter(accepted = 0)
	notStartOrderItems = cust.orderitem_set.filter(accepted = 1, status = 2)
	retList = chain(ongoingOrderItems, pendingApprovalOrderItems, notStartOrderItems)
	print(retList)
	context={
		"items":retList
	}
	return render(request,'services_temp/order_ongoing.html',context)