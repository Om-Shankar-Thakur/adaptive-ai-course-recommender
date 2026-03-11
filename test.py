<<<<<<< HEAD
# # from sentence_transformers import SentenceTransformer
# # SentenceTransformer("Sentence-transformers/all-MiniLM-L6-v2")

# from groq import Groq
# import os
# from dotenv import load_dotenv
# load_dotenv()
# client = Groq(api_key=os.getenv("GROQ_API_KEY"))
# response = client.chat.completions.create(
#    model="meta-llama/llama-4-scout-17b-16e-instruct",
#    messages=[{"role":"user","content":"Hello"}]
# )
# print(response.choices[0].message.content)


from qdrant_client.http.models import PayloadSchemaType
from app.db.qdrant_client import client
client.create_payload_index(
   collection_name="courses",
   field_name="domain",
   field_schema=PayloadSchemaType.KEYWORD
)
client.create_payload_index(
   collection_name="courses",
   field_name="difficulty_tag",
   field_schema=PayloadSchemaType.KEYWORD
)
=======
from sentence_transformers import SentenceTransformer
SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
>>>>>>> 7277fa7be57a9c65d2e08b5d5a3aa617940e4636
