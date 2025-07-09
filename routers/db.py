from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import ChatPromptTemplate

sqlite_uri = "sqlite:///./zus_coffee.db"

db = SQLDatabase.from_uri(sqlite_uri)

def run_query(query):
    return db.run(query)

# Cleaning SQL schema output 
def clean_sql_output(output: str) -> str:
    # Remove Markdown ```sql ``` or ```
    return (
        output.strip()
        .replace("```sql", "")
        .replace("```", "")
        .strip()
    )

# System prompt for user depends on user qusetion to generate schema
sql_prompt = ChatPromptTemplate.from_template("""
Based on the table schema below, write a SQL query that would answer the user's question:
{schema}

Question: {question}
SQL Query:""")

# Define the prompt for generating the final natural language answer
nl_response_prompt = ChatPromptTemplate.from_template("""
Based on the table schema below, question, sql query, and sql response, write a natural language response:
{schema}

Question: {question}
SQL Query: {query}
SQL Response: {response}
""")


intent_prompt = ChatPromptTemplate.from_template("""
You are an assistant that decides if a user's question is specific enough to generate a SQL query.
Answer only "Yes" or "No".

Question: {question}
Is the question clear enough to answer with a database query?
""")
