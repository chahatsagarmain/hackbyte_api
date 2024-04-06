from rest_framework import serializers
from django.contrib.auth import get_user_model
from parser.serializers import PDFserializer
from chat.serializers import ChatSessionSerializer

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    pdfs = PDFserializer(many=True )

    class Meta:
        model = User
        fields = ['id','username','email','pdfs','chats']