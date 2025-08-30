from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
#============sighup==========
def signup(request):
    if request.method =="POST":
        first_name=request.POST.get("firstName")
        last_name=request.POST.get("lastName")
        email=request.POST.get("email")
        password=request.POST.get("password")
        confirm_password=request.POST.get("confirmPassword")
        # print("First Name:", first_name)
        # print("Last Name:", last_name)
        # print("Email:", email)
        # print("Password:", password)
        # print("Confirm Password:", confirm_password)

        if password != confirm_password: 
            return render( request,"register.html")
        if User.objects.filter(username=email).exists():
            messages.error(request, "User with this email already exists!")
            return render(request, "register.html")
        
        new_user = User.objects.create_user(
             username=email,
             email=email,
            first_name=first_name,
            last_name=last_name,
        )
        new_user.set_password(password)
        new_user.save()
        messages.success(request, "Account created successfully!")
        return redirect("home")
        
    return render(request,"register.html")