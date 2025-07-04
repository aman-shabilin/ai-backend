import os

import pprint
from dotenv import load_dotenv
from pinecone import Pinecone


load_dotenv()
pinecone_client = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

index_name = "zus-drinkware"

if not pinecone_client.has_index(index_name):
    index_model=pinecone_client.create_index_for_model(
        name=index_name,
        cloud="aws",
        region="us-east-1",
        embed={"model":"multilingual-e5-large","field_map" :{"text": "chunk_text"}}
    )

index = pinecone_client.Index(index_name)