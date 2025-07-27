from django.urls import path
from explore import views

urlpatterns = [
    path("",views.explore,name="explore")
]