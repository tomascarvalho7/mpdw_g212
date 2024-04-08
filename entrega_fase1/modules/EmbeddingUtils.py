import os
from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn.functional as F
import pickle

class EmbeddingUtils:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/msmarco-distilbert-base-v2")
        self.model = AutoModel.from_pretrained("sentence-transformers/msmarco-distilbert-base-v2")

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

