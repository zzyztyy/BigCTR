import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize
import scipy.signal as signal

import basicFun as bc
import StaticRocsatLonSeason as srls

import os

value = bc.magstormexcle()
PB_list = list()  # [lon, sea, 1 or 2 or 0]


def day_static(text):
    curve = list()
    adata = srls.RocData()
    lonbin = [2] * 36
    for a in text:
        adata.get(a)
        choose = 1 - bc.isMagstorm(adata.year, adata.days, adata.hour, value)
        choose = choose * (adata.local_time > 19 or adata.local_time < 6) * (abs(adata.dip) < 20)
        if choose:
            if len(curve) < 10:
                curve.append(adata.lgNe)
            else:
                curve.remove(curve[0])
                curve.append(adata.lgNe)
                if srls.isPB(curve):
                    adata.pb = True
                else:
                    adata.pb = False
            lonnum = int((float(adata.lon) + 180.) / 10) % 36
            if adata.pb:
                lonbin[lonnum] = 1
            else:
                is_arrive = abs(adata.dip) < 10 and adata.local_time > 20
                if lonbin[lonnum] == 2 and is_arrive:
                    lonbin[lonnum] = 0
        else:
            srls.restart_static(curve)

    for i in range(36):
        PB_list.append([i, adata.days, lonbin[i]])


def deal_all_files():
    for year in range(2000, 2001):
        path = 'D:\\sattelite data\\ROCSAT\\IPEI\\' + str(year)
        # path = 'testdata\\'
        for name in os.listdir(path):
            print(year, name)
            try:
                day_static(srls.read_roc(name, path + '\\'))
            except:
                print('Error for File')
    print(PB_list)
    draw_scatter()


def draw_scatter():
    # lon = [x[0] for x in PB_list]
    # doy = [x[1] for x in PB_list]
    z = [x[2] for x in PB_list]
    z = np.array(z).reshape(365, 36)
    plt.imshow(z, aspect='auto', cmap='CMRmap_r')
    # plt.scatter(lon, doy, c=z, marker='s')
    plt.show()


def read1():
    with open('dlt.txt', 'r') as f:
        text = f.readlines()[0].replace('[', ' ').replace(']', ' ')
        data = text.split(',')
        result = []
        print(len(data))
        for i in range(365):
            for j in range(36):
                result.append(int(data[(i * 36 + j) * 3 + 2]))
        result = np.array(result).reshape(365, 36)
        plt.imshow(result, aspect='auto', cmap='CMRmap_r')
        plt.colorbar()
        plt.show()


if __name__ == '__main__':
    """Find PB in scatter graph to check the occurrence in lon-sea."""
    # deal_all_files()
    read1()
