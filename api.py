from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn

from openai_dm.conversation import Conversation

app = FastAPI()

conv = Conversation(20, True)


class APIRequest(BaseModel):
    user_input: str
    max_tokens: int
    gpt4: bool


@app.post("/chat/")
def predict(request: APIRequest):
    """
    Test with:
        curl -X POST http://127.0.0.1:5000/chat
            -H 'Content-Type: application/json'
            -d '{"user_input": "Hi, Dungeon Master!", "max_tokens": 50, "gpt4": True}'
    """
    reply = conv.send_message(request.user_input)
    return JSONResponse(content={"response": reply})


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=5000,
        # debug=True,
    )
