import numpy as np
import matplotlib.pyplot as plt
import datetime

import basicFun as bf
from DrawChampProfile import get_curve_kind


def getOrbitList(fin):
    startline = 0
    chalist = []
    temp = 0
    while startline < len(fin):
        cha, nextline = bf.get_one_orb(fin, startline)
        year = cha.date[:4]
        chose = True  # (year in ['2002'])
        if chose:
            temp = temp + 1
            if cha.name == 'CHAMP':
                chalist.append(cha)
            else:
                print(cha.name)
        startline = nextline
    return chalist
    # return static_season_lon(chalist)


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


def output_champ_ck():
    res = {}

    path = 'D:/Program/BigCTR/Text/champOrb/'
    fin = []
    for i in range(18, 24):
        fin = fin + bf.readfile(path + format(i * 1.0, '.1f') + '.txt')

    # res = set()
    chalist = getOrbitList(fin)
    for i in range(len(chalist)):
        cha = chalist[i]
        mlat0, den0 = cha.mlat_den()
        mlat, den = [], []
        for i in range(len(mlat0)):
            if -27 < mlat0[i] < 27:
                den.append(den0[i])
                mlat.append(mlat0[i])
        if len(mlat) > 35:
            # res.add(cha.date)
            ck, ctr = get_curve_kind(mlat, den)
            doy = bf.orderday(cha.date)
            k = cha.date[:4] + str(doy).zfill(3)
            if k not in res:
                res[k] = []
            res[k].append([ck, str(round(ctr, 3)), str(cha.midlon), str(round(cha.midlt, 2))])
    # print(sorted(res))
    with open('champ_ck.txt', 'w+') as f:
        for k in res.keys():
            print(k)
            for s in res[k]:
                f.write(k + ' ' + ' '.join(s) + '\n')


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


def draw_kind_time():
    num_type = {'flat': 0, 'deep': 1, 'bubble': 2}
    res = {2001: {}, 2002: {}, 2003: {}, 2004: {}}
    with open('D:/Program/BigCTR/Text/fourPic/champ_ck.txt', 'r') as f:
        texts = f.readlines()
        for text in texts:
            a = text.split()
            year = int(a[0][:4])
            doy = int(a[0][4:])
            type = a[1]
            if doy not in res[year]:
                # flat deep bubble
                res[year][doy] = [0, 0, 0]
            if type != 'error':
                res[year][doy][num_type[type]] += 1
    width = 1
    plt.figure(figsize=[8, 6], dpi=150)
    plt.subplot(4, 1, 1)
    plt.title('Numbers of Samples in Different Days')
    for year in [2001, 2002, 2003, 2004]:
        plt.subplot(4, 1, year - 2000)
        plt.subplots_adjust(left=0.05, bottom=0.05, right=0.98, top=0.95, hspace=0)
        # plt.plot(range(0, 366), 0*(2004-year)*np.ones(366), c='k')
        x = res[year].keys()
        f = np.array([res[year][z][0] for z in x])
        d = np.array([res[year][z][1] for z in x])
        b = np.array([res[year][z][2] for z in x])
        p1 = plt.bar(x, f, bottom=0, color='g', width=width)
        p2 = plt.bar(x, d, bottom=f, color='r', width=width)
        p3 = plt.bar(x, b, bottom=f + d, color='b', width=width)
        plt.text(330, 20, year, size=16)
        if year == 2001:
            plt.legend([p1, p2, p3], ['Flat', 'Deep', 'Bubble'], loc='upper left')
        plt.axis([0.5, 366.5, 0, 24])
        if year != 2004:
            plt.xticks([])
        else:
            plt.xticks([1, 32, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335, 366],
                       [str((x - 1) % 12 + 1) + '/1' for x in range(1, 14)])
        plt.yticks([0, 8, 16], [0, 8, 16])
    plt.show()


z0 = bf.magline(0)
if __name__ == '__main__':
    # output_champ_ck()
    draw_kind_time()
