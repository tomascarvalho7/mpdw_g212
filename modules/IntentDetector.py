import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import json

class IntentDetector:
    def __init__(self):
        with open('./all_intents.json', 'r') as all_intents_json:
            all_intents = json.load(all_intents_json)
            
            id_to_intent, intent_to_id = dict(), dict()
            for i, intent in enumerate(all_intents):
                id_to_intent[i] = intent
                intent_to_id[intent] = i

<<<<<<< HEAD
        # Custom intent mapping
        self.intent_mapping = {
            "Greetings": "GreetingIntent",
            "Search recipe": "QuestionIntent",
            "Out of scope": "OutOfScopeIntent",
            "Yes": "YesIntent",
            "No": "NoIntent",
            "Start task": "StartStepsIntent",
            "Next": "NextStepIntent",
            "Stop": "StopIntent"
        }

        # Reverse mapping
        self.reverse_mapping = {v: k for k, v in self.intent_mapping.items()}
        print(f"Reverse Mapping: {self.reverse_mapping}")

        # Create id to intent and intent to id mappings based on the pre-trained model's space
        id_to_intent, intent_to_id = dict(), dict()
        for i, intent in enumerate(self.reverse_mapping.keys()):
            id_to_intent[i] = intent
            intent_to_id[intent] = i
=======
>>>>>>> new-branch

        self.tokenizer = AutoTokenizer.from_pretrained("roberta-base")
        
        self.model = AutoModelForSequenceClassification.from_pretrained(
<<<<<<< HEAD
            model_name,
            num_labels=len(self.reverse_mapping),
            id2label=id_to_intent,
            label2id=intent_to_id,
            ignore_mismatched_sizes=True
        )
        self.tokenizer = AutoTokenizer.from_pretrained("roberta-base")
=======
            "NOVA-vision-language/task-intent-detector",
            num_labels=len(all_intents), 
            id2label=id_to_intent, 
            label2id=intent_to_id
            )
>>>>>>> new-branch

    def detect_intent(self, text):
        model_in = self.tokenizer(text, return_tensors='pt')
        with torch.no_grad():
            logits = self.model(**model_in).logits
            predicted_class_id = logits.argmax().item()
<<<<<<< HEAD
            detected_intent = self.model.config.id2label[predicted_class_id]

        print(f"Detected intent in model's label space: {detected_intent}")
        mapped_intent = self.reverse_mapping.get(detected_intent, "Out of scope")
        print(f"Mapped intent: {mapped_intent}")
        return mapped_intent
=======
            intent = self.model.config.id2label[predicted_class_id]
        return intent
>>>>>>> new-branch
