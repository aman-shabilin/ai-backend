import os
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain_community.vectorstores import FAISS
from bs4 import SoupStrainer
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


class VectorStore(): 
    def __init__(self, index_name="zusdrinkware", namespace="default"):
        self.pinecone = Pinecone()
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

        bs4_strainer = SoupStrainer("product-list", class_="product-list")
        
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


    def similarity_search(self, query, k=5):
        if self.vector_store is None:
            raise ValueError("Vector store is empty. Please add documents first.")
        return self.vector_store.similarity_search(query, k=k)    







