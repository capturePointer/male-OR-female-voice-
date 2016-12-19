#!/usr/bin/env python
# -*- coding: utf -*-
from __future__ import division
from scipy import *
import os.path
from maleORfemale import Decide
from os import system
import sys

WAV_AMOUNT = ['%.3d' % i for i in range(92)]

def Test(male_Hz, female_Hz):

    mg, mb, fg, fb = 0, 0, 0, 0
    for i in WAV_AMOUNT:
        file = "train_sox/" + i + "_K.wav"
        if os.path.exists(file):
            #print(file)
            obj = Decide(file, male_Hz, female_Hz)
            result = obj.compute()
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
                result = obj.compute()
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

def n_square_cross_corelation_finder(precision):
    best_Hz = ((None, None))
    best_score = 0
    for male_Hz in range(60, 240, precision):
        for female_Hz in range(140, 500, precision):
            population = Test(male_Hz, female_Hz)
            if population > best_score:
                print('\n', male_Hz, "Hz &", female_Hz, "Hz >", best_Hz[0], "Hz &", best_Hz[1], "Hz  by ",
                      '%.5f' % (population - best_score), "p\n")
                best_Hz = ((male_Hz, female_Hz))
                best_score = population

    print(best_Hz, best_score)
    return (best_Hz, best_score)

def FindBestHz_cross_corelation(_range, foo):

    def generate_raw_vector(_range, foo):
        vector = []
        for i in WAV_AMOUNT:
            file = "train_sox/" + i + "_K.wav"
            if os.path.exists(file):
                obj = Decide(file)
                vector.append(['K'])
                d = {}  # or d = dict()
                for Hz in _range:
                    d[Hz] = obj.cross_corelation_raw_score(Hz, foo)
                vector[-1].append(d)
            else:
                list_ = list(file)
                list_[-5] = 'M'
                file = "".join(list_)
                if os.path.exists(file):
                    obj = Decide(file)
                    vector.append(['M'])
                    d = {}
                    for Hz in _range:
                        d[Hz] = obj.cross_corelation_raw_score(Hz, foo)
                    vector[-1].append(d)

            print("\r", "%.2f%%" % (int(i) / len(WAV_AMOUNT)), end="")
        return vector

    def get_point(silce, male_Hz, female_Hz):
        sex, dict = silce
        if not(male_Hz in dict and female_Hz in dict):
            raise Exception("There is no key such as "+str(male_Hz)+"or"+str(female_Hz))
        if sex == 'M':
            return dict[male_Hz] > dict[female_Hz]
        elif sex == 'K':
            return dict[male_Hz] <= dict[female_Hz] # in favour of finding woman :3
        else:
            raise Exception("No such sex as"+sex)

    vector = generate_raw_vector(_range, foo)
    print("\rphase one finished")

    best_score = 0
    wins_log = []
    for male_Hz in _range:
        for female_Hz in _range:
            score = 0
            for file in vector:
                score += get_point(file, male_Hz, female_Hz)
            if score >= best_score:
                best_score = score
                best_Hz = (male_Hz, female_Hz)
                elem_num = len(vector)
                print("Congratulations! ", best_Hz, "got score of ", '%.3f%%' % (100*(score/elem_num)))
                wins_log.append((best_score, best_Hz))
            elif abs(score - best_score) < 3:
                print("might be good ", (male_Hz, female_Hz), "with score of ", '%.3f%%' % (100 * (score / len(vector))))
                #pass
                #print(male_Hz,female_Hz," has  %.3f%%" % 100*(score/elem_num))
    print("We Have a winner! ", best_Hz, "got score of ", '%.3f%%' % (100 * best_score / len(vector)))
    return wins_log


if __name__ == "__main__":
    FindBestHz_cross_corelation(range(40, 500), average)
    input()