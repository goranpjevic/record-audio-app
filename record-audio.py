#!/usr/bin/env python3

import argparse

from datetime import datetime
import pyaudio
import wave

from scipy.io.wavfile import read
import numpy as np
from numpy.fft import fft
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib import gridspec

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

def visualize(filename, sin_frequency, window_length, overlap):
    frame_rate, audio_read = read(filename)
    time_interval = np.arange(0,audio_read.size/frame_rate,1/frame_rate)

    audio_dft = fft(audio_read)
    freq = np.arange(0, frame_rate, frame_rate/len(audio_dft))

    sinusoid = np.sin(2*np.pi*sin_frequency*time_interval)
    scalar_product = np.dot(audio_read, sinusoid)

    plt.rcParams["figure.figsize"] = [15, 8]
    plt.rcParams["figure.autolayout"] = True
    figure = plt.figure()
    gs = gridspec.GridSpec(4, 2, height_ratios=[5, 5, 1, 1])

    plt.subplot(gs[0,0]).plot(time_interval, audio_read)
    plt.subplot(gs[0,0]).set_title("input sound")
    plt.subplot(gs[0,0]).set_ylabel("amplitude")
    plt.subplot(gs[0,0]).set_xlabel("time [s]")

    plt.subplot(gs[1,0]).plot(freq, np.abs(audio_dft))
    plt.subplot(gs[1,0]).set_title("dft(input sound)")
    plt.subplot(gs[1,0]).set_ylabel("fft amplitude |x(freq)|")
    plt.subplot(gs[1,0]).set_xlabel("frequency [Hz]")

    sin_line, = plt.subplot(gs[0,1]).plot(time_interval, sinusoid)
    plt.subplot(gs[0,1]).set_title("sinusoid with frequency " + str(sin_frequency) + " Hz\n"
            "scalar product with input sound = " + str(scalar_product))
    plt.subplot(gs[0,1]).set_ylabel("amplitude")
    plt.subplot(gs[0,1]).set_xlabel("time [s]")

    plt.subplot(gs[1,1]).specgram(audio_read, NFFT=int(window_length*frame_rate), Fs=frame_rate, noverlap=int(overlap*window_length*frame_rate))
    plt.subplot(gs[1,1]).set_title("stdft(input sound)")
    plt.subplot(gs[1,1]).set_xlabel("time [s]")
    plt.subplot(gs[1,1]).set_ylabel("frequency [Hz]")

    def update_spectrogram(val):
        window_length = window_length_slider.val
        overlap = overlap_slider.val
        plt.subplot(gs[1,1]).specgram(audio_read, NFFT=int(window_length*frame_rate), Fs=frame_rate, noverlap=int(overlap*window_length*frame_rate))
        figure.canvas.draw_idle()

    def update_sinusoid(val):
        sinusoid = np.sin(2*np.pi*freq_slider.val*time_interval)
        scalar_product = np.dot(audio_read, sinusoid)
        sin_line.set_ydata(sinusoid)
        plt.subplot(gs[0,1]).set_title("sinusoid with frequency " + str(freq_slider.val) + " Hz\n"
            "scalar product with input sound = " + str(scalar_product))

    window_length_slider = Slider(
        ax=plt.subplot(gs[2,0]),
        label="stdft window length [s]",
        valmin=0.1,
        valmax=audio_read.size/frame_rate,
        valinit=window_length,
    )
    overlap_slider = Slider(
        ax=plt.subplot(gs[2,1]),
        label="stdft window overlap",
        valmin=0,
        valmax=0.99,
        valinit=overlap,
    )
    freq_slider = Slider(
        ax=plt.subplot(gs[3,:]),
        label="sinusoid frequency [Hz]",
        valmin=1,
        valmax=frame_rate/2,
        valinit=sin_frequency,
    )
    window_length_slider.on_changed(update_spectrogram)
    overlap_slider.on_changed(update_spectrogram)
    freq_slider.on_changed(update_sinusoid)

    plt.show()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--record", help="record audio and save it to a file", type=str)
    parser.add_argument("-d", "--duration", help="duration of the recording in seconds", default=5, type=float)
    parser.add_argument("-v", "--visualize", help="visualize audio file", type=str)
    parser.add_argument("-s", "--sin-frequency", help="frequency of the sinusoid", default=1, type=float)
    parser.add_argument("-w", "--window-length", help="window length in seconds for the stdft", default=0.1, type=float)
    parser.add_argument("-o", "--overlap", help="window proportion overlap for the stdft", default=0, type=float)
    args = parser.parse_args()
    if (args.record != None):
        record(args.record, args.duration)
    elif (args.visualize != None):
        visualize(args.visualize, args.sin_frequency, args.window_length, args.overlap)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
