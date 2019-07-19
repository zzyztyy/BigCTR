import numpy as np
import matplotlib.pyplot as plt
import time
import datetime

from basicFun import get_one_orb


def read_digisonde(dig_lon, filename, path=''):
    res = {}
    with open(path + filename) as f:
        text = f.readlines()
        lenth = len(text)
        for i in range(2, lenth):
            a = text[i].replace('---', '-1').split()
            date = a[0].replace('.', '')
            uts = a[2]
            ut = float(a[2][:2]) + float(a[2][3:5]) / 60 + float(a[2][6:8]) / 3600
            lt = (ut + dig_lon / 15.) % 24
            timestamp = time.mktime(time.strptime(date + ' ' + uts, "%Y%m%d %H:%M:%S"))
            f0f2 = float(a[4])
            hmf2 = float(a[5])
            if 17.5 < lt < 23.5 and hmf2 != -1:
                # res.append([date, lt, timestamp, hmf2, f0f2])
                if date in res:
                    res[date].append([lt, timestamp, hmf2, f0f2])
                else:
                    res.get(date)
                    res[date] = [[lt, timestamp, hmf2, f0f2]]
        return res


def read_file(dig_lon, lt):
    text = open('D:/Program/BigCTR/Text/champOrb/' + str(lt * 1.0) + '.txt').readlines()
    temp_line = 0
    cha_list = []
    temp = 0
    while temp_line < len(text):
        temp = temp + 1
        cha, temp_line = get_one_orb(text, temp_line)
        cha.midlon, dig_lon = cha.midlon % 360, dig_lon % 360
        delta_lon = min(abs(cha.midlon - dig_lon), abs(cha.midlon - dig_lon - 360), abs(cha.midlon - dig_lon + 360))
        # print(cha.date)
        if delta_lon < 15:

            date = cha.date
            lt = cha.midlt
            ut = cha.midut

            hour = int(ut)
            minute = int(ut * 60 - hour * 60)
            sec = int((ut - hour) * 3600 - minute * 60)
            uts = str(hour).zfill(2) + ':' + str(minute).zfill(2) + ':' + str(sec).zfill(2)
            if uts == '24:00:00':
                uts = '23:59:59'
            timestamp = time.mktime(time.strptime(str(date) + ' ' + uts, "%Y%m%d %H:%M:%S"))

            lat_list = [abs(x[11]) for x in cha.data]
            eq_index = lat_list.index(np.min(lat_list))
            net = cha.data[eq_index][10]
            alt = cha.data[eq_index][7] - 6371.
            # mlat, den = cha.mlat_den()
            ck, ctr = cha.ck, cha.ctr
            # if date in ['20030410', '20040905', '20061017', '20021021', '20040326']:
            # if date in ['20011027']:
            #     #  print(date, uts, alt, lt)
            #     plt.plot(mlat, den)
            #     plt.title(date+' LT='+str(lt)[:5])
            #     #  plt.show()
            #     plt.savefig(date+'.jpg')
            #     plt.close()
            if timestamp > 0 * 1.057 * 10 ** 9 and ck != 'error':
                cha_list.append([date, lt, timestamp, alt, net, ck, ctr])
    return cha_list


def static_f0f2():
    dig_lon = -76.87
    f2 = 'JI91J.txt'

    cha_list = []
    for i in range(18, 24):
        cha_list = cha_list + read_file(dig_lon, i)

    dig_data = read_digisonde(dig_lon, f2, 'D:/SpaceScienceData/Digisonde/hmf2/')
    fdot = []
    ddot = []
    for cha in cha_list:
        a = []

        mytime = cha[0]
        my_another_day = (datetime.datetime(int(mytime[0:4]), int(mytime[4:6]), int(mytime[6:8]))
                          + datetime.timedelta(days=-1)).strftime('%Y%m%d')

        if my_another_day in dig_data:
            a = a + dig_data[my_another_day]
        if cha[0] in dig_data:
            a = a + dig_data[cha[0]]

        if len(a) != 0:
            lt = cha[1]
            timestamp = cha[2]
            temp = 0
            for i in range(len(a)):
                if abs(a[i][1] - timestamp) / 3600 < 8:
                    # if abs(a[i][1] - timestamp) < abs(a[temp][1] - timestamp):
                    if abs(a[i][0] - lt) < abs(a[temp][0] - lt):
                        temp = i
            dalt = -a[temp][2] + cha[3]
            ck = cha[5]
            ctr = cha[6]
            nmf2 = 0.0124 * a[temp][3] ** 2 * 10 ** 6
            hmf2 = a[temp][2]
            net = cha[4]

            if abs(a[temp][0] - lt) < 0.25:
                if ck == 'flat':
                    fdot.append([lt, dalt, ck, ctr, nmf2, net, hmf2])
                elif ck == 'deep':
                    ddot.append([lt, dalt, ck, ctr, nmf2, net, hmf2])

    res = {'fbelow': [], 'fabove': [], 'dbelow': [], 'dabove': []}
    for dot in fdot + ddot:
        if dot[0] > 18.5:
            if dot[1] < 0 and dot[2] == 'flat':
                res['fbelow'].append(dot)
            elif dot[1] < 0 and dot[2] == 'deep':
                res['dbelow'].append(dot)
            elif dot[1] >= 0 and dot[2] == 'flat':
                res['fabove'].append(dot)
            elif dot[1] >= 0 and dot[2] == 'deep':
                res['dabove'].append(dot)

    plt.scatter([], [], marker='o', edgecolors='k', c='', alpha=0.5)
    plt.scatter([], [], marker='x', c='k', alpha=0.5)
    plt.legend(['H_sat < hmF2', 'H_sat > hmF2'], loc='lower right')
    color = {'f': 'k', 'd': 'k'}
    marker = {'below': 'o', 'above': 'x'}
    for k in res.keys():
        if k[1:] == 'below':
            plt.scatter([x[3] for x in res[k]], [x[4] / x[5] for x in res[k]],
                        edgecolors=color[k[0]], marker=marker[k[1:]], c='', alpha=0.5)
        else:
            plt.scatter([x[3] for x in res[k]], [x[4] / x[5] for x in res[k]],
                        marker=marker[k[1:]], c='k', alpha=0.5)

    # nmf2 = 0.0124 * f0f2 ** 2 * 10 ** 6
    # def f(z):
    #     return np.sqrt(z/(0.0124*2*10**6))
    # plt.scatter([x[0] for x in fdot+ddot], [f(x[5])-f(x[4]) for x in fdot+ddot],
    # c=[x[1] for x in fdot+ddot], cmap='brg')
    # plt.plot([x[4] for x in fdot+ddot], [x[4] for x in fdot+ddot])
    # plt.plot([x[4] for x in fdot + ddot]+[0], [2*x[4] for x in fdot + ddot]+[0])

    plt.plot([6, 6], [0.5, 2000 / 4], ls='--', c='k')
    plt.axis([0.9, 1500, 0.5, 2000 / 4])

    # plt.plot([5, 1500], [5/4, 1500/4], c='k')
    # plt.text(x=120, y=15, s='y = 0.25x', fontsize=12)
    plt.text(x=1.5, y=180, s='Flat', fontsize=20)
    plt.text(x=20, y=180, s='Deep', fontsize=20)

    # print([round(x[3], 4) for x in res])
    # print([round(x[4] / x[5], 1) for x in res])

    plt.semilogx()
    plt.semilogy()
    # plt.colorbar()

    plt.xlabel('CTR')
    # plt.ylabel('dalt')
    plt.ylabel('NmF2 / Ne_trough')
    plt.show()


def cmp_alt(loc_num):
    # m = {'flat': 'r', 'error': 'k', 'deep': 'g', 'bubble': 'b'}
    dig_lons = [-76.87, -45.0]
    dig_files = ['JI91J.txt', 'CAJ2M.TXT']
    titles = ['Jicamarca', 'Cachoeira Paulista']

    dig_lon = dig_lons[loc_num]
    f2 = dig_files[loc_num]

    cha_list = []
    for i in range(18, 24):
        cha_list = cha_list + read_file(dig_lon, i)

    dig_data = read_digisonde(dig_lon, f2, 'D:/SpaceScienceData/Digisonde/hmf2/')
    fdot = []
    ddot = []
    bdot = []
    for cha in cha_list:
        a = []

        mytime = cha[0]
        my_another_day = (datetime.datetime(int(mytime[0:4]), int(mytime[4:6]), int(mytime[6:8]))
                          + datetime.timedelta(days=-1)).strftime('%Y%m%d')

        if my_another_day in dig_data:
            a = a + dig_data[my_another_day]
        if cha[0] in dig_data:
            a = a + dig_data[cha[0]]

        if len(a) != 0:
            lt = cha[1]
            timestamp = cha[2]
            temp = 0
            for i in range(len(a)):
                if abs(a[i][1] - timestamp) / 3600 < 5:
                    # if abs(a[i][1] - timestamp) < abs(a[temp][1] - timestamp):
                    if abs(a[i][0] - lt) < abs(a[temp][0] - lt):
                        temp = i
            dalt = -a[temp][2] + cha[3]
            ck = cha[5]
            ctr = np.log10(cha[6])
            # if abs(a[temp][1] - timestamp) / 3600 < 0.5:
            if abs(a[temp][0] - lt) < 0.25:
                if ck == 'flat':
                    # if dalt < -10:
                    #     print(cha[0], round(dalt, 4), round(10**ctr, 4), lt, a[temp][2], round(cha[3], 4))
                    fdot.append([lt, dalt, ck, ctr])
                elif ck == 'deep':
                    if dalt > 0:
                        print(cha[0], round(dalt, 4), round(10 ** ctr, 4), lt, a[temp][2], round(cha[3], 4))
                    #     print(a[temp][0], lt, a[temp][0] - lt)
                    ddot.append([lt, dalt, ck, ctr])
                elif ck == 'bubble':
                    # if dalt < -200:
                    #     print(cha[0], round(dalt, 4), round(10**ctr, 4), lt, a[temp][2], round(cha[3], 4))
                    #     print(a[temp][0], lt, a[temp][0] - lt)
                    bdot.append([lt, dalt, ck, ctr])
    plt.scatter([x[0] for x in fdot], [x[1] for x in fdot], c='g')
    # plt.scatter([x[0] for x in ddot+fdot], [x[1] for x in ddot+fdot], c=[x[3] for x in ddot+fdot], marker='s',
    #             cmap='rainbow_r')
    # plt.scatter([x[3] for x in ddot + fdot], [x[1] for x in ddot + fdot], c=[x[0] for x in ddot + fdot], marker='o')
    plt.scatter([x[0] for x in ddot], [x[1] for x in ddot], c='r')
    # plt.colorbar()
    plt.scatter([x[0] for x in bdot], [x[1] for x in bdot], c='b', marker='o')
    # plt.legend(['Flat', 'Deep', 'Bubble'])
    # plt.plot(np.arange(16, 26) - 0.5, [0] * 10, c='k', linestyle='--')
    plt.ylabel('H_sat - hmF2 /km')
    plt.xlabel('Local Time /h')
    # plt.xlabel('lg_CTR')
    plt.title('2001-2004 ' + titles[loc_num])
    plt.xlim([17, 24])
    plt.ylim([-200, 200])
    # plt.show()


def draw_dalt_lt():
    plt.figure(figsize=[8, 8])
    plt.subplot(2, 1, 1)
    cmp_alt(0)
    plt.plot(np.arange(16, 26) - 0.5, [0] * 10, c='k', linestyle='--')
    plt.subplot(2, 1, 2)
    cmp_alt(1)
    plt.legend(['Flat', 'Deep', 'Bubble'], loc='lower right')
    plt.plot(np.arange(16, 26) - 0.5, [0] * 10, c='k', linestyle='--')
    plt.show()


if __name__ == '__main__':
    draw_dalt_lt()
    # cmp_alt(0)
    # plt.show()
    # static_f0f2()
