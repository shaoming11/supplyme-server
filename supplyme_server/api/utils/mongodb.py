from mongoengine import *
from .gemini import *
import os

connect(host=os.getenv('ATLAS_URI'))

class Company(Document):
    name = StringField(required=True)
    description = StringField(required=True)
    country = StringField(required=True)
    embedding = ListField(FloatField())

class Supplier(Document):
    name = StringField(required=True)
    description = StringField(required=True)
    country = StringField(required=True)
    embedding = ListField(FloatField())
    company = ReferenceField(Company, reverse_delete_rule=CASCADE)

def addCompany(companyName, companyCountry):
    companyDescription = generateCompanyDescription(f"{companyName} ({companyCountry})")
    company = Company(name=companyName, companyDescription=companyDescription, embedding=generateEmbedding(f"{companyName} ({companyCountry}):\n\n {companyDescription}")).save()

def addSupplier(companyID, supplierName, supplierCountry):
    supplierDescription = generateSupplierDescription(f"{supplierName} ({supplierCountry})")
    supplier = Supplier(name=supplierName, supplierDescription=supplierDescription, embedding=generateEmbedding(f"{supplierName} ({supplierCountry}):\n\n {supplierDescription}"), company=companyID).save()

def findBestCompanies(prompt, numberOfCompanies):
    pass

def findBestSuppliers(prompt, companyID, numberOfSuppliers):
    pass