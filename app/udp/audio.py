from pydub import AudioSegment

# 加载音频文件
audio = AudioSegment.from_file("audio/recording-52b2a7c51ba9423aaee80ba1282ad70d.wav")

# 获取采样率
sample_rate = audio.frame_rate
print(f"Sample Rate: {sample_rate} Hz")

# 获取采样宽度
sample_width = audio.sample_width
print(f"Sample Width: {sample_width} bytes")

# 获取声道数
channels = audio.channels
print(f"Channels: {channels}")


"""
Sample Rate: 32000 Hz
Sample Width: 2 bytes
Channels: 1
"""