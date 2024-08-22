import json
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
import paho.mqtt.client as mqtt
import conversation
import html_page
from mqtt.manager import mqtt_manager
from mqtt.client import publish as mqtt_publish
import asyncio
from udp.server import start_udp_server, udp_server_running


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        print(f"Try to connect and start MQTT client")
        mqtt_manager.connect()
        print(f"Succeed to connect and start MQTT client")

        print(f"Try to start udp server")
        asyncio.create_task(start_udp_server())
        print(f"Succeed to start udp server")

        yield
    except Exception as e:
        print(f"Failed to connect or start MQTT client: {e}")
    finally:
        print(f"Try to disconnect and stop MQTT client")
        mqtt_manager.disconnect()
        print(f"Succeed to disconnect and stop MQTT client")

        global udp_server_running
        udp_server_running = False
        print("Shutting down UDP server...")

app = FastAPI(lifespan=lifespan)

@app.post("/publish/")
async def publish_message(topic: str, message: str):
    result = mqtt_publish(topic, message)
    if result.rc == 0:
        return {"status": "Message published successfully"}
    else:
        return {"status": f"Failed to publish message, return code {result.rc}"}
    

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
            
        stream_response = conversation.stream_answer(user_input)
        
        print("Assistant: ", end="")
        for output_text in stream_response:
            print(output_text, end="")
            await websocket.send_json({"round": round, "output": output_text})
        print("")
