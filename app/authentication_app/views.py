from rest_framework.views import APIView 
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny , IsAuthenticated
from rest_framework.parsers import MultiPartParser , FormParser
from rest_framework.exceptions import status
from rest_framework.response import Response
from django.contrib.auth import login , logout , authenticate 
from rest_framework.authentication import get_user_model

User = get_user_model()

class LoginAPIView(APIView):
    
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser , FormParser]
    
    def post(self , request , format = None):

        email : str = request.data.get('email',None)
        password : str = request.data.get('password',None)
        
        if not email or not password :
            return Response(status=status.HTTP_404_NOT_FOUND , data={"message" : "email or pass missing"})
        
        try:
     
            user = authenticate(request , email = email , password = password)
     
            if user is None :
                return Response({"message" : "error while authenticating user"} , status=status.HTTP_400_BAD_REQUEST)
            
            login(request,user)

            return Response({"message" : "Successfully logged in"} , status=status.HTTP_200_OK)
        
        except Exception as e:
            
            return Response({"error" : e} , status = status.HTTP_500_INTERNAL_SERVER_ERROR)

class RegisterAPIView(APIView):
    
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser , FormParser]
    
    def post(self, request, format=None):
        name = request.data.get('name', None)
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        if not name or not email or not password:
            return Response({"message": "Username, email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        user_found = User.objects.filter(email = email)
        
        if user_found :
            return Response(data = {"message" : "choose unique email "} , status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.create_user(email, password , username = name)
            
            login(request , user)
            
            return Response({"message": "Successfully registered."}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class LogoutAPIView(APIView):
    
    def post(self , request , format = None):
        
        logout(request= request)
        
        return Response({"message" : "User logged out"})
        
#test route
class TestAPIView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def get(self , request):
        
        serialized = UserSerializer(request.user)
        
        return Response({"user" : serialized.data}) 