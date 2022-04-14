#!/usr/bin/env python3

import argparse

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
    freq = np.arange(0, frame_rate, frame_rate/len(audio_dft))

    figure, axis = plt.subplots(2)
    axis[0].plot(time_interval, audio_read)
    axis[0].set_title("input sound")
    axis[0].set_ylabel("amplitude")
    axis[0].set_xlabel("time [s]")
    axis[1].plot(freq, np.abs(audio_dft))
    axis[1].set_title("dft(input sound)")
    axis[1].set_ylabel("fft amplitude |x(freq)|")
    axis[1].set_xlabel("frequency [Hz]")
    plt.show()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--record", help="record audio and save it to a file", type=str)
    parser.add_argument("-d", "--duration", help="duration of the recording in seconds", type=float)
    parser.add_argument("-v", "--visualize", help="visualize audio file", type=str)
    args = parser.parse_args()
    if (args.record != None and args.duration != None):
        record(args.record, args.duration)
    elif (args.visualize != None):
        visualize(args.visualize)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
