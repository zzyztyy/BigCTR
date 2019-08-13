import numpy as np
import matplotlib.pyplot as plt

import datetime
import os

import basicFun as bf

oschamp = 'D:/SpaceScienceData/CHAMP/CH-ME-2-PLP/'


def get_hmf2_days():
    file_path = 'D:/SpaceScienceData/Digisonde/hmf2/'
    name = 'CAJ2M.TXT'
    file_name = file_path + name
    days_start = bf.julday('20010515')
    days_end = bf.julday('20041231')
    hmf2s = {}
    for lct in range(18, 24):
        hmf2s[lct] = [[] for _ in range(days_start, days_end + 1)]

    with open(file_name) as f:
        texts = f.readlines()
        for text in texts:
            date, doy, clock, cc, f0f2, hmf2 = text.split()
            if hmf2 != '---':
                year, month, day = [int(x) for x in date.split('.')]
                doy = bf.orderday(date.replace('.', ''))
                days = bf.julday(date.replace('.', ''))
                hh, mm, ss = [int(x) for x in clock.split(':')]
                ut = hh + mm / 60 + ss / 3600
                lct = round(ut - 45.01 / 15) % 24
                if 18 <= lct <= 24 and days <= days_end and not bf.is_magstorm(year, doy, hh, value):
                    hmf2s[round(lct)][days - days_start].append(float(hmf2))
    res = {'hmf2': [], 'days': [], 'lct': []}
    for lct in range(18, 24):
        for x in range(days_start, days_end + 1):
            if len(hmf2s[lct][x - days_start]) > 0:
                res['hmf2'].append(np.mean(hmf2s[lct][x - days_start]))
                res['days'].append(x)
                res['lct'].append(lct)
        # hmf2s[lct] = [np.mean(hmf2s[lct][x]) for x in range(days_end-days_start+1)]
        # res['hmf2'] = bf.smooth(res, 11)
        print(lct)
        for i in range(len(res['hmf2'])):
            print(res['days'][i], round(res['hmf2'][i], 2))
        res['hmf2'].clear()
        res['days'].clear()
        # plt.scatter(res['days'], np.array(res['hmf2']) + 150*(23-lct))
    return res


def static_alt(date):
    jac_lon = -76.87
    jac_lat = -11.95
    num = 0
    ans = []
    namelast = ['1', '2', '3', '4', '21']
    while num <= 4:
        year = (date[:4])
        month = (date[4:6])
        day = (date[6:])
        champname = year + '/CH-ME-2-PLP+' + year + '-' + month + '-' + day + '_' + namelast[num] + '.dat'
        oschamp = 'D:/SpaceScienceData/CHAMP/CH-ME-2-PLP/'
        champfilename = oschamp + champname

        if os.path.exists(champfilename):
            datacha = bf.readfile(champfilename)
            state = 18
            while state < len(datacha) - 1:
                state = state + 1
                a = datacha[state].split()
                lat = float(a[8])
                lon = float(a[9])
                alt = float(a[7]) - 6371.42
                year = int(a[1])
                month = int(a[2])
                day = int(a[3])
                hour = int(a[4])
                doy = bf.orderday(date)
                # if abs((jac_lon-lon) % 360) < 15 and abs(lat-jac_lat) < 15:
                if not bf.is_magstorm(year, doy, hour, value):
                    ans.append(alt)
            num = 10
        else:
            num = num + 1
    if num == 5:
        print(date)
    return ans


def get_cha_alt():
    res = {'alt': [], 'days': []}
    for year in range(2001, 2005):
        for month in range(1, 13):
            for day in range(1, 32):
                date = str(year) + str(month + 100)[1:3] + str(day + 100)[1:3]
                # print(date)
                try:
                    alts = static_alt(date)
                    if len(alts) > 0:
                        res['alt'].append(np.mean(alts))
                        res['days'].append(bf.julday(date))
                except:
                    print('error!' + str(date))
    for i in range(len(res['alt'])):
        print(res['days'][i], round(res['alt'][i], 2))


def draw_hmf2_alt_time(num):
    files = ['lct_hmf2_Jacamarca.txt', 'Fortaleza.txt', 'SaoLuis.txt', 'CaoBalista.txt']
    colors = ['r', 'g', 'b', 'y']
    path = 'D:/Program/BigCTR/Text/alt_hmf2_lcat/'
    cha_file = 'cha_alt.txt'
    hmf2_file = files[num]
    cha_alt = {'alt': [], 'days': []}
    with open(path + cha_file, 'r') as f:
        cha_texts = f.readlines()
        for s in cha_texts:
            days, alt = [float(x) for x in s.split()]
            cha_alt['alt'].append(alt)
            cha_alt['days'].append(days)
    hmf2s = {'hmf2': [], 'days': []}
    with open(path + hmf2_file, 'r') as f:
        hmf2_texts = f.readlines()
        n = len(hmf2_texts)
        for i in range(n):
            a = hmf2_texts[i].split()
            if len(a) == 1:
                lct = int(a[0])
                if lct != 18:
                    plt.plot(hmf2s['days'], np.array(bf.smooth(hmf2s['hmf2'], 11)) + 200 * (24 - lct), c=colors[num])
                    plt.plot(cha_alt['days'], np.array(cha_alt['alt']) + 200 * (24 - lct), c='k')
                hmf2s['hmf2'].clear()
                hmf2s['days'].clear()
                # hmf2s = {'hmf2': [], 'days': []}
            else:
                days, hmf2 = [float(x) for x in a]
                hmf2s['hmf2'].append(hmf2)
                hmf2s['days'].append(days)
    dates = ['20010701',
             '20020101', '20020701',
             '20030101', '20030701',
             '20040101', '20040701',
             '20050101']
    x_ticks = [bf.julday(x) for x in dates]
    dates = ['7/1\n2001',
             '1/1\n2002', '7/1\n2002',
             '1/1\n2003', '7/1\n2003',
             '1/1\n2004', '7/1\n2004',
             '1/1\n2005']
    plt.xticks(x_ticks, dates)
    y_ticks = np.array([320, 380, 440, 520, 580, 640,
                        720, 780, 840, 920, 980, 1040,
                        1120, 1180, 1240, 1320, 1380, 1440]) + 40
    hight = np.array([320, 380, 440, 320, 380, 440,
                      320, 380, 440, 320, 380, 440,
                      320, 380, 440, 320, 380, 440]) + 40
    plt.yticks(y_ticks, hight)
    plt.grid(c='k', ls='--')
    for lct in range(18, 24):
        plt.text(800, (23 - lct) * 200 + 420, 'LT=' + str(lct), size=12)
    plt.title('CHAMP_alt & Jacamarca_hmF2')
    plt.legend(['hmF2', 'H_sat'])
    plt.xlabel('Date')
    plt.ylabel('Altitude/km')
    # plt.show()


if __name__ == '__main__':
    value = bf.magstormexcle()
    # hmf2s = get_hmf2_days()
    # get_cha_alt()
    draw_hmf2_alt_time(0)
    # draw_hmf2_alt_time(2)
    plt.show()
