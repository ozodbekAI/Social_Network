from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.response import Response
from rest_framework import status
from users.models import User
from users.serializers import UserFirendsSerializer, UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny, ]


    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data


        user  = User.objects.create(
            email = validated_data['email'],
            username = validated_data['username'],
            phone = validated_data['phone'],
            password = make_password(validated_data['password'])
            )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            raise AuthenticationFailed("User does not exist")
        

        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password")
        
        refresh = RefreshToken.for_user(user)

        response = Response()

        response['Authorization'] = str(refresh.access_token)
        response['refresh'] = str(refresh)

        response.data = {
            "refresh": str(refresh),
            "access_token": str(refresh.access_token),
            "status": status.HTTP_200_OK
        }

        return response
    

class FriednShip(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserFirendsSerializer

    def get_queryset(self):
        return self.request.user.friends.all()
    
    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        friendship = self.get_object()
        if friendship.to_user != request.user:
            raise Response({
                'detail': "You cant not accept this friendship",
                'status': status.HTTP_403_FORBIDDEN
            })
        friendship.accept()
        return Response({
           'status': status.HTTP_200_OK
        })

