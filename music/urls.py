from django.urls import path,include
from .views import post_song,get_all_songs,PlaylistViews,PlaylistDetailViews,cpu_intensive

urlpatterns = [
    path('',get_all_songs),
    path('playlist/',PlaylistViews.as_view()),
    path('playlist/<int:id>',PlaylistDetailViews.as_view()),
    path('post_song',post_song),
    path('cpu_intensive',cpu_intensive), 
]

