from django.shortcuts import render

def gettingStarted(request):
    return render(request, "index.html",{})