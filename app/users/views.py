from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

class RegisterUserView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
        
            user = serializer.save()
        
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomLoginView(ObtainAuthToken):

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):

        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.filter(username=username).first()

        if user.check_password(password):

            response = super().post(request, *args, **kwargs)
            
            return Response({
                'token': response.data['token'],
                'username': user.username,
                'email': user.email,
            })

        else:

            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
