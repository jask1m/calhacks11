import singlestoredb as s2
import tiktoken
import os
from meeting_agents import vector_search_agent
from uagents import Context
from dotenv import load_dotenv
from openai import OpenAI
import asyncio
from confluent_kafka import Consumer, KafkaError

# Kafka consumer configuration
consumer_conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'transcription-group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(consumer_conf)

load_dotenv()

username = os.getenv('S2_USERNAME')
password = os.getenv('S2_PASSWORD')
host = os.getenv('S2_HOST')
port = os.getenv('S2_PORT')
database = os.getenv('S2_DATABASE')

connection_string = f"{username}:{password}@{host}:{port}/{database}"
conn = s2.connect(connection_string)
tokenizer = tiktoken.encoding_for_model("text-embedding-ada-002")

def consume_messages():
    consumer.subscribe(['transcription-topic'])

    while True:
        msg = consumer.poll(1.0)  # Wait for 1 second for a message
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(f"Kafka error: {msg.error()}")
                break
        else:
            transcription_data = msg.value().decode('utf-8')
            print(f"Received transcription: {transcription_data}")
            # Call your embedding function here
            create_and_insert_embeddings(transcription_data)

    consumer.close()
    
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
    print(response.data[0].embedding)
    

async def create_and_insert_embeddings(text, model="text-embedding-ada-002"):   
    client = OpenAI(
    # This is the default and can be omitted
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

    print(vector_embeddings)

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
    try:
        asyncio.run(consume_messages())  # Run the Kafka consumer in the asyncio event loop
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        consumer.close() 
