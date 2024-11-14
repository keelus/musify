from django.db import models

class Usuario(models.Model):
    objects = models.Manager() # Para que el LSP no me de error

    nombre = models.CharField(max_length = 20)
    email = models.CharField(max_length = 100)
    contrasenya_hash = models.CharField(max_length = 32) # Md5 char length

    def __str__(self):
        return f'{self.nombre} ({self.email})'

# Grupos o personas
class Artista(models.Model):
    objects = models.Manager()

    nombre = models.CharField(max_length = 100)

    def __str__(self):
        return str(self.nombre)

class Cancion(models.Model):
    objects = models.Manager()

    nombre = models.CharField(max_length = 100)
    archivo = models.FileField()
    artistas = models.ManyToManyField(Artista)

    def __str__(self):
        artistasVisual = []
        for artista in self.artistas.all():
            artistasVisual.append(artista.nombre)
        return f'{self.nombre} - {", ".join(artistasVisual)}'

class Playlist(models.Model):
    objects = models.Manager()

    nombre = models.CharField(max_length = 100)
    autor = models.OneToOneField(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.nombre)
