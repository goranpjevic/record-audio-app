#!/usr/bin/env python3

import sys

from datetime import datetime
import pyaudio
import wave

from scipy.io.wavfile import read
import numpy as np
from numpy.fft import fft
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
    frame_rate = input_data[0]
    audio_read = input_data[1]
    time_interval = np.arange(0,audio_read.size/frame_rate,1/frame_rate)

    audio_dft = fft(audio_read)
    N = len(audio_dft)
    n = np.arange(N)
    T = N/frame_rate
    freq = n/T

    figure, axis = plt.subplots(2)
    axis[0].plot(time_interval, audio_read)
    axis[0].set_ylabel("amplitude")
    axis[0].set_xlabel("time [s]")
    axis[1].stem(freq, np.abs(audio_dft), linefmt='b', markerfmt=" ", basefmt="-b")
    #axis[1].plot(audio_dft)
    axis[1].set_ylabel("fft amplitude |x(freq)|")
    axis[1].set_xlabel("frequency [Hz]")
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
