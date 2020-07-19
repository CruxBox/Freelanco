from django.shortcuts import render

def gettingStarted(request):
    return render(request, "index.html",{})


##for testing
def display404(request):
    return render(request,"notfound.html",{})

def displayOrderHist(request):
    return render(request,"order_history.html")