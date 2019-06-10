import numpy as np
import matplotlib.pyplot as plt
import basicFun as Bf
import seaborn as sns

import time


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
    file_names = ['JI91J.txt', 'CAJ2M.TXT']
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
            date, doy, clock, cc, f0f2, hmf2 = text.split()
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


def fit_curve():
    from scipy.optimize import curve_fit
    x = [1.3188, 5.397, 5.5609, 1.5161, 3.4449, 3.0419, 2.5284, 2.2811, 2.4741, 1.1425, 2.729, 2.0496, 1.6585, 1.6357,
         1, 1.4565, 1.5189, 1.6962, 1.4225, 2.7678, 3.6379, 2.1252, 2.8787, 1.8189, 1.498, 2.7498, 2.0249, 3.4992,
         3.8104, 2.1366, 2.2518, 1.3534, 1.7863, 1.6412, 5.8483, 5.0237, 2.4948, 1.6986, 2.3434, 1.7506, 4.5821, 5.7164,
         1.2597, 1.4592, 1.3598, 2.3008, 3.0709, 1.4668, 2.2642, 3.5965, 2.5035, 1.9142, 3.0689, 5.2084, 3.6024, 3.69,
         1.8168, 3.2288, 5.7401, 18.5222, 18.1988, 470.8285, 220.2128, 238.961, 15.5978, 42.4694, 50.9162, 50.4442,
         7.5322, 8.9222, 12.668, 114.3948, 43.9377, 6.6224, 805.0847, 908.4881, 798.0296, 834.4828, 217.6966, 64.2361,
         50.7868, 1169.2015, 36.0606, 61.1782, 41.4439, 10.0414, 16.3318, 8.7289, 20.9946, 9.6322, 13.5172, 17.2962,
         18.6548, 137.4294, 845.9658, 31.913, 70.8861, 188.8889, 52.5773, 56.6021, 553.4506, 190.0474, 39.4357, 27.8105,
         102.8047, 233.712, 6.3821, 9.9052, 293.0423, 8.3122, 9.8142, 228.4538, 1054.5506, 284.8952, 25.4142, 104.0339,
         25.3512, 15.4001, 11.5088, 19.5884, 8.5635, 352.3598]
    y = [1.1, 1.7, 1.2, 1.2, 2.6, 3.0, 1.2, 1.3, 0.9, 1.0, 2.0, 1.5, 1.0, 0.9, 1.0, 1.1, 0.9, 1.1, 0.7, 1.6, 1.2, 0.9,
         1.2, 0.9, 1.0, 1.1, 1.1, 1.4, 2.4, 1.1, 1.3, 1.0, 1.1, 0.8, 1.7, 1.9, 1.1, 1.2, 0.9, 0.9, 1.7, 1.4, 1.0, 0.9,
         1.2, 1.7, 1.6, 0.8, 0.7, 1.6, 1.5, 0.6, 0.9, 1.7, 0.7, 2.2, 0.5, 0.9, 1.5, 6.3, 5.4, 73.5, 36.4, 26.9, 5.7,
         6.2, 14.0, 4.8, 2.2, 1.6, 5.5, 11.2, 15.0, 2.0, 59.0, 140.6, 222.8, 321.0, 35.9, 10.6, 11.2, 224.0, 9.0, 7.7,
         10.4, 2.9, 4.6, 3.3, 7.7, 2.8, 3.3, 4.9, 4.4, 10.5, 168.9, 6.7, 7.1, 37.1, 12.3, 12.6, 65.7, 31.1, 11.3, 5.2,
         63.1, 71.6, 1.7, 1.4, 38.4, 1.7, 3.2, 26.9, 89.9, 30.6, 4.6, 19.2, 13.7, 3.3, 3.5, 4.7, 1.2, 209.8]

    x = [np.log10(z) for z in x]
    y = [np.log10(z) for z in y]

    def func(z, aa, bb):
        return aa * z + bb

    popt, pcov = curve_fit(func, x, y)
    a = popt[0]  # popt里面是拟合系数，读者可以自己help其用法
    b = popt[1]

    print(a, b)
    yvals = [a * z + b for z in x]
    plt.plot(x, y, '*', c='k', label='original values')
    plt.scatter(x, yvals, c='r', label='curve_fit values')
    yvals = [1 * z + np.log10(0.4) for z in x]
    plt.scatter(x, yvals, c='b', label='guess values')
    plt.show()


def champ_filter():
    for lt in range(18, 24):
        with open('D:/Program/BigCTR/Text/champOrb/' + str(lt * 1.0) + '.txt', 'r') as f:
            text = f.readlines()
        temp_line = 0
        while temp_line < len(text):

            cha, temp_line = Bf.get_one_orb(text, temp_line)
            mlat, den = cha.mlat_den()
            # den = [10**x for x in den]
            try:
                if len(mlat) > 80:
                    plt.figure(figsize=[10, 10], dpi=75)
                    title = cha.date + '_' + str(round(cha.midlt, 2)) + '_' + str(round(cha.midlon, 2))
                    plt.subplot(2, 1, 1)
                    plt.title(title)
                    plt.scatter(mlat, den, c='k')
                    # [b, a] = signal.butter(16, 0.4, 'low')
                    # filtedData = signal.filtfilt(b, a, den)
                    # filtedData = signal.medfilt(den, 3)
                    # filtedData = (np.array([den[0]]+den[:-1])+np.array(den[1:]+[den[-1]])+np.array(den))/3
                    filted_data = (np.array([den[0]] + den[:-1]) + np.array(den[1:] + [den[-1]])) / 2
                    plt.plot(mlat, filted_data, linestyle='--', c='r')
                    # [b, a] = signal.butter(16, 0.4, 'high')
                    # filtedData = signal.filtfilt(b, a, den)  # data为要过滤的信号
                    filted_data = den - filted_data
                    plt.subplot(2, 1, 2)
                    filted_data = [abs(x) for x in filted_data]
                    # plt.plot(mlat, filtedData)
                    plt.bar(mlat, filted_data)
                    plt.plot(mlat, np.ones(len(mlat)) * 0.1, c='grey')
                    plt.ylim([0, 0.3])
                    # maxfl = max(filted_data)
                    bubble_count = sum([x > 0.1 for x in filted_data])
                    # for i in range(8):
                    #     plt.plot(mlat, i*10000*np.ones(len(mlat)), c='grey')
                    # plt.show()
                    plt.savefig('D:/Program/BigCTR/Picture/champPrfFilter2/' + str(lt) + '/'
                                + str(bubble_count) + '_' + title + '.png')
                    plt.close()
            except:
                print(temp_line, lt)


season = ['sum', 'spr', 'win']
area = ['Eur', 'Asi', 'Pac', 'Ame']
if __name__ == '__main__':
    static_d2()
    # static_hmf2('jicarmarca')
    # fit_curve()
    # champ_filter()
