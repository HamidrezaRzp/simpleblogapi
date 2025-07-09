import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from .utils import create_jwt_token


@csrf_exempt
def login_view(request):
    if request.method != 'POST' :
        return JsonResponse({'error':'only post method is allowed!'}, status=405)
    
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')

    user = authenticate(username=username, password=password)

    if user is not None:
        token = create_jwt_token(user)
        return JsonResponse({'token' : token})
    else : 
        return JsonResponse({'error':'invalid credentials!'}, status=401)
