from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn

import openai

app = FastAPI()


@app.post("/chat/")
def predict(request: APIRequest):
    """
    Test with:
        curl -X POST http://127.0.0.1:5000/chat
            -H 'Content-Type: application/json'
            -d '{"user_input": "Hi, Dungeon Master!", "max_tokens": 50, "gpt4": True}'
    """
    try:
        conv
    except NameError:
        conv = openai.conversation.Conversation(
            request.max_tokens,
            request.gpt4,
        )
        return JSONResponse(
            content={"response": conv.current_node.context[-1]["content"]}
        )

    reply = conv.send_message(request.user_input)
    return JSONResponse(content={"response": reply})


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=5000,
        # debug=True,
    )
