import jwt 
from datetime import datetime, timedelta, timezone
from django.conf import settings

def create_jwt_token(user):
    payload = {
        'id' : user.id,
        'username':user.username,
        'exp' : datetime.now(timezone.utc) + timedelta(seconds=settings.JWT_EXP_DELTA_SECONDS),
        'iat' : datetime.now(timezone.utc),
    }
    token = jwt.encode(payload, settings.JWT_SECRET_KEY , algorithm=settings.JWT_ALGORITHM)
    return token
