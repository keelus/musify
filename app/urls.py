from django.contrib import admin
from django.urls import path

from app import views
urlpatterns = [
    path('', view=views.paginaCanciones, name="inicio"),
    path('playlists', view=views.paginaPlaylists, name="inicio"),
    path('playlist/<str:playlistID>', view=views.paginaPlaylist, name="inicio"),
    #path('audio', view=views.apiConseguirAudio, name="audio"),


    path('api/audio/informacion/<str:audioID>', view=views.apiConseguirAudioInformacion, name="audio"),
    path('api/audio/archivo/<str:audioID>', view=views.apiConseguirAudioArchivo, name="audio"),
    #Aqui esta el path que permite que al poner "register" en la ruta vaya al apartado de registro

    path('login', view=views.login, name="login"),
    path('register', view=views.registrarse, name="registrarse"),
]

