import json
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
import paho.mqtt.client as mqtt
import conversation
import html_page


def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("test/topic")

def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()} on topic {msg.topic}")

mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        print(f"Try to connect and start MQTT client")
        mqtt_client.connect("127.0.0.1", 1883, 60)
        mqtt_client.loop_start()
        print(f"Succeed to connect and start MQTT client")
        yield
    except Exception as e:
        print(f"Failed to connect or start MQTT client: {e}")
    finally:
        print(f"Try to disconnect and stop MQTT client")
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
        print(f"Succeed to disconnect and stop MQTT client")

app = FastAPI(lifespan=lifespan)

@app.post("/publish/")
async def publish_message(topic: str, message: str):
    result = mqtt_client.publish(topic, message)
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
            
        stream_response = conversation.answer(user_input)
        
        print("Assistant: ", end="")
        for output_text in stream_response:
            print(output_text, end="")
            await websocket.send_json({"round": round, "output": output_text})
        print("")
