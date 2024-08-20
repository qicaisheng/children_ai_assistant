import json
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import conversation
import html_page

app = FastAPI()


@app.get("/")
async def root():
    return HTMLResponse(html_page.html)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        request = await websocket.receive_text()
        round = json.loads(request)['round']
        user_input = json.loads(request)['input']
        print(f"""User: {user_input}""")
            
        stream_response = conversation.answer(user_input)
        
        print("Assistant: ", end="")
        for output_text in stream_response:
            print(output_text, end="")
            await websocket.send_json({"round": round, "output": output_text})
        print("")
