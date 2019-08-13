import numpy as np
import matplotlib.pyplot as plt
import datetime

import basicFun as bF


def get_orbit_list(texts):
    startline = 0
    chalist = []
    temp = 0
    while startline < len(texts):
        cha, nextline = bF.get_one_orb(texts, startline)
        temp = temp + 1
        if cha.name == 'CHAMP':
            chalist.append(cha)
        else:
            print(cha.name)
        startline = nextline
    return chalist


def write_champ_ck():
    res = {}
    path = 'D:/Program/BigCTR/Text/champOrb/'
    texts = []
    for lct in range(18, 24):
        with open(path + format(lct * 1.0, '.1f') + '.txt', 'r') as f:
            texts += f.readlines()
    chalist = get_orbit_list(texts)

    for i in range(len(chalist)):
        cha = chalist[i]
        mlat0, den0 = cha.mlat_den()
        mlat, den = [], []
        for j in range(len(mlat0)):
            if -27 < mlat0[j] < 27:
                den.append(den0[j])
                mlat.append(mlat0[j])
        if len(mlat) > 35:
            ck, ctr = bF.get_curve_kind(mlat, den)
            doy = bF.orderday(cha.date)
            k = cha.date[:4] + str(doy).zfill(3)
            if k not in res:
                res[k] = []
            res[k].append([ck, str(round(ctr, 3)), str(cha.midlon), str(round(cha.midlt, 2))])

    with open('champ_ck.txt', 'w+') as f:
        for k in res.keys():
            print(k)
            for s in res[k]:
                f.write(k + ' ' + ' '.join(s) + '\n')


def write_champ_ck_rate(kind='deep'):
    res = {'doy': [], 'lon': [], kind: []}
    with open('D:/Program/BigCTR/Text/LonDoy/champ_ck.txt', 'r') as f:
        texts = f.readlines()
    for text in texts:
        a = text.split()
        date, ck, ctr, lon, lct = a[0], a[1], float(a[2]), float(a[3]), float(a[4])
        lon = ((lon + 180) % 360 - 180)
        doy = bF.orderday(bF.date_tran(date))
        if lct > 18.5:
            res['doy'].append(doy)
            res['lon'].append(lon)
            if ck == kind:
                res[kind].append(1)
            else:
                res[kind].append(0)
    occ_rate = bF.idw2d(res['lon'], res['doy'], res[kind], -180, 180, 1, 366, 48, 24, 3, 3)
    for a in occ_rate:
        print(' '.join([str(round(x, 4)) for x in a]))


def write_rocsat_pb():
    from StaticRocsatLonSeason import sort_plasma_bubble
    res = {}
    for delta_days in range(1260):
        date = datetime.date(2001, 1, 1) + datetime.timedelta(days=delta_days)
        path = 'D:/SpaceScienceData/ROCSAT/IPEI/' + str(date.year) + '/'
        name = str(date.year)[2:] + str(date.timetuple().tm_yday).zfill(3) + '.dat'
        if date.day == 1:
            print(date)
        try:
            with open(path + name, 'r') as f:
                texts = f.readlines()
            res[str(date)] = sort_plasma_bubble(texts[1:])
        except FileExistsError as fee:
            print(fee)
        except Exception as e:
            print('ERROR: %s' % e)

    with open('epb_date.txt', 'a+') as f:
        for k in res:
            print('Writing: ' + k)
            s = k.replace('-', ' ') + ' ' + ' '.join([str(x) for x in res[k]]) + '\n'
            f.write(s)


def write_rocsat_not_pb(para='v_drift'):
    # para = v_drift or lg_ne
    from StaticRocsatLonSeason import sort_not_plasma_bubble
    res = {'date': [], 'lon': [], para: [], 'lct': []}
    for delta_days in range(1260):
        date = datetime.date(2001, 1, 1) + datetime.timedelta(days=delta_days)
        path = 'D:/SpaceScienceData/ROCSAT/IPEI/' + str(date.year) + '/'
        name = str(date.year)[2:] + str(date.timetuple().tm_yday).zfill(3) + '.dat'
        if date.day == 1:
            print(date)
        try:
            with open(path + name, 'r') as f:
                texts = f.readlines()
            lon_list, para_value_list, lct_list = sort_not_plasma_bubble(texts[1:], para)
            num = len(lon_list)
            for i in range(num):
                res['date'].append(str(date).replace('-', ' '))
                res['lon'].append(lon_list[i])
                res[para].append(para_value_list[i])
                res['lct'].append(lct_list[i])
        except FileExistsError as fee:
            print(fee)
        except Exception as e:
            print('ERROR: %s' % e)

    with open(para + '_date.txt', 'a+') as f:
        num = len(res['date'])
        print('Writing......')
        for i in range(num):
            s = (res['date'][i] + str(round(res['lon'][i], 2)).rjust(10) + str(round(res[para][i], 4)).rjust(10) +
                 str(round(res['lct'][i], 4)).rjust(10) + '\n')
            f.write(s)


def write_not_pb_sl(para='v_drift'):
    path = 'D:/Program/BigCTR/Text/LonDoy/'
    res = {'doy': [], 'lon': [], para: []}
    with open(path + para + '_date.txt', 'r') as f:
        texts = f.readlines()
    for text in texts:
        yy, mm, dd, lon, value = text.split()
        print(yy + mm + dd)
        res['doy'].append(bF.orderday(yy + mm + dd))
        res['lon'].append(float(lon))
        res[para].append(float(value))
    print('idw......')
    # plt.scatter(res['lon'], res['doy'], c=res[para], s=2, cmap='bwr', vmax=90, vmin=-90)
    # para_sl = bF.idw2d(res['lon'], res['doy'], res[para], -180, 180, 0, 366, 48, 24, mode=3, max_distant=3)
    # for a in para_sl:
    #     print(' '.join([str(round(x, 4)) for x in a]))
    # plt.pcolor(para_sl)
    plt.colorbar()
    plt.show()
    # print(np.mean(res[para]), np.std(res[para]))
    # plt.hist(res[para], 150)
    # plt.show()


def write_pb_sl():
    path = 'D:/Program/BigCTR/Text/LonDoy/'
    file_name = 'epb_date.txt'
    sum0 = np.zeros([12, 24])
    sum1 = np.zeros([12, 24])
    with open(path + file_name, 'r') as f:
        texts = f.readlines()
    for text in texts:
        a = [int(x) for x in text.split()]
        yy, mm, dd = a[:3]
        epbs = a[3:]
        for i in range(24):
            if epbs[i] == 0:
                sum0[mm - 1][i] += 1
            elif epbs[i] == 1:
                sum0[mm - 1][i] += 1
                sum1[mm - 1][i] += 1
            elif epbs[i] == 2:
                pass
            else:
                print('Wrong Date in ' + file_name)
    pb_rate = sum1 / sum0
    for a in pb_rate:
        print(' '.join([str(round(x, 4)).rjust(6) for x in a]))
    plt.pcolor(pb_rate)
    plt.colorbar()
    plt.show()


if __name__ == '__main__':
    # write_rocsat_pb()
    write_rocsat_not_pb('v_drift')
    # write_not_pb_sl('v_drift_20.5_22.5')
    # write_pb_sl()
    # write_champ_ck_rate('bubble')
