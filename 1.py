import spacy
from pdfminer.high_level import extract_text
import re
import os
import pandas as pd

path = r'C:\fission_labs2\project_assigned\Life Insurances-20240813T190456Z-001\Life Insurances\Aditya Birla Sun Life'

file = [f for f in os.listdir(path) if f.endswith('.pdf')]

nlp = spacy.load('en_core_web_sm')

def parse_content(text):
    pattern_name = r'(Mr\.?\s+[A-Z][a-z]*\s+[A-Z][a-z]*|Ms\.?\s+[A-Z][a-z]*\s+[A-Z][a-z]*)'
    pattern_age = r'(\b\d{1,3}\s*(Years|yrs)\b)'
    pattern_gender = r'\b(Male|Female)\b'
    pattern_smoker = r'Smoker Status\s*:\s*(Tobacco User|Non-Tobacco User|Chews Tobacco|Uses Tobacco|Smoker|Non-Smoker|Ex-Smoker|Occasional Smoker|Heavy Smoker)'
    pattern_provider = r'\b([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*)\b'
    #pattern_policy = r'\b([A-Za-z0-9\-]+(?:\s+[A-Za-z0-9\-]+)*)\b'
    pattern_policy = r'\b[A-Za-z0-9\s\-]+Plan\b'

    pattern_premium_term = r'Premium Paying Term\s*:\s*(\d+\s*(Years|Months))'

    pattern_premium_mode = r'\b(Monthly|Quarterly|Semi-Annually|Yearly|Bi-Annually|Single)\b'
    pattern_premium_amount = r'\b([₹$€£]?\s*\d+(?:,\d{3})*(?:\.\d{1,2})?)\b'
    pattern_sum_assured = r"Sum Assured\s*:\s*Rs?\.?\s*\d+"
#pattern_sum_assured = r'\b(Sum Assured\s*:\s*Rs\.?\s*(\d+(?:,\d{3})*(?:\.\d{1,2,0})?))'


    name_matches = re.findall(pattern_name, text)
    age_matches = re.findall(pattern_age, text)
    gender_matches = re.findall(pattern_gender, text)
    smoker_matches = re.findall(pattern_smoker, text)
    #tobacco_matches = re.findall(pattern_tobacco, text)
    provider_matches = re.findall(pattern_provider, text)
    policy_matches = re.findall(pattern_policy, text)
    premium_mode_matches = re.findall(pattern_premium_mode, text)
    premium_term_matches = re.findall(pattern_premium_term, text)
    premium_amount_matches = re.findall(pattern_premium_amount, text)
    sum_assured_matches = re.findall(pattern_sum_assured, text)

    if name_matches:
        name = name_matches[0]
        print("Name:", name)
    else:
        print("No name match found.")
    
    if age_matches:
        age = age_matches[0][0]  # [0][0] to get the age number alone
        print("Age:", age)
    else:
        print("No age match found.")
    
    if gender_matches:
        gender = gender_matches[0]
        print("Gender:", gender)
    else:
        print("No gender match found.")
    
    if smoker_matches:
        smoker_status = smoker_matches[0]
        print("Smoker Status:", smoker_status)
    else:
        print("No smoker status match found.")
    

    if provider_matches:
        provider = provider_matches[0]
        print("Insurance Provider:", provider)
    else:
        print("No insurance provider match found.")
    
    if policy_matches:
        policy = policy_matches[0]
        print("Insurance Policy/Product Name:", policy)
    else:
        print("No insurance policy/product name match found.")
    
    if premium_mode_matches:
        premium_mode = premium_mode_matches[0]
        print("Mode of Premium:", premium_mode)
    else:
        print("No mode of premium match found.")
    
    if premium_term_matches:
        premium_term = premium_term_matches[0][0]  # [0][0] to get the term number alone
        print("Premium Term:", premium_term)
    else:
        print("No premium term match found.")
    
    if premium_amount_matches:
        premium_amount = premium_amount_matches[0]
        print("Premium Amount (1st Premium without Tax/GST):", premium_amount)
    else:
        print("No premium amount match found.")
    
    if sum_assured_matches:
        sum_assured = sum_assured_matches[0]
        print("Sum Assured:", sum_assured)
    else:
        print("No sum assured match found.")


for f in file:
    print('Reading PDF File...')
    text = extract_text(os.path.join(path,f), page_numbers = [0])

    parse_content(text)