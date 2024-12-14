from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string

from app.models import Cancion, Playlist


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
    if not request.user.is_authenticated:
        return pagina(request, "no-autorizado.html", {}, "reducido" not in request.headers)

    usuario = request.user

    playlists = []

    for playlistObjetoBd in Playlist.objects.filter(autor=usuario):
        playlist = {
            "id": playlistObjetoBd.id,
            "nombre": playlistObjetoBd.nombre,
            "cover": playlistObjetoBd.cover,
        }
        playlists.append(playlist)
    return pagina(request, "playlists.html", {
        "playlists": playlists
    }, "reducido" not in request.headers)

# Pagina de playlist
def paginaPlaylist(request, playlistID):
    if not request.user.is_authenticated:
        return pagina(request, "no-autorizado.html", {}, "reducido" not in request.headers)

    usuario = request.user

    try:
        playlist = get_object_or_404(Playlist, pk=playlistID, autor=usuario)
    except:
        return HttpResponse(b"La playlist no existe.", status=404)

    canciones = []

    for cancionObjetoBd in reversed(playlist.canciones.all()):
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

    return pagina(request, "playlist.html", {
        "playlist": playlist,
        "canciones": canciones,
    }, "reducido" not in request.headers)

def registrarse(request):
    usuario = request.GET.get("usuario") # Si el registro falla, aqui se guarda el input
    error = request.GET.get("error") # Si el registro falla, aqui se guarda el input

    return render(request, "registro.html", {
        "usuario": usuario,
        "error": error,
    })

def login(request):
    usuario = request.GET.get("usuario") # Si el login falla, aqui se guarda el input
    error = request.GET.get("error") # Si el login falla, aqui se guarda el input

    return render(request, "login.html", {
        "usuario": usuario,
        "error": error,
    })


