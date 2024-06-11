import os

import requests
import pprint as pp

class PlanLLMUtils:
    def __init__(self):
        self.max_timeout = 10
        self.url = "https://twiz.novasearch.org/structured"

    def generate_base_json(self, recipe_json, dialog):
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
            "dialog": dialog
        }

        return json_data

    def add_to_json(self, convo_json, ai_or_user, text, step):
        # Add user input or AI response to JSON
        if ai_or_user == "user": 
            convo_json["dialog"].append({"current_step": step, "user": text})
        elif ai_or_user == "ai":
            convo_json["dialog"][step]["system"] = text
        return convo_json

    def send_to_planllm(self, conversation):

        data = {
            "dialog": conversation,
            "max_tokens": 100,
            "temperature": 0.0,
            "top_p": 1,
            "top_k": -1,
        }

        response = requests.post(self.url, json=data, timeout=self.max_timeout)
        return response.text