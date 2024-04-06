from rest_framework.views import APIView
from .models import ChatSession , Chat
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .utils import chat_response
from .serializers import ChatSessionSerializer
from parser.models import PDF

class ChatView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def post(self , request , format = None):
        
        decoded_body = request.data
        
        user = request.user
        chat_session_id : str | None = decoded_body.get("chat_session_id",None)
        pdf_id : str | None = decoded_body.get("pdf_id",None)
        message : str = decoded_body.get("message","")
        
        if not pdf_id:
            return Response({"message" : "pdf_id not found"} )
        
        #creating a new chatsession
        if not chat_session_id:
            pdf = PDF.objects.filter(id = pdf_id)[0]
            chat_session = ChatSession.objects.create(user = user , pdf = pdf)
            chat = Chat.objects.create(message = message , session = chat_session)
            response = chat_response()
            chat = Chat.objects.create(message = response , session = chat_session)
            serialzed_chat = ChatSessionSerializer(chat_session)
            print(serialzed_chat.data)
            return Response({"response" : response})
        
        chat_session = ChatSession.objects.get(id=chat_session_id)
        chat = Chat.objects.create(message=message, session=chat_session)
        response = chat_response()
        chat = Chat.objects.create(message=response, session=chat_session)
        serialized_chat = ChatSessionSerializer(chat_session)
        print(serialized_chat.data)
        return Response({"response" : response})

class ChatSessionView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def get(self  , request , format = None):
        
        chat_session_id : str | None = request.data.get("chat_session_id",None)
        
        if not chat_session_id:
            return Response({"message" : "chat session id not provided"})
        
        chat_session = ChatSession.objects.get(id = chat_session_id)
        
        serialzied_data = ChatSessionSerializer(chat_session)
        
        return Response({"chat_session" : serialzied_data.data})
    
    def post(self , request , format = None):
        
        pdf_id : str | None = request.data.get("pdf_id",None)
        
        user = request.user
        
        if not pdf_id :
            return Response({"message" : "pdf_id missing"} , status=status.HTTP_404_NOT_FOUND)
        
        pdf = PDF.objects.filter(id = pdf_id)
        
        chat_session = ChatSession.objects.create(pdf = pdf[0] , user = user)
        
        return Response({"chat_session_id" : chat_session.id})