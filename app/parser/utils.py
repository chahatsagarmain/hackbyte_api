import pdfplumber
from langchain.text_splitter import RecursiveCharacterTextSplitter
import boto3
import os
from botocore import client
from pydantic import BaseModel
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import torch
import google.generativeai as genai

tokenizer = AutoTokenizer.from_pretrained("ProtectAI/deberta-v3-base-prompt-injection")
model = AutoModelForSequenceClassification.from_pretrained("ProtectAI/deberta-v3-base-prompt-injection")

classifier = pipeline(
  "text-classification",
  model=model,
  tokenizer=tokenizer,
  truncation=True,
  max_length=512,
  device=torch.device("cuda" if torch.cuda.is_available() else "cpu"),
)

genai.configure( api_key=os.getenv("GOOGLE_API_KEY"))

model = ChatGoogleGenerativeAI(model="gemini-pro",google_api_key=os.getenv("GOOGLE_API_KEY"),temperature=0.2,convert_system_message_to_human=True)
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001",google_api_key=os.getenv("GOOGLE_API_KEY"))

expiration = 60 * 60 * 60 *60

def parse_pdf(pdf_id : str) -> str:
    
    with pdfplumber.open(f"./uploads/{pdf_id}.pdf") as pdf:
        raw_text : str = ""
        for i in range(len(pdf.pages)):
            pages = pdf.pages[i]
            raw_text += pages.extract_text()
            
        if len(raw_text) == 0:
            raise ValueError("no data found")
        
        return raw_text
        

def text_splitter(raw_text : str,user_id : str, pdf_id : str):
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000 , chunk_overlap = 0)
    splitted_text = text_splitter.split_text(raw_text)
    directory = f"./chroma_db/{user_id}/{pdf_id}"
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    Chroma.from_texts(splitted_text, embeddings,persist_directory=directory).as_retriever()
    
    return True



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
