from django.contrib import admin
from .models import Playlist, Cancion, Artista

# Register your models here.
admin.site.register(Playlist)
admin.site.register(Cancion)
admin.site.register(Artista)
