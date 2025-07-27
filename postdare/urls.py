from django.urls import path
from postdare import views

urlpatterns = [
    path("",views.postdare,name="postdare")
]