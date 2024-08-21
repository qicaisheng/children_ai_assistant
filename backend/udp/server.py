import socket
import uuid
import asyncio
import os

udp_server_running = True

async def start_udp_server(host='0.0.0.0', port=8086):
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
        
        frame_type = data[:1]
        token = data[1:17]  # 16 字节的 token
        recording_id = data[17:19]  # 2 字节的 RecordingId
        payload = data[19:]
        print(f"Received token: {token.hex()} RecordingId: {int.from_bytes(recording_id, 'big')}")
        print(f"Received frame type: {frame_type}")

        if frame_type == b'\x02':  # 开始或结束帧
            if payload:
                print(f"Unexpected payload in end frame from {addr}")
            if current_recording:
                file_id = str(uuid.uuid4())
                directory = "../audio"
                file_name = f"{directory}/recording-{file_id}.wav"
                
                if not os.path.exists(directory):
                    os.makedirs(directory)
                with open(file_name, 'wb') as f:
                    f.write(current_recording)
                print(f"Recording saved as {file_name}")
                current_recording = b''
            else:
                print(f"Start receiving from {addr}")

        elif frame_type == b'\x01':  # 中间帧
            current_recording += payload
            print(f"Received {len(payload)} bytes from {addr}")
        else:
            print(f"Unknown frame type: {frame_type} from {addr}")
    
    sock.close()
    print("UDP server closed")

