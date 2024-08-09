from django.shortcuts import get_object_or_404
from ninja import NinjaAPI
from ninja.errors import HttpError
from ninja.orm import create_schema
from ninja.security import HttpBearer
from pytz import timezone as pytz_timezone

from django.utils import timezone

from .models import Persona, Vehiculo, Oficial, Infraccion
from .utils import create_jwt_token, verify_jwt_token

env_timezone = 'America/Asuncion'

api = NinjaAPI(
   title="Infracciones API",
   description="Una demo API para consulta de registros y carga de infracciones")

# Schemas
PersonaIn = create_schema(Persona, exclude=["id"])
PersonaOut = create_schema(Persona)

VehiculoIn = create_schema(Vehiculo)
VehiculoOut = create_schema(Vehiculo)

OficialIn = create_schema(Oficial, exclude=["id"])
OficialOut = create_schema(Oficial)

InfraccionIn = create_schema(Infraccion, exclude=["id"])
InfraccionOut = create_schema(Infraccion)


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            oficial = verify_jwt_token(token)
            if oficial:
                request.oficial = oficial
                return token
        raise HttpError(401, "Unauthorized")

@api.get("/bearer")
def bearer(request, nui: str):
    try:
        oficial = Oficial.objects.get(nui=nui)
        token = create_jwt_token(oficial)
        return {"token": token}
    except Oficial.DoesNotExist:
        return {"error": "Invalid NUI"}, 400


# API endpoints for Persona
@api.get("/personas", response=list[PersonaOut], auth=AuthBearer())
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

@api.post("/infracciones", response=InfraccionOut, auth=AuthBearer())
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

@api.get("/generar_informe", response=list[InfraccionOut])
def generar_informe(request, email):
    persona = get_object_or_404(Persona, correo=email)
    vehiculos = Vehiculo.objects.filter(persona_id=persona.id)
    if not vehiculos:
        raise HttpError(404, f"No existe vehiculo asociado con el email {email}")

    infracciones = Infraccion.objects.filter(vehiculo__in=vehiculos)
    if not infracciones:
        raise HttpError(404, f"No existen infracciones asociadas con el email {email}, enhorabuena!")

    return infracciones


