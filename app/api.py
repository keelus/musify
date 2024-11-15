from django.core.handlers.asgi import FileResponse
from django.http import HttpResponseRedirect, JsonResponse
from app.models import Cancion

# Devuelve un audio de ejemplo, simula por ahora el BLOB de la BD
def getAudioInformacion(request, audioID):
    cancion = Cancion.objects.get(id=audioID)
    nombresArtistas = []
    for artistaObjectoBd in cancion.artistas.all():
        nombresArtistas.append(artistaObjectoBd.nombre)

    return JsonResponse({
        "nombre": cancion.nombre,
        "artistas": nombresArtistas,
    })

def getAudioArchivo(request, audioID):
    archivo = Cancion.objects.get(id=audioID).archivo
    return FileResponse(archivo, content_type="audio/mpeg")

def getAudioCover(request, audioID):
    archivo = Cancion.objects.get(id=audioID).cover
    return FileResponse(archivo, content_type="image/jpeg")

# Apartado sesiones
def cerrarSesion(request):
    return HttpResponseRedirect("/login")

