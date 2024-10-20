import json
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from uagents import Model
from uagents.query import query
from uagents.envelope import Envelope 
import singlestoredb as s2
from pydantic import BaseModel
import os

username = os.getenv('S2_USERNAME')
password = os.getenv('S2_PASSWORD')
host = os.getenv('S2_HOST')
port = os.getenv('S2_PORT')
database = os.getenv('S2_DATABASE')

connection_string = f"{username}:{password}@{host}:{port}/{database}"
conn = s2.connect(connection_string)
 
AUDIENCE_FEEDBACK_AGENT_ADDRESS = "agent1qfs4klegx9nmuaaxd26payed2uawzx94uemg7huvh6p86aw8l3z0xcy8su2"
SENTIMENT_ANALYSIS_AGENT_ADDRESS = "agent1qgr4n3yuftz9rhe939kchwkvuctdyk5r7k98ujxdkmu63nthjswfcaa8jkk" 

class User(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    email_address: str

class Request(Model):
    message: str

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return({"message": "hello word"})

@app.get("/")
def read_root():
    return "Hello from the Agent controller"


@app.post("/query-agent")
async def make_agent_call(req: Request):
    try:
        res = await agent_query(req)
        return f"successful call - agent response: {res}"
    except Exception:
        return "unsuccessful agent call"

@app.post("/create-user")
async def create_user(user: User):
    try:
        with conn.cursor() as cur:
            cur.execute(
                'INSERT INTO users (user_id, first_name, last_name, email_address) VALUES (%s, %s, %s, %s)',
                (user.user_id, user.first_name, user.last_name, user.email_address)
            )
            conn.commit()
        return {"message": "User created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



if __name__ == "main":
    uvicorn.run("server:app", port=8000, reload=True)

