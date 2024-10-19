from fastapi import FastAPI
import uvicorn
import random


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

if __name__ == "main":
    uvicorn.run("server:app", port=8000, reload=True)

@app.get("/flip-coin")
def flipcoin():
    val = random.random()
    head_tail = ""
    if(val <= 0.5):
        head_tail = "heads"
    else:
        head_tail = "tails"
    return({ "value": head_tail})

@app.get("/flip-coins")
def flip_coins(times: int):
    if times and times > 0:
        head_count = 0
        tail_count = 0
        for _ in range(times):
            val = random.random()
            if(val <= 0.5):
                head_count += 1
            else:
                tail_count += 1
        return ({ "heads": head_count, "tails": tail_count})
    else:
        return({ "message": "you need to send valid times"})