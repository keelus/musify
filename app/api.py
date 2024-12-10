import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.handlers.asgi import FileResponse
from django.db.models.query import django
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import  csrf_exempt
from django.core.cache import cache
from app.models import Cancion, Playlist
import requests

SERVIDOR_NETLIFY = "https://6739df0f568f31ee4f8bd20a--deluxe-pika-39355f.netlify.app"

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
    llave_cache = f'audio_{audioID}'
    contenido_cache = cache.get(llave_cache)
    if contenido_cache:
        return HttpResponse(contenido_cache, content_type="audio/ogg")

    archivo = Cancion.objects.get(id=audioID).archivo
    respuesta = requests.get(f'{SERVIDOR_NETLIFY}/audios/{archivo}')

    if respuesta.ok:
        contenido = respuesta.content
        cache.set(llave_cache, contenido)
        return HttpResponse(contenido, content_type="audio/ogg")

def getAudioCover(request, audioID):
    llave_cache = f'cover_{audioID}'
    contenido_cache = cache.get(llave_cache)
    if contenido_cache:
        return HttpResponse(contenido_cache, content_type="image/webp")

    archivo = Cancion.objects.get(id=audioID).cover
    respuesta = requests.get(f'{SERVIDOR_NETLIFY}/imagenes/{archivo}')

    if respuesta.ok:
        contenido = respuesta.content
        cache.set(llave_cache, contenido)
        return HttpResponse(contenido, content_type="image/webp")

# Apartado sesiones
def cerrarSesion(request):
    logout(request)
    return HttpResponseRedirect("/login")

def iniciarSesion(request):
    if request.method == "POST":
        nombre = request.POST.get("usuario")
        contra = request.POST.get("contra")
        if nombre and contra:
            usuario = authenticate(request, username=nombre, password=contra) # TODO: hacer que se pueda iniciar sesion
            if usuario is not None:
                login(request, usuario)
                return HttpResponseRedirect("/")
            else:
                mensaje = "¡Las credenciales son incorrectas!"
                return redirect(f"/login?usuario={nombre}&error={mensaje}")
                return HttpResponse('Usuario o contraseña incorrectos', status=401)
        else:
            return redirect(f"/login?usuario={nombre}")
            #return HttpResponse('Fallo a la hora de registrar los datos', status=400)
    return HttpResponse('Método no permitido', status=405)

def procesarDatosFormulario(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        correo = request.POST.get("correo")
        contra = request.POST.get("contra")
        if nombre and correo and contra:
            usuario = User.objects.create_user(username=nombre, email=correo, password=contra)
            usuario.save()
            return HttpResponseRedirect("/login")
        else:
            return HttpResponse('Fallo a la hora de registrar los datos')
    return HttpResponse('Metodo no permitido', status=405)


@csrf_exempt
def playlistActualizarInformacion(request, playlistID):
    if not request.user.is_authenticated:
        return HttpResponse("Inicia sesion primero.", status=401);

    usuario = request.user

    if request.method == "POST":
        datos = json.loads(request.body)

        nuevo_nombre : str = datos["nombre"]

        # Se verifica en cliente, pero
        # tambien en servidor.
        if nuevo_nombre.lstrip() == "":
            return HttpResponse(b"El nombre no puede estar vacio.", status=403);

        nueva_cover = datos["cover"]

        try:
            playlist = Playlist.objects.get(id = playlistID, autor = usuario)
            playlist.nombre = nuevo_nombre
            playlist.cover = nueva_cover
            playlist.save()

            return HttpResponse(b'OK', status=200)
        except:
            return HttpResponse("La playlist no existe, o no es tuya.", status=404);
        
    return HttpResponse('Metodo no permitido', status=405)

def getPlaylistInformacion(request, playlistID):
    if not request.user.is_authenticated:
        return HttpResponse("Inicia sesion primero.", status=401);

    usuario = request.user

    try:
        playlist = Playlist.objects.get(id=playlistID, autor=usuario)
        canciones = []
        for cancion in reversed(playlist.canciones.all()):
            canciones.append({
                "id": cancion.id,
            })

        return JsonResponse({
            "canciones": canciones
        })
    except:
        return HttpResponse("La playlist no existe, o no es tuya.", status=404);

@csrf_exempt
def playlistCrear(request):
    if not request.user.is_authenticated:
        return HttpResponse("Inicia sesion primero.", status=401);

    usuario = request.user

    if request.method == "POST":
        playlist = Playlist(
            nombre = "Tu nueva playlist",
            autor = usuario, # Temporal
            cover = "https://media.tenor.com/BiEdW2zVchkAAAAM/cat.gif",
        )

        playlist.save()

        id = str(playlist.pk)
        return HttpResponse(id, status=200)
    return HttpResponse('Metodo no permitido', status=405)

def playlistEliminar(request, playlistID):
    if not request.user.is_authenticated:
        return HttpResponse("Inicia sesion primero.", status=401);

    usuario = request.user
    try:
        playlist = Playlist.objects.get(id=playlistID, autor=usuario)
    except:
        return HttpResponse(b"La playlist no existe o no es tuya.", status=404)

    playlist.delete()
    return HttpResponse(b"Ok", status=200)

def playlistCancionesAnyadibles(request, playlistID):
    if not request.user.is_authenticated:
        return HttpResponse("Inicia sesion primero.", status=401);

    usuario = request.user

    try:
        playlist = Playlist.objects.get(id=playlistID, autor=usuario)
        canciones_en_playlist = []
        canciones_anyadibles = []

        for cancion in playlist.canciones.all():
            canciones_en_playlist.append(cancion.id)

        for cancion in Cancion.objects.all():
            if cancion.id not in canciones_en_playlist:
                canciones_anyadibles.append({
                    "id": cancion.id,
                    "nombre": cancion.nombre,
                    "coverUrl": cancion.cover,
                })

        return JsonResponse({
            "canciones": canciones_anyadibles
        })
    except:
        return HttpResponse(b"La playlist no existe o no es tuya.", status=404)

def playlistAnyadirCancion(request, playlistID, cancionID):
    if not request.user.is_authenticated:
        return HttpResponse("Inicia sesion primero.", status=401);

    usuario = request.user

    try:
        playlist = Playlist.objects.get(id=playlistID, autor=usuario)
    except:
        return HttpResponse(b"La playlist no existe o no es tuya.", status=404)

    try:
        cancion = Cancion.objects.get(id=cancionID)
    except:
        return HttpResponse(b"La cancion no existe", status=404)

    if cancion not in playlist.canciones.all():
        playlist.canciones.add(cancion)
        playlist.save()

    return HttpResponse(b"Ok", status=200)

def playlistEliminarCancion(request, playlistID, cancionID):
    if not request.user.is_authenticated:
        return HttpResponse("Inicia sesion primero.", status=401);

    usuario = request.user

    try:
        playlist = Playlist.objects.get(id=playlistID, autor=usuario)
    except:
        return HttpResponse(b"La playlist no existe o no es tuya.", status=404)

    try:
        cancion = Cancion.objects.get(id=cancionID)
    except:
        return HttpResponse(b"La cancion no existe", status=404)

    playlist.canciones.remove(cancion)
    playlist.save()

    return HttpResponse(b"Ok", status=200)
