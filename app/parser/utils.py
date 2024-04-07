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
import json
import google.generativeai as genai
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
import http.client
import requests
from langchain.chains import RetrievalQA
from  langchain_core.prompts import PromptTemplate


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
from optimum.onnxruntime import ORTModelForSequenceClassification
from transformers import AutoTokenizer, pipeline


tokenizer = AutoTokenizer.from_pretrained("laiyer/unbiased-toxic-roberta-onnx")
model = ORTModelForSequenceClassification.from_pretrained("laiyer/unbiased-toxic-roberta-onnx",file_name="model.onnx")
toxic_classifier = pipeline(
    task="text-classification",
    model=model,
    tokenizer=tokenizer,
)


genai.configure( api_key=os.getenv("GOOGLE_API_KEY"))

model = ChatGoogleGenerativeAI(model="gemini-pro",google_api_key=os.getenv("GOOGLE_API_KEY"),temperature=0.2,convert_system_message_to_human=True)

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
    # create the open-source embedding function
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
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

def response_from_pdf(question:str,user_id:str,pdf_id: str,toxic_check: bool):
    # if classifier( question)[0]['label']=="INJECTION":
    #     return {"response":"prompt_injection"}
    if toxic_check:
        if toxic_classifier(question)[0]['score']>=0.6:
          return {"response":"toxic_prompt"}
    directory = f"./chroma_db/{user_id}/{pdf_id}"
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_index = Chroma(persist_directory=directory, embedding_function=embeddings).as_retriever()
    template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. Keep the answer as concise as possible. Always say "thanks for asking!" at the end of the answer.
    {context}
    Question: {question}
    Helpful Answer:"""
    QA_CHAIN_PROMPT = PromptTemplate.from_template(template)# Run chain
    qa_chain = RetrievalQA.from_chain_type(model,retriever=vector_index,return_source_documents=True,chain_type_kwargs={"prompt": QA_CHAIN_PROMPT})
   
    result = qa_chain({"query": question})
    return {"response": result["result"]}

def send_raw_text( pdf_id : str, user_id : str):
    
    raw_text = parse_pdf(pdf_id)
    print("2")
    data = {
        "pdf_id" : pdf_id,
        "text" : str(raw_text),
        "user_id" : user_id
    }
    
    headers = {
        "Content-Type": "application/json",
        # Add any other headers that you need
    }
    
    conn = http.client.HTTPSConnection("fb16-14-139-241-214.ngrok-free.app")
    conn.request("POST", "/upload", body=json.dumps(data), headers=headers)
    
    response = conn.getresponse()
    print(response.status)