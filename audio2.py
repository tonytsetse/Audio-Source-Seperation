import pyaudio
import wave
import numpy as np
import sys

np.set_printoptions(threshold=sys.maxsize)

a = input()

FORMAT = pyaudio.paInt16
CHANNELS = 8
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 7
WAVE_OUTPUT_FILENAME = "file.wav"
output8 = [None]*8
for i in range(CHANNELS):
    output8[i]="Channel"+str(i)+".wav"
audio = pyaudio.PyAudio()

# start Recording
stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK)
print ("recording...")
frames = []
frames8 = [b'' for i in range(CHANNELS)]

counter = 0
max = 0
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    data3 = np.frombuffer(data,np.int16)
    data2 = np.frombuffer(data,np.int16)*10 #higher volume
    w_data = np.frombuffer(data,np.int16)
    w_data.shape = -1,CHANNELS
    w_data = w_data.T
    
    #print(w_data)
    #print(w_data[0])
    #print(w_data.size)
    #print(w_data[7].tobytes())
    #print("End\n\n")
    #for j in range(data.shape())
    '''
    for j in range(data3.size):
        if (abs(data3[j])>=100 and counter<10):
            print(j%8)
            counter= counter +1
    '''
    max = data3.argmax()%8
    if (abs(data3[max])>50):
        print(max)
    for j in range(CHANNELS):
        frames8[j]+=(w_data[j].tobytes())
    #print(data)
    frames.append(data2)
    #frames.append(data)
print ("finished recording")

#print(max) 
 
# stop Recording
stream.stop_stream()
stream.close()
audio.terminate()
 
waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()

for i in range(CHANNELS):
    waveFile = wave.open(output8[i], 'wb')
    waveFile.setnchannels(1)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(frames8[i])
    waveFile.close()