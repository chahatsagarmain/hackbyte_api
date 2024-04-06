from rest_framework import serializers
from .models import PDF
from chat.models import ChatSession
from chat.models import ChatSession

class PDFserializer(serializers.ModelSerializer):
    #chat_sessions = serializers.PrimaryKeyRelatedField(many=True, queryset=ChatSession.objects.all())

    class Meta:
        model = PDF
        fields = ['id','file_url','uploaded_by']