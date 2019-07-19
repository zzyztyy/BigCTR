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
        elif self.name == 'ROCSAT':
            xtemp = 4
            ytemp = 3
        else:
            print('Error')
        lat = [float(x[xtemp]) for x in alldata]
        den = [float(x[ytemp]) for x in alldata]
        plt.plot(lat, den)
        plt.show()

    def mlat_den(self):
        xtemp = 0
        ytemp = 0
        alldata = self.data
        if self.name == 'CHAMP':
            xtemp = 11
            ytemp = 10
        else:
            print('Error')
        mlat = [float(x[xtemp]) for x in alldata]
        den = [np.log10(float(x[ytemp])) for x in alldata]
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
    a = text[startline].split()
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
    mlat0, den0 = cha.mlat_den()
    mlat, den = [], []
    for i in range(len(mlat0)):
        if -27 < mlat0[i] < 27:
            den.append(den0[i])
            mlat.append(mlat0[i])
    if len(mlat) > 35:
        cha.ck, cha.ctr = get_curve_kind(mlat, den)
    else:
        cha.ck, cha.ctr = 'loss', -2
    return cha, nextline


def repair_bubble(mlat, den):
    filted_data = abs((np.array([den[0]] + den[:-1]) + np.array(den[1:] + [den[-1]])) / 2 - den)
    filted_data[0] = 0
    filted_data[-1] = 0
    bubble_count = sum([x > 0.1 for x in filted_data])
    x, y = [], []
    for i in range(len(filted_data)):
        if filted_data[i] < 0.1:
            x.append(mlat[i])
            y.append(den[i])
    fun = interp1d(x, y, 'linear')
    den_rp = [fun(z) for z in mlat]
    return den_rp, bubble_count


def get_curve_kind(mlat, den):
    """
    error:
        南侧峰或北侧峰不存在
    flat:
        1.谷值和南侧峰或北侧峰高度相等，可能是单峰或无峰
        2.ctr <= 6
    deep:
        ctr > 6
    bubble:
        修补次数大于8.1
    """
    den_rp, step = repair_bubble(mlat, den)

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

    vally_value = 7
    for i in range(len(mlat)):
        if mlat[south_peak_index] <= mlat[i] <= mlat[north_peak_index]:
            if vally_value > den_rp[i]:
                vally_value = den_rp[i]

    if vally_value >= north_peak_value or vally_value >= south_peak_value:
        return 'flat', 1

    ctr = (10 ** north_peak_value + 10 ** south_peak_value) / (2 * 10 ** vally_value)
    if ctr > 6:
        return 'deep', ctr
    else:
        return 'flat', ctr


def readfile(filename):
    with open(filename, 'r') as f:
        return f.readlines()


def read_file_nomagstorm(filename, date, value):
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


def find_sorted_position(the_list, target):
    low = 0
    high = len(the_list) - 1
    while low <= high:
        mid = (high + low) // 2
        if the_list[mid] == target:
            return mid
        elif target < the_list[mid]:
            high = mid - 1
        else:
            low = mid + 1
    return low


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
    return value[int(year - 1999)][day - 1][hour]


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


def idw2d(x, y, value, x_min, x_max, y_min, y_max, x_bins, y_bins, mode=0, max_distant=3):
    """
    :param x: input x
    :param y: input y
    :param value: input value
    :param out_x: output x
    :param out_y: output y
    :param mode: 0 for no round, 1 for x round, 2 for y round, 3 for x and y round
    :return: np.array() out_x * out_y
    """
    res = np.zeros([x_bins, y_bins])
    x_dis = (x_max - x_min) / x_bins
    y_dis = (y_max - y_min) / y_bins
    x_r = [(temp - x_min) / x_dis for temp in x]
    y_r = [(temp - y_min) / y_dis for temp in y]
    N = len(x)
    for i in range(x_bins):
        for j in range(y_bins):
            # x_temp = i+0.5
            # y_temp = j+0.5
            # sum0 = 0
            # sum1 = 0
            # for k in range(N):
            #     distant_x = x_r[k] - x_temp
            #     distant_y = y_r[k] - y_temp
            #     if mode == 1 or mode == 3:
            #         distant_x = min(abs(distant_x-x_bins), abs(distant_x),  abs(distant_x+x_bins))
            #     if mode == 2 or mode == 3:
            #         distant_y = min(abs(distant_y - y_bins), abs(distant_y), abs(distant_y + y_bins))
            #     distant = np.sqrt(distant_x**2+distant_y**2)
            #     sum0 += value[k]/distant
            #     sum1 += 1/distant
            # res[i][j] = sum0/sum1
            res[i][j] = idw2d_1dot(x, y, value, x_min, x_max, y_min, y_max, x_bins, y_bins,
                                   x_min + (i + 0.5) * x_dis, y_min + (j + 0.5) * y_dis, mode=mode,
                                   max_distant=max_distant)
    return res.transpose()


def idw2d_1dot(x, y, value, x_min, x_max, y_min, y_max, x_bins, y_bins, dot_x, dot_y, mode=0, max_distant=3):
    x_dis = (x_max - x_min) / x_bins
    y_dis = (y_max - y_min) / y_bins
    x_r = [(temp - x_min) / x_dis for temp in x]
    y_r = [(temp - y_min) / y_dis for temp in y]
    N = len(x)
    x_temp = (dot_x - x_min) / x_dis
    y_temp = (dot_y - y_min) / y_dis
    sum0 = 0
    sum1 = 0
    for k in range(N):
        distant_x = x_r[k] - x_temp
        distant_y = y_r[k] - y_temp
        if mode == 1 or mode == 3:
            distant_x = min(abs(distant_x - x_bins), abs(distant_x), abs(distant_x + x_bins))
        if mode == 2 or mode == 3:
            distant_y = min(abs(distant_y - y_bins), abs(distant_y), abs(distant_y + y_bins))
        distant = np.sqrt(distant_x ** 2 + distant_y ** 2)
        if distant < max_distant:
            sum0 += value[k] / distant
            sum1 += 1 / distant
    if sum1 != 0:
        return sum0 / sum1
    else:
        return None


if __name__ == '__main__':
    # mse = magstormexcle()
    # print(is_magstorm(2004, 366, 12, mse))
    # print(orderday('20010101'))
    # print(a)
    # print(a[1].split())
    # print(julday('20010201'))
    # print(dip_lat(0, -76.87, 0))
    x = np.random.rand(500) * 20 - 10
    y = np.random.rand(500) * 40 - 20
    z = [np.sin((x[i] + y[i]) * 0.3) for i in range(500)]
    ans = np.array([[np.sin((i + j - 29) * 0.3) for i in range(20)] for j in range(40)])
    dot_x = np.random.random() * 20 - 10
    dot_y = np.random.random() * 40 - 20
    res = idw2d(x, y, z, -10, 10, -20, 20, 20, 40, max_distant=1)
    plt.subplot(3, 1, 1)
    plt.pcolor(res, cmap='jet')
    plt.colorbar()
    plt.subplot(3, 1, 2)
    plt.scatter(x + 10, y + 20, c=z, cmap='jet')
    plt.colorbar()
    plt.subplot(3, 1, 3)
    plt.pcolor(ans - res, cmap='bwr', vmax=1, vmin=-1)
    plt.colorbar()
    # plt.scatter(x + 10, y + 20, c=z, cmap='jet')
    plt.show()
