import spacy
from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams
import re
import os
import pandas as pd

# Define the path to the main directory
main_path = r'C:\fission_labs\project_assigned\Life Insurances-20240813T190456Z-001\Life Insurances'

# Define the output directory and file path
output_dir = r'C:\fission_labs\project_assigned\Life Insurances'
output_file = os.path.join(output_dir, 'insurance_data5.xlsx')

# Create the output directory if it does not exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Initialize spaCy model
nlp = spacy.load('en_core_web_sm')

def parse_content(text):
    patterns = {
        'Name': r'(?:Name\s+of\s+the\s*:\s*|Mr\.?|Mrs\.?|Ms\.?|Dear)\s*[A-Z][a-z]+\s+[A-Z][a-z]+',
        'Age': r'Age\s*:\s*\d{1,9}\b|\b\d{1,9}\s*(?:Years|yrs)\b',
        'Gender': r'\b(?:Male|Female|male|female)\b',
        'Smoker Status': r'(?:Smoker\s*Status\s*:\s*(?:Smoker|Non-Smoker|Yes|No)|Smoker\s*:\s*(?:Yes|No))',
        'Insurance Provider': r'\b[A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*\b',
        'Insurance Policy/Product Name': r'\b[A-Za-z0-9\s\-]+Plan\b',
        'Premium Term': r'Premium Paying Term\s*:\s*\d+\s*(?:Years|Months)',
        'Mode of Premium': r'\b(?:Monthly|Quarterly|Semi-Annually|Yearly|Bi-Annually|Single)\b',
        'Premium Amount': r'\b[₹$€£]?\s*\d+(?:,\d{3})*(?:\.\d{1,2})?\b',
        'Sum Assured': r'Sum Assured\s*:\s*Rs?\.?\s*[₹$€£]?\s*\d+(?:,\d{3})*(?:\.\d{1,2})?\b'
    }
    
    results = {}
    for key, pattern in patterns.items():
        matches = re.findall(pattern, text)
        if matches:
            results[key] = matches[0] if isinstance(matches[0], str) else " ".join(matches[0])
        else:
            results[key] = "Not found"
    
    return results

# Create a list to store results
results_list = []

# Iterate through each folder in the main directory
for root, dirs, files in os.walk(main_path):
    for file in files:
        if file.endswith('.pdf'):
            file_path = os.path.join(root, file)
            print(f'Reading PDF File: {file_path}')
            
            # Extract text from all pages using LAParams
            try:
                laparams = LAParams()
                text = extract_text(file_path, laparams=laparams)
            except Exception as e:
                print(f"Error reading {file}: {str(e)}")
                continue
            
            content = parse_content(text)
            content['File Name'] = file
            results_list.append(content)

# Convert the results list to a DataFrame
results_df = pd.DataFrame(results_list, columns=[
    'File Name', 'Name', 'Age', 'Gender', 'Smoker Status', 'Insurance Provider',
    'Insurance Policy/Product Name', 'Premium Term', 'Mode of Premium',
    'Premium Amount', 'Sum Assured'
])

# Save the results to an Excel file
results_df.to_excel(output_file, index=False)

print(f'Data has been successfully written to {output_file}')
