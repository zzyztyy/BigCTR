import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize
import scipy.signal as signal

import basicFun as bc

import os

# Date0 HH:MM:SS1 LH:LM:LS2 Vx_rpy3 Vy_rpy4 Vz_rpy5 Vpar6 VperM7 VperZ8
# LogN9 Temp10 O+11 H12 He13 NO14 GLAT15 GLON16 DipLat17 ALT18
value = bc.magstormexcle()
abin = list()
for i in range(12):
    abin.append(list())
    for j in range(24):
        abin[i].append(list())

abin2 = list()
for i in range(12):
    abin2.append(list())
    for k in range(72):
        abin2[i].append(list())


def linear_function(x, a, b):
    return a * x + b


class RocData(object):
    def __init__(self):
        self.date = '00000000'
        self.local_time = 0.0
        self.lon = 0.
        self.month = 0
        self.dip = 0.
        self.lgNe = 0.
        self.hour = 0.
        self.days = 0
        self.pb = False
        self.year = 0

    def get(self, astr):
        a = astr.split()
        self.local_time = float(a[2][:2]) + float(a[2][3:5]) / 60. + float(a[2][6:]) / 3600.
        self.dip = float(a[17])
        self.lgNe = float(a[9])
        self.date = a[0]
        self.lon = float(a[16])
        if self.date[6:] == '99':
            self.year = 1999
        else:
            self.year = int('20' + self.date[6:])
        self.days = bc.orderday(str(self.year) + self.date[:2] + self.date[3:5])
        self.hour = int(a[1][:2])
        self.month = int(self.date[:2])


def read_roc(filename, filepath=''):
    with open(filepath + filename, 'r') as file:
        text = file.readlines()
        return text[1:]


def sort_data1(text):
    lonbin_list = [[] for x in range(36)]
    lonbin = [-1000000. for x in range(36)]
    for a in text:
        a = a.split()
        local_time = float(a[2][:2]) + float(a[2][3:5]) / 60. + float(a[2][6:]) / 3600.
        dip = float(a[17])
        v_drift = float(a[7])
        choose = (abs(dip) < 5) * (local_time > 17.5) * (local_time < 19.5)
        date = a[0]
        if date[6:] == '99':
            year = 1999
        else:
            year = int('20' + date[6:])
        days = bc.orderday(str(year) + date[:2] + date[3:5])
        hour = int(a[1][:2])
        choose = choose * (1 - bc.is_magstorm(year, days, hour, value))
        if choose:
            month = int(a[0][:2]) - 1
            # print(a[16])
            lonnum = int((float(a[16]) + 180.) / 10) % 36
            # print(lon, month)
            # abin[month][lon].append(v_drift)
            # return abin
            lonbin_list[lonnum].append(v_drift)
    for i in range(36):
        if len(lonbin_list[i]) > 0:
            a = np.median(lonbin_list[i])
            lonbin[i] = float(a)
    return lonbin


def sort_data2(text):
    lonbin_list = [[] for x in range(36)]
    lonbin = [-1. for x in range(36)]
    for a in text:
        a = a.split()
        local_time = float(a[2][:2]) + float(a[2][3:5]) / 60. + float(a[2][6:]) / 3600.
        dip = float(a[17])
        lgNe = float(a[9])
        choose = (abs(dip) < 5) * (local_time > 19.5) * (local_time < 23.5)
        date = a[0]
        if date[6:] == '99':
            year = 1999
        else:
            year = int('20' + date[6:])
        days = bc.orderday(str(year) + date[:2] + date[3:5])
        hour = int(a[1][:2])
        choose = choose * (1 - bc.is_magstorm(year, days, hour, value))
        if choose:
            month = int(a[0][:2]) - 1
            # print(a[16])
            lonnum = int((float(a[16]) + 180.) / 10) % 36
            # print(lon, month)
            lonbin_list[lonnum].append(lgNe)
            # abin[month][lon].append(lgNe)
    for i in range(36):
        if len(lonbin_list[i]) > 0:
            a = np.median(lonbin_list[i])
            lonbin[i] = float(a)
    return lonbin


def sort_data3(text):
    curve = list()
    adata = RocData()
    lonbin = [2] * 24
    for a in text:
        adata.get(a)
        choose = 1 - bc.is_magstorm(adata.year, adata.days, adata.hour, value)
        choose = choose * (adata.local_time > 19 or adata.local_time < 6) * (abs(adata.dip) < 20)
        if choose:
            if len(curve) < 10:
                curve.append(adata.lgNe)
            else:
                curve.remove(curve[0])
                curve.append(adata.lgNe)
                if isPB(curve):
                    adata.pb = True
                else:
                    adata.pb = False
            lonnum = int((float(adata.lon) + 180.) / 15) % 24
            if adata.pb:
                lonbin[lonnum] = 1
            else:
                is_arrive = abs(adata.dip) < 10 and adata.local_time > 20
                if lonbin[lonnum] == 2 and is_arrive:
                    lonbin[lonnum] = 0
        else:
            restart_static(curve)

    month = adata.month - 1
    for lon in range(24):
        abin[month][lon].append(lonbin[lon])
    # return lonbin


def sort_data4(text):
    curve = list()
    adata = RocData()
    lonbin = [2] * 72
    for a in text:
        adata.get(a)
        choose = 1 - bc.is_magstorm(adata.year, adata.days, adata.hour, value)
        if choose:
            if len(curve) < 10:
                curve.append(adata.lgNe)
            else:
                curve.remove(curve[0])
                curve.append(adata.lgNe)
                if isPB(curve):
                    adata.pb = True
                else:
                    adata.pb = False
            lonnum = int((float(adata.lon) + 180.) / 5) % 24
            if adata.pb:
                lonbin[lonnum] = 1
            else:
                is_arrive = abs(adata.dip) < 10 and adata.local_time > 20
                if lonbin[lonnum] == 2 and is_arrive:
                    lonbin[lonnum] = 0
        else:
            restart_static(curve)
    month = adata.month - 1
    for lon in range(72):
        abin2[month][lon].append(lonbin[lon])


def restart_static(curvelist):
    curvelist.clear()


def isPB(curvelist):
    curvearr = np.array(curvelist)
    A1, B1 = optimize.curve_fit(linear_function, range(len(curvelist)), curvelist)[0]
    fitarr = A1 * np.arange(len(curvelist)) + B1
    sigma = 100. * np.sqrt(np.mean((curvearr - fitarr) ** 2)) / np.mean(fitarr)
    # plt.plot(fitarr)
    # plt.scatter(range(10), curvearr)
    # print(sigma)
    # plt.show()
    if sigma > 0.3:
        return True
    else:
        return False


def fill_bin(arrlist, outfilename):
    for i in range(12):
        print(arrlist[i])
    result = np.array([[-1.] * 24] * 12)
    for month in range(12):
        for lon in range(24):
            result[month][lon] = np.median(np.array(arrlist[month][lon]))

    with open(outfilename, 'w') as file:
        for i in range(len(result)):
            arr = [format(x, '.3f') for x in result[i]]
            lines = ' '.join(arr)
            lines = lines + '\n'
            file.writelines(lines)
    plt.imshow(result)
    plt.colorbar()
    plt.yticks(np.arange(0, 12), np.arange(1, 13))
    plt.xticks(np.arange(0, 25, 2) - 0.5, np.arange(-180, 181, 30))
    plt.axis([-0.5, 23.5, -0.5, 11.5])
    plt.show()


def fill_PBoccurence(arrlist, outfilename):
    result = np.array([[-1.] * 24] * 12)
    for month in range(12):
        for lon in range(24):
            asum = 0
            apb = 0
            for temp in arrlist[month][lon]:
                if temp == 1:
                    asum += 1
                    apb += 1
                elif temp == 0:
                    asum += 1
            if asum != 0:
                result[month][lon] = apb / asum

    with open(outfilename, 'w') as file:
        for i in range(len(result)):
            arr = [format(x, '.3f') for x in result[i]]
            lines = ' '.join(arr)
            lines = lines + '\n'
            file.writelines(lines)
    plt.imshow(result)
    plt.colorbar()
    plt.yticks(np.arange(0, 12), np.arange(1, 13))
    plt.xticks(np.arange(0, 25, 2) - 0.5, np.arange(-180, 181, 30))
    plt.axis([-0.5, 23.5, -0.5, 11.5])
    plt.show()


def fill_PBoccurence2(arrlist, outfilename):
    result = np.array([[-1.] * 72] * 12)
    for month in range(12):
        for lon in range(72):
            asum = 0
            apb = 0
            for temp in arrlist[month][lon]:
                if temp == 1:
                    asum += 1
                    apb += 1
                elif temp == 0:
                    asum += 1
            if asum != 0:
                result[month][lon] = apb / asum

    with open(outfilename, 'w') as file:
        for i in range(len(result)):
            arr = [format(x, '.3f') for x in result[i]]
            lines = ' '.join(arr)
            lines = lines + '\n'
            file.writelines(lines)
    plt.imshow(result)
    plt.colorbar()
    plt.yticks(np.arange(0, 12), np.arange(1, 13))
    plt.xticks(np.arange(0, 73, 6) - 0.5, np.arange(-180, 181, 30))
    plt.axis([-0.5, 23.5, -0.5, 11.5])
    plt.show()


def static_Vdrift():
    res = {}
    for year in range(2001, 2005):
        path = 'D:/SpaceScienceData/ROCSAT/IPEI/' + str(year)
        for name in os.listdir(path):
            print(year, name)
            try:
                res[str(year) + name[2:5]] = sort_data1(read_roc(name, path + '/'))
            except:
                print('Error for File')
                # print(abin)
    # fill_bin(abin, outfilename)
    with open('Vdrift.txt', 'w+') as f:
        for k in res.keys():
            print(k)
            f.write(k + ' ' + ' '.join([str(round(x, 2)).rjust(5, ' ') for x in res[k]]) + '\n')


def static_lgNe():
    res = {}
    for year in range(2001, 2005):
        path = 'D:/SpaceScienceData/ROCSAT/IPEI/' + str(year)
        for name in os.listdir(path):
            print(year, name)
            try:
                res[str(year) + name[2:5]] = sort_data2(read_roc(name, path + '/'))
            except:
                print('Error for File')
    # fill_bin(abin, outfilename)
    with open('lgNe.txt', 'w+') as f:
        for k in res.keys():
            print(k)
            f.write(k + ' ' + ' '.join([str(round(x, 2)).rjust(5, ' ') for x in res[k]]) + '\n')


def static_epb():
    res = {}
    for year in range(2001, 2005):
        path = 'D:/SpaceScienceData/ROCSAT/IPEI/' + str(year)
        # path = 'D:/Program/BigCTR/TestData'
        for name in os.listdir(path):
            print(year, name)
            try:
                sort_data3(read_roc(name, path + '/'))
                # res[str(year) + name[2:5]] = sort_data3(read_roc(name, path + '/'))
            except:
                print('Error for File')
    for i in range(12):
        for j in range(24):
            print(abin[i][j])
    fill_PBoccurence(abin, outfilename)
    # with open('EPB.txt', 'w+') as f:
    #     for k in res.keys():
    #         print(k)
    #         f.write(k + ' ' + ' '.join([str(x) for x in res[k]]) + '\n')


def draw_V_PB_BD_Ne():
    path = 'D:/Program/BigCTR/Text/lonSeasonPickData/'
    plt.figure()

    plt.subplot(2, 2, 1)
    plt.title('ROCSAT lgNe')
    draw_one_panel(path + 'lgNe_2001_2004.txt')

    plt.subplot(2, 2, 2)
    plt.title('ROCSAT PB')
    draw_one_panel(path + 'EPB_1999_2004_a.txt')

    from fourPic import draw_champ
    plt.subplot(2, 2, 3)
    draw_champ()
    # plt.title('CHAMP Deep&Bubble')
    # draw_one_panel('BubbleAndDeep.txt')

    plt.subplot(2, 2, 4)
    plt.title('ROCSAT Vz')
    draw_one_panel(path + 'V_drift_2001_2004.txt')

    plt.show()


def draw_one_panel(filename):
    result = list()
    with open(filename, 'r') as file:
        data = file.readlines()
        for arr in data:
            alist = [float(x) for x in arr.split()]
            result.append(alist)
    result = np.array(result)
    result2 = signal.medfilt2d(result, (3, 3))
    (m, n) = result.shape
    result2[0][0] = result[0][0]
    result2[m - 1][0] = result[m - 1][0]
    result2[m - 1][n - 1] = result[m - 1][n - 1]
    result2[0][n - 1] = result[0][n - 1]

    plt.imshow(result2, cmap='gnuplot', aspect='auto')
    plt.colorbar()
    plt.yticks(np.arange(0, 12), np.arange(1, 13))
    plt.xticks(np.arange(0, 25, 2) - 0.5, np.arange(-180, 181, 30))
    plt.axis([-0.5, 23.5, -0.5, 11.5])


if __name__ == '__main__':
    outfilename = 'EPB_2001_2004_a.txt'
    static_epb()
    # static_lgNe()
    # static_Vdrift()
    # draw_one_panel(outfilename)
    # plt.show()
    # draw_V_PB_BD_Ne()
