from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    return render(request,"base.html")

@login_required(login_url='login')
def dashboard_view(request):
    return render(request, 'home/dashboard.html', {'user': request.user})
