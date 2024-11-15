import fitz  # PyMuPDF for PDF reading
import requests  # For API calls to Hugging Face or Groq
import spacy  # For NER
import re

# Load a pre-trained NER model for insurance documents if available (or use 'en_core_web_sm')
nlp = spacy.load('en_core_web_sm')

# Function to extract text from PDF using PyMuPDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

# Preprocess extracted text for better model performance
def preprocess_text(text):
    # Remove any unnecessary line breaks and excessive whitespace
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Function to use spaCy NER for initial data extraction
def extract_entities_with_spacy(text):
    doc = nlp(text)
    entities = {
        "PERSON": [],
        "ORG": [],
        "DATE": [],
        "MONEY": []
    }
    for ent in doc.ents:
        if ent.label_ in entities:
            entities[ent.label_].append(ent.text)
    return entities

# Function to query Hugging Face or Groq API for more refined information extraction
def extract_details_with_huggingface(text):
    api_url = 'https://huggingface.co/stabilityai/stable-diffusion-3.5-medium'  # Replace with your model endpoint
    headers = {
        'Authorization': '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'  # Replace with your Hugging Face API key
    }

    payload = {
        "inputs": {
            "text": f"""
            Extract the following information from the insurance document provided:
            - Insurance Provider's name
            - Insurance Policy/Product name
            - Name of the Policy holder/Policy Insured's name
            - Age or DOB
            - Gender
            - Smoker status and Tobacco user
            - Mode of premium
            - Premium Term
            - Premium amount (1st Premium without Tax/GST)
            - Sum Assured

            Document:
            {text}
            """
        }
    }

    response = requests.post(api_url, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        print("Error:", response.status_code, response.text)
        return None

# Main function to combine NER and LLM for extraction
def extract_insurance_details(pdf_path):
    # Step 1: Extract text from PDF
    pdf_text = extract_text_from_pdf(pdf_path)
    pdf_text = preprocess_text(pdf_text)

    # Step 2: Use spaCy NER for initial entity extraction
    initial_entities = extract_entities_with_spacy(pdf_text)
    print("Initial entities extracted using NER:", initial_entities)

    # Step 3: Use Hugging Face model for detailed extraction and refinement
    extracted_details = extract_details_with_huggingface(pdf_text)
    
    if extracted_details:
        print("\nDetails extracted using the model:\n")
        print(extracted_details)

    return extracted_details

# Path to the insurance PDF
pdf_path = r'C:\fission_labs\project_assigned\Life Insurances-20240813T190456Z-001\sample\1\01 - Aditya Birla Sun Life.pdf'
extracted_info = extract_insurance_details(pdf_path)