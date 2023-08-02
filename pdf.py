import os
import requests
import io
from urllib.parse import urlparse, quote
import PyPDF2

urls = ["https://www.ashoka.edu.in/wp-content/uploads/2021/06/History-HB.pdf", "https://ashoka.edu.in/wp-content/uploads/2021/06/Handbook-Philosophy.pdf", "https://ashoka.edu.in/static/doc_uploads/file_1600847875.pdf" ,"https://ashoka.edu.in/wp-content/uploads/2021/06/Bio-Handbook-2021.pdf", "https://www.ashoka.edu.in/wp-content/uploads/2021/06/Physics-HB.pdf"]
def pdf_to_text(pdf_content):
    pdf_file = io.BytesIO(pdf_content)
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""

    for page in pdf_reader.pages:
        text += page.extract_text()

    return text

def crawl(url):
    local_domain = urlparse(url).netloc
    if not os.path.exists("pdffiles"):
        os.mkdir("pdffiles")
    
    response = requests.get(url)
    sanitized_url = quote(url, safe='')

    if response.headers.get('Content-Type') == "application/pdf":
        pdf_text = pdf_to_text(response.content)
        
        with open('pdffiles/' + local_domain + sanitized_url + '.txt', "w", encoding="utf-8") as f:
            f.write(pdf_text)

# Example usage
for url in urls:
    crawl(url)

