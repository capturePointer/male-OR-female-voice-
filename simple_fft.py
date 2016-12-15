#!/usr/bin/env python
# -*- coding: utf -*-
from __future__ import division
from pylab import *
from numpy import *
from scipy import *

w = 21          # częstotliwość próbkowania [Hz]
T = 1            # rozważany okres [s]

n = T * w        # liczba próbek
#n = 10
t = linspace(0, T, n, endpoint=False) # punkty na osi OX [s]

f = lambda t : sin(2*pi*t) + sin(4*pi*t)    # def. funkcji
x = random.random(10)
signal = f(t)                 # funkcja spróbkowana
#signal = x

print(signal)

subplot(211)
plot(t, signal, '*')

signal1 = fft(signal)
signal1 = abs(signal1)        # moduł

subplot(212)
freqs = linspace(0, w, n, endpoint=False)              # <-- ZACZNIJ TUTAJ. Użyj linspace
#freqs = range(n)
print(max(signal1))
stem(freqs, signal1, '-*')
xlabel("czestotliwość")
ylabel("spektrum")


show()