from django.shortcuts import render ,redirect
from django.contrib.auth.models import User
from django.contrib import auth,messages
from django.contrib.auth.decorators import login_required


# Create your views here.
#=========login===========
def login_user(request):
    if request.method=="POST":
        email=request.POST.get("email")
        password=request.POST.get("password")
        user=auth.authenticate(request,email=email,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect("home")
        return render(request,"register.html")
    return render(request,"login.html")
#===============logout===========
@login_required
def logout_user(request):
    auth.logout(request)

    return redirect("home")