from django.urls import path
from userprofile import views

urlpatterns = [
    path("create-room/", views.create_private_room, name="create_private_room"),
    path("room/<uuid:room_uuid>/", views.private_room, name="private_room"),
    path("room/<uuid:room_uuid>/dare/<int:dare_id>/edit/", views.edit_private_room_dare, name="edit_private_room_dare"),
    path("room/<uuid:room_uuid>/dare/<int:dare_id>/delete/", views.delete_private_room_dare, name="delete_private_room_dare"),
    path("room/<uuid:room_uuid>/dare/<int:dare_id>/accept/", views.accept_private_room_dare, name="accept_private_room_dare"),
    # Profile page (GET and POST for edit/save)
    path("", views.user_profile, name="profile"),
    # Accept dare page
    path("accept/<int:dare_id>/", views.accept_dare, name="accept_dare"),
    # Network page
    path("network/", views.network, name="network"),
]
