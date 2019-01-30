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
            date, ck, ctr, lon = a[0], a[1], float(a[2]), float(a[3])
            lon = (lon + 180) % 360 - 180
            days = bf.julday(date_tran(date))
            doy = bf.orderday(date_tran(date))
            year = int(date[:4])
            if year <= 2004:
                if ck == 'flat':
                    dot_f['x'].append(days)
                    dot_f['y'].append(lon)
                    dot_f['c'].append('r')
                if ck == 'deep':
                    dot_d['x'].append(days)
                    dot_d['y'].append(lon)
                    dot_d['c'].append('r')
                if ck == 'bubble':
                    dot_b['x'].append(days)
                    dot_b['y'].append(lon)
                    dot_b['c'].append('r')
    plt.scatter(dot_f['y'], dot_f['x'], c='r', alpha=0.1, s=25)
    plt.scatter(dot_d['y'], dot_d['x'], c='g', alpha=0.3, s=25)
    plt.scatter(dot_b['y'], dot_b['x'], c='b', alpha=0.2, s=25)
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
    # dot = {'x': [], 'y': [], 'c': []}
    # bin = []
    # with open('D:/Program/BigCTR/Text/fourPic/Vdrift.txt', 'r') as f:
    #     texts = f.readlines()
    #     for text in texts:
    #         a = text.split()
    #         days = bf.julday(date_tran(a[0]))
    #         lgnes = [float(x) for x in a[1:]]
    #         n = len(lgnes)
    #         dot['x'] += list(days * np.ones(n))
    #         dot['y'] += range(n)
    #         dot['c'] += lgnes
    #         bin.append(lgnes)
    # # bin = np.array(bin).transpose()
    # # plt.imshow(bin, cmap='hot_r', aspect='auto', vmin=-40, vmax=40)
    # plt.scatter(dot['x'], dot['y'], c=dot['c'], cmap='gnuplot', s=12, alpha=0.5, vmin=-10, vmax=40)
    with open('D:/Program/BigCTR/Text/fourPic/' + file_name, 'r') as f:
        texts = f.readlines()
        res = []
        for i in range(len(texts)):
            text = texts[i]
            a = [float(x) for x in text[1:-2].replace(',', ' ').split()]
            res.append(bf.smooth(a, 2))
            res.append([loss for x in a])
            # plt.plot(a + np.zeros(len(a))-80*i)
            # plt.plot(np.zeros(len(a))-80*i)
    plt.imshow(res, cmap='gnuplot2', aspect='auto', vmax=vmax, vmin=vmin)
    # plt.colorbar()


def test():
    plt.figure(figsize=[12, 10])
    plt.subplot(1, 4, 1)
    draw_champ()
    plt.axis([-180, 180, 1300, 120])
    plt.title('CHAMP')
    # plt.colorbar()
    # plt.xlim([100, 1260])
    plt.subplot(1, 4, 4)
    draw_one_pannel('vdrift_plot.txt', 70, -10, 1000)
    plt.title('V_drift')
    # plt.colorbar()
    # plt.xlim([100, 1260])
    plt.subplot(1, 4, 2)
    draw_one_pannel('epb_plot.txt', 1.1, 0, 1000)
    plt.title('EPB')
    # plt.colorbar()
    # plt.xlim([100, 1260])
    plt.subplot(1, 4, 3)
    draw_one_pannel('lgne_plot.txt', 6.4, 5.4, 1000)
    plt.title('lgNe')
    # plt.colorbar()
    # plt.xlim([100, 1260])
    # plt.savefig('a.jpg')
    plt.show()


if __name__ == '__main__':
    # draw_vdrift()
    test()
    # draw_one_pannel('vdrift_plot.txt')
