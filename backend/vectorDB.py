import os
from meeting_agents import vector_search_agent
from uagents import Context
from dotenv import load_dotenv
from openai import OpenAI
import struct
import asyncio
from concurrent.futures import ThreadPoolExecutor
from confluent_kafka import Consumer, KafkaError
import tiktoken  # Assuming this is correctly imported for the tokenizer
import singlestoredb as s2

load_dotenv()

# Fetch environment variables
username = os.getenv('S2_USERNAME')
password = os.getenv('S2_PASSWORD')
host = os.getenv('S2_HOST')
port = os.getenv('S2_PORT')
database = os.getenv('S2_DATABASE')

# Database connection
connection_string = f"{username}:{password}@{host}:{port}/{database}"
try:
    conn = s2.connect(connection_string)
except Exception as e:
    print(f"Failed to connect to the database: {e}")
    raise

tokenizer = tiktoken.encoding_for_model("text-embedding-ada-002")

# Kafka consumer configuration
consumer_conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'transcription-group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(consumer_conf)

# Create a ThreadPoolExecutor for running blocking tasks
executor = ThreadPoolExecutor()

# Kafka consumer function to handle messages asynchronously
async def consume_messages():
    consumer.subscribe(['transcription-topic'])
    print("Subscribed to topic: transcription-topic")

    loop = asyncio.get_event_loop()

    while True:
        # Run the blocking Kafka consumer.poll() in a separate thread
        msg = await loop.run_in_executor(executor, consumer.poll, 1.0)  # Poll for 1 second
        
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
            # Call the embedding function asynchronously
            try:
                await create_and_insert_embeddings(transcription_data)
            except Exception as e:
                print(f"Error in create_and_insert_embeddings: {e}")

    consumer.close()
    print("Consumer closed")

# Test embeddings function (sync)
def test_embeddings(text, model="text-embedding-ada-002"):
    client = OpenAI(api_key=os.environ.get("OPEN_AI_API_KEY"))
    response = client.embeddings.create(input=text, model=model)
    print(response.data[0].embedding)

# Async embedding creation and insertion function
async def create_and_insert_embeddings(text, model="text-embedding-ada-002"):
    client = OpenAI(api_key=os.environ.get("OPEN_AI_API_KEY"))
    
    # Tokenize text
    tokens = tokenizer.encode(text)
    tokenized_text = tokenizer.decode(tokens)

    # Call OpenAI to get embeddings
    response = client.embeddings.create(model=model, input=tokenizer.decode(tokens))
    vector_embeddings = response.data[0].embedding

    # Pack embeddings into binary format
    vector_embeddings_blob = struct.pack(f'{len(vector_embeddings)}f', *vector_embeddings)

    print(vector_embeddings)

    insert_to_vector_query = """
        INSERT INTO myvectortable (text, vector) VALUES (%s, %s);
    """

    # Insert embeddings into database
    with conn.cursor() as cur:
        cur.execute(insert_to_vector_query, (text, vector_embeddings_blob))
        conn.commit()

    # Use the vector search agent
    await use_vector_search_agent(tokenized_text, vector_embeddings_blob)

# Async vector search agent interaction
async def use_vector_search_agent(text, vector_embeddings_blob):
    ctx = Context()
    ctx.logger.info(f"Using {vector_search_agent.name} for text: {text}")
    
    # Create a query and call the agent
    query = {
        "text": text,
        "vector": vector_embeddings_blob
    }
    response = await vector_search_agent.query(query)
    return response

# Main function to run the consumer in the event loop
if __name__ == "__main__":
    try:
        asyncio.run(consume_messages())  # Run the Kafka consumer asynchronously
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        consumer.close()
