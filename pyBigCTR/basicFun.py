import numpy as np
import matplotlib.pyplot as plt
import datetime
from scipy.interpolate import interp1d
from scipy.interpolate import griddata

from pyIGRF import igrf_value


class Orb(object):
    def __init__(self):
        self.name = 'not define'
        self.lenth = 0
        self.data = []
        self.midlon = 0.
        self.midut = 0.
        self.midlt = 0.
        self.date = '00000000'
        self.ck = 'not define'
        self.ctr = None

    def insert(self, a):
        self.data.append(a)

    def latden(self):
        xtemp = 0
        ytemp = 0
        alldata = self.data
        if self.name == 'CHAMP':
            xtemp = 8
            ytemp = 10
            # alldata = [x.split() for x in alldata]
        elif self.name == 'ROCSAT':
            xtemp = 4
            ytemp = 3
        else:
            print('Error')
        lat = [float(x[xtemp]) for x in alldata]
        den = [float(x[ytemp]) for x in alldata]
        plt.plot(lat, den)
        plt.show()

    def mlat_den(self):  # 仅限axx.x.txt类文件使用
        xtemp = 0
        ytemp = 0
        alldata = self.data
        if self.name == 'CHAMP':
            xtemp = 11
            ytemp = 10
            # alldata = [x.split() for x in alldata]
        else:
            print('Error')
        mlat = [float(x[xtemp]) for x in alldata]
        den = [np.log10(float(x[ytemp])) for x in alldata]
        # plt.plot(mlat, den)
        # plt.show()
        return mlat, den

    def clear(self):
        self.data.clear()

    def outtext(self, fout):
        fout.write(self.name + ' ' + str(self.lenth) + ' ' + self.date + ' ' + format(self.midlon, '.2f') + ' '
                   + format(self.midut, '.2f') + ' ' + format(self.midlt, '.2f') + '\n')
        if self.name == 'CHAMP':
            fout.write('GPS yy mm dd hh mm ss radius lat lon den mlat\n')
        elif self.name == 'ROCSAT':
            fout.write('ut lt Vpm lgN Diplat glat glon\n')
        for i in range(self.lenth):
            outstr = str(self.data[i]).replace('[', '').replace(']', '').replace(',', ' ').replace('\n', '')
            outstr = outstr.replace("'", '')
            fout.write(outstr + '\n')


def get_one_orb(text, startline):
    cha = Orb()
    # nextline = startline
    a = text[startline].split()
    # print(text[startline])
    cha.name = a[0]
    cha.lenth = int(a[1])
    cha.date = a[2]
    cha.midlon = float(a[3])
    cha.midut = float(a[4])
    cha.midlt = float(a[5])
    for i in range(cha.lenth):
        a = text[startline + i + 2].split()
        cha.insert([float(x) for x in a])
    nextline = startline + cha.lenth + 2
    # print(text[startline+cha.lenth+2])
    mlat0, den0 = cha.mlat_den()
    mlat, den = [], []
    for i in range(len(mlat0)):
        if -27 < mlat0[i] < 27:
            den.append(den0[i])
            mlat.append(mlat0[i])
    if len(mlat) > 35:
        cha.ck, cha.ctr = get_curve_kind(mlat, den)
    else:
        cha.ck, cha.ctr = 'less', -2
    return cha, nextline


def repair_bubble(den, den_d2):
    step = 0
    den1 = den.copy()
    while max(abs(den_d2)) > 0.2 and step < 20:
        ind = np.argmax(abs(den_d2))
        den1[ind + 1] = 0.5 * (den1[ind] + den1[ind + 2])
        den_d2 = den1[:-2] + den1[2:] - 2 * den1[1:-1]
        step += 1
    return den1, den_d2, step


def get_curve_kind(mlat, den):
    """
    error:
        南侧峰或北侧峰不存在
    flat:
        1.谷值和南侧峰或北侧峰高度相等，可能是单峰或无峰
        2.ctr <= 5
    deep:
        ctr > 5
    bubble:
        修补次数大于8.1
    """
    den = np.array(den)
    den_d2 = den[:-2] + den[2:] - 2 * den[1:-1]
    den_rp, den_d2_rp, step = repair_bubble(den, den_d2)

    if step > 8.1:
        return 'bubble', -1

    north_peak_index = None
    north_peak_value = 0.
    south_peak_index = None
    south_peak_value = 0.
    for i in range(len(mlat)):
        if -25 < mlat[i] < -5:
            if den_rp[i] > south_peak_value:
                south_peak_value = den_rp[i]
                south_peak_index = i
        elif 5 < mlat[i] < 25:
            if den_rp[i] > north_peak_value:
                north_peak_value = den_rp[i]
                north_peak_index = i

    if not north_peak_index or not south_peak_index:
        return 'error', 0

    # vally_index = -1
    vally_value = 7
    for i in range(len(mlat)):
        if mlat[south_peak_index] <= mlat[i] <= mlat[north_peak_index]:
            if vally_value > den_rp[i]:
                vally_value = den_rp[i]
                # vally_index = i

    if vally_value >= north_peak_value or vally_value >= south_peak_value:
        return 'flat', 1

    # if step <= 5:
    #     ctr = (10**north_peak_value + 10**south_peak_value)/(2*10**vally_value)
    # else:
    # n_indexs = [max(north_peak_index-1, 0), north_peak_index, min(north_peak_index+1, len(mlat)-1)]
    # v_indexs = [max(vally_index-1, 0), vally_index, min(vally_index+1, len(mlat)-1)]
    # s_indexs = [max(south_peak_index-1, 0), south_peak_index, min(south_peak_index+1, len(mlat)-1)]
    # peak_value = []
    # if [den[x] for x in n_indexs] == [den_rp[x] for x in n_indexs]:
    #     peak_value.append(10**north_peak_value)
    # if [den[x] for x in s_indexs] == [den_rp[x] for x in s_indexs]:
    #     peak_value.append(10**south_peak_value)
    # if len(peak_value) > 0 and [den[x] for x in v_indexs] == [den_rp[x] for x in v_indexs]:
    #     print(peak_value, 10**vally_value)

    # ctr = np.mean([])/(10**vally_value)
    # else:
    #     return 'bubble'

    ctr = (10 ** north_peak_value + 10 ** south_peak_value) / (2 * 10 ** vally_value)
    # print(ctr)
    if ctr > 5:
        return 'deep', ctr
    else:
        return 'flat', ctr


def readfile(filename):
    with open(filename, 'r') as f:
        return f.readlines()


def readfilenomagstorm(filename, date, value):
    year = int(date[:4])
    # month = int(date[4:6])
    # day = int(date[6:])
    dd = datetime.datetime.strptime(date, "%Y%m%d")
    days = dd.timetuple().tm_yday
    f1 = open(filename, 'r')
    text = f1.readlines()
    text2 = []
    for i in range(18, len(text)):
        a = text[i].split()
        # print(a)
        hour = int(float(a[4]))
        if 1 - is_magstorm(year, days, hour, value):
            text2.append(text[i])
    return text2


def sort2(l1, l2):
    """按l2大小为l1排序"""
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
        dstkpdata = readfile('D:\\SpaceScienceData\\mag_data\\' + str(1999 + i) + 'mag.txt')
        for j in range(len(dstkpdata)):
            a = dstkpdata[j].split()
            if float(a[3]) >= 30 or float(a[4]) <= -30:
                value[i][int(float(a[1])) - 1][int(float(a[2]))] = True
    # print(value)
    return value


def is_magstorm(year, day, hour, value):
    return value[int(year - 1999)][day][hour]


def smooth(y, box_pts):
    box = np.ones(box_pts) / box_pts
    y_smooth = np.convolve(y, box, mode='same')
    # print(y_smooth)
    for i in range(int(box_pts / 2)):
        y_smooth[i] = y_smooth[i] * box_pts / (int(box_pts / 2 + 0.5) + i)
        y_smooth[len(y) - i - 1] = y_smooth[len(y) - i - 1] * box_pts / (int(box_pts / 2) + i + 1)
    # print(y_smooth)
    return y_smooth


def orderday(date):
    dd = datetime.datetime.strptime(date, "%Y%m%d")
    days = dd.timetuple().tm_yday
    return days


def julday(date):
    dd = datetime.datetime.strptime(date, "%Y%m%d")
    delta_day = (datetime.date(dd.year, dd.month, dd.day) - datetime.date(2001, 1, 1))
    return delta_day.days


def magline(maglat):  # input longitude output glat
    f = open('D:/SpaceScienceData/maglatline/' + str(maglat) + 'maglatline.txt', 'r')
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
    vg = griddata(np.array(xl, yl), zl, (xg, yg), method='linear')
    plt.contourf(xg, yg, vg, 10, cmap='jet', vmax=1, vmin=0)
    # plt.axis([-180, 180, 0, 366])
    plt.colorbar()
    plt.ylabel('DOY')
    plt.xlabel('glon')
    plt.title('Big CTR distribution')
    plt.show()


def dip_lat(lat, lon, alt, year=2005.):
    fact = 180 / np.pi
    mag = igrf_value(lat, lon, alt, year)
    mlat = np.tan(mag[1] / 2 / fact) * fact
    return mlat


if __name__ == '__main__':
    # mse = magstormexcle()
    # a=readfilenomagstorm('CH-ME-2-PLP+2002-01-01_2.dat', '20020101', mse)
    # print(a)
    # print(a[1].split())
    dip_lat(0, 0, 0)
