from django.http import HttpRequest
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from .utils.gemini import *
from .utils.mongodb import *

class GetResults(APIView):
    def get(self, request, format=None):
        prompt = request.query_params["prompt"]
        prompt_embedding = generateEmbedding(prompt)

        companies = findBestCompanies(prompt)

        results = []

        for company in companies:
            results.append({
                "name": company["name"],
                "description": company["description"],
                "country": company["country"],
                "suppliers": []
            })

            suppliers = findBestSuppliers(prompt, company["_id"])

            for supplier in suppliers:
                results[-1]["suppliers"].append({
                    "name": supplier["name"],
                    "description": supplier["description"],
                    "country": supplier["country"]
                })
        
        return Response({"HScode": findHSCode(prompt), "companies": results})

def index(request):
    return render(request, "index.html")
