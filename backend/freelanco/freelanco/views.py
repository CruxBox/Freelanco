from django.shortcuts import render

def gettingStarted(request):
    return render(request, "index.html",{})


##for testing
def display404(request):
    return render(request,"notfound.html",{})
