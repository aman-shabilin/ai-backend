import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from bs4 import SoupStrainer
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()
class VectorStore(): 
    def __init__(self, index_name="zusdrinkware", namespace="default"):
        self.pinecone = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        self.embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")

        if index_name not in [idx['name'] for idx in self.pinecone.list_indexes()]:
            print(f"Creating index {index_name}...")
            self.pinecone.create_index(
                index_name=index_name,
                dimension=384,
                metric="cosine",
                spec=ServerlessSpec(cloud='aws', region='us-east-1')
            )
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

        product_blocks = raw_text.split("+ Quick add")
        
        cleaned_blocks = [
            "+ Quick add\n" + block.strip()
            for block in product_blocks
            if block.strip()
        ]

        docs = [Document(page_content=block) for block in cleaned_blocks]

        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        split_docs = splitter.split_documents(docs)

        return split_docs

    def add_documents(self, documents):
        self.vector_store.add_documents(documents)

    def as_retriever(self):
        return self.vector_store.as_retriever()

    def similarity_search(self, query, k=5):
        if self.vector_store is None:
            raise ValueError("Vector store is empty. Please add documents first.")
        return self.vector_store.similarity_search(query, k=k)    

    def describe(self):
        stats = self.pinecone.describe_index_stats()
        print(stats)
        return stats





