import singlestoredb as s2
import tiktoken
import os
from meeting_agents import vector_search_agent
from uagents import Context
from dotenv import load_dotenv
from openai import OpenAI
import struct

load_dotenv()

username = os.getenv('S2_USERNAME')
password = os.getenv('S2_PASSWORD')
host = os.getenv('S2_HOST')
port = os.getenv('S2_PORT')
database = os.getenv('S2_DATABASE')

connection_string = f"{username}:{password}@{host}:{port}/{database}"
conn = s2.connect(connection_string)
tokenizer = tiktoken.encoding_for_model("text-embedding-ada-002")


def test_embeddings(text, model="text-embedding-ada-002"):
    client = OpenAI(
    # This is the default and can be omitted
        api_key=os.environ.get("OPEN_AI_API_KEY"),
    )
    # Call the OpenAI API to get the embeddings
    response = client.embeddings.create(
        input=text,
        model=model
    )
    
    # Extract the embeddings from the response
    vector_embeddings = response.data[0].embedding

    vector_embeddings_blob = struct.pack(f'{len(vector_embeddings)}f', *vector_embeddings)

    insert_to_vector_query = """
        INSERT INTO myvectortable (text, vector) VALUES (%s, %s);
    """

    # Insert the text and the vector embeddings into the vector database
    with conn.cursor() as cur:
        cur.execute(insert_to_vector_query, (text, vector_embeddings_blob))
        conn.commit()

    return response.data[0].embedding
    

def create_and_insert_embeddings(text, model="text-embedding-ada-002"):   
    client = OpenAI(
        api_key=os.environ.get("OPEN_AI_API_KEY"),
    )
    tokens = tokenizer.encode(text)
    tokenized_text = tokenizer.decode(tokens)

    response = client.embeddings.create(
        model=model,
        input=tokenizer.decode(tokens)
    )

    
    vector_embeddings = response.data[0].embedding

    vector_embeddings_blob = struct.pack(f'{len(vector_embeddings)}f', *vector_embeddings)

    insert_to_vector_query = """
        INSERT INTO myvectortable (text, vector) VALUES (%s, %s);
    """

    # Insert the text and the vector embeddings into the vector database
    with conn.cursor() as cur:
        cur.execute(insert_to_vector_query, (text, vector_embeddings_blob))
        conn.commit()

    use_vector_search_agent(tokenized_text, vector_embeddings_blob)

async def use_vector_search_agent(text, vector_embeddings_blob):
    # Create a context if needed
    ctx = Context()
    ctx.logger.info(f"Using {vector_search_agent.name} for text: {text}")
    # Add your vector search logic here
    # For example, you might send a query to the agent and get a response
    query = {
        "text": text,
        "vector": vector_embeddings_blob
    }
    response = await vector_search_agent.query(query)
    return response


if __name__ == "__main__":
    text = "Hello, how are you?"
    result = test_embeddings(text)
    print(result)





