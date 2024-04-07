import os
from opensearchpy import OpenSearch

class Search:
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
        return

    def SearchTitleTxt(self, query):
        query = self._BuildDefaultTextQuery(query, ['displayName'])

        return self.client.search(
            body = query,
            index = self.index_name
        )

    def SearchTitleEmbeddings(self):
        return

    def SearchDescriptionTxt(self):
        query = self._BuildDefaultTextQuery(query, ['description'])

        return self.client.search(
            body = query,
            index = self.index_name
        )

    def SearchDescriptionEmbeddings(self):
        return
    
    def SearchRecipeTime(self, time, range):
        query = {
            "query": {
                "range": {
                    "age": {
                        "gte": time - range,
                        "lte": time + range
                    }
                }
            }
        }

        return self.client.search(index=self.index_name, body=query)

    def SearchRecipeIngredients(self, ingredients):
        query = self._BuildDefaultTextQuery(ingredients, ['ingredients'])

        return self.client.search(index=self.index_name, body=query)
    
    def SearchRecipeDifficulty(self, difficulty):
        query = {
            "query": {
                "term": {
                    "difficultyLevel": difficulty
                }
            }
        }

        return self.client.search(index=self.index_name, body=query)
    
    def SearchRecipeNutrition(self, nutrition):
        query = self._BuildDefaultTextQuery(nutrition, ['nutrients'])

        return self.client.search(index=self.index_name, body=query)

    
    def _BuildDefaultTextQuery(self, query, fields):
        return {
            'size': 5,
            '_source': ['doc_id'],
            'query': {
                    'multi_match': {
                    'query': query,
                    'fields': fields
                    }
                }
            }
    
    def _BuildDefaultEmbeddingsQuery(self, query, fields):
        query_emb = encode(query)

        query_denc = {
        'size': 5,
        '_source': ['doc_id'],
        "query": {
                "knn": {
                "title_embedding": {
                    "vector": query_emb[0].numpy(),
                    "k": 2
                }
                }
            }
        }

        return self.client.search(
            index = self.index_name, 
            body = query_denc
        )