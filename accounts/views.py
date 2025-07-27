from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
#============sighup==========
def signup(request):
    if request.method =="POST":
        firstName=request.POST.get("firstName")
        lastName=request.POST.get("lastName")
        email=request.POST.get("email")
        password=request.POST.get("password")
        confirm_password=request.POST.get("confirmPassword")

        if password != confirm_password: 
            return render( request,"register.html")
        
        new_user = User.objects.create(
            firstName=firstName,
            lastName=lastName,
            email=email
        )
        new_user.set_password(password)
        new_user.save()
        return redirect("base")
        
    return render(request,"register.html")