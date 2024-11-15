import pdfplumber

# Path to your PDF file
pdf_path = r'C:\fission_labs\project_assigned\Life Insurances-20240813T190456Z-001\sample\1\01 - Aditya Birla Sun Life.pdf'

# Open the PDF file
with pdfplumber.open(pdf_path) as pdf:
    # Loop through all the pages
    for page in pdf.pages:
        # Extract text from the page
        text = page.extract_text()
        print(text)
