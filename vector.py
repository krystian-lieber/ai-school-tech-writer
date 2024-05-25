import os
import pickle
import time
import uuid
from dotenv import load_dotenv
from langchain_community.vectorstores import Pinecone
from langchain_openai import OpenAIEmbeddings
from tqdm import tqdm
from pinecone import Pinecone

load_dotenv()

# Initialize Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# Define the index name
index_name = "rpl"

# Connect to the Pinecone index
index = pc.Index(index_name)

# Initialize the embeddings model
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

# Directory containing the characteristic embeddings
characteristics_directory = os.getenv("DATA_DIR", "data") + "/characteristics"

# Read all the .pkl files and add them to the PineconeVectorStore
file_list = [
    f for f in os.listdir(characteristics_directory) if f.endswith(".embeddings.pkl")
]

for file_name in tqdm(file_list, desc="Processing files"):
    file_path = os.path.join(characteristics_directory, file_name)
    with open(file_path, "rb") as f:
        embedded_texts = pickle.load(f)
        vectors = []
        documents = []
        for doc, embedding in zip(documents, embeddings):
            vector = {
                "id": str(uuid.uuid4()),
                "values": embedding,
                "metadata": {"title": doc["title"]},
            }
            vectors.append(vector)
            if len(vectors) >= 100:  # Batch size limit
                index.upsert(vectors)
                vectors.clear()
                time.sleep(1)  # To avoid rate limit errors
        if vectors:
            index.upsert(vectors)
        # Assuming each embedded_texts is a list of embeddings
        # Create unique IDs for each embedding
        vector_ids = [f"{file_name}_{i}" for i in range(len(embedded_texts))]
        # Add all embeddings to the Pinecone index in one call
        index.upsert(list(zip(vector_ids, embedded_texts)))

print("Finished adding embeddings to Pinecone.")
