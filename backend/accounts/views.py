from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status, serializers
from .serializers import SignupSerializer, ChangePasswordSerializer, LoginSerializer, UserSerializer, UserProfileSerializer
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from users.models import Profile
# Create your views here.


class UserSignupView(APIView):
    permission_classes=[AllowAny]
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer(self, *args, **kwargs):
        return SignupSerializer(*args, **kwargs)


class UserLogoutView(APIView):
     permission_classes = (IsAuthenticated,)
     authentication_classes = [JWTAuthentication]
     def post(self, request):
          try:
               refresh_token = request.data["refresh_token"]
            #    print(refresh_token)
               token = RefreshToken(refresh_token)
               token.access_token.lifetime = timedelta(seconds=1)
               token.access_token.set_exp = timezone.now()
               token.blacklist()
               return Response(status=status.HTTP_205_RESET_CONTENT)
          except Exception as e:
               return Response(status=status.HTTP_400_BAD_REQUEST)
          

class UserChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        try:
            serializer = ChangePasswordSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            user = request.user
            data = serializer.validated_data

            if not user.check_password(data['password']):
                return Response({'error': ['Wrong password.']}, status=status.HTTP_400_BAD_REQUEST)
            
            user.set_password(data['new_password'])
            user.save()
            update_session_auth_hash(request, user)
            return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            return Response({'error': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            user_obj = User.objects.get(pk=user.id)
            
            try:
                user_profile_obj = Profile.objects.get(user=user)
                user_profile_serializer = UserProfileSerializer(user_profile_obj)
            except Profile.DoesNotExist:
                user_profile_serializer = None

            user_serializer = UserSerializer(user_obj)
            
            # Generate refresh and access tokens
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            response_data = {
                'user': user_serializer.data,
                'profile': user_profile_serializer.data if user_profile_serializer else None,
                'refresh_token': str(refresh),
                'access_token': str(access_token),
            }

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer(self, *args, **kwargs):
        return LoginSerializer(*args, **kwargs)