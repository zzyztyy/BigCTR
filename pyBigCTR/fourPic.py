import numpy as np
import matplotlib.pyplot as plt
import datetime

import os

import basicFun as bf
from StaticRocsatLonSeason import read_roc, sort_data3

value = bf.magstormexcle()


def date_tran(date):
    year = date[:4]
    doy = date[-3:]
    date = datetime.date(int(year), 1, 1) + datetime.timedelta(days=int(doy) - 1)
    return year + str(date.month).zfill(2) + str(date.day).zfill(2)


def sort_data(text, res):
    for a in text:
        a = a.split()
        local_time = float(a[2][:2]) + float(a[2][3:5]) / 60. + float(a[2][6:]) / 3600.
        dip = float(a[17])
        v_drift = float(a[7])
        lgNe = float(a[9])
        choose = (abs(dip) < 5) * (local_time > 17.5) * (local_time < 19.5)
        date = a[0]
        if date[6:] == '99':
            year = 1999
        else:
            year = int('20' + date[6:])
        days = bf.orderday(str(year) + date[:2] + date[3:5])
        hour = int(a[1][:2])
        choose = choose * (1 - bf.is_magstorm(year, days, hour, value))
        if choose:
            lonnum = int((float(a[16]) + 180.) / 10) % 36
            res[lonnum].append(round(lgNe, 3))


def write_rocsat():
    para = '2pb'
    date_range = ['20010515', '20010703',
                  '20010917', '20011111',
                  '20020126', '20020322',
                  '20020606', '20020731',
                  '20021017', '20021211',
                  '20030225', '20030421',
                  '20030706', '20030831',
                  '20031118', '20040107',
                  '20040324', '20040518']
    days_range = [bf.julday(x) for x in date_range]
    for i in range(9):
        if para != 'pb':
            res = [[] for x in range(36)]
        else:
            res = [[] for x in range(24)]
        for d in range(days_range[2 * i], days_range[2 * i + 1]):
            date = datetime.date(2001, 1, 1) + datetime.timedelta(days=d)
            path = 'D:/SpaceScienceData/ROCSAT/IPEI/' + str(date.year)
            name = str(date.year)[2:] + str(date.timetuple().tm_yday).zfill(3) + '.dat'

            try:
                if para != 'pb':
                    sort_data(read_roc(name, path + '/'), res)
                else:
                    epb_lon = sort_data3(read_roc(name, path + '/'))
                    for k in range(len(res)):
                        res[k].append(epb_lon[k])
            except:
                print(date.year, name)
                print('Error for File')
        if para != 'pb':
            ans = [np.median(x) for x in res]
        else:
            ans = []
            for lon_num in range(len(res)):
                sum_num = 0
                pb_num = 0
                for temp in res[lon_num]:
                    if temp == 0:
                        sum_num += 1
                    elif temp == 1:
                        sum_num += 1
                        pb_num += 1
                    else:
                        pass
                ans.append(round(pb_num / sum_num, 4))
        print(ans)


def write_rocsat_sl():
    para = 'npb'

    data = {}
    with open('D:/Program/BigCTR/Text/fourPic/Vdrift.txt', 'r') as f:
        texts = f.readlines()
        for text in texts:
            a = text.split()
            date = datetime.date(int(a[0][:4]), 1, 1) + datetime.timedelta(days=int(a[0][4:]))
            date = str(date.year) + str(date.month).zfill(2) + str(date.day).zfill(2)
            data[date] = a[1:]
            if para != 'pb':
                data[date] = [float(x) for x in data[date]]

    date_range = ['20010515', '20010703', '20010917', '20011111',
                  '20020126', '20020322', '20020606', '20020731',
                  '20021017', '20021211', '20030225', '20030421',
                  '20030706', '20030831', '20031118', '20040107',
                  '20040324', '20040518']
    days_range = [bf.julday(x) for x in date_range]
    res = {}

    for i in range(9):
        for d in range(days_range[2 * i], days_range[2 * i + 1]):
            date = datetime.date(2001, 1, 1) + datetime.timedelta(days=d)
            date = str(date.year) + str(date.month).zfill(2) + str(date.day).zfill(2)
            try:
                if para != 'pb':
                    res[date] = data[date]
                else:
                    res[date] = data[date]
            except:
                print(date)
                print('None of Data')

    if para != 'pb':
        ans0 = []
        for i in range(12):
            ans0.append([])
            for j in range(36):
                ans0[i].append([])
        ans = [[0.] * 36 for x in range(12)]
        for k in res:
            month = int(k[4:6]) - 1
            # print(k, res[k])
            for i in range(36):
                if res[k][i] != -1000000.0:
                    ans0[month][i].append(res[k][i])
        for month in range(12):
            for lon_num in range(36):
                ans[month][lon_num] = float(np.median(ans0[month][lon_num]))
    else:
        sum_num = [[0.] * 24 for x in range(12)]
        pb_num = [[0.] * 24 for x in range(12)]
        ans = [[0.] * 24 for x in range(12)]
        for k in res:
            month = int(k[4:6]) - 1
            for i in range(24):
                temp = res[k][i]
                # print(temp)
                if temp == '0':
                    sum_num[month][i] += 1
                elif temp == '1':
                    sum_num[month][i] += 1
                    pb_num[month][i] += 1
                else:
                    pass
        for month in range(12):
            for lon_num in range(24):
                if sum_num[month][lon_num] != 0:
                    ans[month][lon_num] = round(pb_num[month][lon_num] / sum_num[month][lon_num], 4)
                else:
                    print(month + 1, lon_num * 15 + 7.5 - 180)
                    ans[month][lon_num] = -1
    for a in ans:
        # print(a)
        print(' '.join([str(round(x, 4)) for x in a]))
    plt.contourf(ans)
    plt.show()


def draw_champ():
    # days_list = []
    # lon_list = []
    dot_f = {'x': [], 'y': [], 'c': []}
    dot_d = {'x': [], 'y': [], 'c': []}
    dot_b = {'x': [], 'y': [], 'c': []}
    # c = {'flat': 1, 'deep': 2, 'bubble': 0, 'error': -1}
    with open('D:/Program/BigCTR/Text/fourPic/champ_ck.txt', 'r') as f:
        texts = f.readlines()
        for text in texts:
            a = text.split()
            date, ck, ctr, lon, lct = a[0], a[1], float(a[2]), float(a[3]), float(a[4])
            lon = (lon + 180) % 360 - 180
            days = bf.julday(date_tran(date))
            doy = bf.orderday(date_tran(date))
            year = int(date[:4])
            if year <= 2004 and lct > 18.5:
                if ck == 'flat':
                    dot_f['x'].append(doy)
                    dot_f['y'].append(lon)
                    dot_f['c'].append('g')
                if ck == 'deep':
                    dot_d['x'].append(doy)
                    dot_d['y'].append(lon)
                    dot_d['c'].append('r')
                if ck == 'bubble':
                    dot_b['x'].append(doy)
                    dot_b['y'].append(lon)
                    dot_b['c'].append('r')
    plt.subplot(3, 1, 1)
    s = 20
    plt.scatter(dot_f['y'], dot_f['x'], c='g', alpha=0.15, s=s)
    plt.axis([-180, 180, 0, 366])
    plt.subplot(3, 1, 2)
    plt.scatter(dot_d['y'], dot_d['x'], c='r', alpha=0.5, s=s)
    plt.axis([-180, 180, 0, 366])
    plt.subplot(3, 1, 3)
    plt.scatter(dot_b['y'], dot_b['x'], c='b', alpha=0.5, s=s)
    plt.axis([-180, 180, 0, 366])
    # plt.axis([-180, 180, 0, 366])
    # plt.title('CHAMP')
    # plt.colorbar()


def draw_lgne():
    dot = {'x': [], 'y': [], 'c': []}
    bin = []
    with open('D:/Program/BigCTR/Text/fourPic/lgNe.txt', 'r') as f:
        texts = f.readlines()
        for text in texts:
            a = text.split()
            days = bf.julday(date_tran(a[0]))
            doy = bf.orderday(date_tran(a[0]))
            lgnes = [float(x) for x in a[1:]]
            n = len(lgnes)
            dot['x'] += list(doy * np.ones(n))
            dot['y'] += range(n)
            dot['c'] += lgnes
            bin.append(lgnes)
    # bin = np.array(bin).transpose()
    # plt.imshow(bin, cmap='hot_r', aspect='auto', vmin=5.0, vmax=6.0)
    plt.scatter(dot['y'], dot['x'], c=dot['c'], cmap='hot_r', s=12, alpha=0.2, vmin=4.2, vmax=5.8)


def draw_epb():
    dot = {'x': [], 'y': [], 'c': []}
    bin = []
    with open('D:/Program/BigCTR/Text/fourPic/EPB.txt', 'r') as f:
        texts = f.readlines()
        for text in texts:
            a = text.split()
            days = bf.julday(date_tran(a[0]))
            lgnes = [float(x) for x in a[1:]]
            n = len(lgnes)
            dot['x'] += list(days * np.ones(n))
            dot['y'] += range(n)
            dot['c'] += lgnes
            bin.append(lgnes)
    # bin = np.array(bin).transpose()
    # plt.imshow(bin, cmap='hot', aspect='auto')
    plt.scatter(dot['x'], dot['y'], c=dot['c'], cmap='gnuplot2', s=12, alpha=0.1)


def draw_one_pannel(file_name, vmax, vmin, loss):
    with open('D:/Program/BigCTR/Text/lonSeasonPickData/' + file_name, 'r') as f:
        texts = f.readlines()
        res = []
        for i in range(len(texts)):
            a = texts[i].split()
            a = [float(x) for x in a]
            res.append(bf.smooth(a, 3))
            # res.append([loss for x in a])
            # plt.plot(a + np.zeros(len(a))-80*i)
            # plt.plot(np.zeros(len(a))-80*i)
    plt.imshow(res, cmap='gnuplot2', aspect='auto', vmax=vmax, vmin=vmin)
    # C = plt.contourf(res, 15, cmap='hot', vmax=vmax, vmin=vmin)
    # plt.clabel(C, inline=True, fontsize=10)
    plt.colorbar()
    plt.xticks(np.arange(0, 25, 4) - 0.5, range(-180, 181, 60))
    plt.ylim([-0.5, 11.5])
    plt.yticks(np.arange(0, 12), range(1, 13))

    # plt.colorbar()


def test():
    plt.figure(figsize=[10, 6])
    plt.subplots_adjust(left=0.05, bottom=0.08, right=0.96, top=0.93, wspace=0.1, hspace=0.34)
    plt.subplot(2, 2, 1)
    draw_champ()
    plt.axis([-180, 180, 0, 366])
    plt.xticks(np.arange(-180, 181, 60), range(-180, 181, 60))
    plt.yticks([15, 45, 74, 105, 135, 166, 196, 227, 258, 288, 319, 349], range(1, 13))
    plt.title('CHAMP')
    plt.scatter([], [], c=[], cmap='jet')
    plt.colorbar()
    # plt.xlim([100, 1260])
    plt.subplot(2, 2, 4)
    draw_one_pannel('V_drift_2001_2004.txt', 50, -20, 1000)
    plt.title('V_drift')
    # plt.colorbar()
    # plt.xlim([100, 1260])
    plt.subplot(2, 2, 2)
    draw_one_pannel('EPB_2001_2004_a.txt', 1.0, 0.1, 1000)
    plt.title('EPB')
    # plt.colorbar()
    # plt.xlim([100, 1260])
    plt.subplot(2, 2, 3)
    draw_one_pannel('lgNe_2001_2004.txt', 5.9, 5.1, 1000)
    plt.title('lgNe')
    # plt.colorbar()
    # plt.xlim([100, 1260])
    # plt.savefig('a.jpg')
    plt.subplot(2, 2, 1)
    plt.plot(np.ones(366) * (-76.87), np.arange(366), c='k', ls='--', lw=2)
    for i in range(1, 4):
        plt.subplot(2, 2, i + 1)
        plt.plot(np.ones(14) * (-76.87 + 180) / 15, np.arange(-1, 13), c='k', ls='--', lw=2)
    plt.show()


if __name__ == '__main__':
    # draw_vdrift()
    # test()
    draw_champ()
    plt.show()
    # write_rocsat_sl()
    # draw_one_pannel('vdrift_plot.txt')
