#!/usr/bin/env python3

import sys

from datetime import datetime
import pyaudio
import wave

from scipy.io.wavfile import read
import matplotlib.pyplot as plt

def record(filename, duration):
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
    frames = []
    start_time = datetime.now()
    while (datetime.now() - start_time).total_seconds() < duration:
        data = stream.read(1024)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    audio.terminate()
    sound_file = wave.open(filename, "wb")
    sound_file.setnchannels(1)
    sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    sound_file.setframerate(44100)
    sound_file.writeframes(b''.join(frames))
    sound_file.close()

def visualize(filename):
    plt.rcParams["figure.figsize"] = [7.50, 3.50]
    plt.rcParams["figure.autolayout"] = True
    input_data = read(filename)
    audio_read = input_data[1]
    plt.plot(audio_read)
    plt.ylabel("Amplitude")
    plt.xlabel("Time")
    plt.show()

def main():
    if (len(sys.argv) < 2):
        print("no option specified")
    elif (sys.argv[1] == "r"):
        record(sys.argv[2], float(sys.argv[3]))
    elif (sys.argv[1] == "v"):
        visualize(sys.argv[2])
    else:
        print("invalid option")

if __name__ == "__main__":
    main()
