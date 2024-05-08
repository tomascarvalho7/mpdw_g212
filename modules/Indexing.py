import json
import os
from opensearchpy import OpenSearch
from modules.EmbeddingUtils import EmbeddingUtils
from IPython.display import Image
import pprint as pp

class Indexing:
    def __init__(self):
        self.host = 'api.novasearch.org'
        self.port = 443
        self.user = os.getenv('USER')
        self.password = os.getenv('PASS')
        self.index_name = self.user
        self.titles = []
        self.descriptions = []
        self.titles_embeddings = []
        self.descriptions_embeddings = []
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
        self.utils = EmbeddingUtils()
        

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
                "clip_embeddings": {
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
            self.client.indices.create(index=self.index_name, body=index_body)
            print('\nCreating index')
        
        index_settings = {
            "settings":{
            "index":{
                "refresh_interval" : "1s"
                }
            }
        }
        self.client.indices.put_settings(index = self.index_name, body = index_settings)

    def readAndStoreRecipesFromFile(self, fileName):
        with open(fileName, encoding='utf-8') as f:
            data = json.loads(f.read())
        counter = 0

        for doc in data:
            doc_idx = int(doc)
            doc_info = data[doc]

            ingredients = ""
            for ingredient in doc_info['ingredients']:
                if (ingredient["ingredient"]):
                    ingredients += ingredient["ingredient"] + ' '  

            # create recipe tags
            tags = []

            if doc_info['diets'] is not None:
                tags.extend(doc_info['diets'])

            if doc_info['courses'] is not None:
                tags.extend(doc_info['courses'])

            if doc_info['cuisines'] is not None:
                tags.extend(doc_info['cuisines'])

            images = doc_info['images']
            #if (len(images) > 0): clip_embeddings = map(lambda img: self.utils.encodeImage(Image(img.url)), images)
            #else: clip_embeddings = []
            clip_embeddings = self.utils.encodeCaption(doc_info['displayName'])[0].tolist();

            obj = {
                'doc_id': doc_idx,
                'tags': tags,
                'title': doc_info['displayName'],
                'title_embedding': self.titles_embeddings[doc_idx],
                'clip_embeddings': clip_embeddings,
                'description': doc_info['description'],
                'time': doc_info['totalTimeMinutes'],
                'ingredients': ingredients,
                'contents': str(doc_info)
            }
            pp.pprint(obj);
            # if time is filled add to obj
            if (doc_info['totalTimeMinutes']): obj['time'] = doc_info['totalTimeMinutes']
            # if difficultyLevel is filled add to obj
            if (doc_info['difficultyLevel']): obj['difficultyLevel'] = doc_info['difficultyLevel']
            # if description is filled add to obj
            if (doc_info['description']): obj['description_embedding'] = self.descriptions_embeddings[counter]; counter += 1

            resp = self.client.index(index=self.index_name, id=doc_idx, body=obj)

    def __getTitlesAndDescriptions(self):
        with open('receitas.json', encoding='utf-8') as f:
            data = json.loads(f.read())

        for doc in data:
            doc_info = data[doc]
            self.titles.append(doc_info['displayName'])
            if (doc_info['description'] != None):
                self.descriptions.append(doc_info['description'])

    def __encodeEmbeddings(self):
        return self.utils.encode(self.titles), self.utils.encode(self.descriptions)
    
    def calculateAndStoreEmbeddings(self):
        if os.path.exists('./embeddings/titles_embeddings.pkl') and os.path.exists('./embeddings/description_embeddings.pkl'):
            (titles_emb, description_emb) = self.utils.readEmbeddings()
            self.titles_embeddings = titles_emb.tolist()
            self.descriptions_embeddings = description_emb.tolist()
        else:
            self.__getTitlesAndDescriptions()
            (titles_emb, description_emb) = self.__encodeEmbeddings()
            self.utils.storeEmbeddings(titles_emb, description_emb)
            self.titles_embeddings = titles_emb.tolist()
            self.descriptions_embeddings = description_emb.tolist()