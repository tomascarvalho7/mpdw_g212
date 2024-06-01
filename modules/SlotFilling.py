from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline

class SlotFilling:
    def __init__(self, model_name="deepset/roberta-base-squad2"):
        self.nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)
        self.model = AutoModelForQuestionAnswering.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    def extract_slot(self, question, context):
        QA_input = {
            'question': question,
            'context': context
        }
        result = self.nlp(QA_input)
        return result['answer']
