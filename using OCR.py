import re
import pytesseract
from pdf2image import convert_from_path
import pandas as pd
import os
from PIL import ImageEnhance
from PIL import Image

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Set the path to the poppler executable
poppler_path = r'C:\Program Files\poppler\poppler'

def ocr_extract_text_from_pdf(pdf_path):
    text = ""
    try:
        images = convert_from_path(pdf_path, dpi=200, poppler_path=poppler_path)
        for img in images:
            # Convert image to grayscale
            img = img.convert('L')
            # Enhance image contrast
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(2)  # Increase contrast
            
            page_text = pytesseract.image_to_string(img)
            text += page_text + "\n"
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
        return None
    return text

def structure_extracted_data(text, pdf_path):
    if text is None:
        return None

    data = {
        'File_Name': os.path.basename(pdf_path),
        'Insurance_Prov': '',
        'Policy_Product': '',
        'Policy_Holder': '',
        'Age_or_DOB': '',
        'Gender': '',
        'Smoker_Tobacco': '',
        'Premium_Mode': '',
        'Premium_Term': '',
        'Premium_Amount': '',
        'Sum_Assured': '',
        'Source_Path': pdf_path
    }

    patterns = {
        'Insurance_Prov': r"(?i)(insurance provider|provider)\s*:\s*([A-Za-z\s]+)",
        'Policy_Product': r"(?i)(policy name|product name)\s*:\s*([A-Za-z\s]+)",
        'Policy_Holder': r"(?i)(policy holder|insured name)\s*:\s*([A-Za-z\s]+)",
        'Age_or_DOB': r"(?i)(date of birth|dob|age)\s*:\s*([0-9/-]+)",
        'Gender': r"(?i)(gender)\s*:\s*(male|female)",
        'Smoker_Tobacco': r"(?i)(smoker status|tobacco user)\s*:\s*(yes|no)",
        'Premium_Mode': r"(?i)(mode of premium|premium mode)\s*:\s*([A-Za-z\s]+)",
        'Premium_Term': r"(?i)(premium term)\s*:\s*([0-9]+)",
        'Premium_Amount': r"(?i)(premium amount|1st premium)\s*:\s*([0-9,]+)",
        'Sum_Assured': r"(?i)(sum assured)\s*:\s*([0-9,]+)"
    }

    print("Extracted Text:\n", text)  # Print the entire extracted text for review

    for key, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            data[key] = match.group(2).strip() if match.group(2) else ""
            print(f"Extracted {key}: {data[key]}")
        else:
            print(f"{key} not found in {pdf_path}. Check if pattern needs adjustment.")
    
    return data

def process_pdfs_in_directory(directory_path):
    all_data = []
    for root, dirs, files in os.walk(directory_path):
        for filename in files:
            if filename.endswith(".pdf"):
                pdf_path = os.path.join(root, filename)
                print(f"Processing PDF: {filename}")
                extracted_text = ocr_extract_text_from_pdf(pdf_path)
                if extracted_text is not None:
                    structured_data = structure_extracted_data(extracted_text, pdf_path)
                    if structured_data is not None:
                        all_data.append(structured_data)
    return all_data

def save_to_excel(data, output_file):
    if data:
        df = pd.DataFrame(data)
        df.to_excel(output_file, index=False)
        print(f"Data saved to {output_file}")
    else:
        print("No data to save")

def main():
    directory_path = r'C:\fission_labs\project_assigned\Life Insurances-20240813T190456Z-001\sample\1'
    #output_file = r"C:\f
    output_file = r"C:\fission_labs\project_assigned\Life Insurances-20240813T190456Z-001\sample\insurance_policy_details.xlsx"
    
    print("Starting PDF processing...")
    all_data = process_pdfs_in_directory(directory_path)
    save_to_excel(all_data, output_file)

if __name__ == "__main__":
    main()