from django.urls import path
from postdare import views

urlpatterns = [
    path("",views.postdare,name="postdare"),
    path('post/<int:id>/', views.postdare, name='edit_dare'),  # Edit Dare
    path('delete/<int:id>/', views.delete_dare, name='delete_dare'),
]