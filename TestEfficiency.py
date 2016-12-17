#!/usr/bin/env python
# -*- coding: utf -*-
from __future__ import division
from scipy import *
import os.path
from maleORfemale import Decide

WAV_AMOUNT = ['%.3d' % i for i in range(92)]

def Test(male_Hz, female_Hz):

    mg, mb, fg, fb = 0, 0, 0, 0
    for i in WAV_AMOUNT:
        file = "train_sox/" + i + "_K.wav"
        if os.path.exists(file):
            #print(file)
            obj = Decide(file, male_Hz, female_Hz)
            result = obj.get_result()
            if result == 'K':
                fg +=1
            else:
                fb +=1
        else:
            list_ = list(file)
            list_[-5] = 'M'
            file = "".join(list_)
            if os.path.exists(file):
                #print(file)
                obj = Decide(file, male_Hz, female_Hz)
                result = obj.get_result()
                if result == 'M':
                    mg += 1
                else:
                    mb += 1
            else:
                pass
                #print("failed to find file " + file)
    overall_efficiency = (100 * (mg+fg) / (mg+fg+fb+mb))
    male_efficiency = (100 * mg / (mg + mb))
    female_efficiency = (100 * fg / (fg + fb))
    print()
    print(male_Hz,'Hz',female_Hz,'Hz')
    print('Overall efficiency: ', '%.2f' % overall_efficiency,'\nM: ', '%.2f' % male_efficiency,'\nF: ', '%.2f' % female_efficiency)
    return overall_efficiency

if __name__ == "__main__":
    best_Hz = ((None, None))
    best_score = 0
    for male_Hz in range(60, 240, 5):
        for female_Hz in range(140, 500, 5):
            population = Test(male_Hz, female_Hz)
            if population > best_score:
                print('\n',male_Hz, "Hz &", female_Hz, "Hz >", best_Hz[0], "Hz &", best_Hz[1], "Hz  by ", '%.7f' % (population - best_score), "p\n")
                best_Hz = ((male_Hz, female_Hz))
                best_score = population

    print(best_Hz, best_score)