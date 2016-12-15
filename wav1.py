#!/usr/bin/env python
# -*- coding: utf -*-
from __future__ import division
from pylab import *
from numpy import *
from scipy import *
import scipy.io.wavfile as wav

WAV_URL = "http://www.cs.put.poznan.pl/wjaskowski/pub/teaching/kck/fft/err.wav"
WAV_FILE = "err.wav"

def draw_plot(array, where=211, opis_xlabel="czas", opis_ylabel="czestotliwosc"):
    subplot(where)
    b = max(array)
    a = min(array)
    length = len(array)
    plot(range(length), array, '*')
    xlim([0, length])
    #ylim([a, b])
    yscale('log')
    xlabel(opis_xlabel)
    ylabel(opis_ylabel)
    #show()

if __name__ == "__main__":
    w,signal = wav.read(WAV_FILE)
    signal = [s[0] for s in signal] # pierwszy kanał to s[0]
    signal = signal[::10]
    draw_plot(signal)

    #subplot(211)
    #array = show_spots(SPOTS)
    subplot(212)
    #show_spectrum(array)
    show()