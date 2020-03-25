from django.shortcuts import render
from .forms import *
from allauth.account.forms import SignupForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from .models import *
# Create your views here.

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

def user_login(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('home'))
        else:
            return render(request,'temp/log1.html',{'not_exist':True})
    else:
        return render(request,'temp/log1.html',)


def customer_signup(request):
    if request.method=='POST':
        print("lol")
        username=request.POST['username']
        password1=request.POST['password1']
        password2=request.POST['password2']
        if not CustomUser.objects.filter(username=username).exists():
            user=CustomUser.objects.create_user(username, password=password1)
            user.is_freelancer=False
            user.save()
            cust_profile=CustomerProfile(user=user)
            cust_profile.save()
            user=authenticate(username=username,password=password1)
            login(request,user)
            return render(request,"temp/home.html")
        else:
           return render(request,"temp/signup.html",{"user_exists":True}) 
    else:
        return render(request,"temp/signup.html")

def freelancer_signup(request):
    if request.method=='POST':
        print("lol")
        username=request.POST['username']
        password1=request.POST['password1']
        password2=request.POST['password2']
        if not CustomUser.objects.filter(username=username).exists():
            user=CustomUser.objects.create_user(username, password=password1)
            user.is_freelancer=True
            user.save()
            cust_profile=FreelancerProfile(user=user)
            cust_profile.save()
            user=authenticate(username=username,password=password1)
            login(request,user)
            return render(request,"temp/home.html")
        else:
           return render(request,"temp/signup.html",{"user_exists":True}) 
    else:
        return render(request,"temp/signup.html")

@login_required
def view_customer_profile(request):
    return render(request,"temp/profile.html")


@login_required
def edit_customer_profile(request):
    if request.method=='POST':
        form=EditCustomerProfileForm(request.POST,instance=request.user)
    else:
        form=EditCustomerProfileForm(instance=request.user)
        forml=CustomUserChangeForm(instance=request.user)
        context={"form":form,"forml":forml}
        return render(request,'temp/profile.html',context)
