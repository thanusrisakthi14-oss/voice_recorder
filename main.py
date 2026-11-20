import pyaudio
import wave
import speech_recognition as sr
import numpy as np
import matplotlib.pyplot as plt 
import threading

stop=False
frames=[]
def stop_recording():
    global stop 
    input("Press enter to stop recording...")
    stop=True
p=pyaudio.PyAudio()
stream=p.open(format=pyaudio.paInt16,channels=1,rate=16000,input=True,frames_per_buffer=1024)
print("Recording.....")
threading.Thread(target=stop_recording,daemon=True).start()
while not stop:
    frames.append(stream.read(1024))
stream.stop_stream()
stream.close()
p.terminate()
data=b''.join(frames)
with wave.open('recording.wav','wb') as f:
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(16000)
    f.writeframes(data)

print("Audio Saved")
recognizer=sr.Recognizer()
audio=sr.AudioData(data,16000,2)
try:
    print("Transcription",recognizer.recognize_google(audio))
except Exception as e:
    print(e)
samples=np.frombuffer(data,dtype=np.int16)
plt.plot(samples)
plt.title("Voice Waveform")
plt.xlabel("sample")

plt.ylabel("Amplitude")
plt.grid()
plt.show()


    
