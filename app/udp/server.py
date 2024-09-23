import asyncio
import os
import socket
import uuid

from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError
from sqlalchemy.orm import Session

import app.config as config
from app.core.token import get_user_by_token
from app.core.user import set_current_user
from app.service.audio_service import split_response_to_uploaded_audio
from app.system.db import yield_postgresql_session, postgresql_session_context

MIDDLE_FRAME_FLAG = b'\x01'
START_OR_END_FLAG = b'\x02'

udp_server_running = True
validated_tokens = {}


async def start_udp_server(host='0.0.0.0', port=config.udp_port):
    global udp_server_running
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    print(f"Listening for UDP packets on {host}:{port}")

    current_recording = {}
    while udp_server_running:
        data, addr = await asyncio.get_event_loop().run_in_executor(None, sock.recvfrom, 1043)
        if len(data) < 19:
            print(f"Received unexpected packet from {addr}")
            continue

        token = data[:16]
        recording_id = data[16:18]
        frame_type = data[18:19]
        payload = data[19:]
        recording_id_int = int.from_bytes(recording_id, 'big')
        token_hex = token.hex()
        print(f"Received token: {token_hex} RecordingId: {recording_id_int}")
        print(f"Received frame type: {frame_type}")

        if frame_type == START_OR_END_FLAG:
            if token_hex not in validated_tokens:
                _current_user = get_user_by_token(token_hex)
                if not _current_user:
                    print(f"Invalid token received: {token_hex} from {addr}")
                    continue
                validated_tokens[token_hex] = True
                set_current_user(_current_user)
            if payload:
                print(payload)
                print(f"Unexpected payload in end frame from {addr}")
            if current_recording.get(token_hex):
                file_id = str(uuid.uuid4())
                directory = config.audio_file_direction
                file_path = f"{directory}/recording-{file_id}.wav"

                if not os.path.exists(directory):
                    os.makedirs(directory)
                save_audio_with_pydub(file_path, current_recording[token_hex])
                print(f"Recording saved as {file_path}")
                session: Session = next(yield_postgresql_session())
                pg_context_token = postgresql_session_context.set(session)
                try:
                    await split_response_to_uploaded_audio(file_path, recording_id_int)
                finally:
                    session.close()
                    postgresql_session_context.reset(pg_context_token)

                del validated_tokens[token_hex]
                del current_recording[token_hex]
            else:
                print(f"Start receiving from {addr}")

        elif frame_type == MIDDLE_FRAME_FLAG:
            if validated_tokens.get(token_hex):
                current_recording[token_hex] = current_recording.get(token_hex, b'') + payload
                print(f"Received {len(payload)} bytes from {addr}")
            else:
                print(f"Invalid token, ignoring data from {addr}")
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
