import json
import os
from opensearchpy import OpenSearch

class Indexing:

    def __init__(self):
        self.host = 'api.novasearch.org'
        self.port = 443
        self.user = os.getenv('USER')
        self.password = os.getenv('PASS')
        self.index_name = self.user
        self.client = OpenSearch(
            hosts=[{'host': self.host, 'port': self.port}],
            http_compress=True,  # enables gzip compression for request bodies
            http_auth=(self.user, self.password),
            url_prefix='opensearch',
            use_ssl=True,
            verify_certs=False,
            ssl_assert_hostname=False,
            ssl_show_warn=False
        )

    def createOpenSearchMappings(self):
        index_body = {
        "settings":{
            "index":{
                "number_of_replicas":0,
                "number_of_shards":4,
                "refresh_interval":"-1",
                "knn":"true"
            }
        },
        "mappings":{
            "dynamic":      "strict",
            "properties":{
                "doc_id":{
                    "type":"keyword"
                },
                "tags":{
                    "type":"keyword"
                },
                "title":{
                    "type":"text",
                    "analyzer":"standard",
                    "similarity":"BM25"
                },
                "title_embedding":{
                    "type":"knn_vector",
                    "dimension": 768,
                    "method": {
                        "name": "hnsw",
                        "space_type": "innerproduct",
                        "engine": "faiss",
                        "parameters": {
                            "ef_construction": 256,
                            "m": 48
                        }
                    }
                },
                "description":{
                    "type":"text",
                    "analyzer":"standard",
                    "similarity":"BM25"
                },
                "description_embedding":{
                    "type":"knn_vector",
                    "dimension": 768,
                    "method": {
                        "name": "hnsw",
                        "space_type": "innerproduct",
                        "engine": "faiss",
                        "parameters": {
                            "ef_construction": 256,
                            "m": 48
                        }
                    }
                },
                "ingredients":{
                    "type":"text",
                    "analyzer":"standard",
                    "similarity":"BM25"
                },
                "time":{
                "type":"integer"  
                },
                "difficultyLevel":{
                    "type": "keyword"
                },
                "nutrients": {
                    "type":"text",
                    "analyzer":"standard",
                    "similarity":"BM25"
                },
                "contents":{
                    "type":"text",
                    "analyzer":"standard",
                    "similarity":"BM25",
                    "index": False
                }
            }
        }
        }

        if self.client.indices.exists(index=self.index_name):
            print("Index already existed. Nothing to be done.")
        else:
            response = self.client.indices.create(index=self.index_name, body=index_body)
            print('\nCreating index')

    def storeRecipeInOpenSearch(self, doc_idx, obj):
        resp = self.client.index(index=self.index_name, id=doc_idx, body=obj)
        print(resp['result'])

    def readAndStoreRecipesFromFile(self, fileName):
        with open(fileName, encoding='utf-8') as f:
            data = json.loads(f.read())

        for doc in data:
            doc_idx = int(doc)
            doc_info = data[doc]

            ingredients = ""
            for ingredient in doc_info['ingredients']:
                if ingredient.get("ingredient"):
                    ingredients += ingredient["ingredient"] + ' '

            nutrients = ""
            if doc_info.get('nutrition') and doc_info['nutrition'].get('nutrients'):
                nutrients = str(doc_info['nutrition']['nutrients'])

            obj = {
                'doc_id': doc_idx,
                'tags': ['recipe'],
                'title': doc_info['displayName'],
                'ingredients': ingredients,
                'nutrients': nutrients,
                'description': doc_info['description'],
                'contents': str(doc_info)
            }
            # if time is filled add to obj
            if doc_info.get('totalTimeMinutes'):
                obj['time'] = doc_info['totalTimeMinutes']
            # if difficultyLevel is filled add to obj
            if doc_info.get('difficultyLevel'):
                obj['difficultyLevel'] = doc_info['difficultyLevel']
            self.storeRecipeInOpenSearch(doc_idx, obj)

indexer = Indexing()
indexer.createOpenSearchMappings()
indexer.readAndStoreRecipesFromFile('receitas.json')