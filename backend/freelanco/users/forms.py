from django import forms 
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth import get_user_model
from .models import *
CustomUser=get_user_model()
class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model=CustomUser
        fields=('username','email','is_freelancer')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model=CustomUser
        fields=('email','first_name','last_name')


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model=CustomerProfile
        fields=('location',)

class FreelancerProfileForm(forms.ModelForm):

    class Meta:
        models=FreelancerProfile
        fields=('location',)


class SignupForm(forms.Form):
    freelance=forms.BooleanField(required=False)
    def signup(self,request,user):
        user.is_freelancer=self.cleaned_data['freelance']
        if user.is_freelancer:
            profile=FreelancerProfile.objects.create(user=user)
        else:
            profile=CustomerProfile.objects.create(user=user)

class EditCustomerProfileForm(forms.ModelForm):
    class Meta:
        model=CustomerProfile
        fields=('location','image',)

class EditAddress(forms.ModelForm):

    class Meta:
        model=Address
        fields=('name','address1','address2','pin_code','city','state')
