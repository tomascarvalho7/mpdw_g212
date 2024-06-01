import json
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

class IntentDetector:
    def __init__(self, intents_file_path, model_name):
        with open(intents_file_path, 'r') as json_in:
            data = json.load(json_in)

        id_to_intent, intent_to_id = dict(), dict()
        for i, intent in enumerate(data.values()):
            id_to_intent[i] = intent
            intent_to_id[intent] = i

        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_name, 
            num_labels=len(data), 
            id2label=id_to_intent, 
            label2id=intent_to_id
        )
        self.tokenizer = AutoTokenizer.from_pretrained("roberta-base")

    def detect_intent(self, text):
        model_in = self.tokenizer(text, return_tensors='pt')
        with torch.no_grad():
            logits = self.model(**model_in).logits
            predicted_class_id = logits.argmax().item()
            return self.model.config.id2label[predicted_class_id]
