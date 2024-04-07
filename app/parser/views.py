from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from .models import PDF
from .serializers import PDFserializer

# Import token authentication
from rest_framework.authentication import TokenAuthentication

# Temporary method for unique ids for pdf storing
import os
import json
from .utils import upload_pdf, send_raw_text

class UploadView(APIView):
    
    # Add token authentication
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [FormParser, MultiPartParser]
    
    def post(self, request, format=None):
        
        file = request.data.get('file', None)
        user = request.user
        
        if not file:
            return Response(data={"message": "File Missing"}, status=status.HTTP_404_NOT_FOUND)
        
        filename = file.name 
        
        if filename.split('.')[-1] != 'pdf':
            return Response(data='file uploaded is not pdf', status=status.HTTP_400_BAD_REQUEST)

        pdf = PDF.objects.create(uploaded_by=request.user, file_url="")

        pdf_id = pdf.id

        with open(f"./uploads/{pdf_id}.pdf", 'wb+') as save_file:
            save_file.write(file.read())
            
        send_raw_text(str(pdf_id),str(user.id))

        response = upload_pdf(pdf_id)
        
        if not response:
            return Response({"message": "error while uploading to s3"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        pdf_url = f'https://{os.getenv("bucket")}.s3.{os.getenv("region")}.amazonaws.com/{pdf_id}.pdf'

        pdf.file_url = pdf_url
        pdf.save()

        return Response(data={"message": "pdf saved", "pdf_id": str(pdf_id), "pdf_url": str(pdf_url)})
    
    def delete(self, request, format=None):
                
        pdf_id = json.loads(request.body).get("pdf_id", None)
        
        if not pdf_id:
            return Response({"message": "pdf id not provided"}, status=status.HTTP_404_NOT_FOUND)
        
        if not os.path.exists(f"./uploads/{pdf_id}.pdf"):
            return Response({"message": "pdf does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        pdf = PDF.objects.get(id=pdf_id)
                
        if not pdf:
            return Response({"message": "no pdf with this id "}, status=status.HTTP_404_NOT_FOUND)
        
        pdf.delete()
        os.remove(f"./uploads/{pdf_id}.pdf")
        
        return Response({"message": "pdf deleted"})        
        
        
class PDFView(APIView):
    
    # Add token authentication
    authentication_classes = [TokenAuthentication]
    
    def post(self, request, format=None):
        
        pdf_id = request.data.get("pdf_id", None)
        
        if not pdf_id:
            return Response({"message": "pdf id not provided"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            data = PDF.objects.filter(id=pdf_id).first()
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        if not data:
            return Response({"message": "No PDF found with this ID"}, status=status.HTTP_404_NOT_FOUND)
        
        serialized_data = PDFserializer(data)
        
        return Response(serialized_data.data)

# class ParserView(APIView):

#     # Add token authentication
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request, format=None):
        
#         pdf_id = request.data.get("pdf_id", None)
#         user = request.user
        
#         if not pdf_id:
#             return Response({"message": "pdf id not provided"}, status=status.HTTP_404_NOT_FOUND)

#         if not os.path.exists(f"./uploads/{pdf_id}.pdf"):
#             return Response({"message": "the pdf does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
#         try:
#             raw_text = parse_pdf(pdf_id=pdf_id)
#             text_splitter(raw_text=raw_text, user_id=user.id, pdf_id=pdf_id)
            
#             return Response({"message": "text parsed"})
#         except Exception as e:
            
#             return Response({"message": str(e)})
