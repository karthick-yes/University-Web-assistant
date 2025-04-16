import os
import PyPDF2

def pdf_to_text(pdf_path):
    """Extracts text from a PDF file given its file path."""
    text = ""
    try:
        with open(pdf_path, "rb") as f:
            pdf_reader = PyPDF2.PdfReader(f)
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
    return text

def convert_pdfs_in_directory(directory):
    """
    Searches through the provided directory (including subfolders)
    for any PDF files, converts them to text, and saves the output
    with the same base name in the same directory.
    """
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.pdf'):
                pdf_path = os.path.join(root, file)
                print(f"Processing PDF: {pdf_path}")
                text = pdf_to_text(pdf_path)
                if text:
                    # Create the output file path: same location, same base name, with .txt extension.
                    base_name = os.path.splitext(file)[0]
                    txt_path = os.path.join(root, base_name + ".txt")
                    try:
                        with open(txt_path, "w", encoding="utf-8") as out_file:
                            out_file.write(text)
                        print(f"Saved extracted text to: {txt_path}")
                    except Exception as e:
                        print(f"Error writing to {txt_path}: {e}")
                else:
                    print(f"No text extracted from: {pdf_path}")

if __name__ == "__main__":
    # Hardcode the directory containing PDFs here.
    # Update the path below as needed. For Windows use double backslashes or a raw string (r"").
    directory =  r"C:\\Users\\NITRO\\Downloads\\Department Handbooks (2024-25)-20250416T075326Z-001"
    if os.path.isdir(directory):
        convert_pdfs_in_directory(directory)
    else:
        print("Provided path is not a valid directory.")
