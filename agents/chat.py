from abc import ABC, abstractmethod

class LLM(ABC):
    @abstractmethod
    def chat(self, prompt: str) -> str:
        pass

# class Store(ABC):
#     @abstractmethod
#     def scrape(self, url: str) -> str:
#         pass
#     def split_product(self, raw_text: str):
#         pass
#     def add_documents(self, documents):
#         pass
#     def similarity_search(self, query, k=5):
#         pass
    