#!/usr/bin/env python
# -*- coding: cp936 -*-
import numpy as np
import matplotlib.pyplot as plt
import basicFun as bf
from champ3 import search_orbit
from scipy.interpolate import interp1d
from scipy.interpolate import spline
import datetime
import os

def readfile(filename):
    # print(type(filename))
    f = open(filename, 'r')
    text = f.readlines()
    f.close()
    return text

def getoneorb(text, startline):
    chalist = []
    roclist = []
    a = text[startline].split()
    # print(a)
    lenth1 = int(a[1])
    b = text[startline+lenth1+1].split()
    # print(b)
    lenth2 = int(b[1])
    for i in range(startline+2, startline+lenth1+1):
        chalist.append(text[i])
    for i in range(startline+lenth1+3, startline+lenth1+lenth2+3):
        roclist.append(text[i])
    return startline+lenth1+lenth2+3, chalist, roclist

#GPS0 yy1 mm2 dd3 hh4 mm5 ss6 radius7 lat8 lon9 den10 (Temperature)
#lat lon dlt lgN Vpm
def draw(cha, roc):
    plt.figure(figsize=[10, 10], dpi=300)
    plt.subplots_adjust(hspace=0.1, left=0.1, bottom=0.05, right=0.97, top=0.97)
    den = []
    lat = []
    lgN = []
    Vpm = []
    latr = []
    for i in range(len(cha)):
        a = cha[i].split()
        den.append(np.log10(float(a[10])))
        lat.append(float(a[8]))
    for i in range(len(roc)):
        b = roc[i].split()
        latr.append(float(b[0]))
        lgN.append(float(b[3]))
        Vpm.append(float(b[4]))
    bf.sort2(lgN, latr)
    bf.sort2(Vpm, latr)
    bf.sort2(latr, latr)
    rhs = np.array(latr).min()
    lhs = np.array(latr).max()
    lat2 = np.linspace(rhs, lhs, int((lhs-rhs)/0.05))
    Vpmfun = interp1d(latr, Vpm)
    lgNfun = interp1d(latr, lgN)
    Vpm2 = []
    lgN2 = []
    for i in range(len(lat2)):
        Vpm2.append(Vpmfun(lat2[i]))
        lgN2.append(lgNfun(lat2[i]))
    Vpm2 = bf.smooth(Vpm2, 60)
    lgN2 = bf.smooth(lgN2, 60)
    plt.subplot(3, 1, 1)
    plt.scatter(latr, lgN, s=0.1, c='k')
    plt.plot(lat2, lgN2, linewidth=1, c='r')
    # plt.axis([-50, 50, 3, 9])
    plt.xlim(-20, 20)
    plt.ylim(4.5, 6.5)
    plt.subplot(3, 1, 2)
    plt.scatter(latr, Vpm, s=0.1, c='k')
    plt.plot(lat2, Vpm2, linewidth=1, c='r')
    # plt.axis([-50, 50, -150, 150])
    plt.xlim(-20, 20)
    plt.ylim(-75, 75)
    plt.subplot(3, 1, 3)
    plt.scatter(lat, den, s=1, c='k')
    plt.plot(lat, den, linewidth=1, c='r')
    plt.axis([-20, 20, 3.5, 7])
    # plt.show()

def daydraw(name):
    path = 'mergedOrbqd\\'
    # name = '20011122.txt'
    data = readfile(path+name)
    nextline = 0
    temp = 0
    while nextline < len(data):
        nextline, cha, roc = getoneorb(data, nextline)
        # print(temp)
        draw(cha, roc)
        a = cha[int(len(cha)/2)].split()
        lt = (float(a[4])+float(a[5])/60+float(a[6])/3600+(float(a[9])-72)/15.)%24
        temp = temp+1
        plt.subplot(3, 1, 1)
        title = name[:-4]+'_'+str(temp)+' LT='+format(lt, '.2f')
        plt.title(title)
        plt.savefig('mergedpic\\'+title+'.png')
        # plt.show()
        plt.close()

def daystatic():
    files = os.listdir('mergedOrbqd')
    ctr = []
    vpm = []
    alllt = []
    for file in files:
        path = 'mergedOrbqd\\'
        # name = '20011122.txt'
        data = readfile(path + file)
        nextline = 0
        while nextline < len(data):
            nextline, cha, roc = getoneorb(data, nextline)
            a = cha[int(len(cha) / 2)].split()
            lt = (float(a[4]) + float(a[5]) / 60 + float(a[6]) / 3600 + (float(a[9]) - 72) / 15.) % 24
            alllt.append(lt)
            ctr.append(np.log10(getCTR(cha)))
            vpm.append(getVpm(roc))
    plt.scatter(ctr, vpm, c=alllt, cmap='brg', s=1)
    plt.colorbar()
    plt.show()

def getCTR(cha):
    norpeak = []
    soupeak = []
    valley = []
    for i in range(len(cha)):
        a = cha[i].split()
        lat = float(a[8])
        if lat <-10 and lat>-20:
            soupeak.append(float(a[10]))
        elif lat <5 and lat>-5:
            valley.append(float(a[10]))
        elif lat >10 and lat<20:
            norpeak.append(float(a[10]))
    ctr= (np.array(soupeak).mean()+np.array(norpeak).mean())/(2*np.array(valley).mean())
    return max(ctr, 1)

def getVpm(roc):
    Vpm = []
    for i in range(len(roc)):
        a = roc[i].split()
        lat = float(a[0])
        if lat >-5 and lat<5:
            Vpm.append(float(a[4]))
    return np.array(Vpm).mean()


if __name__ == '__main__':
    # files = os.listdir('mergedOrbqd')
    # for file in files:
    #     try:
    #         daydraw(file)
    #     except:
    #         print(file)
    daystatic()
