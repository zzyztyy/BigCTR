import numpy as np
import matplotlib.pyplot as plt
import datetime
from scipy.interpolate import interp1d
from scipy.interpolate import griddata
import scipy.signal as signal


def readfile(filename):
    f1 = open(filename, 'r')
    text = f1.readlines()
    f1.close()
    return text


def readfilenomagstorm(filename, date, value):
    year = int(date[:4])
    month = int(date[4:6])
    day = int(date[6:])
    dd = datetime.datetime.strptime(date, "%Y%m%d")
    days = dd.timetuple().tm_yday
    f1 = open(filename, 'r')
    text = f1.readlines()
    text2 = []
    for i in range(18, len(text)):
        a = text[i].split()
        # print(a)
        hour = int(float(a[4]))
        if 1-isMagstorm(year, days, hour, value):
            text2.append(text[i])
    return text2


def sort2(l1, l2):#按l2大小为l1排序
    l3 = []
    for i in range(len(l1)):
        l3.append([l1[i], l2[i]])
    # print(l3)
    c = sorted(l3, key=lambda x: x[1])
    for i in range(len(l1)):
        l1[i] = c[i][0]
    return l1


def magstormexcle():
    value = np.array([[[False] * 24] * 366] * 12)
    for i in range(12):
        dstkpdata = readfile('D:\\SatteliteData\\mag_data\\' + str(1999 + i) + 'mag.txt')
        for j in range(len(dstkpdata)):
            a = dstkpdata[j].split()
            if float(a[3]) >= 30 or float(a[4]) <= -30:
                value[i][int(float(a[1])) - 1][int(float(a[2]))] = True
    # print(value)
    return value


def isMagstorm(year, day, hour, value):
    return value[int(year - 1999)][day][hour]


def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    # print(y_smooth)
    for i in range(int(box_pts/2)):
        y_smooth[i] = y_smooth[i]*box_pts/(int(box_pts/2+0.5)+i)
        y_smooth[len(y)-i-1] = y_smooth[len(y)-i-1]*box_pts/(int(box_pts/2)+i+1)
    # print(y_smooth)
    return y_smooth


def orderday(date):
    dd = datetime.datetime.strptime(date, "%Y%m%d")
    days = dd.timetuple().tm_yday
    return days


def julday(date):
    dd = datetime.datetime.strptime(date, "%Y%m%d")
    deltaDay = (datetime.date(dd.year, dd.month, dd.day) - datetime.date(2001, 1, 1))
    return deltaDay.days


def magline(maglat):  # input longitude output glat
    f = open('maglatline\\' + str(maglat) + 'maglatline.txt', 'r')
    # type of ns is bool,north=true
    ml = f.readlines()
    y = []
    x = []
    for i in range(len(ml)):
        a = ml[i].split()
        y.append(float(a[0]))
        x.append(float(a[1]))
    z = interp1d(x, y, kind='cubic')
    return z


def drawcountourf(xl, yl, zl):
    # n = 256
    # x = np.linspace(-3, 3, n)
    # y = np.linspace(-3, 3, n)
    xg, yg = np.mgrid[-180: 180:12j, 0:390:12j]
    vg = griddata((xl, yl), zl, (xg, yg), method='linear')
    plt.contourf(xg, yg, vg, 10, cmap='jet', vmax=1, vmin=0)
    # plt.axis([-180, 180, 0, 366])
    plt.colorbar()
    plt.ylabel('DOY')
    plt.xlabel('glon')
    plt.title('Big CTR distribution')
    plt.show()


if __name__ == '__main__':
    # mse = magstormexcle()
    # a=readfilenomagstorm('CH-ME-2-PLP+2002-01-01_2.dat', '20020101', mse)
    # print(a)
    # print(a[1].split())
    value = magstormexcle()
    print(isMagstorm(2001, 159, 9, value))
