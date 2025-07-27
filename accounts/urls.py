from django.urls import path,include
from accounts import views
urlpatterns = [
    path('', views.signup,name="register"),
    path('login/',  include("login.urls")),
]
