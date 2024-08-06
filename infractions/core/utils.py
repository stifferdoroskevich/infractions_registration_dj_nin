import jwt
import datetime as dt
from django.conf import settings
from .models import Oficial

def create_jwt_token(oficial: Oficial):
    payload = {
        'nui': oficial.nui,
        'exp': dt.datetime.utcnow() + settings.JWT_EXPIRATION_DELTA,
        'iat': dt.datetime.utcnow()
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token

def verify_jwt_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return Oficial.objects.get(nui=payload['nui'])
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, Oficial.DoesNotExist):
        return None
