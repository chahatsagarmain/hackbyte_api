from rest_framework import serializers
from .models import ChatSession, Chat
# from authentication_app.serializers import UserSerializer
# from parser.serializers import PDFserializer

class ChatSerializer(serializers.ModelSerializer):
    # users = UserSerializer(many = True , read_only = True)
    # pdfs = PDFserializer(many = True , read_only = True)
    class Meta:
        model = Chat
        fields = '__all__'

class ChatSessionSerializer(serializers.ModelSerializer):
    chats = ChatSerializer(many=True, read_only=True)

    class Meta:
        model = ChatSession
        fields = ['timestamp', 'chats']