import socket
import uuid
import asyncio
import os
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError
from app.service.audio_service import split_response_to_uploaded_audio
import config

udp_server_running = True

async def start_udp_server(host='0.0.0.0', port=config.udp_port):
    global udp_server_running
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    print(f"Listening for UDP packets on {host}:{port}")

    current_recording = b''
    while udp_server_running:
        data, addr = await asyncio.get_event_loop().run_in_executor(None, sock.recvfrom, 1043)
        if len(data) < 19:  # 长度不符合预期
            print(f"Received unexpected packet from {addr}")
            continue
        
        token = data[:16] 
        recording_id = data[16:18]
        frame_type = data[18:19]
        payload = data[19:]
        recording_id_int = int.from_bytes(recording_id, 'big')
        print(f"Received token: {token.hex()} RecordingId: {recording_id_int}")
        print(f"Received frame type: {frame_type}")

        if frame_type == b'\x02':  # 开始或结束帧
            if payload:
                print(payload)
                print(f"Unexpected payload in end frame from {addr}")
            if current_recording:
                file_id = str(uuid.uuid4())
                directory = config.audio_file_direction
                file_path = f"{directory}/recording-{file_id}.wav"
                
                if not os.path.exists(directory):
                    os.makedirs(directory)
                save_audio_with_pydub(file_path, current_recording)
                print(f"Recording saved as {file_path}")
                await split_response_to_uploaded_audio(file_path, recording_id_int)
                current_recording = b''
            else:
                print(f"Start receiving from {addr}")

        elif frame_type == b'\x01':  # 中间帧
            print(f"中间: {payload[:10]}")
            current_recording += payload
            print(f"Received {len(payload)} bytes from {addr}")
        else:
            print(f"Unknown frame type: {frame_type} from {addr}")
    
    sock.close()
    print("UDP server closed")


def save_audio_with_pydub(file_name, audio_data):
    try:
        # Create an AudioSegment from raw data
        audio_segment = AudioSegment(
            data=audio_data,
            sample_width=2,  # 2 bytes per sample (16-bit PCM)
            frame_rate=32000,  # Sample rate
            channels=1  # Mono
        )

        # Export the AudioSegment to a WAV file
        audio_segment.export(file_name, format="wav")
        print(f"Audio saved successfully with pydub as {file_name}")

    except CouldntDecodeError:
        print(f"Could not decode audio data for {file_name}")

