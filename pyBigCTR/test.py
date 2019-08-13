import numpy as np
import matplotlib.pyplot as plt
import basicFun as bF
import seaborn as sns

import time


def static_hmf2(location):
    lons = [-76.87, -45.0]
    file_names = ['JI91J.txt', 'CAJ2M.TXT']
    if location == 'Jicamarca':
        loc = 0
    elif location == 'Cachoeira_Paulista':
        loc = 1
    else:
        loc = -1
        print('Location Error')

    file_name = 'D:/SpaceScienceData/Digisonde/hmf2/' + file_names[loc]
    time_line = []
    hmf2s = []
    with open(file_name) as f:
        texts = f.readlines()
        for text in texts:
            print(text)
            date, doy, clock, cc, f0f2, hmf2 = text.split()
            if hmf2 != '---':
                # year, month, day = [int(x) for x in date.split('.')]
                # doy = int(doy[1:-1])
                hh, mm, ss = [int(x) for x in clock.split(':')]
                # hmF2 = float(hmf2)
                ut = hh + mm / 60 + ss / 3600
                lct = (ut + lons[loc] / 15) % 24

                if 19.5 < lct < 20.5:
                    uts = str(hh).zfill(2) + ':' + str(mm).zfill(2) + ':' + str(ss).zfill(2)
                    timestamp = time.mktime(time.strptime(date + ' ' + uts, "%Y.%m.%d %H:%M:%S"))

                    time_line.append(timestamp)
                    hmf2s.append(hmf2)
    plt.scatter(time_line, hmf2s, s=5)
    plt.show()


def fit_curve():
    from scipy.optimize import curve_fit
    x = [1.3188, 5.397, 5.5609, 1.5161, 3.4449, 3.0419, 2.5284, 2.2811, 2.4741, 1.1425, 2.729, 2.0496, 1.6585, 1.6357,
         1, 1.4565, 1.5189, 1.6962, 1.4225, 2.7678, 3.6379, 2.1252, 2.8787, 1.8189, 1.498, 2.7498, 2.0249, 3.4992,
         3.8104, 2.1366, 2.2518, 1.3534, 1.7863, 1.6412, 5.8483, 5.0237, 2.4948, 1.6986, 2.3434, 1.7506, 4.5821, 5.7164,
         1.2597, 1.4592, 1.3598, 2.3008, 3.0709, 1.4668, 2.2642, 3.5965, 2.5035, 1.9142, 3.0689, 5.2084, 3.6024, 3.69,
         1.8168, 3.2288, 5.7401, 18.5222, 18.1988, 470.8285, 220.2128, 238.961, 15.5978, 42.4694, 50.9162, 50.4442,
         7.5322, 8.9222, 12.668, 114.3948, 43.9377, 6.6224, 805.0847, 908.4881, 798.0296, 834.4828, 217.6966, 64.2361,
         50.7868, 1169.2015, 36.0606, 61.1782, 41.4439, 10.0414, 16.3318, 8.7289, 20.9946, 9.6322, 13.5172, 17.2962,
         18.6548, 137.4294, 845.9658, 31.913, 70.8861, 188.8889, 52.5773, 56.6021, 553.4506, 190.0474, 39.4357, 27.8105,
         102.8047, 233.712, 6.3821, 9.9052, 293.0423, 8.3122, 9.8142, 228.4538, 1054.5506, 284.8952, 25.4142, 104.0339,
         25.3512, 15.4001, 11.5088, 19.5884, 8.5635, 352.3598]
    y = [1.1, 1.7, 1.2, 1.2, 2.6, 3.0, 1.2, 1.3, 0.9, 1.0, 2.0, 1.5, 1.0, 0.9, 1.0, 1.1, 0.9, 1.1, 0.7, 1.6, 1.2, 0.9,
         1.2, 0.9, 1.0, 1.1, 1.1, 1.4, 2.4, 1.1, 1.3, 1.0, 1.1, 0.8, 1.7, 1.9, 1.1, 1.2, 0.9, 0.9, 1.7, 1.4, 1.0, 0.9,
         1.2, 1.7, 1.6, 0.8, 0.7, 1.6, 1.5, 0.6, 0.9, 1.7, 0.7, 2.2, 0.5, 0.9, 1.5, 6.3, 5.4, 73.5, 36.4, 26.9, 5.7,
         6.2, 14.0, 4.8, 2.2, 1.6, 5.5, 11.2, 15.0, 2.0, 59.0, 140.6, 222.8, 321.0, 35.9, 10.6, 11.2, 224.0, 9.0, 7.7,
         10.4, 2.9, 4.6, 3.3, 7.7, 2.8, 3.3, 4.9, 4.4, 10.5, 168.9, 6.7, 7.1, 37.1, 12.3, 12.6, 65.7, 31.1, 11.3, 5.2,
         63.1, 71.6, 1.7, 1.4, 38.4, 1.7, 3.2, 26.9, 89.9, 30.6, 4.6, 19.2, 13.7, 3.3, 3.5, 4.7, 1.2, 209.8]

    x = [np.log10(z) for z in x]
    y = [np.log10(z) for z in y]

    def func(z, aa, bb):
        return aa * z + bb

    popt, pcov = curve_fit(func, x, y)
    a = popt[0]
    b = popt[1]

    print(a, b)
    yvals = [a * z + b for z in x]
    plt.plot(x, y, '*', c='k', label='original values')
    plt.scatter(x, yvals, c='r', label='curve_fit values')
    yvals = [1 * z + np.log10(0.4) for z in x]
    plt.scatter(x, yvals, c='b', label='guess values')
    plt.show()


def champ_filter():
    for lt in range(18, 24):
        with open('D:/Program/BigCTR/Text/champOrb/' + str(lt * 1.0) + '.txt', 'r') as f:
            text = f.readlines()
        temp_line = 0
        while temp_line < len(text):

            cha, temp_line = bF.get_one_orb(text, temp_line)
            mlat, den = cha.mlat_den()
            # den = [10**x for x in den]
            if len(mlat) > 80:
                plt.figure(figsize=[10, 10], dpi=75)
                title = cha.date + '_' + str(round(cha.midlt, 2)) + '_' + str(round(cha.midlon, 2))
                plt.subplot(2, 1, 1)
                plt.title(title)
                plt.scatter(mlat, den, c='k')
                # [b, a] = signal.butter(16, 0.4, 'low')
                # filtedData = signal.filtfilt(b, a, den)
                # filtedData = signal.medfilt(den, 3)
                # filtedData = (np.array([den[0]]+den[:-1])+np.array(den[1:]+[den[-1]])+np.array(den))/3
                filted_data = (np.array([den[0]] + den[:-1]) + np.array(den[1:] + [den[-1]])) / 2
                plt.plot(mlat, filted_data, linestyle='--', c='r')
                # [b, a] = signal.butter(16, 0.4, 'high')
                # filtedData = signal.filtfilt(b, a, den)  # data为要过滤的信号
                filted_data = den - filted_data
                plt.subplot(2, 1, 2)
                filted_data = [abs(x) for x in filted_data]
                # plt.plot(mlat, filtedData)
                plt.bar(mlat, filted_data)
                plt.plot(mlat, np.ones(len(mlat)) * 0.1, c='grey')
                plt.ylim([0, 0.3])
                # maxfl = max(filted_data)
                bubble_count = sum([x > 0.1 for x in filted_data])
                # for i in range(8):
                #     plt.plot(mlat, i*10000*np.ones(len(mlat)), c='grey')
                # plt.show()
                plt.savefig('D:/Program/BigCTR/Picture/champPrfFilter2/' + str(lt) + '/'
                            + str(bubble_count) + '_' + title + '.png')
                plt.close()


def static_cosmic_hmf2():
    res = {'days': [], 'lon': [], 'hmf2': [], 'doy': [], 'den': [], 'lct': [], 'year': []}
    # with open('D:/Program/BigCTR/Text/cosmicOcc/cosmicOccHmf2WithoutStorm.txt', 'r') as f:
    with open('D:/Program/BigCTR/Text/cosmicOcc/cosmic_south.txt', 'r') as f:
        texts = f.readlines()
    for text in texts:
        yy, mm, dd, gps_time, lct, hmf2, lat, lon, den = [float(x) for x in text.split()]
        print(yy, mm, dd)
        doy = bF.orderday(str(int(yy)) + str(int(mm)).zfill(2) + str(int(dd)).zfill(2))
        days = bF.julday(str(int(yy)) + str(int(mm)).zfill(2) + str(int(dd)).zfill(2)) - bF.julday('20120101')
        # chose_wind = -45 < lon < -15 and 152 < doy < 213
        # chose_drift = -45 < lon < -15 and (doy < 30 or doy > 335)
        # chose_drift = (lon < -165 or lon > 165) and 152 < doy < 213
        # chose_none = -100 < lon < -70 and 152 < doy < 213
        # chose_both = -15 < lon < 15 and 152 < doy < 213
        chose_wind = (lon < -165 or lon > 165) and (doy < 30 or doy > 335)
        # mlat = bF.dip_lat(lat, lon, hmf2, year=yy)
        if 0 < lct < 24 and 200 < hmf2 < 650 and chose_wind:
            res['days'].append(days)
            res['lon'].append(lon)
            res['hmf2'].append(hmf2)
            res['doy'].append(doy)
            res['den'].append(den)
            res['lct'].append(lct)
            res['year'].append(yy)

    # print(res)

    plt.scatter(res['lct'], res['hmf2'], c=res['year'], s=8, cmap='Set1', vmax=2020)
    b = sorted(enumerate(res['lct']), key=lambda x: x[1])
    lcts = [x[1] for x in b]
    hmf2s = [res['hmf2'][x[0]] for x in b]
    print(np.round(lcts, 2))
    print(np.round(hmf2s, 2))
    y = bF.smooth(hmf2s, 50)
    y = bF.smooth(y, 10)
    plt.plot(lcts, y)

    # res_lenth = len(res['lct'])
    # lcts = np.linspace(17.5, 23.5, 25)
    # hmf2_mean = []
    # hmf2_std = []
    # for lct in lcts:
    #     hmf2s = []
    #     for i in range(res_lenth):
    #         if abs(res['lct'][i]-lct) < 0.125:
    #             hmf2s.append(res['hmf2'][i])
    #     hmf2_mean.append(np.mean(hmf2s))
    #     hmf2_std.append(np.std(hmf2s))
    #     # print(lct, np.mean(hmf2s), np.std(hmf2s))
    # # plt.plot(range(18, 24), hmf2_mean)
    # plt.errorbar(lcts, hmf2_mean, hmf2_std)
    # plt.show()
    # print(list(lcts))
    # print(list(np.round(hmf2_mean, 2)))
    # print(list(np.round(hmf2_std, 2)))

    # print(np.array(lcts))
    # print(y)
    # plt.colorbar()
    # hmf2_bins = bF.idw2d(res['lon'], res['doy'], res['hmf2'], -180, 180, 1, 366, 48, 24, mode=3, max_distant=1.5)
    # nmf2_bins = bF.idw2d(res['lon'], res['doy'], res['den'], -180, 180, 1, 366, 48, 24, mode=3, max_distant=3)

    # print('hmf2')
    # for a in hmf2_bins:
    #     print(' '.join([str(round(x, 4)) for x in a]))
    # print('nmf2')
    # for a in nmf2_bins:
    #     print(' '.join([str(round(x)) for x in a]))
    # plt.pcolor(nmf2_bins, cmap='jet')
    # plt.colorbar()
    # plt.show()
    # plt.pcolor(hmf2_bins, cmap='jet')
    # plt.colorbar()
    # plt.show()
    # plt.hist(res['hmf2'], bins=50)
    # print(np.mean(res['hmf2']), np.std(res['hmf2']))
    # plt.show()
    # plt.hist(res['den'], bins=50)
    # print(np.mean(res['den']), np.std(res['den']))
    # plt.show()


def static_cosmic_lct(lct_target):
    res = {'days': [], 'lon': [], 'hmf2': [], 'doy': [], 'den': [], 'lct': []}
    # with open('D:/Program/BigCTR/Text/cosmicOcc/cosmic_magequ.txt', 'r') as f:
    #     texts = f.readlines()
    with open('D:/Program/BigCTR/Text/cosmicOcc/cosmic_magequ.txt', 'r') as f:
        texts = f.readlines()
    for text in texts:
        yy, mm, dd, gps_time, lct, hmf2, lat, lon, den = [float(x) for x in text.split()]
        print(yy, mm, dd)
        doy = bF.orderday(str(int(yy)) + str(int(mm)).zfill(2) + str(int(dd)).zfill(2))
        days = bF.julday(str(int(yy)) + str(int(mm)).zfill(2) + str(int(dd)).zfill(2)) - bF.julday('20120101')
        if abs(lct - lct_target) < 0.5 and 200 < hmf2 < 650:
            res['days'].append(days)
            res['lon'].append(lon)
            res['hmf2'].append(hmf2)
            res['doy'].append(doy)
            res['den'].append(den)
            res['lct'].append(lct)
    # plt.scatter(res['lon'], res['days'], c=res['hmf2'], s=8, cmap='jet', vmax=650, vmin=200)
    hmf2_bins = bF.idw2d(res['lon'], res['doy'], res['den'], -180, 180, 1, 366, 48, 24, mode=3, max_distant=1.5)
    plt.pcolor(hmf2_bins, cmap='jet', vmax=2 * 10 ** 6, vmin=0.5 * 10 ** 6)
    plt.yticks([], [])
    plt.xticks([], [])
    # plt.colorbar()
    # plt.show()
    # hmf2_bins = bF.idw2d(res['lon'], res['doy'], res['hmf2'], -180, 180, 1, 366, 48, 24, mode=3, max_distant=3)


def test_idw():
    x = np.random.rand(500) * 20 - 10
    y = np.random.rand(500) * 40 - 20
    z = [np.sin((x[i] + y[i]) * 0.3) for i in range(500)]
    ans = np.array([[np.sin((i + j - 29) * 0.3) for i in range(20)] for j in range(40)])
    res = bF.idw2d(x, y, z, -10, 10, -20, 20, 20, 40, max_distant=1)
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


def get_champ_ck_hmf2(ck_file, hmf2_file):
    cosmic_data = {'days': [], 'lon': [], 'hmf2': [], 'doy': [], 'den': [], 'lct': []}
    with open('D:/Program/BigCTR/Text/cosmicOcc/' + hmf2_file, 'r') as f:
        texts = f.readlines()
    for text in texts:
        yy, mm, dd, gps_time, lct, hmf2, lat, lon, den = [float(x) for x in text.split()]
        # print(yy, mm, dd)
        doy = bF.orderday(str(int(yy)) + str(int(mm)).zfill(2) + str(int(dd)).zfill(2))
        days = bF.julday(str(int(yy)) + str(int(mm)).zfill(2) + str(int(dd)).zfill(2)) - bF.julday('20120101')
        if 18.5 < lct < 23.5 and 200 < hmf2 < 650:
            cosmic_data['days'].append(days)
            cosmic_data['lon'].append(lon)
            cosmic_data['hmf2'].append(hmf2)
            cosmic_data['doy'].append(doy)
            cosmic_data['den'].append(den)
            cosmic_data['lct'].append(lct)

    champ_ck = {'flat': [], 'deep': [], 'bubble': []}
    with open('D:/Program/BigCTR/Text/LonDoy/' + ck_file, 'r') as f:
        texts = f.readlines()
    for text in texts:
        a = text.split()
        date, ck, ctr, lon, lct = a[0], a[1], float(a[2]), float(a[3]), float(a[4])
        print(date)
        if lct > 18.5 and date[:4] == '2004':
            lon = ((lon + 180) % 360 - 180)
            doy = bF.orderday(bF.date_tran(date))
            # if not (doy > 300 and -30 < lon < 30):
            hmf2_idw = bF.idw2d_1dot(cosmic_data['lon'], cosmic_data['doy'], cosmic_data['hmf2'],
                                     -180, 180, 1, 366, 48, 24, lon, doy, 3, 1.5)
            if ck in champ_ck.keys() and hmf2_idw:
                champ_ck[ck].append(hmf2_idw)
    color = {'flat': 'g', 'deep': 'r', 'bubble': 'b'}
    bins = 50
    all_ck = champ_ck['flat'] + champ_ck['deep'] + champ_ck['bubble']
    hist_all, bin_edges = np.histogram(all_ck, bins=bins, range=[300, 550])

    for k in champ_ck.keys():
        hist, bin_edges = np.histogram(champ_ck[k], bins=bins, range=[300, 550])
        plt.subplot(2, 1, 1)
        # plt.bar((bin_edges[1:]+bin_edges[:-1])/2, hist/len(champ_ck[k]),
        #         alpha=0.5, width=250/bins, color=color[k])
        # plt.plot((bin_edges[1:] + bin_edges[:-1]) / 2, hist / len(champ_ck[k]), color=color[k])
        sns.distplot(champ_ck[k], color=color[k])
        plt.subplot(2, 1, 2)
        plt.bar((bin_edges[1:] + bin_edges[:-1]) / 2, hist / len(champ_ck[k]) - hist_all / len(all_ck),
                alpha=0.5, width=250 / bins, color=color[k])
        # plt.plot((bin_edges[1:]+bin_edges[:-1])/2, hist/len(champ_ck[k]), color=color[k])
        # plt.hist(champ_ck[k], 45, alpha=0.5, color=color[k])
    # plt.bar((bin_edges[1:]+bin_edges[:-1])/2, hist/len(all_ck), alpha=0.5, width=450/bins, color='k')
    # plt.plot((bin_edges[1:]+bin_edges[:-1])/2, hist/len(all_ck), color='k')
    plt.subplot(2, 1, 1)
    sns.kdeplot(all_ck, color='k')
    plt.legend(['flat', 'deep', 'bubble', 'all'])
    plt.xlim([300, 550])
    plt.subplot(2, 1, 2)
    plt.legend(['flat', 'deep', 'bubble'])
    plt.xlim([300, 550])
    plt.show()


def plt_hmf2_lct():
    hmf2_dic = {
        'drift_lct': '''17.51 17.55 17.57 17.7  17.74 17.77 17.83 17.84 17.92 17.97 18.02 18.09
                     18.11 18.17 18.23 18.25 18.29 18.29 18.32 18.41 18.44 18.45 18.49 18.53
                     18.53 18.53 18.55 18.58 18.64 18.66 18.72 18.85 18.85 18.9  18.9  18.91
                     18.94 18.97 18.98 18.98 19.03 19.07 19.08 19.08 19.09 19.11 19.18 19.22
                     19.24 19.27 19.27 19.29 19.4  19.4  19.42 19.43 19.44 19.49 19.5  19.57
                     19.57 19.57 19.58 19.72 19.75 19.81 19.83 19.84 19.85 19.89 19.9  19.91
                     19.94 19.95 20.04 20.05 20.05 20.08 20.11 20.17 20.26 20.29 20.34 20.39
                     20.43 20.48 20.5  20.53 20.54 20.61 20.66 20.76 20.76 20.95 21.   21.04
                     21.08 21.13 21.14 21.14 21.16 21.23 21.24 21.28 21.3  21.31 21.33 21.4
                     21.44 21.54 21.64 21.65 21.7  21.72 21.76 21.76 21.78 21.86 21.91 22.07
                     22.08 22.2  22.27 22.34 22.35 22.37 22.45 22.45 22.57 22.81 23.01 23.04
                     23.15 23.19 23.23 23.24 23.27 23.33 23.37 23.42 23.47 23.47''',
        'drift_hmf2': '''399.85 370.62 414.35 344.11 389.72 333.4  389.84 374.15 374.05 319.04
                     386.91 377.56 360.11 400.2  378.23 361.75 392.77 353.77 443.75 333.49
                     406.06 401.21 410.05 358.96 445.47 364.59 358.14 442.55 352.96 347.08
                     399.38 594.82 367.59 409.35 328.51 368.05 447.84 443.96 468.51 378.37
                     369.92 344.5  397.93 396.81 370.88 433.83 347.66 333.66 474.33 416.55
                     428.35 367.14 454.28 500.36 361.26 398.15 386.68 371.52 433.48 366.56
                     370.33 627.58 415.44 382.91 379.08 358.71 361.33 506.7  395.75 425.29
                     445.19 385.39 432.31 431.83 345.14 379.72 415.22 328.84 351.85 442.51
                     418.26 393.24 397.9  429.38 420.53 426.24 400.37 305.58 299.58 339.63
                     374.88 438.77 341.04 415.72 386.31 273.21 417.44 401.98 358.29 368.75
                     431.53 466.46 323.26 294.6  377.69 405.18 419.37 469.58 271.45 400.07
                     305.02 305.77 311.65 392.41 283.36 336.17 424.39 382.25 460.4  370.18
                     350.53 373.05 320.73 320.47 383.16 493.06 473.6  312.06 415.78 389.41
                     438.27 353.07 379.14 418.26 390.17 326.4  300.31 336.3  239.34 360.07
                     296.17 344.6''',
        'sum_lct': '''17.55 17.63 17.69 17.72 17.79 17.79 17.82 17.87 17.93 17.95 17.96 17.96
                     18.01 18.03 18.1  18.12 18.19 18.2  18.2  18.22 18.24 18.3  18.34 18.34
                     18.38 18.46 18.48 18.5  18.51 18.56 18.56 18.56 18.59 18.64 18.7  18.71
                     18.72 18.75 18.85 18.86 18.87 18.88 18.94 19.03 19.07 19.08 19.1  19.1
                     19.11 19.13 19.13 19.14 19.18 19.21 19.21 19.25 19.27 19.27 19.36 19.48
                     19.51 19.53 19.57 19.57 19.58 19.78 19.81 19.9  19.92 19.94 19.98 20.04
                     20.06 20.17 20.25 20.28 20.29 20.36 20.36 20.44 20.47 20.47 20.53 20.72
                     20.84 20.88 20.88 20.91 21.01 21.08 21.09 21.12 21.14 21.15 21.19 21.23
                     21.26 21.35 21.4  21.44 21.48 21.49 21.56 21.67 21.82 21.9  21.9  21.93
                     22.08 22.27 22.28 22.34 22.35 22.44 22.47 22.48 22.52 22.55 22.69 22.8
                     22.8  22.91 23.23 23.24 23.31 23.36 23.48''',
        'sum_hmf2': '''321.66 389.1  399.59 359.02 379.01 365.65 385.18 324.5  366.66 294.5
                     356.71 351.78 339.08 322.3  406.91 382.94 368.65 326.05 366.49 307.81
                     302.56 329.03 310.77 345.22 326.54 339.7  321.12 373.99 345.46 372.32
                     363.68 329.63 324.84 382.07 364.65 335.85 379.63 322.52 336.06 325.85
                     307.12 344.01 319.45 367.81 326.28 307.1  402.67 428.67 329.43 334.4
                     377.35 403.71 356.98 290.45 342.79 334.18 343.23 359.81 304.94 353.87
                     328.39 352.95 338.88 360.27 401.65 378.28 368.23 335.18 468.31 293.04
                     338.3  371.78 394.32 384.31 360.63 416.93 346.96 435.96 357.87 377.61
                     399.72 430.19 367.62 440.74 402.73 484.7  451.21 347.16 368.64 463.45
                     332.65 370.26 462.58 326.71 476.95 399.56 393.4  361.84 424.15 438.41
                     301.9  392.05 411.03 356.67 432.83 379.66 441.18 331.82 443.04 432.73
                     442.19 369.2  433.81 457.24 432.   563.87 540.81 439.76 364.68 395.15
                     387.09 466.09 454.09 435.54 420.81 500.08 221.53''',
        'win_lct': '''17.6  17.6  17.68 17.77 17.8  17.82 17.84 17.84 18.01 18.01 18.01 18.04
                     18.05 18.09 18.1  18.11 18.13 18.19 18.31 18.32 18.38 18.39 18.39 18.41
                     18.44 18.47 18.5  18.52 18.56 18.65 18.67 18.68 18.79 18.82 18.85 18.97
                     19.   19.04 19.06 19.07 19.1  19.38 19.38 19.39 19.42 19.44 19.5  19.52
                     19.53 19.67 19.69 19.7  19.76 19.82 19.82 19.83 19.95 19.96 19.96 19.97
                     19.99 20.02 20.1  20.21 20.32 20.35 20.4  20.41 20.46 20.47 20.49 20.5
                     20.54 20.55 20.56 20.75 20.77 20.77 20.81 20.96 21.03 21.13 21.15 21.18
                     21.46 21.5  21.51 21.54 21.65 21.66 21.92 22.15 22.24 22.26 22.32 22.38
                     22.44 22.5  22.55 22.58 22.64 22.72 22.74 22.9  23.   23.12 23.12 23.28
                     23.3  23.32 23.37 23.39''',
        'win_hmf2': '''394.67 329.08 347.07 414.25 308.63 337.39 372.25 395.84 360.89 274.86
                     359.52 363.88 379.25 390.1  508.15 410.55 317.55 368.33 390.36 356.69
                     420.37 411.6  382.11 439.95 320.68 398.5  320.36 422.84 390.67 499.72
                     419.35 467.56 386.25 511.17 408.93 406.97 410.35 526.63 433.78 407.11
                     357.69 347.24 522.7  428.67 398.3  559.84 510.49 453.48 451.76 488.98
                     468.25 385.5  538.85 394.66 330.78 498.42 333.55 485.87 435.6  415.85
                     424.34 417.08 410.52 442.14 469.32 423.84 517.19 400.   390.31 511.67
                     416.26 423.36 448.31 530.68 404.54 297.79 423.2  476.81 447.41 346.32
                     473.11 504.02 399.5  459.1  439.62 407.77 400.92 404.57 374.33 424.2
                     449.9  268.47 368.82 400.51 427.18 333.7  287.79 349.29 261.78 260.87
                     323.84 255.8  403.69 341.79 287.65 344.11 377.37 291.58 281.95 310.53
                     268.21 370.63''',
        'sum_peak_lct': '''17.56 17.59 17.65 17.68 17.7  17.79 17.81 17.86 17.89 18.04 18.09 18.14
                         18.18 18.22 18.24 18.24 18.25 18.26 18.27 18.38 18.49 18.51 18.54 18.72
                         18.77 18.81 18.85 18.88 18.91 18.95 18.97 19.05 19.11 19.12 19.13 19.14
                         19.19 19.25 19.32 19.38 19.41 19.43 19.46 19.56 19.57 19.63 19.64 19.7
                         19.75 19.75 19.77 19.77 19.78 19.79 19.91 19.95 19.97 20.08 20.12 20.14
                         20.16 20.18 20.19 20.21 20.3  20.31 20.31 20.33 20.34 20.36 20.42 20.48
                         20.53 20.54 20.58 20.64 20.66 20.74 20.91 20.93 20.96 20.96 21.01 21.09
                         21.21 21.3  21.32 21.33 21.4  21.41 21.42 21.49 21.5  21.67 21.71 21.79
                         21.8  21.89 21.92 21.93 21.95 21.97 21.99 22.02 22.22 22.29 22.29 22.32
                         22.49 22.54 22.55 22.57 22.6  22.69 22.7  22.78 22.78 22.83 22.84 22.86
                         22.93 22.95 22.98 23.01 23.15 23.18 23.21 23.23 23.32 23.33 23.34 23.37
                         23.38 23.43''',
        'sum_peak_hmf2': '''314.44 331.52 301.82 308.85 288.25 287.17 283.5  280.99 286.7  316.06
                         300.74 314.28 299.3  313.77 307.12 335.5  355.36 275.27 308.26 325.96
                         320.95 311.26 302.72 325.83 328.55 322.32 386.2  321.74 279.36 280.46
                         292.82 266.61 335.22 355.13 318.63 339.4  340.54 312.1  319.79 364.41
                         321.46 357.31 321.78 365.31 365.76 392.87 372.53 300.83 409.72 335.44
                         345.23 395.36 352.28 381.02 443.14 344.62 426.46 374.02 434.34 446.99
                         367.81 382.13 380.55 374.29 453.96 397.45 448.36 442.85 373.02 458.92
                         427.4  349.8  384.43 450.42 319.11 328.95 374.61 416.74 388.77 353.25
                         390.5  401.41 419.04 347.03 385.92 421.01 456.63 481.38 404.03 382.91
                         347.25 359.85 406.55 429.86 388.58 401.31 407.98 363.83 418.5  406.42
                         424.34 402.94 371.28 396.78 419.32 419.74 460.55 385.21 432.37 359.88
                         408.26 435.4  405.61 347.88 430.26 393.04 432.2  408.61 435.59 393.94
                         460.28 419.56 393.24 425.18 394.04 383.49 430.89 376.62 399.57 391.15
                         416.76 447.78 473.08 390.19''',
        'win_peak_lct': '''17.51 17.52 17.54 17.61 17.62 17.63 17.63 17.64 17.88 17.95 18.   18.01
                         18.07 18.07 18.08 18.09 18.12 18.13 18.41 18.43 18.43 18.48 18.49 18.51
                         18.59 18.64 18.65 18.65 18.71 18.98 19.04 19.07 19.1  19.13 19.17 19.37
                         19.41 19.47 19.5  19.62 19.7  19.92 20.1  20.17 20.17 20.23 20.45 20.5
                         20.5  20.56 20.62 21.05 21.25 21.3  21.31 21.6  21.68 21.74 22.04 22.44
                         22.45 22.46 22.59 22.73 22.75 22.83 22.94 22.95 22.98 23.02 23.13 23.27
                         23.44 23.45''',
        'win_peak_hmf2': '''397.22 303.06 344.   374.29 354.45 331.13 366.15 375.22 294.66 341.15
                         325.72 397.14 390.68 389.74 399.29 402.11 382.97 367.5  428.51 403.22
                         368.48 330.32 405.78 343.   333.54 357.87 425.41 402.67 373.53 370.68
                         410.13 432.67 408.23 436.89 379.77 376.87 398.45 403.67 400.72 406.51
                         422.6  389.2  397.08 377.41 437.71 430.95 425.97 409.88 414.8  461.07
                         402.2  396.43 391.49 419.69 383.77 392.96 387.87 419.14 359.13 370.76
                         383.88 382.62 334.09 377.33 334.56 360.06 333.3  317.31 381.01 315.65
                         420.42 360.69 330.31 346.54'''
    }
    wind_lct = np.linspace(17.5, 23.5, 25)
    wind_dic = {
        'sum_equ': '''9.9674 3.1437 -4.3191 -12.2849 -20.6063 -29.1287 -37.6931 -46.1394 -54.3083 
                    -62.0444 -69.1987 -75.6318 -81.2183 -85.8519 -89.4512 -91.966 -93.3823 -93.7251 -93.0506 
                    -91.469 -89.0973 -86.0732 -82.54 -78.6373 -74.4952''',
        'sum_peak': '''12.243 6.2173 -0.8349 -8.7796 -17.454 -26.6687 -36.2127 -45.8569 -55.3597 
                    -64.4741 -72.9549 -80.5688 -87.1046 -92.3856 -96.2805 -98.7135 -99.6702 -99.1988 -97.3841 
                    -94.4198 -90.4698 -85.7363 -80.4257 -74.7396 -68.8685''',
        'win_equ': '''90.5066 97.4882 103.5152 108.4348 112.1406 114.5695 115.6977 115.5379 
                    114.1375 111.5777 107.9717 103.4631 98.2221 92.4403 86.3243 80.0882 
                    73.9444 68.0951 62.7236 57.9866 54.0086 50.878 48.6442 47.3184 46.8739''',
        'win_peak': '''65.7416 75.6104 85.4838 95.0903 104.1787 112.5224 119.9211 126.202 131.2219 
                    134.8699 137.0711 137.7905 137.036 134.8607 131.3621 126.681 120.9966 
                    114.5197 107.4846 100.139 92.7335 85.5115 78.7002 72.5027 67.0917''',
        'drift_equ': '''9.0509 8.8685 8.228 7.1088 5.5033 3.4182 0.8758 -2.085 -5.4094 -9.0274 
                    -12.8554 -16.799 -20.756 -24.6196 -28.2826 -31.6405 -34.5957 -37.0602 
                    -38.9587 -40.2307 -40.8323 -40.7377 -39.9397 -38.4503 -36.3014''',
        'drift_peak': '''34.0618 32.4584 29.5191 25.2793 19.819 13.2604 5.7653 -2.4702 -11.222 
                    -20.2455 -29.2848 -38.0818 -46.3857 -53.9626 -60.6034 -66.132 -70.4106 
                    -73.3445 -74.8843 -75.0265 -73.8133 -71.3296 -67.7001 -63.0845 -57.6724'''
    }
    for k in hmf2_dic.keys():
        hmf2_dic[k] = [float(x) for x in hmf2_dic[k].split()]
        if k[-4:] == 'hmf2':
            hmf2_dic[k] = bF.smooth(hmf2_dic[k], 50)
            hmf2_dic[k] = bF.smooth(hmf2_dic[k], 10)
    for k in wind_dic.keys():
        wind_dic[k] = [float(x) for x in wind_dic[k].split()]
    # fig = plt.figure()
    # ax1 = fig.add_subplot(3, 1, 3)
    # ax1.plot(hmf2_dic['drift_lct'], hmf2_dic['drift_hmf2'])
    # plt.ylim([300, 450])
    # ax2 = ax1.twinx()
    # ax2.plot(wind_lct, np.abs(wind_dic['drift_equ']))
    # plt.ylim([0, 150])
    # ax1 = fig.add_subplot(3, 1, 1)
    # ax1.plot(hmf2_dic['sum_lct'], hmf2_dic['sum_hmf2'])
    # plt.ylim([300, 450])
    # ax2 = ax1.twinx()
    # ax2.plot(wind_lct, np.abs(wind_dic['sum_equ']))
    # plt.ylim([0, 150])
    # ax1 = fig.add_subplot(3, 1, 2)
    # ax1.plot(hmf2_dic['win_lct'], hmf2_dic['win_hmf2'])
    # plt.ylim([300, 450])
    # ax2 = ax1.twinx()
    # ax2.plot(wind_lct, np.abs(wind_dic['win_equ']))
    # plt.ylim([0, 150])

    plt.subplot(2, 1, 1)
    plt.ylabel('cosmic_hmf2')
    plt.plot(hmf2_dic['drift_lct'], hmf2_dic['drift_hmf2'])
    plt.plot(hmf2_dic['sum_lct'], hmf2_dic['sum_hmf2'])
    plt.plot(hmf2_dic['win_lct'], hmf2_dic['win_hmf2'])
    plt.legend(['Upward Drift', 'Southward Wind', 'Northward Wind'])
    plt.ylim([340, 450])
    plt.subplot(2, 1, 2)
    plt.ylabel('hwm2014_wind')
    plt.xlabel('local_time')
    plt.plot(wind_lct, np.abs(wind_dic['drift_equ']))
    plt.plot(wind_lct, np.abs(wind_dic['sum_equ']))
    plt.plot(wind_lct, np.abs(wind_dic['win_equ']))
    # plt.legend(['Drift', 'Southward Wind', 'Northward Wind'])
    plt.ylim([0, 120])
    # plt.subplot(2, 2, 2)
    # plt.plot(hmf2_dic['sum_peak_lct'], hmf2_dic['sum_peak_hmf2'])
    # plt.plot(hmf2_dic['win_peak_lct'], hmf2_dic['win_peak_hmf2'])
    # plt.ylim([300, 450])
    # plt.subplot(2, 2, 4)
    # plt.plot(wind_lct, np.abs(wind_dic['sum_peak']))
    # plt.plot(wind_lct, np.abs(wind_dic['win_peak']))
    # plt.ylim([0, 150])
    plt.show()


def plt_v_drift_lct(file):
    pb_excel = {}
    with open('D:/Program/BigCTR/Text/LonDoy/epb_date.txt', 'r') as f:
        texts = f.readlines()
    for text in texts:
        a = text.split()
        pb_excel[a[0] + a[1] + a[2]] = a[3:]
    res = {'days': [], 'lon': [], 'v': [], 'lct': []}
    with open(file, 'r') as f:
        texts = f.readlines()
    for text in texts:
        yy, mm, dd, lon, value, lct = text.split()
        # if float(value) > 50:
        #     print(yy, mm, dd)
        lon_num = int((float(lon) + 180) // 15)
        if pb_excel[yy + mm + dd][lon_num] != '1' and yy != '2005':
            res['days'].append(bF.julday(yy + mm + dd))
            # res['lon'].append(float(lon))
            res['lct'].append(float(lct))
            res['v'].append(float(value))
    plt.scatter(res['lct'], res['v'], c=res['days'], cmap='Set2', s=8, alpha=0.5)
    b = sorted(enumerate(res['lct']), key=lambda x: x[1])
    lcts = [x[1] for x in b]
    v_drift = [res['v'][x[0]] for x in b]
    y = bF.smooth(v_drift, 200)
    # y = bF.smooth(y, 20)
    plt.plot(lcts, y, c='k')
    plt.plot([17., 24.], [0, 0], c='k', ls='--')
    # plt.plot(range(len(res['v'])), res['v'], c='k')
    # plt.scatter(range(len(res['v'])), res['v'], c=res['lct'], cmap='jet')
    # plt.scatter(res['lct'], res['v'], c=res['days'], cmap='jet')
    plt.colorbar()
    plt.axis([17., 24, -80, 80])
    # plt.colorbar()
    # plt.show()


def draw_rocsat():
    res = {'ut': [], 'lct': [], 'vpm': [], 'lgn': [], 'lon': [], 'dip_lat': []}
    with open('D:/Program/BigCTR/TestData/01183.dat', 'r') as f:
        texts = f.readlines()[1:]
    for text in texts:
        a = text.split()
        hh, mm, ss = [float(x) for x in a[1].split(':')]
        lh, lm, ls = [float(x) for x in a[2].split(':')]
        vpm = float(a[7])
        lgn = float(a[9])
        lon = (float(a[16]) + 180) % 360 - 180
        dip_lat = float(a[17])
        if abs(dip_lat) < 75 and lh > 17 and -450 < lon < 1500 and 20 <= hh < 21:
            res['ut'].append(hh + mm / 60 + ss / 3600)
            res['lct'].append(lh + lm / 60 + ls / 3600)
            res['vpm'].append(vpm)
            res['lgn'].append(lgn)
            res['lon'].append(lon)
            res['dip_lat'].append(dip_lat)
    plt.subplot(2, 1, 1)
    plt.scatter(res['ut'], res['vpm'], c=res['lct'], cmap='jet', s=6)
    plt.colorbar()
    plt.subplot(2, 1, 2)
    plt.scatter(res['ut'], res['lgn'], c=res['lct'], cmap='jet', s=6)
    plt.colorbar()
    plt.show()


season = ['sum', 'spr', 'win']
area = ['Eur', 'Asi', 'Pac', 'Ame']
if __name__ == '__main__':
    # static_hmf2('jicarmarca')
    # fit_curve()
    # champ_filter()
    # for lct_tar in range(18, 24):
    #     plt.subplot(3, 2, lct_tar-17)
    #     static_cosmic_lct(lct_tar)
    # static_cosmic_hmf2()
    # plt.colorbar()
    # get_champ_ck_hmf2('champ_ck.txt', 'cosmic_magequ.txt')
    plt_hmf2_lct()
    # plt.subplot(1, 2, 1)
    # plt_v_drift_lct('v_drift_wind_winter_date.txt')
    # plt.title('Drift')
    # plt.subplot(1, 2, 2)
    # plt_v_drift_lct('v_drift_wind_date.txt')
    # plt.title('Wind')
    # draw_rocsat()
    plt.show()
