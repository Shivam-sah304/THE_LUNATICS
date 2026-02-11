import io, pytesseract, pdfplumber, docx
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def read_license(nmc):
    file_type = nmc.content_type
    print(file_type)

    file = nmc.read()
    
    if file_type in ['image/png', 'image/jpeg']:
      image = Image.open(io.BytesIO(file))
      file_text = pytesseract.image_to_string(image, lang='eng', config="--oem 3 --psm 6")

      print(file_text if file_text.strip() else "[NO TEXT FOUND]")

    
    elif file_type == 'application/pdf':
      with pdfplumber.open(io.BytesIO(file)) as pdf:
        file_text = []
        for page in pdf.pages:
            file_text.append(page.extract_text() or "")
        file_text = ' '.join(file_text)

    elif file_type == 'docx':
        document = docx.Document(io.BytesIO(file))
        file_text = ' '.join([para.text for para in document.paragraphs])

    elif file_type == 'txt':
      file_text = file

    else:
      return ('Unsupported file type')
    print(file_text)
    return {'name': 'Neeta Timilsina',
            'nmc': '13039',
            'degree': 'MBBS'}

