from django.shortcuts import render
from .forms import *
# Create your views here.
def add_customer(request):
    if request.method=='POST':
        uform=CustomUserCreationForm(data=request.POST)
        pform=CustomerProfileForm(data=request.POST)
        if uform.is_valid() and pform.is_valid():
            user=uform.save()
            profile=pform.save(commit=False)
            profile.user=user
            profile.save()
            return render(request,"index.html")
    else:
        uform=UserCreationForm()
        pform=CustomerProfileForm()
        kwargs={"uform":uform,"pform":pform}
        return render(request,"social_app/profile.html",kwargs)