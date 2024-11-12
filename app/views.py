from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string

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
    return pagina(request, "canciones.html", {}, "reducido" not in request.headers)

# Pagina de playlists
def paginaPlaylists(request):
    return pagina(request, "playlists.html", {}, "reducido" not in request.headers)

# Pagina de playlist
def paginaPlaylist(request, playlistID):
    return pagina(request, "playlist.html", {
        "playlistID": playlistID,
    }, "reducido" not in request.headers)
