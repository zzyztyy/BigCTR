import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize

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
        choose = choose * (1 - bc.isMagstorm(year, days, hour, value))
        if choose:
            month = int(a[0][:2]) - 1
            # print(a[16])
            lon = int((float(a[16]) + 180.) / 15) % 24
            # print(lon, month)
            abin[month][lon].append(v_drift)
            # return abin


def sort_data2(text):
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
        choose = choose * (1 - bc.isMagstorm(year, days, hour, value))
        if choose:
            month = int(a[0][:2]) - 1
            # print(a[16])
            lon = int((float(a[16]) + 180.) / 15) % 24
            # print(lon, month)
            abin[month][lon].append(lgNe)


def sort_data3(text):
    curve = list()
    adata = RocData()
    lonbin = [2] * 24
    for a in text:
        adata.get(a)
        choose = 1 - bc.isMagstorm(adata.year, adata.days, adata.hour, value)
        if choose:
            if len(curve) < 10:
                curve.append(adata.lgNe)
            else:
                curve.remove(curve[0])
                curve.append(adata.lgNe)
                if isPB(curve):
                    adata.pb = True
            lonnum = int((float(adata.lon) + 180.) / 15) % 24
            if adata.pb:
                lonbin[lonnum] = 1
            else:
                lonbin[lonnum] = 0
        else:
            restart_static(curve)
    month = adata.month - 1
    for lon in range(24):
        abin[month][lon].append(lonbin[lon])


def restart_static(curvelist):
    curvelist.clear()


def isPB(curvelist):
    curvearr = np.array(curvelist)
    A1, B1 = optimize.curve_fit(linear_function, range(len(curvelist)), curvelist)[0]
    fitarr = A1 * np.arange(len(curvelist)) + B1
    sigma = 100. * np.sqrt(np.mean((curvearr - fitarr) ** 2)) / np.mean(fitarr)
    if sigma > 0.3:
        return True
    else:
        return False


def fill_bin(arrlist):
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


def fill_PBoccurence(arrlist):
    result = np.array([[-1.] * 24] * 12)
    for month in range(12):
        for lon in range(24):
            asum = 0.000001
            apb = 0
            for temp in arrlist[month][lon]:
                if temp == 1:
                    asum += 1
                    apb += 1
                if temp == 0:
                    asum += 1
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


def static_Vdrift():
    for year in range(2001, 2005):
        path = 'D:\\sattelite data\\ROCSAT\\IPEI\\' + str(year)
        for name in os.listdir(path):
            print(year, name)
            # for i in range(366):
            #     print(i)
            #     name = '01'+format(i+1).zfill(3)+'.dat'
            try:
                sort_data1(read_roc(name, path + '\\'))
            except:
                print('Error for File')
                # print(abin)
    fill_bin(abin)


def static_lgNe():
    for year in range(1999, 2003):
        path = 'D:\\sattelite data\\ROCSAT\\IPEI\\' + str(year)
        for name in os.listdir(path):
            print(year, name)
            # for i in range(366):
            #     print(i)
            #     name = '01'+format(i+1).zfill(3)+'.dat'
            try:
                sort_data2(read_roc(name, path + '\\'))
            except:
                print('Error for File')
                # print(abin)
    fill_bin(abin)


def static_EPB():
    for year in range(2001, 2005):
        path = 'D:\\sattelite data\\ROCSAT\\IPEI\\' + str(year)
        # path = 'testdata\\'
        for name in os.listdir(path):
            print(year, name)
            try:
                sort_data3(read_roc(name, path + '\\'))
            except:
                print('Error for File')
                # print(abin)
    fill_PBoccurence(abin)


if __name__ == '__main__':
    outfilename = 'EPB_2001_2004.txt'
    static_EPB()
