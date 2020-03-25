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
	path('profile/view',view=edit_customer_profile,name='profile_view'),
	path('login/',view=user_login,name='login'),
	path('logout/',view=user_logout,name="logout"),
	path('',include('django.contrib.auth.urls')),
	#path('login'),
	#path()
]
