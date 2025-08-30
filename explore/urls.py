from django.urls import path
from . import views

urlpatterns = [
    path("", views.explore, name="explore"),
    path("category/<slug:category_slug>/", views.category_dares, name="category_dares"),
]
