from rest_framework.views import APIView 
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.exceptions import status
from rest_framework.response import Response
from django.contrib.auth import logout
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token


User = get_user_model()

class LoginAPIView(APIView):
    
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request, format=None):

        email = request.data.get('email', None)
        password = request.data.get('password', None)
        
        if not email or not password:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"message": "email or pass missing"})
        
        try:
            user = User.objects.get(email=email)
            if not user.check_password(password):
                return Response({"message": "Incorrect password."}, status=status.HTTP_400_BAD_REQUEST)
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        
        except User.DoesNotExist:
            return Response({"message": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RegisterAPIView(APIView):
    
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request, format=None):
        name = request.data.get('name', None)
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        if not name or not email or not password:
            return Response({"message": "Username, email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        user_found = User.objects.filter(email=email)
        
        if user_found:
            return Response(data={"message": "choose unique email "}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.create_user(email, password, username=name)
            
            token = Token.objects.create(user=user)

            return Response({"message": "Successfully registered.",  "token": token.key}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LogoutAPIView(APIView):
    
    def post(self, request, format=None):
        request.user.auth_token.delete()
        return Response({"message": "User logged out"})

# Test route
class TestAPIView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serialized = UserSerializer(request.user)
        return Response({"user": serialized.data})
