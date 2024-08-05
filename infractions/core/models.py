from django.db import models
from django.utils import timezone
from pytz import timezone as pytz_timezone

class Persona(models.Model):
    nombre = models.CharField(max_length=255)
    correo = models.EmailField()

    def __str__(self):
        return self.nombre


class Vehiculo(models.Model):
    placa_patente = models.CharField(max_length=10, primary_key=True)
    marca = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)

    def __str__(self):
        return self.placa_patente


class Oficial(models.Model):
    nombre = models.CharField(max_length=255)
    nui = models.IntegerField(unique=True)

    def __str__(self):
        return self.nombre

class Infraccion(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    comentarios = models.TextField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return f"Infracción de {self.vehiculo.placa_patente} en {self.timestamp}"
