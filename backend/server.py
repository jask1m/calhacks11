import json
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from uagents import Model
from uagents.query import query
from uagents.envelope import Envelope 
 
AUDIENCE_FEEDBACK_AGENT_ADDRESS = "agent1qfs4klegx9nmuaaxd26payed2uawzx94uemg7huvh6p86aw8l3z0xcy8su2"
SENTIMENT_ANALYSIS_AGENT_ADDRESS = "agent1qgr4n3yuftz9rhe939kchwkvuctdyk5r7k98ujxdkmu63nthjswfcaa8jkk" 
 
class TestRequest(Model):
    message: str

app = FastAPI()

async def agent_query(req):
    response = await query(destination=AGENT_ADDRESS, message=req, timeout=15)
    if isinstance(response, Envelope):
        data = json.loads(response.decode_payload())
        return data["text"]
    return response

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


@app.post("/command")
async def make_agent_call(req: Request):
    try:
        res = await agent_query(req)
        return f"successful call - agent response: {res}"
    except Exception:
        return "unsuccessful agent call"
    
if __name__ == "main":
    uvicorn.run("server:app", port=8000, reload=True)