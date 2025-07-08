from langchain_community.utilities import SQLDatabase

sqlite_uri = "sqlite:///./zus_coffee.db"

db = SQLDatabase.from_uri(sqlite_uri)