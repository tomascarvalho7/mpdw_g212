from transformers import ViltProcessor, ViltForQuestionAnswering, AutoTokenizer, AutoConfig
import requests

model_path = "dandelin/vilt-b32-finetuned-vqa"

class QuestionImage:
    def __init__(self):
        self.config = AutoConfig.from_pretrained(model_path,  output_hidden_states=True, output_attentions=True)  
        self.processor = ViltProcessor.from_pretrained(model_path)
        self.model = ViltForQuestionAnswering.from_pretrained(model_path, config=self.config)

    def ask(self, question, img):
        VQ_encoding = self.processor(img, question, return_tensors="pt")
        VQ_encoding.keys()
        self.processor.tokenizer.convert_ids_to_tokens(VQ_encoding["input_ids"][0])
        self.processor.tokenizer.decode(VQ_encoding["input_ids"][0].tolist())
        outputs = self.model(**VQ_encoding, return_dict = True)
        logits = outputs.logits
        idx = logits.argmax(-1).item()
        answer = self.model.config.id2label[idx]
        return answer