import os
from .EmbeddingUtils import EmbeddingUtils
from opensearchpy import OpenSearch
<<<<<<< HEAD
from .SearchBuilder import SearchBuilder
from .SlotFilling import SlotFilling
from .IntentDetector import IntentDetector
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import json
=======
from modules.SearchBuilder import SearchBuilder
>>>>>>> new-branch


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
<<<<<<< HEAD
        # Initialize intent detector
        self.intent_detector = IntentDetector("./all_intents.json", "NOVA-vision-language/task-intent-detector")

        # Initialize slot filling
        self.slot_filling = SlotFilling()

        # Initialize state tracking
        self.current_recipe_id = None
        self.current_step = 0


    def detect_intent(self, text):
        return self.intent_detector.detect_intent(text)
    
    def get_recipe_by_id(self, recipe_id):
        # Function to fetch the recipe by ID from the database
        with open("../receitas.json", 'r') as f:
            data = json.load(f)
        return data.get(recipe_id, None)
    
    def get_step(self, recipe_id, step_number):
        recipe = self.get_recipe_by_id(recipe_id)
        if not recipe:
            return "Recipe not found."
        
        instructions = recipe.get("instructions", [])
        if 0 <= step_number < len(instructions):
            step = instructions[step_number]
            return f"Step {step['stepNumber']}: {step['stepText']}"
        else:
            return "Step not found."
        
    def get_next_step(self, recipe_id):
        return self.get_step(recipe_id, self.current_step)
        
    def get_previous_step(self, recipe_id):
        return self.get_step(recipe_id, self.current_step - 2)


##### daqui para cima ####
=======
>>>>>>> new-branch

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
        return searchBuilder.SearchByTitleEmbeddings(query)

    def SearchDescriptionEmbeddings(self, query):
        searchBuilder = SearchBuilder()
        return searchBuilder.SearchByDescriptionEmbeddings(query)
    
    def SearchByImageEmbeddings(self, query):
        searchBuilder = SearchBuilder()
        return searchBuilder.SearchByImageEmbeddings(query)

    def SearchByCaptionEmbeddings(self, query):
        searchBuilder = SearchBuilder()
<<<<<<< HEAD
        return searchBuilder.SearchByCaptionEmbeddings(query)
    
    def process_query(self, text):
        intent = self.detect_intent(text)
        print(f"Detected intent: {intent}")


        if intent == 'Search recipe':
            self.current_recipe_id = None
            self.current_step = 0
            return self.SearchTitleAndDescriptionTxt(text)
        
        elif intent == 'Next':
            if self.current_recipe_id is not None:
                self.current_step += 1
                return self.get_next_step(self.current_recipe_id)
            else:
                return "You haven't started any recipe. Please search for a recipe first."
            
        elif intent == 'Yes':
            return "Confirmed."
        
        elif intent == 'No':
            return "Action canceled."
        
        ## aqui current step should be 0 or am i wrong ##
        elif intent == 'Start task':
            self.current_step = 1
            if self.current_recipe_id is not None:
                return self.get_next_step(self.current_recipe_id)
            else:
                return "You haven't started any recipe. Please search for a recipe first."
            
        elif intent == 'Stop':
            self.current_recipe_id = None
            self.current_step = 0
            return "Stopping the task."
        
        elif intent == 'Greetings':
            return "Hello! How can I assist you today?"
        
        elif intent == 'Out of scope':
            return "I'm sorry, I cannot assist with that request."
        
        elif "previous" in text.lower():
            if self.current_recipe_id is not None:
                self.current_step -= 1
                return self.get_previous_step(self.current_recipe_id)
            else:
                return "You haven't started any recipe. Please search for a recipe first."
            
        elif "jump to step" in text.lower():
            step_number = int(text.split()[-1])
            if self.current_recipe_id is not None:
                self.current_step = step_number
                return self.get_step(self.current_recipe_id, step_number - 1)
            else:
                return "You haven't started any recipe. Please search for a recipe first."
            
        elif "go two steps forward" in text.lower():
            if self.current_recipe_id is not None:
                self.current_step += 2
                return self.get_next_step(self.current_recipe_id)
            else:
                return "You haven't started any recipe. Please search for a recipe first."
            
        elif "first step" in text.lower():
            self.current_step = 1
            if self.current_recipe_id is not None:
                return self.get_step(self.current_recipe_id, 0)
            else:
                return "You haven't started any recipe. Please search for a recipe first."
            
        elif "last step" in text.lower():
            if self.current_recipe_id is not None:
                recipe = self.get_recipe_by_id(self.current_recipe_id)
                if recipe:
                    last_step = len(recipe.get("instructions", []))
                    self.current_step = last_step
                    return self.get_step(self.current_recipe_id, last_step - 1)
                else:
                    return "Recipe not found."
            else:
                return "You haven't started any recipe. Please search for a recipe first."
            
        elif "step number" in text.lower():
            step_number = int(text.split()[-1])
            if self.current_recipe_id is not None:
                return self.get_step(self.current_recipe_id, step_number - 1)
            else:
                return "You haven't started any recipe. Please search for a recipe first."
            
        elif "name of the recipe" in text.lower():
            if self.current_recipe_id is not None:
                recipe = self.get_recipe_by_id(self.current_recipe_id)
                if recipe:
                    return f"The recipe is {recipe['displayName']}."
                else:
                    return "Recipe not found."
            else:
                return "You haven't started any recipe. Please search for a recipe first."
            
        elif "is it over" in text.lower():
            instructions = recipe.get("instructions", [])
            if self.current_step == len(instructions) -1:
                return "I believe we have reached the end of the task. Remember, you can always come back to revisit an old recipe or start a new project. Have a wonderful day and happy cooking!"
            else:
                return "No"
        elif "quit" in text.lower():
            return "Goodbye!"
        else:
            return "I'm not sure how to handle that request."
        
    def extract_slot_value(self, question, context):
        return self.slot_filling.extract_slot(question, context)
=======
        return searchBuilder.SearchByCaptionEmbeddings(query)
>>>>>>> new-branch
