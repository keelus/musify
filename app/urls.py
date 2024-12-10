from django.contrib import admin
from django.urls import path

from app import api, views
urlpatterns = [
    # Vistas principales
    path('', view=views.paginaCanciones, name="inicio"),
    path('playlists', view=views.paginaPlaylists, name="inicio"),
    path('playlist/<int:playlistID>', view=views.paginaPlaylist, name="inicio"),

    # Vistas de autenticacion
    path('login', view=views.login, name="login"),
    path('register', view=views.registrarse, name="registrarse"),

    # Api
    path('api/cancion/<str:audioID>/informacion', view=api.getAudioInformacion, name="audio_informacion"),
    path('api/cancion/<str:audioID>/archivo', view=api.getAudioArchivo, name="audio_archivo"),
    path('api/cancion/<str:audioID>/cover', view=api.getAudioCover, name="audio_cover"),

    path('api/playlist/<str:playlistID>/informacion', view=api.getPlaylistInformacion , name="playlist_informacion"),
    path('api/playlist/<str:playlistID>/actualizarInformacion', view=api.playlistActualizarInformacion, name="playlist_actualizar_informacion"),
    path('api/playlist/<str:playlistID>/cancionesAnyadibles', view=api.playlistCancionesAnyadibles, name="playlist_canciones_anyadibles"),
    path('api/playlist/<str:playlistID>/anyadirCancion/<str:cancionID>', view=api.playlistAnyadirCancion, name="playlist_anyadir_cancion"),
    path('api/playlist/<str:playlistID>/eliminarCancion/<str:cancionID>', view=api.playlistEliminarCancion, name="playlist_eliminar_cancion"),
    path('api/playlist/<str:playlistID>/eliminar', view=api.playlistEliminar, name="playlist_crear"),
    path('api/playlist/crear', view=api.playlistCrear, name="playlist_crear"),


    path('api/sesion/cerrar', view=api.cerrarSesion, name="audio"),
    path('api/sesion/iniciar', view=api.iniciarSesion, name="inicio"),
    path('procesarDatos', view=api.procesarDatosFormulario, name="procesarDatosFormulario"),
]

