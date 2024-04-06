from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FormParser , MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from .models import PDF
from .serializers import PDFserializer

#temporary method for unique ids for pdf storing
import os
import json
from .utils import parse_pdf , text_splitter , upload_pdf , get_presigned_url

class UploadView(APIView):
    
    #Allow any for now 
    permission_classes = [IsAuthenticated]
    parser_classes = [FormParser,MultiPartParser]
    
    def post(self , request , format = None):
        
        file = request.data.get('file',None)
        
        if not file :
            return Response(data = {"message" : "File Missing"} , status=404)
        
        filename : str = file.name 
        
        if filename.split('.')[-1] != 'pdf':
            return Response(data = 'file uploaded is not pdf', status=status.HTTP_400_BAD_REQUEST)
        

        pdf = PDF.objects.create(uploaded_by = request.user , file_url = "")
        
        pdf_id = pdf.id
        
        with open(f"./uploads/{pdf_id}.pdf",'wb+') as save_file:
            save_file.write(file.read())

        response = upload_pdf(pdf_id)
        
        if not response:
            return Response({"message" : "error while uploading to s3"} , status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        pdf_url = f'https://{os.getenv("bucket")}.s3.{os.getenv("region")}.amazonaws.com/{pdf_id}.pdf'

        
        pdf.file_url = pdf_url
        pdf.save()

        return Response(data={"message" : "pdf saved" , "pdf_id" : pdf_id , "pdf_url" : pdf_url})
    
    def delete(self , request , format = None):
                
        pdf_id : str | None = json.loads(request.body).get("pdf_id",None)
        
        if not pdf_id:
            return Response({"message" : "pdf id not provided"} , status=status.HTTP_404_NOT_FOUND)
        
        if not os.path.exists(f"./uploads/{pdf_id}.pdf"):
            return Response({"message" : "pdf does not exist"} , status=status.HTTP_404_NOT_FOUND)
        
        pdf = PDF.objects.get(id = pdf_id)
                
        if not pdf :
            return Response({"message" : "no pdf with this id "} , status=status.HTTP_404_NOT_FOUND)
        
        pdf.delete()
 
        os.remove(f"./uploads/{pdf_id}.pdf")
        
        return Response({"message" : "pdf deleted"})        
        
        
class PDFView(APIView):
    
    def get(self , request , format = None):
        
        pdf_id : str | None = request.data.get("pdf_id",None)
        
        if not pdf_id:
            return Response({"message" : "pdf id not provided"} , status=status.HTTP_404_NOT_FOUND)
        
        data = PDF.objects.filter(id = pdf_id)[0]
        
        serialized_data = PDFserializer(data)
        
        return Response({"data" : serialized_data.data})

class ParserView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self , request , format = None):
        
        pdf_id : str | None = json.loads(request.body).get("pdf_id",None)
        
        if not pdf_id:
            return Response({"message" : "pdf id not provided"} , status=status.HTTP_404_NOT_FOUND)

        
        if not os.path.exists(f"./uploads/{pdf_id}.pdf"):
            return Response({"message" : "the pdf does not exist"} , status=status.HTTP_404_NOT_FOUND)
        
        try:
            raw_text : str = parse_pdf(pdf_id=pdf_id)
            text_splitter(raw_text=raw_text)
            
            return Response({"message" : "text parsed"})
        except Exception as e:
            
            return Response({"message" : str(e)})
        
