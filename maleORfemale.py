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
WAV_AMOUNT = ['%.3d'%i for i in range(92)]



class Decide:
    def __init__(self, filename, male_Hz=100, female_Hz=200):
        self.read(filename)
        #print(self.sampling_rate)
        self.male_Hz, self.female_Hz = male_Hz, female_Hz
        self.compute()
        print(self.result)
        print(min(self.data), max(self.data))

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

    @safe_read
    def read_scipy(self, filename):
        '''uses scipy.io.wavfile to read the .wav file If it fails,
         the method from  audo module should be called.'''
        self.sampling_rate, self.data = scipy.io.wavfile.read(filename)

        return
    @safe_read
    def read_soundfile(self, filename):
        #print("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW")
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
        self.result = None

    def auto_corelation(self):
        pass



if __name__ == "__main__":
    '''A test to return effeciancy!'''
    for i in WAV_AMOUNT:
        file = "train_sox/"+i+"_K.wav"
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
