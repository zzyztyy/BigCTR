#!/usr/bin/env python
# -*- coding: cp936 -*-
import numpy as np
import matplotlib.pyplot as plt
import string
import scipy.fftpack as scf
import math
import scipy.signal as ssg
from scipy.interpolate import interp1d
import datetime

# 从原始数据中寻找轨道，并输出
def readfile():
    line = []
    num = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10"]
    for i in range(0, 10):
        f = open("D:\\data&pic\\sort_season_earthmag\\"+num[i]+"_win_low.txt")
        line =line + f.readlines()
        f.close()
    return line

def search_orbit(text, temp):
    length = len(text)
    orbit = list()
    nmag = magline(True)
    smag = magline(False)
    # print(text)
    for i in range(temp, int(length)):
        # a = (str(text[2*i])+str(text[2*i+1])).split()
        a = (text[i]).split()
        try:
            if float(a[8]) > smag(float(a[9])) and float(a[8]) < nmag(float(a[9])):
                for j in range(11):
                    a[j] = float(a[j])
                orbit.append(a)
            elif len(orbit) > 80 and len(orbit) < 120:
                # print("get it")
                if float(a[8]) < 0.:
                    orbit.reverse()
                # print(orbit[50])
                orbit.append(i)
                return orbit
            elif len(orbit) > 120:
                orbit.clear()
                # print("too long")
            elif len(orbit) < 80 and len(orbit) > 0:
                # print(len(orbit))
                orbit.clear()
                # print("too short")
        except:
            # p=0
            print(2)
            print(a)
    orbit.clear()
    #orbit.append("end of file")
    return orbit

def draw_lat_den(orbit):
    lat = list()
    den = list()
    for i in range(len(orbit)-1):
        a = orbit[i]
        lat.append(a[8])
        den.append(a[10])
    p = plt.plot(lat, den, c='k', linewidth=1)
    p = plt.plot(lat, ssg.savgol_filter(den, 15, 2, 0), c='r', linewidth=1)
    #mean = sum(den)/len(den)+np.arange(len(den))*0
    mid = np.percentile(den, 67)+np.arange(len(den))*0#np.median(den) + np.arange(len(den))*0
    p = plt.plot(lat, mid, c='b')
    #p = plt.plot(lat, mean, c='g')
    plt.title(str(int(a[1]))+'/'+str(int(a[2]))+'/'+str(int(a[3]))+" lon="+str(a[9])+\
              " LT="+str(int(a[4]+a[5]/60.+a[6]/3600.+a[9]/15.)%24)+"h")
    #plt.savefig("D:\\pic1\\a"+str(a)+".png")
    #plt.close()
    plt.axis([-50, 50, 0, 4000000])
    plt.show()
    return p

def get_peak(orbit):
    lat = list()
    den = list()
    for i in range(len(orbit)-1):
        a = orbit[i]
        lat.append(a[8])
        den.append(a[10])
    sgden = ssg.savgol_filter(den, 15, 2, 0)
    mean = sum(den) / len(den)
    mid = np.percentile(den, 67)#np.median(den)
    step = []
    if sgden[0] < mid and sgden[len(sgden) - 1] < mid:
        for i in range(2, len(sgden)-2):
            if sgden[i-1] < sgden[i] and sgden[i+1] <= sgden[i] and sgden[i] > mid:
                temp = i
                for j in range(-2, 3):
                    if den[temp] < den[temp+j]:
                        temp = temp+j
                step.append(temp)
    outpeak = []#numpeak year DOY time high lt lat lon den
    r = 0
    if len(step) == 2:
        temp = step[0]
        for i in range(step[0], step[1]):
            if den[temp] > den[i]:
                temp = i
        r = temp

    step2 = []
    if len(step) == 1:
        step2.append(step[0])
    elif len(step) == 2:
        step2.append(step[0])
        step2.append(r)
        step2.append(step[1])
    else:
        step2.append(int(len(orbit)/2))

    for i in range(len(step2)):
        outpeak.append(len(step))
        outpeak.append(int(orbit[step2[i]][1]))
        outpeak.append(datetime.date(int(orbit[step2[i]][1]), int(orbit[step2[i]][2]),\
                                 int(orbit[step2[i]][3])).timetuple()[7])
        outpeak.append(orbit[step2[i]][4]+orbit[step2[i]][5]/60.+orbit[step2[i]][6]/3600.)
        outpeak.append(orbit[step2[i]][7])
        LT = (orbit[step2[i]][4] + orbit[step2[i]][5] / 60. \
                + orbit[step2[i]][6] / 3600. + orbit[step2[i]][9] / 15.) % 24
        outpeak.append(LT)
        outpeak.append(orbit[step2[i]][8])
        outpeak.append(orbit[step2[i]][9])
        outpeak.append(orbit[step2[i]][10])
    #print(outpeak)
    return outpeak

def magline( ns):#input longitude output 40 maglat
    #type of ns is bool,north=true
    if ns:
        f = open("50maglatline.txt", 'r')
    else:
        f = open("-50maglatline.txt", 'r')
    ml = f.readlines()
    y = []
    x = []
    for i in range(len(ml)):
        a = ml[i].split()
        y.append(float(a[0]))
        x.append(float(a[1]))
    z = interp1d(x, y, kind='cubic')
    return z

if __name__ == "__main__":
    alltext = open("D:\\data&pic\\CH-ME-2-PLP+2002-04-01_2.dat").readlines()
    state = 0
    orb = list()
    while state < len(alltext):
        #print(state)
        orb = search_orbit(alltext, state)
        if len(orb) > 1:
            state = int(float(orb[len(orb)-1]))
        else:
            print(orb)
            break
        a = get_peak(orb)
        peaknum = a[0]

        try:
            print(a[1])
            print(a[2])
            a = str(a)
            a = a.replace("[", "")
            a = a.replace("]", "")
            a = a.replace(",", "")
            draw_lat_den(orb)
        except:
            print(1)
            print(a)
