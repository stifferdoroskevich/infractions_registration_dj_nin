from django.contrib import admin
from .models import Persona, Vehiculo, Oficial, Infraccion

admin.site.register(Persona)
admin.site.register(Vehiculo)
admin.site.register(Oficial)
admin.site.register(Infraccion)
