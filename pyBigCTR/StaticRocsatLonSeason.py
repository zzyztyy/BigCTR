import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize
# import scipy.signal as signal

import basicFun as bF

# Date0 HH:MM:SS1 LH:LM:LS2 Vx_rpy3 Vy_rpy4 Vz_rpy5 Vpar6 VperM7 VperZ8
# LogN9 Temp10 O+11 H12 He13 NO14 GLAT15 GLON16 DipLat17 ALT18
value = bF.magstormexcle()


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
        self.days = bF.orderday(str(self.year) + self.date[:2] + self.date[3:5])
        self.hour = int(a[1][:2])
        self.month = int(self.date[:2])


def linear_function(x, a, b):
    return a * x + b


def is_plasma_bubble(curvelist):
    curvearr = np.array(curvelist)
    a1, b1 = optimize.curve_fit(linear_function, range(len(curvelist)), curvelist)[0]
    fitarr = a1 * np.arange(len(curvelist)) + b1
    sigma = 100. * np.sqrt(np.mean((curvearr - fitarr) ** 2)) / np.mean(fitarr)
    if sigma > 0.3:
        return True
    else:
        return False


def sort_plasma_bubble(text):
    curve = list()
    adata = RocData()
    lonbin = [2] * 24
    for a in text:
        adata.get(a)
        not_magstorm = not bF.is_magstorm(adata.year, adata.days, adata.hour, value)
        lct = adata.local_time
        if (lct > 19 or lct < 6) and not_magstorm and abs(adata.dip) < 20:
            if len(curve) < 10:
                curve.append(adata.lgNe)
            else:
                curve.remove(curve[0])
                curve.append(adata.lgNe)
                adata.pb = is_plasma_bubble(curve)
            lonnum = int((float(adata.lon) + 180.) / 15) % 24
            if adata.pb:
                lonbin[lonnum] = 1
            else:
                is_arrive = abs(adata.dip) < 10 and adata.local_time > 20
                if lonbin[lonnum] == 2 and is_arrive:
                    lonbin[lonnum] = 0
        else:
            curve.clear()
    return lonbin


def sort_not_plasma_bubble(texts, para='v_drift'):
    # para = v_drift / lg_ne
    lon_list = []
    para_list = []
    lct_list = []
    for text in texts:
        a = text.split()
        local_time = float(a[2][:2]) + float(a[2][3:5]) / 60. + float(a[2][6:]) / 3600.
        dip = float(a[17])
        lon = (float(a[16]) + 180) % 360 - 180
        if para == 'v_drift':
            para_value = float(a[7])
        elif para == 'lg_ne':
            para_value = float(a[9])
        else:
            print('Wrong Parameter: %s', para)
            break
        date = a[0]
        if date[6:] == '99':
            year = 1999
        else:
            year = int('20' + date[6:])
        days = bF.orderday(str(year) + date[:2] + date[3:5])
        hour = int(a[1][:2])
        not_magstorm = not bF.is_magstorm(year, days, hour, value)
        if abs(dip) < 5 and not_magstorm:
            # if para == 'v_drift' and 17.5 < local_time < 19.5:
            if para == 'v_drift' and 17.5 < local_time < 23.5 and (lon < -165 or lon > 165) and (
                    days < 30 or days > 335):
                lon_list.append(lon)
                para_list.append(para_value)
                lct_list.append(local_time)
            elif para == 'lg_ne' and 19.5 < local_time < 23.5:
                lon_list.append(lon)
                para_list.append(para_value)
    return lon_list, para_list, lct_list


if __name__ == '__main__':
    plt.show()
