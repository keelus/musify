from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.handlers.asgi import FileResponse
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
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
                return HttpResponse('Usuario o contraseña incorrectos', status=401)
        else:
            return HttpResponse('Fallo a la hora de registrar los datos', status=400)
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