from django.contrib.auth.models import User
from django.db import models
from django.db.models import ManyToManyField

# Grupos o personas
class Artista(models.Model):
    objects = models.Manager()

    nombre = models.CharField(max_length = 100)

    def __str__(self):
        return str(self.nombre)

class Cancion(models.Model):
    objects = models.Manager()

    nombre = models.CharField(max_length = 100)
    artistas = models.ManyToManyField(Artista)

    archivo = models.CharField(max_length = 200)
    cover = models.CharField(max_length = 200)

    def __str__(self):
        artistasVisual = []
        for artista in self.artistas.all():
            artistasVisual.append(artista.nombre)
        return f'{self.nombre} - {", ".join(artistasVisual)}'

class Playlist(models.Model):
    objects = models.Manager()

    nombre = models.CharField(max_length = 100)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    canciones = models.ManyToManyField(Cancion, blank=True)
    cover = models.CharField(max_length = 200)

    def __str__(self):
        return str(self.nombre)


