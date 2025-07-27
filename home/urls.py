from django.urls import path,include
from home import views
from .views import dashboard_view
urlpatterns = [
     path('',views.home, name="home"),
    path('dashboard/', dashboard_view, name='dashboard'),
    
]
