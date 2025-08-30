from django.shortcuts import render ,redirect
from django.contrib.auth.models import User
from django.contrib import auth,messages
from django.contrib.auth.decorators import login_required


# Create your views here.
#=========login===========
def login_user(request):
    if request.method == "POST":
        username = request.POST.get("email")
        password = request.POST.get("password")
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("dashboard_home")  # Redirect to dashboard after login
        else:
            # Redirect to register page if user not found
            messages.info(request, "User not found. Please register.")
            return redirect("register")
    return render(request, "login.html")

#=========register===========
def register_user(request):
    if request.method == "POST":
        username = request.POST.get("email")
        password = request.POST.get("password")
        first_name = request.POST.get("first_name", "")
        last_name = request.POST.get("last_name", "")
        if User.objects.filter(username=username).exists():
            messages.error(request, "User already exists. Please login.")
            return redirect("login")
        user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
        user.save()
        auth.login(request, user)
        return redirect("dashboard_home")  # Redirect to dashboard after registration
    return render(request, "register.html")
#===============logout===========
@login_required
def logout_user(request):
    auth.logout(request)

    return redirect("home")