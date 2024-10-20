from uagents import Model, Agent, Context, Bureau
from typing import Dict, Any
import google.generativeai as genai
import os
import singlestoredb as s2
import requests

conn = s2.connect('https://user:password@host:port/database?local_infile=True')

class Request(Model):
    context: str

class Response(Model):
    notes: str

context_agent = Agent(
    name = "Context Agent",
    seed = "Context Agent recovery phrase"
)

notes_agent = Agent(
    name = "Note taking Agent",
    seed = "Note taking Agent recovery phrase"
)

@notes_agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"Starting up {notes_agent.name}")
    ctx.logger.info(f"With address: {notes_agent.address}")

@context_agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"Starting up {context_agent.name}")
    ctx.logger.info(f"With address: {context_agent.address}")

@notes_agent.on_query(model=Response)
async def handle_notes(ctx: Context, notes: Response) -> Dict[str, Any]:
    with conn.cursor() as cur:
        cur.execute('SELECT notes FROM meeting_notes WHERE meeting_id = 1')
        text_from_db = cur.fetchall()
    
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel('models/gemini-1.5-pro-latest')
    
    input_prompt = f"""
    Given the raw text from a meeting: {text_from_db}, please generate the following:
    1. A concise summary of the key points discussed in the meeting.
    2. A detailed list of notes, including:
        - Key decisions made
        - Action items with assigned responsibilities
        - Important deadlines
        - Any unresolved issues or next steps.
    Ensure the output is clear, organized, and professional.
    """

    generated_content = model.generate_content(input_prompt)
    with conn.cursor() as cur:
        insert_query = 'INSERT INTO meeting_notes (meeting_id, notes) VALUES (%s, %s)'
        cur.execute(insert_query, (1, generated_content))
    

    
