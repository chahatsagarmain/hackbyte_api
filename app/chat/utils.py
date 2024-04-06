from parser.utils import parse_pdf , text_splitter , response_from_pdf

def chat_response(message , pdf_id, user_id):
    
    raw_text = parse_pdf(pdf_id)
    
    if not text_splitter(raw_text,user_id,pdf_id):
        return None
    
    return response_from_pdf(message , user_id , pdf_id , True)