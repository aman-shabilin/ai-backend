import os
import re
from bs4 import SoupStrainer
from pinecone import Pinecone
from langchain_core.documents import Document
from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import WebBaseLoader
class VectorStore(): 
    def __init__(self, index_name="zusdrinkware", namespace="default"):
        self.pinecone = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        self.embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")

        self.vector_store = PineconeVectorStore(
            index_name=index_name,
            namespace=namespace,
            embedding=self.embeddings,
        )
    
    def scrape(self, url="https://shop.zuscoffee.com/collections/tumbler"):

        bs4_strainer = SoupStrainer(class_=("product-list", "product-card__info", "product-card__title", "price-list", "product-card__variant-list") )
        
        loader = WebBaseLoader(
            web_paths=(url,),
            bs_kwargs={"parse_only": bs4_strainer},
        )
        
        docs = loader.load()

        return docs[0].page_content

    def split_product(self, raw_text: str):

    # Split on "+ Quick add" as the raw data is extracted from a single page 
        raw_products = re.split(r"\+ Quick add\s*", raw_text)

        product_docs = []
        seen = set()

        for raw in raw_products:
            product = raw.strip()
            if not product:
                continue

            full_text = f"+ Quick add {product}"

            if full_text not in seen:
                seen.add(full_text)
                product_docs.append(Document(page_content=full_text))

        return product_docs

    def add_documents(self, documents):
        self.vector_store.add_documents(documents)
    
    def retrieve(self, query, k=5):
        return self.vector_store.similarity_search(query, k=k)
    
    def is_vector_store_empty(self, index_name="zusdrinkware", namespace: str = "default") -> bool:
        index = self.pinecone.Index(index_name)
        stats = index.describe_index_stats()
        
        namespace_stats = stats.get("namespaces", {}).get(namespace, {})
        vector_count = namespace_stats.get("vector_count", 0)

        print(f"[Startup] Vector count in namespace '{namespace}': {vector_count}")
        return vector_count == 0





