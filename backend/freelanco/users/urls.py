from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .views import *
app_name = 'users'

urlpatterns = [
	path('signup/customer',view=customer_signup,name='customer_signup'),
	path('signup/freelancer',view=freelancer_signup,name='freelancer_signup'),
	path('profile/view',view=view_customer_profile,name='profile_view'),
	#path('profile/edit',view=edit_customer_profile,name='profile_edit'),
	path('profile/edit/details',view=edit_customer_profile,name='profile_edit_details'),
	path('profile/edit/address/<int:pk>',view=edit_customer_address,name='profile_edit_address'),
	path('profile/add/address',view=add_customer_address,name='profile_add_address'),
	path('profile/delete/address/<int:pk>',view=delete_customer_address,name='profile_delete_address'),
	path('login/',view=user_login,name='login'),
	path('logout/',view=user_logout,name="logout"),
	path('',include('django.contrib.auth.urls')),
	#path('login'),
	#path()
]
