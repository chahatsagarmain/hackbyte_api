import pdfplumber
from langchain.text_splitter import RecursiveCharacterTextSplitter
import boto3
import os
from botocore import client

expiration = 60 * 60 * 60 

def parse_pdf(pdf_id : str) -> str:
    
    with pdfplumber.open(f"./uploads/{pdf_id}.pdf") as pdf:
        raw_text : str = ""
        for i in range(len(pdf.pages)):
            pages = pdf.pages[i]
            raw_text += pages.extract_text()
            
        if len(raw_text) == 0:
            raise ValueError("no data found")
        
        return raw_text
        

def text_splitter(raw_text : str):
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000 , chunk_overlap = 0)
    splitted_text = text_splitter.split_text(raw_text)
    #deal with chroma here 

def get_presigned_url(file_id):
    print(os.getenv("region"))
    s3_client = boto3.client('s3' , region_name=os.getenv("region") , config= client.Config(signature_version='s3v4'))

    global expiration
    
    print(str(file_id) + ".pdf")
    
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': "hackbyte-bucket",
                                                            'Key': str(file_id) + ".pdf"},
                                                    ExpiresIn=expiration,
                                                    )
    except Exception as e:
        return None
    
    return response

def upload_pdf(file_id):
    
    s3_client = boto3.client('s3' , region_name=os.getenv("region") , config= client.Config(signature_version='s3v4'))
    file_name = str(file_id) + ".pdf"
        
    try:
        s3_client.upload_file(Filename = f"./uploads/{file_name}",Bucket = os.getenv("bucket") , Key = file_name)
    except Exception as e:
        print(e)
        return False
    
    return True
