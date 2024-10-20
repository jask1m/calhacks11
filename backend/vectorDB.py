import singlestoredb as s2
from openai import OpenAI
import os
import asyncio

username = os.getenv('S2_USERNAME')
password = os.getenv('S2_PASSWORD')
host = os.getenv('S2_HOST')
port = os.getenv('S2_PORT')
database = os.getenv('S2_DATABASE')

connection_string = f"{username}:{password}@{host}:{port}/{database}"
conn = s2.connect(connection_string)

client = OpenAI()

cur = conn.cursor()


def insert_embedding(text, embedding):
    # SQL query to insert text and embeddings into the myvectortable
    insert_query = """
    INSERT INTO myvectortable (text, vector)
    VALUES (%s, %s);
    """
    cur.execute(insert_query, (text, embedding))
    conn.commit()



def create_embeddings(model="text-embedding-3-small"):
   # SQL query to select the newly updated text from the transcriptions table
   select_query = """
   SELECT text FROM transcriptions WHERE id = (SELECT MAX(transcription_id) FROM transcriptions);
   """
   text = cur.execute(select_query)
   return client.embeddings.create(input = [text], model=model).data[0].embedding
