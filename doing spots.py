#!/usr/bin/env python
# -*- coding: utf -*-
from __future__ import division
from pylab import *
from numpy import *
from scipy import *

SPOTS = "http://www.cs.put.poznan.pl/wjaskowski/pub/teaching/kck/fft/spots.txt"

def show_spots(text):
    array = genfromtxt(text)
    b = max(array)
    a = min(array)
    plot(range(len(array)),array, '*')
    xlim([0,len(array)])
    ylim([0,max(array)])
    return array

def show_spectrum(array):
    signal = fft(array)
    signal = abs(signal)
    signal = signal[1:]
    stem(range(len(signal)), signal, '-*')
    xlim([0,len(array)])
    ylim([0,max(signal)])
    print(max(signal))
    for i, s in enumerate(signal):
        if s == max(signal):
            print(i+1)

if __name__ == "__main__":
    subplot(211)
    array = show_spots(SPOTS)
    subplot(212)
    show_spectrum(array)
    show()

