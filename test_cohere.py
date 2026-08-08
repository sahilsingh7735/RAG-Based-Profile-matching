import os
import cohere
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("COHERE_API_KEY")

if not api_key:
    raise ValueError("COHERE_API_KEY not found in .env file")

co = cohere.ClientV2(api_key=api_key)

text = "Full Stack Developer with React, Node.js and MongoDB experience."

response = co.embed(
    model="embed-v4.0",
    texts=[text],
    input_type="search_document",
    output_dimension=1024,
    embedding_types=["float"],
)

embedding = response.embeddings.float[0]

print("Cohere connection successful!")
print("Embedding dimensions:", len(embedding))
print("First 5 values:", embedding[:5])