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
            hmf2 = float(a[6])
            if 18.5 < lt < 23.5 and hmf2 != -1:
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
        print(cha.date)
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
    f2 = 'JI91J_ALL.txt'

    cha_list = []
    for i in range(18, 24):
        cha_list = cha_list + read_file(dig_lon, i)

    dig_data = read_digisonde(dig_lon, f2, 'D:/SpaceScienceData/Digisonde/hmf2/')
    fdot = []
    ddot = []
    for cha in cha_list:
        a = []

        mytime = cha[0]
        myday = datetime.datetime(int(mytime[0:4]), int(mytime[4:6]), int(mytime[6:8]))
        delta = datetime.timedelta(days=-1)
        my_yestoday = myday + delta
        my_yes_time = my_yestoday.strftime('%Y%m%d')

        if my_yes_time in dig_data:
            a = a + dig_data[my_yes_time]
        if cha[0] in dig_data:
            a = a + dig_data[cha[0]]

        if len(a) != 0:
            lt = cha[1]
            timestamp = cha[2]
            temp = 0
            for i in range(len(a)):
                if abs(a[i][1] - timestamp) < abs(a[temp][1] - timestamp):
                    temp = i
            dalt = -a[temp][2] + cha[3]
            ck = cha[5]
            ctr = cha[6]
            nmf2 = 0.0124 * a[temp][3] ** 2 * 10 ** 6
            net = cha[4]

            if abs(a[temp][1] - timestamp) / 3600 < 0.5:
                if ck == 'flat':
                    fdot.append([lt, dalt, ck, ctr, nmf2, net])
                elif ck == 'deep':
                    ddot.append([lt, dalt, ck, ctr, nmf2, net])

    cmap = 'jet'
    plt.scatter([x[3] for x in fdot], [x[4] / x[5] for x in fdot], c=[x[0] for x in fdot], marker='+', cmap=cmap)
    plt.scatter([x[3] for x in ddot], [x[4] / x[5] for x in ddot], c=[x[0] for x in ddot], marker='s', cmap=cmap)
    plt.plot(range(10 ** 5, 10 ** 7), range(10 ** 5, 10 ** 7), c='k')
    plt.semilogx()
    plt.semilogy()
    plt.colorbar()
    plt.xlabel('CTR')
    plt.ylabel('NmF2/Ne_equator')
    plt.show()


def test(loc_num):
    # m = {'flat': 'r', 'error': 'k', 'deep': 'g', 'bubble': 'b'}
    dig_lons = [-76.87, -45.0]
    dig_files = ['JI91J_ALL.txt', 'CAJ2M_ALL.TXT']

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
        myday = datetime.datetime(int(mytime[0:4]), int(mytime[4:6]), int(mytime[6:8]))
        delta = datetime.timedelta(days=-1)
        my_yestoday = myday + delta
        my_yes_time = my_yestoday.strftime('%Y%m%d')

        if my_yes_time in dig_data:
            a = a + dig_data[my_yes_time]
        if cha[0] in dig_data:
            a = a + dig_data[cha[0]]

        if len(a) != 0:
            lt = cha[1]
            timestamp = cha[2]
            temp = 0
            for i in range(len(a)):
                if abs(a[i][1] - timestamp) < abs(a[temp][1] - timestamp):
                    temp = i
            dalt = -a[temp][2] + cha[3]
            ck = cha[5]
            ctr = np.log10(cha[6])
            if abs(a[temp][1] - timestamp) / 3600 < 0.5:
                if ck == 'flat':
                    fdot.append([lt, dalt, ck, ctr])
                elif ck == 'deep':
                    ddot.append([lt, dalt, ck, ctr])
                elif ck == 'bubble':
                    bdot.append([lt, dalt, ck, ctr])

    plt.scatter([x[0] for x in fdot], [x[1] for x in fdot], c='r', marker='+')
    plt.scatter([x[0] for x in ddot], [x[1] for x in ddot], c=[x[3] for x in ddot], marker='s', cmap='rainbow_r')
    plt.colorbar()
    plt.scatter([x[0] for x in bdot], [x[1] for x in bdot], c='b', marker='x')
    plt.plot(np.arange(18, 26) - 0.5, [0] * 8, c='k', linestyle='--')
    plt.ylabel('HmF2 - Horbit /km')
    plt.xlabel('Local Time /h')
    plt.title('2001-2006')
    plt.xlim([17.5, 24])
    plt.ylim([-200, 200])
    plt.show()


if __name__ == '__main__':
    # read_digisonde('JI91J_20010606(157).TXT', 'jicamarcaDigisonde//')
    # test(1)
    static_f0f2()
