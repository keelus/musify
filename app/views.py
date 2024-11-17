from django.contrib.auth.models import User
from django.core.handlers.asgi import FileResponse
from django.db.models.fields import return_None
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string

from app.models import Cancion

def pagina(request, archivo_contenido, contexto_contenido, mostrar_completa):
    if mostrar_completa:
        return render(request, "index.html", {
            "seccionActiva": archivo_contenido,
            "contenido": render_to_string(archivo_contenido, contexto_contenido)
        })
    else:
        return render(request, archivo_contenido, contexto_contenido)

# Pagina de canciones
def paginaCanciones(request):
    canciones = []

    for cancionObjetoBd in Cancion.objects.all():
        cancion = {
            "id": cancionObjetoBd.id,
            "nombre": cancionObjetoBd.nombre,
            "coverUrl": cancionObjetoBd.cover,
            "artistas": []
        }

        for artistaObjetoBd in cancionObjetoBd.artistas.all():
            cancion["artistas"].append({
                "id": artistaObjetoBd.id,
                "nombre": artistaObjetoBd.nombre,
            })
        canciones.append(cancion)

    return pagina(request, "canciones.html", {
        "canciones": canciones
    }, "reducido" not in request.headers)

# Pagina de playlists
def paginaPlaylists(request):
    return pagina(request, "playlists.html", {}, "reducido" not in request.headers)

# Pagina de playlist
def paginaPlaylist(request, playlistID):
    return pagina(request, "playlist.html", {
        "playlistID": playlistID,
    }, "reducido" not in request.headers)

def registrarse(request):
    return render(request, "registro.html")

def login(request):
    return render(request, "login.html")


