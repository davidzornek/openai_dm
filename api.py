from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn

from openai_dm.conversation import Conversation

app = FastAPI()
# app.mount("/static/", StaticFiles(directory="static"), name="static")

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(Path(BASE_DIR, "templates")))

conv = Conversation(20, True)


class APIRequest(BaseModel):
    user_input: str
    max_tokens: int
    gpt4: bool


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # Serve the HTML file
    return templates.TemplateResponse("index.html", {"request": {}})


@app.get("/chat/")
def chat(request: APIRequest):
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
