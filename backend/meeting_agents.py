from uagents import Model, Agent, Context, Bureau
from typing import Dict, Any
import google.generativeai as genai
import os
import singlestoredb as s2
from typing import List 
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

username = os.getenv('S2_USERNAME')
password = os.getenv('S2_PASSWORD')
host = os.getenv('S2_HOST')
port = os.getenv('S2_PORT')
database = os.getenv('S2_DATABASE')

connection_string = f"{username}:{password}@{host}:{port}/{database}"
conn = s2.connect(connection_string)

class Response(Model):
    query: str
    results: List[List[float]]
class Notes(Model):
    notes: str

notes_agent = Agent(
    name = "Note taking Agent",
    seed = "Note taking Agent recovery phrase"
)

vector_search_agent = Agent(
    name = "Vector Search Agent",
    seed = "Vector Search Agent recovery phrase"
)

@notes_agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"Starting up {notes_agent.name}")
    ctx.logger.info(f"With address: {notes_agent.address}")

@vector_search_agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"Starting up {vector_search_agent.name}")
    ctx.logger.info(f"With address: {vector_search_agent.address}")

@vector_search_agent.on_query(model=Response)
async def vector_search(ctx: Context, response: Response, query: dict):
    ctx.logger.info(f"Vector search query: {query}")

    text = query.get("text")
    vector = query.get("vector")
    
    # add vector index
    alter_table = """alter table myvectortable add vector index hnsw_pq2 (vector) INDEX_OPTIONS '{"index_type": "HNSW_PQ", "m": 512}'"""
    
    with conn.cursor() as cur:
        cur.execute(alter_table)

    search_query = """
        SET @qv = (SELECT vector FROM myvectortable WHERE text = %s);
        SELECT text, v <*> @qv as sim
        FROM myvectortable
        ORDER BY sim USE INDEX (ivfpq_nlist) desc
        limit 10;
    """

    with conn.cursor() as cur:
        cur.execute(search_query, (text,))
        results = cur.fetchall()
    
    # Process the results and return a response
    response = {
        "query": text,
        "results": [result[0] for result in results]
    }
    ctx.logger.info(f"Vector search results: {response}")
    return response

@notes_agent.on_query(model=Notes) 
async def handle_notes(ctx: Context, response: Response):  
    ctx.logger.info(f"Handling notes query with embeddings: {response.results}")

    combined_text = ""

    # SQL query to find the closest text based on the embedding
    search_query = """
        SET @qv = %s;
        SELECT text, vector <*> @qv as sim
        FROM myvectortable
        ORDER BY sim DESC
        LIMIT 1;
    """

    # Loop through each embedding and retrieve the corresponding text
    for embedding in response.results:
        embedding_str = ','.join(map(str, embedding))  # Convert embedding to a string for SQL
        with conn.cursor() as cur:
            cur.execute(search_query, (embedding_str,))
            result = cur.fetchone()  # Get the text with the highest similarity
            if result:
                text = result[0]  # Assuming 'text' is in the first column
                combined_text += f" {text}"

    ctx.logger.info(f"Combined text from embeddings: {combined_text}")


    # Configure the Gemini model
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel('models/gemini-1.5-pro-latest')

    # Prepare the input prompt for the AI model
    input_prompt = f"""
    Given the following combined raw text: {combined_text}, please generate:
    1. A concise summary of the key points discussed.
    2. A detailed list of notes, including:
        - Key decisions made
        - Action items with assigned responsibilities
        - Important deadlines
        - Any unresolved issues or next steps.
    Ensure the output is clear, organized, and professional.
    """

    # Generate the notes using the Gemini model
    generated_notes = model.generate_content(input_prompt)

    # Prepare the notes
    notes = {
        "notes": generated_notes
    }

    insert_query = """
        INSERT INTO notes VALUES (%s, %s, %s)
    """
    
    with conn.cursor() as cur:
        cur.execute('SELECT MAX(note_id) FROM meeting_notes')
        highest_note_id = cur.fetchone()[0] + 1
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cur.execute(insert_query, (highest_note_id, generated_notes, current_time))
        conn.commit()

    ctx.logger.info(f"Generated notes: {generated_notes}")
    return notes
    
bureau = Bureau()
bureau.add(notes_agent)
bureau.add(vector_search_agent)
 
if __name__ == "__main__":
    bureau.run()

