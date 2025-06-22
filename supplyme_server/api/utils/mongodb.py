from .gemini import *
import os
from pymongo.mongo_client import MongoClient
from pymongo.operations import SearchIndexModel
import certifi
import json

URI = os.getenv('ATLAS_URI')
# connect(host=URI)

client = MongoClient(URI, tlsCAFile=certifi.where())
db = client['companyData']
collection = db['companyCollection']

NUMBER_OF_COMPANIES = 100

def createSearchIndex():
    # Create a search index model for vector similarity search
    # stores index structure in database
    search_index_model = SearchIndexModel(
    definition={
        "fields": [
        {
            "type": "vector",
            "path": "embedding",
            "numDimensions": 3072,
            "similarity": "dotProduct",
            "quantization": "scalar"
        },
        {
            "type": "filter",
            "path": "type"
        }
        ]
    },
    name="vector_index",
    type="vectorSearch"
    )
    result = collection.create_search_index(model=search_index_model)
    # print("New search index named " + result + " is building.")
    return result

def semanticSearch(query, neighbours, limit, companyID="-1", type="company"):
    # define pipeline
    pipeline = [
    {
        '$vectorSearch': {
            'index': 'vector_index', 
            'path': 'embedding', # property within the collection with the embedding
            'queryVector': generateEmbedding(query),
            'numCandidates': neighbours, # consider 99 nearest neighbours
            'limit': limit, # limit 10 closest results
            'company': companyID,
            'filter': {
                'type': type
            }
        }
    }, {
        '$project': {
        '_id': 0, 
        'name': 1,  # include in return
        'description': 1, 
        'company': 1,
        'country': 1
        }
    }
    ]
    # run pipeline
    result = client["companyData"]["companyCollection"].aggregate(pipeline)
    # # print results
    # for i in result:
    #     print(i)
    return result

def addCompany(companyName, companyCountry):
    description = generateCompanyDescription(companyName)

    collection.insert_one({
        "name": companyName,
        "description": description,
        "company": -1,
        "country": companyCountry,
        "embedding": generateEmbedding(f"{companyName} ({companyCountry}):\n\n {description}"),
        "type": "company"
    })

    id = collection.find_one({"name": companyName})["_id"]
    # print(id)
    return id

def addSupplier(companyID, supplierName, supplierCountry):
    description = generateSupplierDescription(supplierName)
    
    collection.insert_one({
        "name": supplierName,
        "description": description,
        "company": companyID,
        "country": supplierCountry,
        "embedding": generateEmbedding(f"{supplierName} ({supplierCountry}):\n\n {description}"),
        "type": "supplier"
    })

def findBestCompanies(prompt, numberOfCompanies=5):
    '''
    Vector search companies and product embeddings
    Returns: numberOfCompanies closest companies

    5
    '''
    result = semanticSearch(prompt, 100, numberOfCompanies, "-1", "company")
    return result

def findBestSuppliers(prompt, companyID, numberOfSuppliers=3):
    '''
    Vector search suppliers and product embeddings.
    Each supplier of the companies is compared to the product embedding.

    Returns: Rank of supplier companies?
    '''
    result = semanticSearch(prompt, 100, numberOfSuppliers, companyID, "supplier")
    return result

def addToCollection():
    with open('res.json', 'r') as f:
        data = json.load(f)
    for obj in data:
        # Companies
        id = addCompany(obj['name'].strip(), obj['country'].strip())

        # Suppliers
        for supplier in obj['suppliers']:
            addSupplier(id, supplier['name'].strip(), supplier['country'].strip())

# createSearchIndex()
print(list(findBestSuppliers("Coffee Beans", '6857c3cf8621971d5facdabc')))
# addToCollection()

# client.close()