import os
from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn.functional as F
import pickle
from PIL import Image
import requests
import torch
from transformers import CLIPProcessor, CLIPModel
import pprint as pp


class EmbeddingUtils:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/msmarco-distilbert-base-v2")
        self.model = AutoModel.from_pretrained("sentence-transformers/msmarco-distilbert-base-v2")
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.clipProcessor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        self.clipModel = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(self.device)

    def mean_pooling(self, model_output, attention_mask):
        token_embeddings = model_output.last_hidden_state #First element of model_output contains all token embeddings
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

    def encode(self, texts):
        # Tokenize sentences
        encoded_input = self.tokenizer(texts, padding=True, truncation=True, return_tensors='pt')

        # Compute token embeddings
        with torch.no_grad():
            model_output = self.model(**encoded_input, return_dict=True)

        # Perform pooling
        embeddings = self.mean_pooling(model_output, encoded_input['attention_mask'])

        # Normalize embeddings
        embeddings = F.normalize(embeddings, p=2, dim=1)
        
        return embeddings

    def encodeCaption(self, caption):
        input_encoding = self.clipProcessor(text=[caption], 
                        return_tensors="pt", 
                        padding=True).to(self.device)
        text_embeddings = self.clipModel.get_text_features(**input_encoding)
        text_embeddings = text_embeddings / text_embeddings.norm(dim=-1, keepdim=True)
        return text_embeddings
    
    def encodeImage(self, images):
        input_img = self.clipProcessor(images=images, return_tensors="pt").to(self.device)
        image_embeddings = self.clipModel.get_image_features(**input_img)
        image_embeddings = image_embeddings / image_embeddings.norm(dim=-1, keepdim=True)
        return image_embeddings.detach().numpy()
    
    # store embedding vectors
    def storeEmbeddings(self, titles, description):
        with open('./embeddings/titles_embeddings.pkl', 'wb') as f:
            pickle.dump(titles, f)
        with open('./embeddings/description_embeddings.pkl', 'wb') as f:
            pickle.dump(description, f)

    # read embedding vectors
    def readEmbeddings(self):
        with open('./embeddings/titles_embeddings.pkl', 'rb') as f:
            title_embeddings = pickle.load(f)
        with open('./embeddings/description_embeddings.pkl', 'rb') as f:
            descriptions_embeddings = pickle.load(f)
        return (title_embeddings, descriptions_embeddings)

