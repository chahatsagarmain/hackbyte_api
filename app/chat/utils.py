from parser.utils import parse_pdf , text_splitter , response_from_pdf
import requests

def chat_response(message : str , pdf_id : str, user_id : str):
    
    raw_text = parse_pdf(pdf_id)
    
    data = {
        "query" : message,
        "pdf_id" : pdf_id,
        "user_id" : user_id,
        "toxic_check" : True
    }
    response = requests.post("https://fb16-14-139-241-214.ngrok-free.app/qna",json=data)
    
    print(response)
    
    return response.json()
    
    
    
    