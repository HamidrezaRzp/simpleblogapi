import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import authentication, exceptions

User = get_user_model()

class CustomJWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startwith('Bearer '):
            return None
    
        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token has expired!')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('Invalid token')
        
        try:
            user = User.objects.get(id=payload['id'])
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('User not found')
        
        return (user, None)