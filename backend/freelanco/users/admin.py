from django.contrib import admin
from .forms import CustomUserChangeForm,CustomUserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.
CustomUser=get_user_model()


admin.site.register(CustomUser)
admin.site.register(FreelancerProfile)
admin.site.register(CustomerProfile)
admin.site.register(Address)