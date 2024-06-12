import os
from .EmbeddingUtils import EmbeddingUtils
from opensearchpy import OpenSearch
from modules.SearchBuilder import SearchBuilder


class Search:
    def __init__(self):
        self.host = 'api.novasearch.org'
        self.port = 443
        self.user = 'user212'
        self.password = 'soO-2518'
        self.index_name = self.user
        self.utils = EmbeddingUtils()
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

    def SearchTitleAndDescriptionTxt(self, query):
        searchBuilder = SearchBuilder()
        searchBuilder.setSourceAsIdAndContent()
        searchBuilder.setResultLength(5)
        return searchBuilder.Search(query)
    
    def SearchSingleTitleAndDescriptionTxtInstructions(self, query):
        searchBuilder = SearchBuilder()
        searchBuilder.setSourceAsIdAndInstructions()
        searchBuilder.setResultLength(1)
        return searchBuilder.Search(query)
    
    def SearchRecipeTime(self, time, range):
        searchBuilder = SearchBuilder()
        searchBuilder.setSourceAsIdAndContent()
        searchBuilder.setResultLength(5)
        searchBuilder.setTimeFrame(time, range)
        return searchBuilder.Search('')
    
    def SearchRecipeNameTime(self, time, range, ingredient):
        searchBuilder = SearchBuilder()
        searchBuilder.setSourceAsIdAndContent()
        searchBuilder.setResultLength(5)
        searchBuilder.setTimeFrame(time, range)
        return searchBuilder.Search(ingredient)

    def SearchRecipeIngredients(self, ingredients):
        searchBuilder = SearchBuilder()
        searchBuilder.setSourceAsIdAndContent()
        searchBuilder.setResultLength(5)
        searchBuilder.setIngredients(ingredients)
        return searchBuilder.Search('')
    
    def SearchRecipeExcludeIngredients(self, ingredients, name):
        searchBuilder = SearchBuilder()
        searchBuilder.setSourceAsIdAndContent()
        searchBuilder.setResultLength(5)
        searchBuilder.excludeIngredients(ingredients)
        return searchBuilder.Search(name)

    def SearchRecipeDifficulty(self, difficulty):
        searchBuilder = SearchBuilder()
        searchBuilder.setSourceAsIdAndContent()
        searchBuilder.setResultLength(5)
        searchBuilder.setDifficulty(difficulty)
        return searchBuilder.Search('')
    
    def SearchRecipeNameDifficulty(self, difficulty, name):
        searchBuilder = SearchBuilder()
        searchBuilder.setSourceAsIdAndContent()
        searchBuilder.setResultLength(5)
        searchBuilder.setDifficulty(difficulty)
        return searchBuilder.Search(name)

    def SearchTitleEmbeddings(self, query):
        searchBuilder = SearchBuilder()
        searchBuilder.setSourceAsHeader()
        searchBuilder.setResultLength(5)
        return searchBuilder.SearchByTitleEmbeddings(query)

    def SearchDescriptionEmbeddings(self, query):
        searchBuilder = SearchBuilder()
        return searchBuilder.SearchByDescriptionEmbeddings(query)
    
    def SearchByImageEmbeddings(self, query):
        searchBuilder = SearchBuilder()
        return searchBuilder.SearchByImageEmbeddings(query)

    def SearchByCaptionEmbeddings(self, query):
        searchBuilder = SearchBuilder()
        return searchBuilder.SearchByCaptionEmbeddings(query)
