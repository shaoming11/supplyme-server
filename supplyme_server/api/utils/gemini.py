from google import genai
from dotenv import load_dotenv
import os
import requests

load_dotenv() # Load variables from .env

api_key = os.getenv('API_KEY')

client = genai.Client(api_key=api_key)

def generateEmbedding(text):
    api_endpoint = "https://gemini.googleapis.com/v1/projects/your-project-id/locations/your-location/models/your-model-id:embedText"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer your-api-key"
    }
    data = {
        "text": text
    }
    response = requests.post(api_endpoint, headers=headers, json=data)
    response = client.models.generate_content(
    model="gemini-2.5-flash", contents="Explain how AI works in a few words"
    )
    if response.status_code == 200:
        return response.json()["embedding"]
    else:
        raise Exception("Failed to generate embedding")

def findHSCode(text):
    pass

def generateCompanyDescription(companyName):
    pass

def generateSupplierDescription(companyName):
    pass