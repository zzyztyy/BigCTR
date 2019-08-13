import numpy as np
import matplotlib.pyplot as plt

import basicFun as bF


def draw_champ_lon_time(mode='doy'):
    dot_f = {'x': [], 'y': [], 'c': []}
    dot_d = {'x': [], 'y': [], 'c': []}
    dot_b = {'x': [], 'y': [], 'c': []}
    with open('D:/Program/BigCTR/Text/LonDoy/champ_ck.txt', 'r') as f:
        texts = f.readlines()
        for text in texts:
            a = text.split()
            date, ck, ctr, lon, lct = a[0], a[1], float(a[2]), float(a[3]), float(a[4])
            lon = ((lon + 180) % 360 - 180)
            if mode == 'days':
                time = bF.julday(bF.date_tran(date))
            elif mode == 'doy':
                time = bF.orderday(bF.date_tran(date))
            else:
                print('Error Parameter: "mode=%s"', mode)
                break
            if lct > 18.5:
                if ck == 'flat':
                    dot_f['x'].append(time)
                    dot_f['y'].append(lon)
                    dot_f['c'].append('g')
                if ck == 'deep':
                    dot_d['x'].append(time)
                    dot_d['y'].append(lon)
                    dot_d['c'].append(np.log10(ctr))
                if ck == 'bubble':
                    dot_b['x'].append(time)
                    dot_b['y'].append(lon)
                    dot_b['c'].append('b')
    if mode == 'days':
        plt.figure(figsize=[20, 100], dpi=75)
        plt.subplots_adjust(left=0.1, bottom=0.02, right=0.95, top=0.97)
        s = 16
        plt.scatter(dot_f['y'], dot_f['x'], c='r', s=s, marker='+')
        plt.scatter(dot_d['y'], dot_d['x'], c=dot_d['c'], s=s, marker='s', cmap='rainbow_r')
        plt.scatter(dot_b['y'], dot_b['x'], c='b', s=s, marker='x')

        for i in range(4):
            plt.plot(range(-180, 181), np.arange(-180, 181) * 0 + 80 + i * 365, c='g')
            plt.plot(range(-180, 181), np.arange(-180, 181) * 0 + 266 + i * 365, c='y')

        plt.savefig('a.pdf')
        plt.savefig('a.png')
        plt.close()
    elif mode == 'doy':
        s = 6
        plt.subplot(3, 2, 1)
        plt.scatter((np.array(dot_f['y']) + 180) / 360 * 48, np.array(dot_f['x']) / 365.24 * 24,
                    color='', alpha=1, s=s, edgecolors='g')
        # plt.axis([-180, 180, 1, 366])
        plt.subplot(3, 2, 3)
        plt.scatter((np.array(dot_d['y']) + 180) / 360 * 48, np.array(dot_d['x']) / 365.24 * 24,
                    color='', alpha=1, s=s, edgecolors='r')
        # plt.axis([-180, 180, 1, 366])
        plt.subplot(3, 2, 5)
        plt.scatter((np.array(dot_b['y']) + 180) / 360 * 48, np.array(dot_b['x']) / 365.24 * 24,
                    color='', alpha=1, s=s, edgecolors='b')
        # plt.axis([-180, 180, 1, 366])
        # plt.title('2004')
        # plt.colorbar()
    else:
        pass


def draw_kind_time():
    num_type = {'flat': 0, 'deep': 1, 'bubble': 2}
    res = {2001: {}, 2002: {}, 2003: {}, 2004: {}}
    with open('D:/Program/BigCTR/Text/fourPic/champ_ck.txt', 'r') as f:
        texts = f.readlines()
        for text in texts:
            a = text.split()
            year = int(a[0][:4])
            doy = int(a[0][4:])
            kind = a[1]
            if doy not in res[year]:
                # flat deep bubble
                res[year][doy] = [0, 0, 0]
            if kind != 'error':
                res[year][doy][num_type[kind]] += 1
    width = 1
    plt.figure(figsize=[8, 6], dpi=150)
    plt.subplot(4, 1, 1)
    plt.title('Numbers of Samples in Different Days')
    for year in [2001, 2002, 2003, 2004]:
        plt.subplot(4, 1, year - 2000)
        plt.subplots_adjust(left=0.05, bottom=0.05, right=0.98, top=0.95, hspace=0)
        # plt.plot(range(0, 366), 0*(2004-year)*np.ones(366), c='k')
        x = res[year].keys()
        f = np.array([res[year][z][0] for z in x])
        d = np.array([res[year][z][1] for z in x])
        b = np.array([res[year][z][2] for z in x])
        p1 = plt.bar(x, f, bottom=0, color='g', width=width)
        p2 = plt.bar(x, d, bottom=f, color='r', width=width)
        p3 = plt.bar(x, b, bottom=f + d, color='b', width=width)
        plt.text(330, 20, year, size=16)
        if year == 2001:
            plt.legend([p1, p2, p3], ['Flat', 'Deep', 'Bubble'], loc='upper left')
        plt.axis([0.5, 366.5, 0, 24])
        if year != 2004:
            plt.xticks([])
        else:
            plt.xticks([1, 32, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335, 366],
                       [str((x - 1) % 12 + 1) + '/1' for x in range(1, 14)])
        plt.yticks([0, 8, 16], [0, 8, 16])
    plt.show()


def draw_one_pannel(file_name, vmax, vmin, norm=False, mean=0., std=1.):
    with open('D:/Program/BigCTR/Text/LonDoy/' + file_name, 'r') as f:
        texts = f.readlines()
    res = []
    for i in range(len(texts)):
        a = texts[i].split()
        a = [float(x) for x in a]
        if norm:
            a = [(x - mean) / std + 0.5 for x in a]
        res.append(a)
        # res.append(bF.smooth(a, 3))
        # res.append([loss for x in a])
        # plt.plot(a + np.zeros(len(a))-80*i)
        # plt.plot(np.zeros(len(a))-80*i)
    if file_name == 'hwm_traneuqatorial_wind_sl.txt':
        res = np.abs(res)
        title = 'abs_' + file_name
        # plt.contour(res)
        plt.pcolor(res, cmap='bwr', vmax=vmax, vmin=vmin)
    elif file_name in ['Bubble_sl.txt', 'Deep_sl.txt', 'Flat_sl.txt']:
        plt.pcolor(res, cmap='rainbow', vmax=vmax, vmin=vmin)
        title = file_name[:-7]
    # elif file_name in ['Flat_sl.txt']:
    #     plt.pcolor(res, cmap='rainbow_r', vmax=vmax, vmin=vmin)
    #     title = file_name[:-7]
    else:
        plt.pcolor(res, vmax=vmax, vmin=vmin, cmap='rainbow')
        title = file_name[:-7]
    # C = plt.contour(res, 15, cmap='brg_r', vmax=vmax, vmin=vmin)
    # plt.clabel(C, inline=True, fontsize=10)
    m, n = len(res), len(res[0])
    plt_ticks_sl(m, n)
    plt.title(title)
    # plt.ylim([-0.5, 11.5])


def plt_ticks_sl(m, n):
    plt.xticks(range(0, n + 1, n // 12), range(-180, 181, (360 * n // 12) // n))
    plt.yticks(np.array([1, 32, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335, 366]) / 366 * m,
               [str((x - 1) % 12 + 1) + '/1' for x in range(1, 14)])
    plt.axis([0, n, 0, m])
    plt.colorbar()


def cmp_sl_map(file1, file2, mean1, std1, mean2, std2):
    plt.figure(figsize=[5, 6])
    plt.subplots_adjust(left=0.1, bottom=0.08, right=1.0, top=0.93, wspace=0.05, hspace=0.34)
    with open('D:/Program/BigCTR/Text/LonDoy/' + file1, 'r') as f:
        texts = f.readlines()
    res1 = []
    for i in range(len(texts)):
        a = texts[i].split()
        a = [float(x) for x in a]
        a = [(x - mean1) / std1 for x in a]
        res1.append(a)

    with open('D:/Program/BigCTR/Text/LonDoy/' + file2, 'r') as f:
        texts = f.readlines()
    res2 = []
    for i in range(len(texts)):
        a = texts[i].split()
        a = [float(x) for x in a]
        a = [(x - mean2) / std2 for x in a]
        res2.append(a)
    m, n = len(res1), len(res1[0])
    delta = np.array(res1) - np.array(res2)
    # vmax = np.max(abs(delta))
    # plt.subplot(3, 1, 1)
    # plt.pcolor(res1, vmax=1.5, vmin=-1.5, cmap='jet')
    # plt.title('rocsat_v_drift')
    # plt_ticks_sl(m, n)
    # plt.subplot(3, 1, 3)
    # plt.pcolor(res2, vmax=1.5, vmin=-1.5, cmap='jet')
    # plt.title('cosmic_hmf2')
    # plt_ticks_sl(m, n)
    plt.subplot(2, 1, 2)
    plt.pcolor(-delta, vmax=1, vmin=-1, cmap='bwr')
    plt.title('delta_hmf2_v_drift')
    # plt.contourf(-delta, 20, cmap='bwr', vmax=1, vmin=-1)
    plt_ticks_sl(m, n)
    # plt.show()


def test():
    plt.figure(figsize=[10, 8])
    plt.subplots_adjust(left=0.07, bottom=0.07, right=1.0, top=0.97, wspace=0.07, hspace=0.30)
    fontsize = 12
    plt.subplot(3, 2, 1)
    # draw_champ_sl_rate('flat')
    draw_one_pannel('Flat_sl.txt', 1, 0)
    plt.ylabel('Date', fontsize=fontsize)
    plt.subplot(3, 2, 3)
    # draw_champ_sl_rate('deep')
    draw_one_pannel('Deep_sl.txt', 1, 0)
    plt.ylabel('Date', fontsize=fontsize)
    plt.subplot(3, 2, 5)
    # draw_champ_sl_rate('bubble')
    draw_one_pannel('Bubble_sl.txt', 1, 0)
    plt.ylabel('Date', fontsize=fontsize)
    plt.xlabel('Longitude', fontsize=fontsize)
    plt.subplot(3, 2, 2)
    draw_one_pannel('hmF2_sl.txt', 480, 340)
    plt.plot([(-76.87 + 180) / 360 * 48, (-76.87 + 180) / 360 * 48], [-10, 50], ls='--', c='k', lw=3)
    plt.subplot(3, 2, 6)
    draw_one_pannel('EPB_sl.txt', 1, 0)
    plt.xlabel('Longitude', fontsize=fontsize)
    plt.subplot(3, 2, 4)
    draw_one_pannel('V_drift_sl.txt', 40, -10)
    draw_champ_lon_time(mode='doy')
    plt.show()


if __name__ == '__main__':
    # draw_champ_lon_time(mode='doy')
    # write_champ_ck()
    # draw_kind_time()
    # draw_hmf2()
    test()
    # cmp_sl_map('V_drift_sl.txt', 'hmF2_sl.txt', 13.22, 25.38, 395.44, 70.80)
    # plt.subplot(2, 1, 1)
    # draw_one_pannel('v_drift_20.5_22.5_sl.txt', 50, -20)
    # plt.show()
