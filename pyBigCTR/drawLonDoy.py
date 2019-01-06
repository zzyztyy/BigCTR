import numpy as np
import matplotlib.pyplot as plt
import datetime

from bc3newMergeOrb import Orb
from bc4staticLT import getoneOrb
import basicFun as bf
from DrawChampProfile import get_curve_kind


def getOrbitList(fin, ):
    startline = 0
    chalist = []
    temp = 0
    while startline < len(fin):
        cha, nextline = getoneOrb(fin, startline)
        year = cha.date[:4]
        chose = True  # (year in ['2002'])
        if chose:
            temp = temp + 1
            if cha.name == 'CHAMP':
                chalist.append(cha)
            else:
                print(cha.name)
        startline = nextline
    static_season_lon(chalist)


def static_season_lon(chalist):
    flat = []
    deep = []
    bubble = []
    nosort = []
    for i in range(len(chalist)):
        cha = chalist[i]
        mlat0, den0 = cha.mlat_den()
        mlat, den = [], []
        for i in range(len(mlat0)):
            if -27 < mlat0[i] < 27:
                den.append(den0[i])
                mlat.append(mlat0[i])
        # ck, ctr = curveKindAndCtr(lat, den)
        if len(mlat) > 35:
            ck, ctr = get_curve_kind(mlat, den)
            days = bf.julday(cha.date)
            month = int(cha.date[4:6])
            lon = (cha.midlon + 180) % 360 - 180
            if ck == 'flat':
                flat.append([lon, month, days])
            elif ck == 'deep':
                deep.append([lon, month, days, np.log10(ctr)])
            elif ck == 'bubble':
                bubble.append([lon, month, days])
            else:
                nosort.append([lon, month, days])
    plt.scatter([x[0] for x in flat], [x[2] for x in flat], c='r', marker='+')
    plt.scatter([x[0] for x in deep], [x[2] for x in deep], c=[float(x[3]) for x in deep], cmap='rainbow_r', marker='s')
    plt.colorbar()
    plt.scatter([x[0] for x in bubble], [x[2] for x in bubble], c='b', marker='x')
    # plt.scatter([x[0] for x in nosort], [x[2] for x in nosort], c='k', s=3, marker='p')
    # static_draw(flat, deep, bubble, nosort)
    # print(len(flat), len(deep), len(bubble), len(nosort))
    # preDrawContourf(flat, deep, bubble, nosort)


def curveKindAndCtr(lat, den):
    N = len(lat)
    den = np.array(den)
    if len(den) > 5:
        den2 = bf.smooth(den, 5)
    else:
        den2 = den
    sigma = abs(den2 - den) / den2
    if sigma.max() > 0.05:
        return 'bubble', 0

    norpeak = []
    soupeak = []
    valley = []
    for i in range(N):
        alat = lat[i]
        if alat < -10 and alat > -20:
            soupeak.append(10 ** den[i])
        elif alat < 5 and alat > -5:
            valley.append(10 ** den[i])
        elif alat > 10 and alat < 20:
            norpeak.append(10 ** den[i])
    if len(soupeak) * len(norpeak) * len(valley) != 0:
        ctr = (np.array(soupeak).max() + np.array(norpeak).max()) / (2 * np.array(valley).min())
    else:
        return 'nosort', -1
    if ctr > 5.:
        return 'deep', ctr
    else:
        return 'flat', ctr


def test():
    path = 'D:/Program/BigCTR/Text/champOrb/'
    fin = []
    for i in range(18, 24):
        fin = fin + bf.readfile(path + format(i * 1.0, '.1f') + '.txt')

    plt.figure(figsize=[30, 100], dpi=130)
    plt.subplots_adjust(left=0.1, bottom=0.02, right=0.95, top=0.97)

    for i in range(6):
        plt.plot(range(-180, 181), np.arange(-180, 181) * 0 + 80 + i * 365, c='g')
        plt.plot(range(-180, 181), np.arange(-180, 181) * 0 + 266 + i * 365, c='y')

    getOrbitList(fin)
    # plt.subplot(3, 1, 1)
    # plt.title(LT)
    # plt.axis([0, 366, 0, 360])
    plt.savefig('a.pdf')
    plt.savefig('a.png')
    plt.close()
    # plt.show()


z0 = bf.magline(0)
if __name__ == '__main__':
    test()
