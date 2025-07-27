
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include("home.urls")),
    path("explore/",include("explore.urls")),
    path("leaderboard/",include("leaderboard.urls")),
    path("community/",include("community.urls")),
    path("user_profile/",include("userprofile.urls")),
    path("postdare/",include("postdare.urls")),
    path("accounts/",include("accounts.urls")),
    path('login/', include('login.urls')), # Login and logout ke liye 

]
