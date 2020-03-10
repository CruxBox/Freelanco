from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from .views import add_customer

urlpatterns = [
	path('',include('allauth.urls')),
	path('profile',add_customer)
]
