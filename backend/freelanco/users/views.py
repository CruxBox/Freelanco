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
    context={"user_type":"Customer","user_exists":False}
    if request.method=='POST':
        print("lol")
        username=request.POST['username']
        password1=request.POST['password1']
        password2=request.POST['password2']
        if not CustomUser.objects.filter(username=username).exists():
            user=CustomUser.objects.create_user(username, password=password1)
            user.is_freelancer=False
            user.save()
            temp_add=Address(address1="Default")
            temp_add.save()
            cust_profile=CustomerProfile(user=user,address=temp_add)
            cust_profile.save()
            user=authenticate(username=username,password=password1)
            login(request,user)
            return HttpResponseRedirect(reverse("home"))
        else:
            context["user_exists"]=True
            return render(request,"temp/signup.html",context)
    else:
        return render(request,"temp/signup.html",context)

def freelancer_signup(request):
    context={"user_type":"Freelancer","user_exists":False}
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
            return HttpResponseRedirect(reverse("home"))
        else:
            context["user_exists"]=True
            return render(request,"temp/signup.html",context) 
    else:
        return render(request,"temp/signup.html",context)

@login_required
def view_customer_profile(request):
    return render(request,"temp/profile.html")


@login_required
def edit_customer_profile(request):
    if request.method=='POST':
        form=CustomUserChangeForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("users:profile_view"))


    else:
        form2=CustomUserChangeForm(instance=request.user)
        context={"form":form2}
        #context={"form_profile":form1,"form_user":form2,"form_address":form3}
        return render(request,'temp/edit_profile.html',context)

@login_required
def edit_customer_address(request):
    if request.method=='POST':
        form=EditAddress(request.POST,instance=request.user.customer_profile.address)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("users:profile_view"))
    else:
        form3=EditAddress(instance=request.user.customer_profile.address)
        context={"form":form3}
        return render(request,'temp/edit_profile.html',context)
