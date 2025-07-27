from django.urls import path,include
from userprofile import views
urlpatterns = [
    
    path('',views.user_profile,name="profile"),
    path('/network',views.network,name="network")
]
