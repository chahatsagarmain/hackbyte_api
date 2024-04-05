from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FormParser , MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from .models import PDF
#temporary method for unique ids for pdf storing
import os
import json
from .utils import parse_pdf , text_splitter

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

        file_id = PDF.objects.create(uploaded_by = request.user).id

        with open(f"./uploads/{file_id}.pdf",'wb+') as save_file:
            save_file.write(file.read())
        
        return Response(data={"message" : "pdf saved" , "pdf_id" : file_id})
    
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
        
