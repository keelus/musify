from django.contrib import admin
from django.urls import path

from app import api, views
urlpatterns = [
    # Vistas principales
    path('', view=views.paginaCanciones, name="inicio"),
    path('playlists', view=views.paginaPlaylists, name="inicio"),
    path('playlist/<str:playlistID>', view=views.paginaPlaylist, name="inicio"),

    # Vistas de autenticacion
    path('login', view=views.login, name="login"),
    path('register', view=views.registrarse, name="registrarse"),
    path('procesarDatos/',views.procesarDatosFormulario, name="procesarDatosFormulario"),

    # Api
    path('api/cancion/<str:audioID>/informacion', view=api.getAudioInformacion, name="audio_informacion"),
    path('api/cancion/<str:audioID>/archivo', view=api.getAudioArchivo, name="audio_archivo"),
    path('api/cancion/<str:audioID>/cover', view=api.getAudioCover, name="audio_cover"),

    path('api/sesion/cerrar', view=api.cerrarSesion, name="audio"),
]

