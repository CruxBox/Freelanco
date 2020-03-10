from django.contrib import admin
from .forms import CustomChangeForm,CustomUserCreationForm
from django.contrib.auth import get_user_model
# Register your models here.
CustomUser=get_user_model()
class CustomUserAdmin(UserAdmin):
    model=CustomUser
    add_form=CustomUserCreationForm
    form=CustomUserChangeForm

admin.site.register(CustomUser,CustomUserAdmin)
