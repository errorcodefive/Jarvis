import pyaudio
import wave
import audioop
from collections import deque

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS =2
RATE = 44100
RECORD_SECONDS = 15
p=pyaudio.PyAudio()
stream = p.open (format = FORMAT, channels = CHANNELS, rate = RATE, input = True, frames_per_buffer = CHUNK)

print ("Recording")
frames = []
for i in range (0,int(RATE/CHUNK*RECORD_SECONDS)):
	data = stream.read(CHUNK)
	frames.append(data)
	
print ("Done")

stream.stop_stream()
stream.close()
p.terminate()

wf= wave.open( "output.wav","wb")
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()
