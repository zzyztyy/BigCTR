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
import seaborn as sns

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
    lt = (float(a[3]) + float(a[2]) / 15.) % 24
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
    return startline + lenth1 + lenth2 + 4, chalist, roclist, lt

#GPS0 yy1 mm2 dd3 hh4 mm5 ss6 radius7 lat8 lon9 den10 (Temperature)
# ut0 lt1 Vpm2 lgN3 Diplat4 glat5 glon6
def draw(cha, roc, lt):
    plt.figure(figsize=[10, 10], dpi=300)
    plt.subplots_adjust(hspace=0.1, left=0.1, bottom=0.05, right=0.97, top=0.97)
    den = []
    lat = []
    lgN = []
    Vpm = []
    latr = []
    dltr = []
    dltc = []
    for i in range(len(cha)):
        a = cha[i].split()
        den.append(np.log10(float(a[10])))
        lat.append(float(a[8]))
        loctime = (float(a[4]) + float(a[5]) / 60 + float(a[6]) / 3600 + (float(a[9]) - 72) / 15.) % 24
        # print(lt, loctime)
        dltc.append(np.median([-1, loctime - lt, 1]))
    for i in range(len(roc)):
        b = roc[i].split()
        dlt = min(abs(float(b[1]) - lt), abs(float(b[1]) - lt + 24), abs(float(b[1]) - lt - 24))
        if dlt < 1:
            latr.append(float(b[4]))
            lgN.append(float(b[3]))
            Vpm.append(float(b[2]))
            dltr.append(np.median([-1, float(b[1]) - lt, 1]))
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
    if len(Vpm) > 60:
        Vpm2 = bf.smooth(Vpm, 60)
    else:
        Vpm2 = Vpm
    # if len(lgN)
    # lgN2 = bf.smooth(lgN, 10)
    plt.subplot(3, 1, 1)
    plt.scatter(latr, lgN, s=1, c=dltr, cmap='brg', vmax=1, vmin=-1)
    plt.plot(latr, lgN, linewidth=1)
    # plt.axis([-50, 50, 3, 9])
    plt.xlim(-20, 20)
    plt.ylim(4.5, 6.5)
    plt.subplot(3, 1, 2)
    plt.scatter(latr, Vpm, s=1, c=dltr, cmap='brg', vmax=1, vmin=-1)
    plt.plot(latr, Vpm2, linewidth=1)
    # plt.axis([-50, 50, -150, 150])
    plt.xlim(-20, 20)
    plt.ylim(-75, 75)
    plt.subplot(3, 1, 3)
    plt.scatter(lat, den, s=15, c=dltc, cmap='brg', vmax=1, vmin=-1)
    plt.plot(lat, den, linewidth=1)
    plt.axis([-20, 20, 3.5, 7])
    # plt.show()

def daydraw(name):
    # path = 'mergedOrbqd\\'
    # name = '20011122.txt'
    data = readfile(name)
    nextline = 0
    temp = 0
    while nextline < len(data):
        nextline, cha, roc, lt = getoneorb(data, nextline)
        # print(temp)
        if len(cha) > 80 and len(roc) > 64:
            a = cha[0].split()
            year = a[1]
            month = a[2]
            day = a[3]
            # lt = (float(a[4])+float(a[5])/60+float(a[6])/3600+(float(a[9])-72)/15.)%24
            draw(cha, roc, lt)
            temp = temp + 1
            plt.subplot(3, 1, 1)
            title = 'LT=' + format(lt, '.2f') + ' ' + year + '_' + month + '_' + day + '_' + str(temp)
            plt.title(title)
            plt.savefig('mergedpic\\' + title + '.png')
            # plt.show()
            plt.close()


def daystatic(choselt):
    # files = os.listdir('mergedOrbqd')
    ctr = []
    vpm = []
    pbw = []
    alllt = []
    # for file in files:
    #     path = 'mergedOrbqd\\'
        # name = '20011122.txt'
    data = readfile('merged15_1qd.txt')
    nextline = 0
    while nextline < len(data):
        nextline, cha, roc, lt = getoneorb(data, nextline)
        year = float(cha[1].split()[1])
        if len(roc) > 64 and len(cha) > 80 and year < 2004.5:
            a = cha[int(len(cha) / 2)].split()
            # lt = (float(a[4]) + float(a[5]) / 60 + float(a[6]) / 3600 + (float(a[9]) - 72) / 15.) % 24
            actr = np.log10(getCTR(cha))
            avpm = getVpm(roc, lt)
            apbw = np.log10(getPBwidth(roc, lt))
            if avpm < 1000 and apbw < 2:
                alllt.append(lt)
                ctr.append(np.log10(getCTR(cha)))
                vpm.append(getVpm(roc, lt))
                pbw.append(np.log10(getPBwidth(roc, lt)))
                # plt.scatter(ctr, vpm, c=alllt, cmap='Dark2', s=3, vmax=24, vmin=16)
                # sns.jointplot(np.array(ctr), np.array(vpm), kind='reg')
                # plt.ylim(-50, 50)
                # plt.xlim(-1, 4)
                # plt.title('lgCTR-Vpm')
                # plt.colorbar()
                # plt.show()
                # plt.savefig('lgCTR-Vpm1 '+str(choselt)+'.png')
                # plt.scatter(ctr, pbw, c=alllt, cmap='Dark2', s=3, vmax=24, vmin=16)
                # sns.jointplot(np.array(ctr), np.array(pbw), kind='reg')
                # plt.ylim(-3, -1)
                # plt.xlim(-1, 4)
                # plt.title('lgCTR-lgPBW')
                # plt.colorbar()
                # plt.show()
                # plt.savefig('lgCTR-lgPBW1 '+str(choselt)+'.png')

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
    ctr = (np.array(soupeak).max() + np.array(norpeak).max()) / (2 * np.array(valley).min())
    # ctr = 1./np.array(valley).mean()
    return ctr


def getVpm(roc, lt):
    Vpm = []
    for i in range(len(roc)):
        a = roc[i].split()
        lat = float(a[4])
        ltr = float(a[1])
        if lat > -20 and lat < 20 and abs(ltr - lt) < 0.5:
            Vpm.append(float(a[2]))
    if len(Vpm) < 10:
        return 1000
    return np.median(Vpm)


def getPBwidth(roc, lt):
    lgN = []
    latr = []
    for i in range(len(roc)):
        a = roc[i].split()
        lat = float(a[4])
        ltr = float(a[1])
        dlt = min(abs(ltr - lt), abs(ltr - lt + 24), abs(ltr - lt - 24))
        # print(lat, ltr, a[0], a[6])
        if lat > -20 and lat < 20 and dlt < 0.5:
            # print('init')
            lgN.append(float(a[3]))
            latr.append(lat)
    bf.sort2(lgN, latr)
    bf.sort2(latr, latr)
    # rhs = np.array(latr).min()
    # lhs = np.array(latr).max()
    # lat2 = np.linspace(rhs, lhs, int((lhs - rhs) / 0.05))
    # lgNfun = interp1d(latr, lgN)
    # lgN2 = []
    # for i in range(len(lat2)):
    #     lgN2.append(lgNfun(lat2[i]))
    if len(lgN) > 10:
        lgN3 = bf.smooth(lgN, 10)
        dlgN = np.array(lgN3) - np.array(lgN)
    else:
        dlgN = np.zeros(len(lgN))
        return 100
    temp = 1
    sigmaup = np.sqrt(bf.smooth(dlgN * dlgN, 10))
    for i in range(len(dlgN)):
        sigma = sigmaup[i] / lgN3[i]
        # print(sigma)
        if sigma > 0.003:
            temp = temp + sigma
    print(temp)
    return temp / len(lgN)


def drawtogether(choselt):
    data = readfile('merged15_1qd.txt')
    nextline = 0
    temp = 0
    plt.figure(figsize=[10, 10], dpi=300)
    plt.subplots_adjust(hspace=0.1, left=0.1, bottom=0.05, right=0.97, top=0.97)
    while nextline < len(data):
        nextline, cha, roc, lt = getoneorb(data, nextline)
        if len(cha) > 80 and len(roc) > 64 and lt > choselt and lt < choselt + 0.5:
            draw(cha, roc, lt)
            temp = temp + 1
    plt.subplot(3, 1, 1)
    title = 'LT=' + str(choselt)
    plt.title(title)
    plt.savefig(title + '.png')
    # plt.savefig('mergedpic\\' + title + '.png')
    # plt.show()
    plt.close()

if __name__ == '__main__':
    # files = os.listdir('mergedOrbqd')
    # for file in files:
    #     try:
    daydraw('merged15_1qd.txt')
    # except:
    #     print(file)
    # for i in range(17, 23):
    # lt = 17.0
    # while lt < 22.9:
    #     drawtogether(lt)
    #     lt = lt + 0.5
        # plt.savefig('a.png')
