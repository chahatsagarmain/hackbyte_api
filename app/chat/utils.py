from parser.utils import parse_pdf , text_splitter , response_from_pdf
import requests

def chat_response(message : str , pdf_id : str, user_id : str):
    
    # raw_text = parse_pdf(pdf_id)
    
    data = {
        "query" : message,
        "pdf_id" : pdf_id,
        "user_id" : user_id,
        "toxic_check" : True
    }
    response = requests.post("http://127.0.0.1:7000/qna",json=data)
            
    return response.json()
    
    
    
    