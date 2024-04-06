from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from authentication_app.serializers import UserSerializer

class UserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        user = request.user
        serialized_user = UserSerializer(user)
        return Response({"user": serialized_user.data}, status=status.HTTP_200_OK)
