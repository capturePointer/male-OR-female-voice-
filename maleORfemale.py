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


WAV_AMOUNT = ['%.3d' % i for i in range(1,92)]


class Decide:
    def __init__(self, filename, male_Hz=127, female_Hz=213):
        self.read(filename)
        # print(self.sampling_rate)
        self.male_Hz, self.female_Hz = male_Hz, female_Hz
        self.generate_sex_sin()

        #print(self.result)
        #print(min(self.data), max(self.data))

    def get_result(self):
        return self.result

    def compute(self):
        functions = self.get_functions()

        probs = [f() for f in functions]
        self.decide(probs)
        return self.result

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

    def get_functions(self):
        '''returns list of the functions used to decide about the voice
        (if there were time to use multiple tests and decide based on them)'''
        list = [self.cross_corelation_abs_average]
        return list

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
    def cross_corelation_abs_average(self):
        male_correlation = average(abs_(correlate(self.male_sin, self.data)))
        female_correlation = average(abs_(correlate(self.female_sin, self.data)))
        return ((male_correlation, female_correlation))

    def generate_sex_sin(self):
        self.male_sin = sin(linspace(0, 2 * pi, self.sampling_rate/self.male_Hz))
        self.female_sin = sin(linspace(0, 2 * pi, self.sampling_rate/self.female_Hz))

    def cross_corelation_raw_score(self, Hz, foo):
        sinus = sin(linspace(0, 2 * pi, self.sampling_rate / Hz))
        return foo(abs_(correlate(sinus, self.data)))


def abs_(iterable):
    return [abs(i) for i in iterable]

if __name__ == "__main__":
    '''A test to return efficiency!'''
    for i in WAV_AMOUNT:
        file = "train_sox/" + i + "_K.wav"
        if os.path.exists(file):
            print(file)
            obj = Decide(file)
            print(obj.compute())
        else:
            list_ = list(file)
            list_[-5] = 'M'
            file = "".join(list_)
            if os.path.exists(file):
                print(file)
                obj = Decide(file)
                print(obj.compute())
            else:
                print("failed to find file " + file)
