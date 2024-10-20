import singlestoredb as s2
from openai import OpenAI
import os
from meeting_agents import vector_search_agent

username = os.getenv('S2_USERNAME')
password = os.getenv('S2_PASSWORD')
host = os.getenv('S2_HOST')
port = os.getenv('S2_PORT')
database = os.getenv('S2_DATABASE')

connection_string = f"{username}:{password}@{host}:{port}/{database}"
conn = s2.connect(connection_string)

client = OpenAI()


def create_and_insert_embeddings(text, model="text-embedding-ada-002"):   
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=text
    )

    # Extract the embedding from the response
    vector_embeddings = response['data'][0]['embedding']

    print(vector_embeddings)

    insert_to_vector_query = """
        INSERT INTO myvectortable (text, vector) VALUES (%s, %s);
    """

    # Insert the text and the vector embeddings into the vector database
    with conn.cursor() as cur:
        cur.execute(insert_to_vector_query, (text, vector_embeddings))
        conn.commit()

    use_vector_search_agent(text, vector_embeddings)

async def use_vector_search_agent(text, vector_embeddings):
    # Create a context if needed
    ctx = Context()
    ctx.logger.info(f"Using {vector_search_agent.name} for text: {text}")
    # Add your vector search logic here
    # For example, you might send a query to the agent and get a response
    query = {
        "text": text,
        "vector": vector_embeddings
    }
    response = await vector_search_agent.query(query)
    return response







