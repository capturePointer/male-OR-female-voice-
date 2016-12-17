#!/usr/bin/env python
# -*- coding: utf -*-
from __future__ import division
from pylab import *
from numpy import *
from scipy import *
import scipy.io.wavfile
from functools import wraps
import soundfile
import os.path

# DO A WRAPPER FOR wav.read to use audio.read if the first fails!
WAV_AMOUNT = ['%.3d' % i for i in range(92)]


class Decide:
    def __init__(self, filename, male_Hz=100, female_Hz=200):
        self.read(filename)
        # print(self.sampling_rate)
        self.male_Hz, self.female_Hz = male_Hz, female_Hz
        self.generate_sex_sin()

        self.compute()
        #print(self.result)
        #print(min(self.data), max(self.data))

    def get_result(self):
        return self.result

    def compute(self):
        functions = self.get_functions()

        probs = [f() for f in functions]
        self.decide(probs)

    def trim_to_channel0(self):
        '''trims the output of safe_read to one channel only'''

        if hasattr(self.data[0], '__iter__'):
            self.data = [data[0] for data in self.data]

    def safe_read(f):
        '''Thanks to: https://docs.python.org/2/library/functools.html'''

        @wraps(f)
        def wrapper(self, *args, **kwargs):
            try:
                f(self, *args, **kwargs)
                self.trim_to_channel0()
                return
            except:
                print(f.__name__, "() Couldnt load file ", args[-1])
                self.read_scipy(*args, **kwargs)
                self.trim_to_channel0()
                return

        return wrapper

    def read_scipy(self, filename):
        '''uses scipy.io.wavfile to read the .wav file If it fails,
         the method from  audo module should be called.'''
        self.sampling_rate, self.data = scipy.io.wavfile.read(filename)

        return

    @safe_read
    def read_soundfile(self, filename):
        # print("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW")
        self.data, self.sampling_rate = soundfile.read(filename)
        return

    def read(self, filename):
        '''alias for read_soundfile'''
        return self.read_soundfile(filename)

    # TODO
    def get_functions(self):
        '''returns list of the functions used to decide about the voice'''
        list = [self.auto_corelation]
        return list

    # TODO
    def decide(self, probs):
        '''right now each method is counted as one point, to be changed!'''
        score = 0
        for probe in probs:
            if(probe[0] > probe[1]):
                score +=1
            else:
                score -=1
        if score > 0:
            self.result = 'M'
        else:
            self.result = 'K'

    # TODO
    def auto_corelation(self):
        male_correlation = max(correlate(self.male_sin, self.data))
        female_correlation = max(correlate(self.female_sin, self.data))
        #if(male_correlation > female_correlation):
        #    print("M")
        #else:
        #    print("K")
        #print(male_correlation, female_correlation)
        return ((male_correlation, female_correlation))
        pass

    def generate_sex_sin(self):
        self.male_sin = sin(linspace(0, 2 * pi, self.sampling_rate/self.male_Hz))
        self.female_sin = sin(linspace(0, 2 * pi, self.sampling_rate/self.female_Hz))


if __name__ == "__main__":
    '''A test to return efficiency!'''
    for i in WAV_AMOUNT:
        file = "train_sox/" + i + "_K.wav"
        if os.path.exists(file):
            print(file)
            Decide(file)
        else:
            list_ = list(file)
            list_[-5] = 'M'
            file = "".join(list_)
            if os.path.exists(file):
                print(file)
                Decide(file)
            else:
                print("failed to find file " + file)
