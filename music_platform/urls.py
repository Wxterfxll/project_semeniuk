from django.contrib import admin
from django.urls import path
from music import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('songs/', views.song_list, name='song_list'),
    path('songs/<int:song_id>/', views.song_detail, name='song_detail'),
    path('my_playlists/', views.my_playlists, name='my_playlists'),
    path('create_playlist/', views.create_playlist, name='create_playlist'),
    path('playlist/<int:playlist_id>/', views.playlist_detail, name='playlist_detail'),
    path('playlist/<int:playlist_id>/delete/', views.delete_playlist, name='delete_playlist'),
    path('add_to_playlist/<int:song_id>/', views.add_to_playlist, name='add_to_playlist'),
    path('remove_from_playlist/<int:playlist_id>/<int:song_id>/', views.remove_from_playlist, name='remove_from_playlist'),

]
