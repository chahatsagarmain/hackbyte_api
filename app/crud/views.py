from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from authentication_app.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status

class UserView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def get(self , request , format=None):
        
        user = request.user
        
        serialized_user = UserSerializer(user)
        
        return Response({"user" : serialized_user.data} , status=status.HTTP_200_OK)
        
    