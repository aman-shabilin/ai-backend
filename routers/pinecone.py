import bs4
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter


class VectorStore: 
    def __init__(self, collection_name="zus_drinkware", persist_directory="chroma_db"):
        self.embeddings = HuggingFaceEmbeddings(model_name='BAAI/bge-small-en-v1.5')

        self.vector_store = Chroma(collection_name=collection_name,
                                   embedding_function=self.embeddings,
                                   persist_directory=persist_directory)
    
def scrape(url="https://shop.zuscoffee.com/collections/tumbler"):

    bs4_strainer = bs4.SoupStrainer("product-list", class_="product-list")
    
    loader = WebBaseLoader(
        web_paths=(url),
        bs_kwargs={"parse_only": bs4_strainer},
    )
    
    docs = loader.load()

    return docs[0].page_content

def split_product(raw_text: str):

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
    """Add documents to the vector store."""
    self.vector_store.add_documents(documents)
    self.vector_store.persist()
    
def similarity_search(self, query, k=5):
    return self.vector_store.similarity_search(query, k=k)






