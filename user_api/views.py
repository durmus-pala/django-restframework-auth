from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import RegistrationSerializer
from rest_framework.authtoken.models import Token
from . import models

# Create your views here.


@api_view(['POST'])
def register_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            acount = serializer.save()
            acount.set_password(acount.password)
            acount.save()
            token, _ = Token.objects.get_or_create(user=acount)
            # data = serializer.data
            data['token'] = token.key
        else:
            data = serializer.errors
        return Response(data)


@api_view(['POST'])
def logout_view(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        data = {
            'message': 'logout, token deleted'
        }
        return Response(data)
