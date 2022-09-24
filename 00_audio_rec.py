import pyaudio
import wave
import struct
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
plt.style.use("dark_background")
import time
import os

# use this backend to display in separate Tk window
plt.ion()

chunk = 2048            
format = pyaudio.paInt16     
channels = 1                 
rate = int(input("Which sample rate do you need... perhaps 22050, 44100 or 4800...:   "))              
pa = pyaudio.PyAudio()

def record():

    rec_name = input("how would you like to name the file:   ")
    seconds = int(input("how long do you want to record:  "))
    time.sleep(1)
    print("Recording......n")

    stream = pa.open(
        format = format,
        channels = channels,
        rate = rate,
        input = True,
        output = True,
        frames_per_buffer=chunk
    )

    fig, ax = plt.subplots()

    x = np.arange(0, 2 *chunk, 2)
    line, = ax.plot(x, np.random.rand(chunk), "-", lw=0.3, color="red")
    ax.set_xlim(0, 2*chunk)
    ax.set_ylim(0, 255)
    ax.set_title("Waveform of your voice")
    ax.set_ylabel("volume")
    ax.set_xlabel("samples")
    plt.setp(ax, xticks=[0, chunk, 2 * chunk], yticks=[ 0, 128, 255])

    print("streaming your Waveform is active")
    while True:
        frames = []
        for i in range(0, int(rate/chunk*seconds)):
        
            data = stream.read(chunk)
            frames.append(data)
            # chunk * 2 because the data is twice as big
            #b is 255
            data_int = struct.unpack(str(2*chunk) + "B", data)
            #make a numpy array
            data_np = np.array(data_int, dtype="b")[::2] +128

            line.set_ydata(data_np)
            fig.canvas.draw()
            fig.canvas.flush_events()

        #time.sleep(2)
        print("the Recording has ended")
        stream.stop_stream()
        stream.close()
        pa.terminate()

        recording = wave.open(f"{rec_name}.wav", "wb")
        recording.setnchannels(channels)
        recording.setsampwidth(pa.get_sample_size(format))
        recording.setframerate(rate)
        recording.writeframes(b"".join(frames))
        recording.close()

        file = wave.open(f"{rec_name}.wav", "rb")


        sample_freq = file.getframerate()
        frames = file.getnframes()
        signal_wave = file.readframes(-1)
        
        file.close()

        t = frames / sample_freq

        #If using 1 channel int16 if its stereo int32
        audio_array = np.frombuffer(signal_wave, dtype=np.int16)

        times = np.linspace(0, t, num=frames)


        data, sr = librosa.load(f"{rec_name}.wav")
        x = librosa.stft(data)
        xdb = librosa.amplitude_to_db(abs(x))

        fig, axs = plt.subplots(2,figsize=(10, 10))
        fig.suptitle("Wave and Spectogram", fontweight="bold", size=20)


        librosa.display.waveshow(data, sr=sr, ax=axs[0])
        librosa.display.specshow(xdb, sr=sr, x_axis="time", y_axis="hz", ax=axs[1])


        plt.savefig(f"{rec_name}.png")


        return file

record()