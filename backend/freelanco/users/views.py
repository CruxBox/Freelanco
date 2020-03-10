from django.shortcuts import render
from .forms import *
from allauth.account.forms import SignupForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
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
        uform=CustomUserCreationForm(data=request.POST)
        if uform.is_valid():
            user=uform.save()
            user.is_freelancer=False
            user.save()
            return render(request,"temp/home.html")
    else:
        uform=UserCreationForm()
        pform=CustomerProfileForm()
        kwargs={"uform":uform,"pform":pform}
        return render(request,"temp/signup.html",kwargs)

def freelancer_signup(request):
    if request.method=='POST':
        uform=CustomUserCreationForm(data=request.POST)
        if uform.is_valid() and pform.is_valid():
            user=uform.save()
            user.is_freelancer=True
            user.save()
            profile=pform.save(commit=False)
            profile.user=user
            profile.save()
            return render(request,"temp/home.html")
    else:
        uform=CustomCreationForm()
        pform=FreelancerProfileForm()
        kwargs={"uform":uform,"pform":pform}
        return render(request,"temp/profile.html",kwargs)
