from google import genai
import os
import time

api_key = os.getenv('API_KEY')

client = genai.Client(api_key=api_key)

def generateEmbedding(text):
    try:
        result = client.models.embed_content(
        model="gemini-embedding-exp-03-07",
        contents=text)
        return result.embeddings[0].values
    except Exception as e:
        print(e)
        if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
            print("Rate limit hit, waiting 60 seconds...")
            time.sleep(60)  # Wait 1 minute
            return generateEmbedding(text)  # Retry
        else:
            raise e

def findHSCode(text):
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite-preview-06-17", contents=f"What is the most likely HS code for the product described below (only return the HS code without any other message): \n\n[\n{text}\n]?"
    )
    return response.text

def findProductName(text):
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite-preview-06-17", contents=f"What is the most likely product name for the product described below (only return the name of the product): \n\n[\n{text}\n]?"
    )
    return response.text

def generateCompanyDescription(companyName, companyCountry):
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=f"Could you describe the company listed below (only list what this company does by providing a brief description) \n\n[\n{companyName} ({companyCountry})\n]?"
    )
    return response.text

def generateSupplierDescription(supplierName, supplierCountry):
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=f"Could you describe what products the company listed below supplies (only list products) \n\n[\n{supplierName} ({supplierCountry})\n]?"
    )
    return response.text