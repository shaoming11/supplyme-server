from google import genai
import os

api_key = os.getenv('API_KEY')

client = genai.Client(api_key=api_key)

def generateEmbedding(text):
    result = client.models.embed_content(
            model="gemini-embedding-exp-03-07",
            contents=text)

    return result

def findHSCode(text):
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite-preview-06-17", contents=f"What is the most likely HS code for the product described below (only return the HS code without any other message): \n\n[\n{text}\n]?"
    )
    return response

def findProductName(text):
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite-preview-06-17", contents=f"What is the most likely product name for the product described below (only return the name of the product): \n\n[\n{text}\n]?"
    )
    return response

def generateCompanyDescription(companyName):
    response = client.models.generate_content(
        model="gemini-2.5-pro", contents=f"Could you describe the company listed below (only list what this company does by providing a brief description) \n\n[\n{companyName}\n]?"
    )
    return response

def generateSupplierDescription(companyName):
    response = client.models.generate_content(
        model="gemini-2.5-pro", contents=f"Could you describe what products the company listed below supplies (only list products) \n\n[\n{companyName}\n]?"
    )
    return response