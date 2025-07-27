from django.shortcuts import render

# Create your views here.
def user_profile(request):
    return render(request,"profile.html")
def network(request):
    return render(request,"network.html")