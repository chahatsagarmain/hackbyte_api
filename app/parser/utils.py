import pdfplumber
from langchain.text_splitter import RecursiveCharacterTextSplitter

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
    