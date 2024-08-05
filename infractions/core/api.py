from ninja import NinjaAPI
from .models import Persona, Vehiculo, Oficial, Infraccion
from django.shortcuts import get_object_or_404
from ninja.orm import create_schema
from pytz import timezone as pytz_timezone

env_timezone = 'America/Asuncion'

api = NinjaAPI()

# Schemas
PersonaIn = create_schema(Persona, exclude=["id"])
PersonaOut = create_schema(Persona)

VehiculoIn = create_schema(Vehiculo)
VehiculoOut = create_schema(Vehiculo)

OficialIn = create_schema(Oficial, exclude=["id"])
OficialOut = create_schema(Oficial)

InfraccionIn = create_schema(Infraccion, exclude=["id"])
InfraccionOut = create_schema(Infraccion)

# API endpoints for Persona
@api.get("/personas", response=list[PersonaOut])
def list_personas(request):
    return Persona.objects.all()

@api.post("/personas", response=PersonaOut)
def create_persona(request, payload: PersonaIn):
    persona = Persona.objects.create(**payload.dict())
    return persona

# API endpoints for Vehiculo
@api.get("/vehiculos", response=list[VehiculoOut])
def list_vehiculos(request):
    return Vehiculo.objects.all()

@api.post("/vehiculos", response=VehiculoOut)
def create_vehiculo(request, payload: VehiculoIn):
    vehiculo = Vehiculo.objects.create(**payload.dict())
    return vehiculo

# API endpoints for Oficial
@api.get("/oficiales", response=list[OficialOut])
def list_oficiales(request):
    return Oficial.objects.all()

@api.post("/oficiales", response=OficialOut)
def create_oficial(request, payload: OficialIn):
    oficial = Oficial.objects.create(**payload.dict())
    return oficial

@api.post("/infracciones", response=InfraccionOut)
def create_infraction(request, payload: InfraccionOut):
    payload_data = payload.dict()
    print("PAYLOAD: ", payload_data)
    vehiculo = get_object_or_404(Vehiculo, placa_patente=payload_data['vehiculo'])
    print("PLACA: ", vehiculo.placa_patente)
    timestamp_tz = pytz_timezone(env_timezone)
    payload_data['timestamp'] = payload_data['timestamp'].astimezone(timestamp_tz)

    infraccion = Infraccion.objects.create(
        vehiculo=vehiculo,
        timestamp=payload_data['timestamp'],
        comentarios=payload_data['comentarios']
    )
    return infraccion
