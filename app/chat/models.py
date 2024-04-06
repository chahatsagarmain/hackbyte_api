from django.db import models
from django.contrib.auth import get_user_model
from parser.models import PDF

User = get_user_model()

class ChatSession(models.Model):
    user = models.ForeignKey(User, related_name='chat_sessions', on_delete=models.CASCADE , null=True , to_field="id")
    pdf = models.ForeignKey(PDF, related_name='chat_sessions', on_delete=models.CASCADE , null=True , to_field="id")
    timestamp = models.DateTimeField(auto_now_add=True)

class Chat(models.Model):
    message = models.TextField(null = True)
    timestamp = models.DateTimeField(auto_now_add=True)
    session = models.ForeignKey(ChatSession, related_name='chats', on_delete=models.CASCADE)