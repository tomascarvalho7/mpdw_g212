import os
from modules.EmbeddingUtils import EmbeddingUtils
from opensearchpy import OpenSearch

# Search Builder API is meant to be used as a tool to easily & in a
# iterative manner build simple or complex search queries
#
# Motivation: This avoids a repetitive and not user friendly API between the user and the open search DB
#
# How to:
# - Change '_source':
#       - setSourceAsId() -> '_source': ['doc_id']
#       - setSourceAsIdAndContent() -> '_source': ['doc_id', 'content']
# - Change number of query results with: 
#       - setResultLength(int number)
# - Change query parameters: (can be called any number of times)
#       - setMandatoryTags(string[] tags)
#       - setOptionalTags(string[] tags)
#       - setTimeFrame(int time, int margin)
#       - setIngredients(string ingredients)
#       - excludeIngredients(string ingredients)
#       - setDifficulty(int difficulty)
# - Execute search:
#       - SearchByTitleEmbeddings(string qtext) -> uses the knn vectors of the titles to query recipes
#       - SearchByDescriptionEmbeddings(string qtext) -> uses the knn vectors of the descriptions to query recipes
#       - Search(string qtext) -> uses multimatch to query recipes
class SearchBuilder:
    def __init__(self):
        self.host = 'api.novasearch.org'
        self.port = 443
        self.user = 'user212'
        self.password = 'soO-2518'
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
        self.queryBuilder = {
            'size': 5,
            '_source': ['doc_id'],
            'query': {
            }
        }
        return

    def setSourceAsId(self):
        self.queryBuilder['_source'] = ['doc_id']

    def setSourceAsIdAndContent(self):
        self.queryBuilder['_source'] = ['doc_id', 'contents']
    
    def setSourceAsIdAndInstructions(self):
        self.queryBuilder['_source'] = ['doc_id', 'title' ,'instructions']

    def setResultLength(self, length):
        self.queryBuilder['size'] = length

    def setMandatoryTags(self, tags):
        tagObj = {
            'terms': {
                'tags' : tags
            }
        }

        if 'bool' not in self.queryBuilder['query']:
            self.queryBuilder['query']['bool'] = {}
        if 'must' not in self.queryBuilder['query']['bool']:
            self.queryBuilder['query']['bool']['must'] = []


        self.queryBuilder['query']['bool']['must'].append(tagObj)

    def setTimeFrame(self, time, margin):
        timeObj = {
            'range': {
                'time': {
                    'gte': time - margin,
                    'lte': time + margin
                }
            }
        }
        
        if 'bool' not in self.queryBuilder['query']:
            self.queryBuilder['query']['bool'] = {}
        if 'must' not in self.queryBuilder['query']['bool']:
            self.queryBuilder['query']['bool']['must'] = []

        self.queryBuilder['query']['bool']['must'].append(timeObj)

    def setIngredients(self, ingredients):
        tagObj = {
            "match": {
                "ingredients" : {
                    "query": ingredients,
                    "operator": "or"
                }
            }
        }

        if 'bool' not in self.queryBuilder['query']:
            self.queryBuilder['query']['bool'] = {}
        if 'must' not in self.queryBuilder['query']['bool']:
            self.queryBuilder['query']['bool']['must'] = []

        self.queryBuilder['query']['bool']['must'].append(tagObj)

    def excludeIngredients(self, ingredients):
        tagObj = {
            "match": {
                "ingredients" : {
                    "query": ingredients,
                    "operator": "or"
                }
            }
        }

        if 'bool' not in self.queryBuilder['query']:
            self.queryBuilder['query']['bool'] = {}
        if 'must_not' not in self.queryBuilder['query']['bool']:
            self.queryBuilder['query']['bool']['must_not'] = []

        self.queryBuilder['query']['bool']['must_not'].append(tagObj)

    def setOptionalTags(self, tags):
        tagObj = {
            'terms': {
                'tags' : tags
            }
        }

        if 'bool' not in self.queryBuilder['query']:
            self.queryBuilder['query']['bool'] = {}
        if 'should' not in self.queryBuilder['query']['bool']:
            self.queryBuilder['query']['bool']['should'] = []

        self.queryBuilder['query']['bool']['should'].append(tagObj)

    def setDifficulty(self, difficulty):
        tagObj = {
            'match': {
                'difficultyLevel': difficulty
            }
        }

        if 'bool' not in self.queryBuilder['query']:
            self.queryBuilder['query']['bool'] = {}
        if 'must' not in self.queryBuilder['query']['bool']:
            self.queryBuilder['query']['bool']['must'] = []

        self.queryBuilder['query']['bool']['must'].append(tagObj)

    def SearchByTitleEmbeddings(self, query):
        query_emb = EmbeddingUtils().encode(query)

        if 'bool' not in self.queryBuilder['query']:
            self.queryBuilder['query']['bool'] = {}
        if 'should' not in self.queryBuilder['query']['bool']:
            self.queryBuilder['query']['bool']['should'] = []

        knnObj = {
                "knn": {
                    "title_embedding": {
                        "vector": query_emb[0].numpy(),
                        "k": 2
                    }
                }
        }

        self.queryBuilder['query']['bool']['should'].append(knnObj)

        return self.client.search(index=self.index_name, body=self.queryBuilder)
    
    def SearchByDescriptionEmbeddings(self, query):
        query_emb = EmbeddingUtils().encode(query)

        if 'bool' not in self.queryBuilder['query']:
            self.queryBuilder['query']['bool'] = {}
        if 'should' not in self.queryBuilder['query']['bool']:
            self.queryBuilder['query']['bool']['should'] = []

        knnObj = {
                "knn": {
                    "description_embedding": {
                        "vector": query_emb[0].numpy(),
                        "k": 2
                    }
                }
        }

        self.queryBuilder['query']['bool']['should'].append(knnObj)

        return self.client.search(index=self.index_name, body=self.queryBuilder)
    

    def SearchByImageEmbeddings(self, query):
        query_emb = EmbeddingUtils().encodeImage(query)

        if 'bool' not in self.queryBuilder['query']:
            self.queryBuilder['query']['bool'] = {}
        if 'should' not in self.queryBuilder['query']['bool']:
            self.queryBuilder['query']['bool']['should'] = []

        knnObj = {
                "knn": {
                    "clip_embeddings": {
                        "vector": query_emb[0].numpy(),
                        "k": 2
                    }
                }
        }

        self.queryBuilder['query']['bool']['should'].append(knnObj)

        return self.client.search(index=self.index_name, body=self.queryBuilder)
    

    def SearchByCaptionEmbeddings(self, query):
        query_emb = EmbeddingUtils().encodeCaption(query)

        if 'bool' not in self.queryBuilder['query']:
            self.queryBuilder['query']['bool'] = {}
        if 'should' not in self.queryBuilder['query']['bool']:
            self.queryBuilder['query']['bool']['should'] = []

        knnObj = {
                "knn": {
                    "caption_embedding": {
                        "vector": query_emb[0].numpy(),
                        "k": 2
                    }
                }
        }

        self.queryBuilder['query']['bool']['should'].append(knnObj)

        return self.client.search(index=self.index_name, body=self.queryBuilder)

    def Search(self, qtext):
        
        if 'bool' not in self.queryBuilder['query']:
            self.queryBuilder['query']['bool'] = {}
        if 'should' not in self.queryBuilder['query']['bool']:
            self.queryBuilder['query']['bool']['should'] = []

        matchObj = {
                'multi_match': {
                'query': qtext,
                'fields': ['title', 'description']
            }
        }

        self.queryBuilder['query']['bool']['should'].append(matchObj)

        return self.client.search(index=self.index_name, body=self.queryBuilder)