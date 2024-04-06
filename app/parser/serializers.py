from rest_framework import serializers
from .models import PDF
from chat.serializers import ChatSessionSerializer

class PDFserializer(serializers.ModelSerializer):
    
    chat_sessions = ChatSessionSerializer(many = True , read_only = True)
    
    class Meta:
        model = PDF
        fields = ['id','file_url','uploaded_by','chat_sessions']