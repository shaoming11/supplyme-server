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
        'country': 1,
        'embedding': 0
        }
    }
    ]
    # run pipeline
    result = client["companyData"]["companyCollection"].aggregate(pipeline)
    # # print results
    # for i in result:
    #     print(i)
    return result
# def semanticSearch(query, neighbours, limit, companyID="-1"):
#     collection = client["companyData"]["companyCollection"]
    
#     # DEBUG 1: Check collection has data
#     total_docs = collection.count_documents({})
#     print(f"Total docs in collection: {total_docs}")
    
#     # DEBUG 2: Check company filter
#     company_docs = collection.count_documents({"company": companyID})
#     print(f"Docs with company '{companyID}': {company_docs}")
    
#     # DEBUG 3: Check embeddings exist
#     embedding_docs = collection.count_documents({"embedding": {"$exists": True}})
#     print(f"Docs with embeddings: {embedding_docs}")
    
#     # DEBUG 4: Try without filter first
#     pipeline_no_filter = [
#         {
#             '$vectorSearch': {
#                 'index': 'vector_index', 
#                 'path': 'embedding',
#                 'queryVector': generateEmbedding(query),
#                 'numCandidates': neighbours,
#                 'limit': limit
#                 # No filter
#             }
#         }
#     ]
    
#     result_no_filter = list(collection.aggregate(pipeline_no_filter))
#     print(f"Results WITHOUT filter: {len(result_no_filter)}")
    
#     # DEBUG 5: Check your embedding
#     query_embedding = generateEmbedding(query)
#     print(f"Query embedding length: {len(query_embedding)}")
#     print(f"First few values: {query_embedding[:5]}")
    
#     # Now try with filter
#     pipeline = [
#         {
#             '$vectorSearch': {
#                 'index': 'vector_index', 
#                 'path': 'embedding',
#                 'queryVector': query_embedding,
#                 'numCandidates': neighbours,
#                 'limit': limit,
#                 'filter': {
#                     'company': companyID
#                 }
#             }
#         }, {
#             '$project': {
#                 '_id': 0, 
#                 'name': 1,
#                 'description': 1, 
#                 'company': 1,
#                 'country': 1,
#                 'embedding': 1
#             }
#         }
#     ]
    
#     result = list(collection.aggregate(pipeline))
#     print(f"Results WITH filter: {len(result)}")
    
#     return result

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
# print(list(findBestCompanies("Handheld device to call and send messages with people")))
# addToCollection()

# client.close()