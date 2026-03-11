from sentence_transformers import SentenceTransformer

MODEL_PATH = "models/all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_PATH)

def get_embedding(text: str):
   return model.encode(text).tolist()