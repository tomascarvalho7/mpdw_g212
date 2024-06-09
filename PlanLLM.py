import json
import os
import pprint as pp

import requests
from modules.Search import Search

search = Search()
max_timeout = 10
url = "https://twiz.novasearch.org/"

def get_initial_user_input():
    # Ask the user for a recipe
    user_input = input("Hello! What recipe would you like to cook today? type 'exit' to quit.\n")
    return user_input

def search_Opensearch(recipeToSearch):
    # add some form of algorithm to use the best search method
    return search.SearchSingleTitleAndDescriptionTxtInstructions(recipeToSearch)

def generate_base_json(recipe_json):
    result = recipe_json["hits"]["hits"][0]["_source"]
    json_data = {
        "dialog_id": "1",
        "system_tone": "neutral",
        "task": {
            "recipe": {
                "displayName": result["title"],
                "instructions": [{"stepText": step["stepText"]} for step in  result["instructions"]],
            }
        },
        "dialog": []
    }

    return json_data

def get_user_input(text):
    user_input = input(text)
    return user_input

def add_to_json(convo_json, ai_or_user, text, step):
    # Add user input or AI response to JSON
    if ai_or_user == "user": 
        convo_json["dialog"].append({"current_step": step, "user": text})
    elif ai_or_user == "ai":
        convo_json["dialog"][step]["system"] = text
    return convo_json

def send_to_planllm(conversation, url):
    url = os.path.join(url, "structured")

    data = {
        "dialog": conversation,
        "max_tokens": 100,
        "temperature": 0.0,
        "top_p": 1,
        "top_k": -1,
    }

    response = requests.post(url, json=data, timeout=max_timeout)
    return response.text

def process_user_input(user_input, step, conversation_json):
    intent = search.detect_intent(user_input)
    response = ""
    if intent == 'Search recipe':
        recipe_json = search_Opensearch(user_input)
        conversation_json = generate_base_json(recipe_json)
        response = "Recipe found. Ready to start cooking?"
    elif intent == 'Next':
        step += 1
        response = search.get_next_step(conversation_json["task"]["recipe"]["id"])
    elif intent == 'Yes':
        response = "Confirmed."
    elif intent == 'No':
        response = "Action canceled."
    elif intent == 'Start task':
        step = 1
        response = search.get_step(conversation_json["task"]["recipe"]["id"], step - 1)
    elif intent == 'Stop':
        response = "Stopping the task."
    elif intent == 'Greetings':
        response = "Hello! How can I assist you today?"
    elif intent == 'Out of scope':
        response = "I'm sorry, I cannot assist with that request."
    else:
        # Slot Filling example
        if "recipe" in user_input and "time" in user_input:
            context = "I want a recipe that takes 30 minutes to prepare."
            question = "How long does the recipe take to prepare?"
            slot_value = search.extract_slot_value(question, context)
            response = f"The recipe takes {slot_value} to prepare."
        else:
            response = "I'm not sure how to handle that request."
    return response, step, conversation_json


def main():
    step = 0
    recipeToSearch = get_initial_user_input()

    recipe_json = search_Opensearch(recipeToSearch)
    conversation_json = generate_base_json(recipe_json)

    while True:
        user_input = get_user_input("What to do now?\n")
        if user_input == "exit" or user_input == "quit" or user_input == "stop" or user_input == "end":
            print("Goodbye!")
            break

        conversation_json = add_to_json(conversation_json, "user", user_input, step)

        response, step, conversation_json = process_user_input(user_input, step, conversation_json)

        conversation_json = add_to_json(conversation_json, "ai", response, step)

        print(response.replace('"', ''))

        ##
        ##ai_response = send_to_planllm(conversation_json, url)

        ##conversation_json = add_to_json(conversation_json, "ai", ai_response, step)

        ##print(ai_response.replace('"', ''))

        step += 1

if __name__ == "__main__":
    main()
