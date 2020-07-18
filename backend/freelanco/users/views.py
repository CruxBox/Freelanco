from django.shortcuts import render
from .forms import *
from .decorators import only_customer
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
            return render(request,'account/log1.html',{'not_exist':True})
    else:
        return render(request,'account/log1.html',)


def customer_signup(request):
    context={"user_type":"Customer","user_exists":False,"pwd_error":False}
    if request.method=='POST':
        username=request.POST['username']
        password1=request.POST['password1']
        password2=request.POST['password2']
        email=request.POST['email']
        if password1!=password2:
            context["pwd_error"]=True
            return render(request,"account/signup.html",context)
        if not CustomUser.objects.filter(username=username).exists():
            user=CustomUser.objects.create_user(username, password=password1,email=email)
            user.is_freelancer=False
            user.save()
            cust_profile=CustomerProfile(user=user)
            cust_profile.save()
            user=authenticate(username=username,password=password1)
            login(request,user)
            return HttpResponseRedirect(reverse("home"))
        else:
            context["user_exists"]=True
            return render(request,"account/signup.html",context)
    else:
        return render(request,"account/signup.html",context)

def freelancer_signup(request):
    context={"user_type":"Freelancer","user_exists":False}
    if request.method=='POST':
        username=request.POST['username']
        password1=request.POST['password1']
        password2=request.POST['password2']
        email=request.POST['email']
        if password1!=password2:
            context["pwd_error"]=True
            return render(request,"account/signup.html",context)
        if not CustomUser.objects.filter(username=username).exists():
            user=CustomUser.objects.create_user(username, password=password1,email=email)
            user.is_freelancer=True
            user.save()
            print("OLOLOL")
            cust_profile=FreelancerProfile(user=user)
            print("cust_profile")
            cust_profile.save()
            user=authenticate(username=username,password=password1)
            login(request,user)
            return HttpResponseRedirect(reverse("home"))
        else:
            context["user_exists"]=True
            return render(request,"account/signup.html",context) 
    else:
        return render(request,"account/signup.html",context)

@login_required
def view_customer_profile(request):
    if request.user.is_freelancer:
        profile=request.user.freelancer_profile
    else:
        profile=request.user.customer_profile
    address=profile.addresses.all()
    context={"profile":profile,"addresses":address}
    return render(request,"account/profile.html",context)

@login_required
def view_freelancer_profile(request):
    profile=request.user.freelancer_profile
    address=profile.addresses.all()
    context={"profile":profile,"addresses":address}
    return render(request,"account/profile.html",context)

@login_required
@only_customer
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
        return render(request,'account/edit_profile.html',context)

@login_required
def edit_customer_address(request,pk):
    if request.method=='POST':
        form=EditAddress(request.POST,instance=request.user.customer_profile.addresses.get(pk=pk))
        #print(form)
        if form.is_valid():
            address=form.save(commit=False)
            name=address.name
            print(address.id)
            adds=Address.objects.filter(name=name,customer=request.user.customer_profile.id).exclude(pk=address.id)
            if adds:
                form3=EditAddress(instance=request.user.customer_profile.addresses.get(pk=pk))
                context={"form":form3,"messages":["Address name already exists"]}
                return render(request,'account/edit_profile.html',context)
            address.save()
            return HttpResponseRedirect(reverse("users:profile_view"))
    else:
        form3=EditAddress(instance=request.user.customer_profile.addresses.get(pk=pk))
        context={"form":form3}
        return render(request,'account/edit_profile.html',context)

@login_required
def add_customer_address(request):
    if request.method=='POST':
        form=EditAddress(request.POST)
        if form.is_valid():
            address=form.save(commit=False)
            name=address.name
            if request.user.is_freelancer:
                adds=Address.objects.filter(name=name,customer=request.user.freelancer_profile.id)
            else:
                adds=Address.objects.filter(name=name,customer=request.user.customer_profile.id)
            if adds:
                address.name=""
                form3=EditAddress(instance=address)
                context={"form":form3,"messages":["Address name already exists"]}
                return render(request,'account/edit_profile.html',context)
            address.save()
            if request.user.is_freelancer:
                request.user.freelancer_profile.addresses.add(address)
            else:
                request.user.customer_profile.addresses.add(address)
        return HttpResponseRedirect(reverse("users:profile_view"))
    else:
        form3=EditAddress()
        context={"form":form3}
        return render(request,'account/edit_profile.html',context)

@login_required
def delete_customer_address(request,pk):
    address=Address.objects.get(pk=pk)
    if request.method=='POST':
        address.delete()
        return HttpResponseRedirect(reverse("users:profile_view"))
