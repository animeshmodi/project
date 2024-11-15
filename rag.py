import os
import faiss
import torch
from transformers import AutoTokenizer, AutoModel
from pdfminer.high_level import extract_text
from langchain_huggingface import HuggingFaceEmbeddings  # Updated import
from langchain_community.vectorstores import FAISS  # Updated import
from langchain.chains import RetrievalQA
from langchain_community.llms import HuggingFacePipeline

# Load the Hugging Face model and tokenizer
model_name = "sentence-transformers/all-MiniLM-L6-v2"  # Corrected model identifier
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

# Create embeddings
embeddings = HuggingFaceEmbeddings(model_name=model_name)  # Updated initialization

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = extract_text(pdf_path)
    return text

# Function to process multiple folders and create a vector store
def process_folders(folder_path):
    all_texts = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".pdf"):
                pdf_path = os.path.join(root, file)
                text = extract_text_from_pdf(pdf_path)
                if text.strip():  # Ensure text is not empty
                    all_texts.append(text)
    
    if not all_texts:
        raise ValueError("No text was extracted from any PDFs.")

    vector_store = FAISS.from_texts(all_texts, embeddings)  # Initialize with actual texts
    return vector_store


# Function to answer questions using the Hugging Face pipeline
def answer_question(vector_store, query):
    # Use Hugging Face pipeline instead of HuggingFaceInference
    qa_pipeline = HuggingFacePipeline.from_pretrained("gpt-3.5-turbo")
    chain = RetrievalQA.from_llm(qa_pipeline, vector_store=vector_store)
    response = chain.run(query)
    return response

# Example usage for processing a folder of PDFs
folder_path = 'C:\fission_labs\project_assigned\Life Insurances-20240813T190456Z-001\sample\1'
vector_store = process_folders(folder_path)

query = "What is the coverage amount in the document?"
response = answer_question(vector_store, query)
print(response)
