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
    print(a)
    lenth1 = int(a[1])
    b = text[startline + lenth1 + 2].split()
    print(b)
    lenth2 = int(b[1])
    for i in range(startline + 2, startline + lenth1 + 2):
        # print(text[i])
        chalist.append(text[i])
    for i in range(startline + lenth1 + 4, startline + lenth1 + lenth2 + 4):
        roclist.append(text[i])
        # print(text[i])
    return startline + lenth1 + lenth2 + 4, chalist, roclist

#GPS0 yy1 mm2 dd3 hh4 mm5 ss6 radius7 lat8 lon9 den10 (Temperature)
# UT0 LT1 VperM2 LogN3 DipLat4
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
        latr.append(float(b[4]))
        lgN.append(float(b[3]))
        Vpm.append(float(b[2]))
    bf.sort2(lgN, latr)
    bf.sort2(Vpm, latr)
    bf.sort2(latr, latr)
    # rhs = np.array(latr).min()
    # lhs = np.array(latr).max()
    # lat2 = np.linspace(rhs, lhs, int((lhs-rhs)/0.05))
    # Vpmfun = interp1d(latr, Vpm)
    # lgNfun = interp1d(latr, lgN)
    # Vpm2 = []
    # lgN2 = []
    # for i in range(len(latr)):
    #     Vpm2.append(Vpmfun(lat2[i]))
    #     lgN2.append(lgNfun(lat2[i]))
    Vpm2 = bf.smooth(Vpm, 60)
    lgN2 = bf.smooth(lgN, 60)
    plt.subplot(3, 1, 1)
    plt.scatter(latr, lgN, s=0.1, c='k')
    plt.plot(latr, lgN2, linewidth=1, c='r')
    # plt.axis([-50, 50, 3, 9])
    plt.xlim(-20, 20)
    plt.ylim(4.5, 6.5)
    plt.subplot(3, 1, 2)
    plt.scatter(latr, Vpm, s=0.1, c='k')
    plt.plot(latr, Vpm2, linewidth=1, c='r')
    # plt.axis([-50, 50, -150, 150])
    plt.xlim(-20, 20)
    plt.ylim(-75, 75)
    plt.subplot(3, 1, 3)
    plt.scatter(lat, den, s=1, c='k')
    plt.plot(lat, den, linewidth=1, c='r')
    plt.axis([-20, 20, 3.5, 7])
    # plt.show()

def daydraw(name):
    # path = 'mergedOrbqd\\'
    # name = '20011122.txt'
    data = readfile(name)
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
    pbw = []
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
            pbw.append(np.log10(getPBwidth(roc)))
    plt.scatter(ctr, vpm, c=alllt, cmap='brg', s=2, vmax=23, vmin=17)
    plt.title('lgCTR-Vpm')
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
    # ctr = 1./np.array(valley).mean()
    return max(ctr, 1)

def getVpm(roc):
    Vpm = []
    for i in range(len(roc)):
        a = roc[i].split()
        lat = float(a[0])
        if lat > -10 and lat < 10:
            Vpm.append(float(a[4]))
    return np.array(Vpm).mean()


def getPBwidth(roc):
    lgN = []
    latr = []
    for i in range(len(roc)):
        a = roc[i].split()
        lat = float(a[0])
        if lat > -20 and lat < 20:
            lgN.append(float(a[3]))
            latr.append(lat)
    bf.sort2(lgN, latr)
    bf.sort2(latr, latr)
    rhs = np.array(latr).min()
    lhs = np.array(latr).max()
    lat2 = np.linspace(rhs, lhs, int((lhs - rhs) / 0.05))
    lgNfun = interp1d(latr, lgN)
    lgN2 = []
    for i in range(len(lat2)):
        lgN2.append(lgNfun(lat2[i]))
    lgN3 = bf.smooth(lgN2, 60)
    if len(lgN2) > 60:
        dlgN = np.array(lgN3) - np.array(lgN2)
    else:
        dlgN = np.ones(len(lgN2))
    temp = 0
    for i in range(len(dlgN)):
        # if abs(dlgN[i]) > 0.2:
        temp = temp + abs(dlgN[i])
    return temp / len(latr)



if __name__ == '__main__':
    # files = os.listdir('mergedOrbqd')
    # for file in files:
    #     try:
    # daydraw('mergedqd.txt')
    #     except:
    #         print(file)
    daystatic()
