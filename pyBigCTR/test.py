import numpy as np
import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
import basicFun as Bf
import seaborn as sns

import time


# GPS0 yy1 mm2 dd3 hh4 mm5 ss6 radius7 lat8 lon9 den10 (Temperature)
def toobig():
    data = Bf.readfile('D:\\sattelite data\\CHAMP\\CH-ME-2-PLP\\toobig\\CH-ME-2-PLP+2002-02-27_1.dat')
    lat = []
    den = []
    lon = []
    ut = 0
    i = 19
    while i in range(18, int(len(data) / 2) - 1):
        i = i + 1
        a = (data[2 * i] + data[2 * i + 1]).split()
        print(a)
        while -70 < float(a[8]) < 70 and i < int(len(data) / 2) - 1:
            lat.append(float(a[8]))
            den.append(np.log10(float(a[10])))
            i = i + 1
            a = (data[2 * i] + data[2 * i + 1]).split()
            ut = float(a[4])
        if len(lat) > 0:
            if lat[0] < 0 and 16 < ut <= 24:
                plt.plot(lat, den)
                lon.append(float(a[9]))
                # plt.show()
            lat.clear()
            den.clear()
    plt.legend(lon)


def fillblog():
    text = open('sortnum.txt', 'r').readlines()
    # data=[[0]*3]*4
    # amax = 50
    for i in range(6):
        lct = text[i * 13][:2]
        print(lct)
        plt.figure(figsize=[4.0, 10.0])
        for j in range(12):
            a = text[i * 13 + j + 1].split()
            r, g, b, y = int(a[0]), int(a[1]), int(a[2]), int(a[3])
            amax = max(r, g, b)
            plt.subplot(3, 1, 1)
            plt.scatter(j % 4, int(j / 4), c=[r / amax, 0, 0], s=2000, marker='s')
            plt.ylim(-0.6, 2.6)
            plt.subplot(3, 1, 2)
            plt.scatter(j % 4, int(j / 4), c=[0, g / amax, 0], s=2000, marker='s')
            plt.ylim(-0.6, 2.6)
            plt.subplot(3, 1, 3)
            plt.scatter(j % 4, int(j / 4), c=[0, 0, b / amax], s=2000, marker='s')
            plt.ylim(-0.6, 2.6)
        plt.xticks(range(4), area)
        plt.yticks(range(3), season)
        plt.ylim(-0.6, 2.6)
        # plt.title(LT)
        plt.savefig(lct + '.png')
        # plt.show()


def bar_plot():
    arr = [[1759, 28, 0],
           [1383, 329, 58],
           [1074, 379, 196],
           [1071, 331, 265],
           [1129, 252, 238],
           [1295, 175, 163]]
    arr = np.array(arr).transpose()
    localtime = [18, 19, 20, 21, 22, 23]
    plt.bar(localtime, arr[0] + arr[1] + arr[2], color='b', width=0.5)
    plt.bar(localtime, arr[0] + arr[1], color='g', width=0.5)
    plt.bar(localtime, arr[0], color='r', width=0.5)
    plt.axis([17, 24, 800, 2000])
    plt.legend(['Bubble', 'Deep', 'Flat'])
    plt.show()


def static_d2():
    res = {'mlat': [], 'den_d2': []}
    with open('D:/Program/BigCTR/Text/den_d2_mlat.txt', 'r') as f:
        text = f.readlines()
        for s in text:
            print(s)
            a = s.split()
            res[a[0]] = res[a[0]] + [float(x) for x in a[2:]]
    # plt.scatter(res['mlat'], res['den_d2'], s=3, alpha=0.1)
    # plt.show()
    sns.distplot(res['den_d2'], bins=1000)
    plt.show()


def static_hmf2(location):
    lons = [-76.87, -45.0]
    file_names = ['JI91J_ALL.txt', 'CAJ2M_ALL.TXT']
    if location == 'Jicamarca':
        loc = 0
    elif location == 'Cachoeira_Paulista':
        loc = 1
    else:
        loc = -1
        print('Location Error')

    file_name = 'D:/SpaceScienceData/Digisonde/hmf2/' + file_names[loc]
    time_line = []
    hmf2s = []
    with open(file_name) as f:
        texts = f.readlines()
        for text in texts:
            print(text)
            date, doy, clock, cc, f0f2, hf, hmf2 = text.split()
            if hmf2 != '---':
                # year, month, day = [int(x) for x in date.split('.')]
                # doy = int(doy[1:-1])
                hh, mm, ss = [int(x) for x in clock.split(':')]
                # hmF2 = float(hmf2)
                ut = hh + mm / 60 + ss / 3600
                lct = (ut + lons[loc] / 15) % 24

                if 19.5 < lct < 20.5:
                    uts = str(hh).zfill(2) + ':' + str(mm).zfill(2) + ':' + str(ss).zfill(2)
                    timestamp = time.mktime(time.strptime(date + ' ' + uts, "%Y.%m.%d %H:%M:%S"))

                    time_line.append(timestamp)
                    hmf2s.append(hmf2)
    plt.scatter(time_line, hmf2s, s=5)
    plt.show()


season = ['sum', 'spr', 'win']
area = ['Eur', 'Asi', 'Pac', 'Ame']
if __name__ == '__main__':
    # static_d2()
    static_hmf2('jicarmarca')
