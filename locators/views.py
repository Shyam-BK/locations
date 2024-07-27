from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import get_user_model
from .serializer import UserSerializer, LatLongSerializer, LoginSerializer, LatLongUpdateSerializer, CustomUserLatLongSerializer
from .models import LatLong, CustomUser
from .permissions import IsSuperUser

User = get_user_model()

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Create token for the user
        token, created = Token.objects.get_or_create(user=user)
        
        
        
        headers = self.get_success_headers(serializer.data)
        return Response({
            'user': serializer.data,
            'token': token.key
        }, status=status.HTTP_201_CREATED, headers=headers)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=status.HTTP_200_OK)

class UserDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        print(f"User: {request.user}")
        print(f"Auth: {request.auth}")
        if request.user.is_authenticated:
            serializer = UserSerializer(request.user)
            return Response(serializer.data)
        else:
            return Response({"detail": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    

class LatLongUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        user = request.user
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')

        # Check if LatLong instance already exists for the user
        latlong, created = LatLong.objects.get_or_create(user=user)
        
        # If it exists, update it; otherwise, create it
        if not created:
            latlong.latitude = latitude
            latlong.longitude = longitude
            latlong.save()
        else:
            # If created, it is already set to the new latitude and longitude
            latlong.latitude = latitude
            latlong.longitude = longitude
            latlong.save()

        serializer = LatLongUpdateSerializer(latlong)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CustomUserLatLongListView(generics.ListAPIView):
    permission_classes = [IsSuperUser]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserLatLongSerializer
    def get_queryset(self):
        return CustomUser.objects.filter(is_superuser=False)
    


class CustomUserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsSuperUser]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class LatLongViewSet(viewsets.ModelViewSet):
    permission_classes = [IsSuperUser]
    queryset = LatLong.objects.all()
    serializer_class = LatLongSerializer
