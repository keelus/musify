from django.contrib import admin
from django.urls import path

from app import views

urlpatterns = [
    path('', view=views.paginaCanciones, name="inicio"),
    path('playlists', view=views.paginaPlaylists, name="inicio"),
    path('playlist/<str:playlistID>', view=views.paginaPlaylist, name="inicio"),
    path('audio', view=views.apiConseguirAudio, name="audio"),
]
