import json
from fastapi import FastAPI, HTTPException, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from uagents import Model
from uagents.query import query
from uagents.envelope import Envelope 
import singlestoredb as s2
from pydantic import BaseModel
import os
import singlestoredb as s2
import uvicorn
from dotenv import load_dotenv
from vectorDB import create_and_insert_embeddings
from confluent_kafka import Producer, KafkaError

load_dotenv()

username = os.getenv('S2_USERNAME')
password = os.getenv('S2_PASSWORD')
host = os.getenv('S2_HOST')
port = os.getenv('S2_PORT')
database = os.getenv('S2_DATABASE')

if not all([port, database, username, password, host]):
    raise EnvironmentError("One or more environment variables are not set.")

connection_string = f"{username}:{password}@{host}:{port}/{database}"
try:
    conn = s2.connect(connection_string)
except Exception as e:
    print(f"Failed to connect to the database: {e}")
    raise

class ConnectionManager:
    def init(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

class User(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    email_address: str

class Request(Model):
    message: str

app = FastAPI()

origins = [""]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=[""],
    allow_headers=["*"],
)

manager = ConnectionManager()

# Kafka producer configuration
producer_conf = {
    'bootstrap.servers': 'localhost:9092',
    'client.id': 'transcription-producer'
}

producer = Producer(producer_conf)

def delivery_report(err, msg):
    """ Callback to handle success or failure of message delivery """
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received message: {data}")
            producer.produce('transcription-topic', data.encode('utf-8'), callback=delivery_report)
            producer.flush()  # Ensure the message is sent
    except WebSocketDisconnect:
        print("WebSocket disconnected")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await websocket.close()
        print("WebSocket connection closed")

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
