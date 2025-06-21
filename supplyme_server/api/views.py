from django.shortcuts import render
from google import genai
from dotenv import load_dotenv

import os

load_dotenv() # Load variables from .env

api_key = os.getenv('API_KEY')
database_url = os.getenv('ATLAS_URI')

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-2.5-flash", contents="Explain how AI works in a few words"
)

def index(request):
    print(response)
    return render(request)