import socket
import config
import os

def send_audio_file(filename, server_ip, server_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    token_str = '2905cc6103c5442985cb15946425e451'  # 示例 token 字符串
    token = bytes.fromhex(token_str)  # 将32字符的字符串转换为16字节
    recording_id = (9).to_bytes(2, 'big')  # 示例 RecordingId，2 字节

    # 发送开始帧
    start_frame = token + recording_id + b'\x02'
    sock.sendto(start_frame, (server_ip, server_port))
    print(f"Sent start frame: {start_frame}")

    # 发送音频数据的中间帧
    with open(filename, 'rb') as f:
        while True:
            chunk = f.read(1024)
            if not chunk:
                break
            data_frame = token + recording_id + b'\x01' + chunk
            sock.sendto(data_frame, (server_ip, server_port))

    print(f"Sent {filename}")

    # 发送结束帧
    end_frame = token + recording_id + b'\x02'
    sock.sendto(end_frame, (server_ip, server_port))
    print(f"Sent end frame: {end_frame}")

    sock.close()

# 示例用法
# send_audio_file('../audio/recording-52b2a7c51ba9423aaee80ba1282ad70d.wav', config.udp_host, config.udp_port)
send_audio_file('../audio/recording-39984d06691544bfb1c91c139e8662a7.wav', config.udp_host, config.udp_port)
