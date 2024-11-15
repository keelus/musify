from django.core.handlers.asgi import FileResponse
from django.http import HttpResponse, JsonResponse
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

# Devuelve un audio de ejemplo, simula por ahora el BLOB de la BD
def apiConseguirAudioInformacion(request, audioID):
    cancion = Cancion.objects.get(id=audioID)
    nombresArtistas = []
    for artistaObjectoBd in cancion.artistas.all():
        nombresArtistas.append(artistaObjectoBd.nombre)

    return JsonResponse({
        "nombre": cancion.nombre,
        "artistas": nombresArtistas,
    })

def apiConseguirAudioArchivo(request, audioID):
    archivo = Cancion.objects.get(id=audioID).archivo
    return FileResponse(archivo, content_type="audio/mpeg")

def registrarse(request):
    return render(request, "registro.html")

