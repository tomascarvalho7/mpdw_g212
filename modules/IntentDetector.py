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


        self.tokenizer = AutoTokenizer.from_pretrained("roberta-base")
        
        self.model = AutoModelForSequenceClassification.from_pretrained(
            "NOVA-vision-language/task-intent-detector",
            num_labels=len(all_intents), 
            id2label=id_to_intent, 
            label2id=intent_to_id
            )

    def detect_intent(self, text):
        model_in = self.tokenizer(text, return_tensors='pt')
        with torch.no_grad():
            logits = self.model(**model_in).logits
            predicted_class_id = logits.argmax().item()
            intent = self.model.config.id2label[predicted_class_id]
        return intent