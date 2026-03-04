from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = os.getenv("EMBEDDING_MODEL")

model = SentenceTransformer(MODEL_NAME)


def get_embedding(text: str):
    return model.encode(text).tolist()