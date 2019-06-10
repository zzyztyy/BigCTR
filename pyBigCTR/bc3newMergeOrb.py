import datetime
import os
import matplotlib.pyplot as plt
import numpy as np
import basicFun as bF

# ut0 lt1 Vpm2 lgN3 Diplat4 glat5 glon6


oschamp = 'D:/SpaceScienceData/CHAMP/CH-ME-2-PLP/'
osroc = 'D:/SpaceScienceData/ROCSAT/IPEI/'


def datetran(date, num):
    year = (date[:4])
    month = (date[4:6])
    day = (date[6:])
    champname = year + '/CH-ME-2-PLP+' + year + '-' + month + '-' + day + '_' + namelast[num] + '.dat'
    # print(champname)
    dd = datetime.datetime.strptime(date, "%Y%m%d")
    days = dd.timetuple().tm_yday
    if days < 10:
        rocname = year + '/' + year[2:4] + '00' + str(days)
    elif days < 100:
        rocname = year + '/' + year[2:4] + '0' + str(days)
    else:
        rocname = year + '/' + year[2:4] + str(days)
    rocname = rocname + '.dat'
    return champname, rocname


# GPS0 yy1 mm2 dd3 hh4 mm5 ss6 radius7 lat8 lon9 den10 (Temperature)
def search_cha(data, state):
    cha = bF.Orb()
    cha.name = 'CHAMP'
    # 找到轨道起始位置
    for i in range(state, len(data)):
        a = data[i].split()
        # print(a)
        lat, lon = float(a[8]), float(a[9])
        if zs([lon])[0] < lat < zn([lon])[0]:
            state = i
            break
    a = data[state].split()
    lat, lon = float(a[8]), float(a[9])
    # 获得轨道
    while zs([lon])[0] < lat < zn([lon])[0] and state < len(data) - 1:
        state = state + 1
        a = data[state].split()
        lat = float(a[8])
        lon = float(a[9])
        den = float(a[10])
        alt = float(a[7]) - 6371.42
        year = float(a[1])
        mlat = round(bF.dip_lat(lat, lon, alt, year), 4)
        if len(a) == 12:
            a[11] = str(mlat)
        else:
            a.append(str(mlat))
        if 10 ** 3 < den < 10 ** 8:
            cha.insert(a)

    # 获取参量
    if len(cha.data) > 0:
        datatemp = cha.data
        cha.midlon = np.median([float(x[9]) % 360. for x in datatemp])
        if cha.midlon < 30 or cha.midlon > 330:
            cha.midlon = np.median([((float(x[9]) - 180) % 360) + 180 for x in datatemp]) % 360
        utarr = [float(x[4]) + float(x[5]) / 60 + float(x[6]) / 3600 for x in datatemp]
        # cha.midut = np.median([x for x in utarr]) % 24
        cha.midut = np.median([(x - 12) % 24 + 12 for x in utarr]) % 24
        cha.midlt = (cha.midut + cha.midlon / 15) % 24

        # print(cha.midlon, cha.midut, midlt)
        yy, mm, dd = float(a[1]), float(a[2]), float(a[3])
        hh = np.median([float(x[4]) for x in datatemp])
        days = bF.orderday(str(int(yy)) + str(100 + int(mm))[1:3] + str(100 + int(dd))[1:3])
        if cha.midlt < 17.5 or cha.midlt > 23.5:
            cha.clear()
        if bF.is_magstorm(int(yy), int(days), int(hh), value):
            cha.clear()
    cha.lenth = len(cha.data)
    return cha, state + 1


# roc 0Date 1HHMMSS 2LHLMLS 3Vx_rpy 4Vy_rpy 5Vz_rpy  6Vpar
# 7VperM 8VperZ  9LogN  10Temp 11O+ 12H 13He 14NO 15GLAT 16GLON 17DipLat 18ALT
def searchROC(data, state):
    roc = bF.Orb()
    roc.name = 'ROCSAT'
    # 寻找轨道起点
    for i in range(state, len(data)):
        a = data[i].split()
        diplat = float(a[17])
        if diplat <= 15. and diplat >= -15.:
            state = i
            break
    a = data[state].split()
    diplat = float(a[17])
    # 获得轨道
    while state < len(data) - 1 and diplat > -15. and diplat < 15.:
        a = data[state].split()
        b = [0.] * 7
        b[0] = round(float(a[1][:2]) + float(a[1][3:5]) / 60 + float(a[1][6:8]) / 3600, 2)  # ut
        b[1] = round(float(a[2][:2]) + float(a[2][3:5]) / 60 + float(a[2][6:8]) / 3600, 2)  # lt
        b[2] = float(a[7])  # Vpm
        b[3] = float(a[9])  # lgN
        b[4] = float(a[17])  # Diplat
        b[5] = float(a[15])  # glat
        b[6] = float(a[16])  # glon
        roc.insert(b)
        state = state + 1
        diplat = b[4]
    if len(roc.data) > 0:
        datatemp = roc.data
        roc.midlon = np.median([float(x[6]) % 360 for x in datatemp])
        if roc.midlon < 30 or roc.midlon > 330:
            roc.midlon = np.median([((float(x[6]) - 180) % 360) + 180 for x in datatemp]) % 360
        # roc.midut = np.median([float(x[0]) for x in datatemp])
        roc.midut = np.median([(float(x[0]) - 12.0) % 24. + 12. for x in datatemp]) % 24
        roc.midlt = (roc.midut + roc.midlon / 15) % 24
        if roc.midlt < 17 or roc.midlt > 24:
            roc.clear()
    roc.lenth = len(roc.data)
    return roc, state + 15


temp = 0


def chaMERroc(chalist, roclist):
    # print(0)
    for i in range(len(chalist)):
        cha = chalist[i]
        rocout = chalist[i]
        dlttemp = 100
        dlontemp = 1000
        for j in range(len(roclist)):
            roc = roclist[j]
            # print(cha.midut, roc.midut)
            # print(cha.midlon, roc.midlon)
            cmidlt = (cha.midut + cha.midlon / 15.) % 24
            rmidlt = (roc.midut + roc.midlon / 15.) % 24
            dlt = min(abs(cmidlt - rmidlt), abs(cmidlt - rmidlt + 24), abs(cmidlt - rmidlt - 24))
            dlon = min(abs(cha.midlon - roc.midlon), abs(cha.midlon - roc.midlon + 360),
                       abs(cha.midlon - roc.midlon - 360))
            # if dlon < dlontemp:
            #     dlontemp = dlon
            if dlt < dlttemp:
                dlttemp = dlt
                dlontemp = dlon
                rocout = roc
        # dlonlsit.append(dlontemp)
        # dltlist.append(dlttemp)
        if dlttemp < 1 and dlontemp < 15:
            cha.outtext()
            rocout.outtext()
            dlonlsit.append(0)


namelast = ['1', '2', '3', '4', '21']


def mergeouttext(date):
    num = 0
    while num <= 4:
        champname, rocname = datetran(date, num)
        champfilename = oschamp + champname
        if os.path.exists(champfilename) and os.path.exists(osroc + rocname):
            datacha = bF.readfile(champfilename)
            dataroc = bF.readfile(osroc + rocname)
            chalist = []
            roclist = []
            # CHAMP
            state = 18
            while state < len(datacha) - 1:
                cha, state = search_cha(datacha, state)
                if cha.lenth != 0:
                    chalist.append(cha)
                    # cha.latden()
            num = 5
            # ROCSAT
            state = 2
            while state < len(dataroc) - 1:
                roc, state = searchROC(dataroc, state)
                if roc.lenth > 0:
                    roclist.append(roc)
                    # roc.latden()
            # merge
            chaMERroc(chalist, roclist)
        else:
            num = num + 1


value = bF.magstormexcle()


def staticLT(date):
    num = 0
    while num <= 4:
        champname, rocname = datetran(date, num)
        champfilename = oschamp + champname

        if os.path.exists(champfilename):
            datacha = bF.readfile(champfilename)
            state = 18
            while state < len(datacha) - 1:
                cha, state = search_cha(datacha, state)
                cha.date = date
                lct = cha.midlt
                filename = outpath + str(round(lct)) + '.txt'
                year = int(date[:4])
                doy = datetime.datetime.strptime(date, "%Y%m%d").timetuple().tm_yday
                hour = int(cha.midut)
                if not bF.is_magstorm(year, doy, hour, value):
                    if cha.lenth != 0:
                        with open(filename, 'a') as fout:
                            cha.outtext(fout)
            num = 5
        else:
            num = num + 1


def staticdraw(chalist, roclist, LT):
    plt.subplot(3, 1, 2)
    plt.plot(range(-30, 30), np.zeros(60), linestyle='--', c='r')
    roc = bF.Orb()
    ftemp = 0
    dtemp = 0
    btemp = 0
    ntemp = 0
    for i in range(len(chalist)):
        cha = chalist[i]
        ck = draw(cha.data, roc.data, LT)
        if ck == 'flat':
            ftemp = ftemp + 1
        elif ck == 'deep':
            dtemp = dtemp + 1
        elif ck == 'bubble':
            btemp = btemp + 1
        else:
            ntemp = ntemp + 1
    cha = bF.Orb()
    for i in range(len(roclist)):
        roc = roclist[i]
        draw(cha.data, roc.data, LT)
    print(ftemp, dtemp, btemp, ntemp)


def curveKind(lat, den):
    N = len(lat)
    gettemp = []
    getct = []
    for i in range(1, N - 1):
        if lat[i] > -25. and lat[i] < 22.:
            if (den[i - 1] - den[i]) * (den[i] - den[i + 1]) <= 0.0:
                if len(gettemp) > 0:
                    if gettemp[len(gettemp) - 1] == i - 1:
                        gettemp[len(gettemp) - 1] = i
                    else:
                        gettemp.append(i)
                        if den[i - 1] < den[i]:
                            getct.append(1)
                        else:
                            getct.append(0)
                else:
                    gettemp.append(i)
                    if den[i - 1] < den[i]:
                        getct.append(1)
                    else:
                        getct.append(0)
    # print(getct)
    # for i in range(len(getct)):
    #     print(lat[gettemp[i]])
    if len(getct) == 0:
        return 'flat'
    if len(getct) == 1:
        if getct[0] == 1:
            return 'flat'
    if len(getct) == 3:
        if getct == [1, 0, 1]:
            ctr = (10. ** den[gettemp[0]] + 10. ** den[gettemp[2]]) / (10. ** den[gettemp[1]] * 2)
            if ctr < 10.:
                return 'flat'
            else:
                return 'deep'
    if len(getct) - np.sum(getct) > 2:
        return 'bubble'
    return 'nosort'


def curveKind2(lat, den):
    N = len(lat)
    den = np.array(den)
    if len(den) > 5:
        den2 = bF.smooth(den, 5)
    else:
        den2 = den
    sigma = abs(den2 - den) / den2
    if sigma.max() > 0.05:
        return 'bubble'

    norpeak = []
    soupeak = []
    valley = []
    for i in range(N):
        alat = lat[i]
        if alat < -10 and alat > -20:
            soupeak.append(10 ** den[i])
        elif alat < 5 and alat > -5:
            valley.append(10 ** den[i])
        elif alat > 10 and alat < 20:
            norpeak.append(10 ** den[i])
    if len(soupeak) * len(norpeak) * len(valley) != 0:
        ctr = (np.array(soupeak).max() + np.array(norpeak).max()) / (2 * np.array(valley).min())
    else:
        return 'nosort'
    if ctr > 5.:
        return 'deep'
    else:
        return 'flat'


def draw(chadata, rocdata, lt):
    den = []
    lat = []
    lgN = []
    Vpm = []
    latr = []
    # print(chadata[0])
    for i in range(len(chadata)):
        a = chadata[i]
        den.append(np.log10(float(a[10])))
        lat.append(float(a[8]) - z0([float(a[9])])[0])
        # print(lt, loctime)
        # dltc.append(np.median([-3, loctime-lt, 3]))
    for i in range(len(rocdata)):
        b = rocdata[i]
        dlt = min(abs(float(b[1]) - lt), abs(float(b[1]) - lt + 24), abs(float(b[1]) - lt - 24))
        if dlt < 0.5:
            latr.append(float(b[4]))
            lgN.append(float(b[3]))
            Vpm.append(float(b[2]))
    bF.sort2(lgN, latr)
    bF.sort2(Vpm, latr)
    bF.sort2(latr, latr)
    if len(Vpm) > 60:
        Vpm2 = bF.smooth(Vpm, 60)
    else:
        Vpm2 = Vpm
    # if len(lgN)
    # lgN2 = bf.smooth(lgN, 10)
    plt.subplot(3, 1, 1)
    plt.plot(latr, lgN, linewidth=1, c='k', alpha=0.1)
    plt.xlim(-20, 20)
    plt.ylim(3.5, 7)
    plt.subplot(3, 1, 2)
    plt.plot(latr, Vpm2, linewidth=1, c='k', alpha=0.1)
    plt.xlim(-20, 20)
    plt.ylim(-75, 75)
    plt.subplot(3, 1, 3)
    ck = 'nosort'
    if len(lat) > 5:
        ck = curveKind2(lat, den)
        # plt.plot(lat, 10**np.array(den), linewidth=1, c='k', alpha=1)
        # plt.xlim(-20, 20)
        # plt.show()
        if ck == 'flat':
            plt.plot(lat, den, linewidth=1, c='r', alpha=0.1)
        elif ck == 'deep':
            plt.plot(lat, den, linewidth=1, c='g', alpha=0.1)
        elif ck == 'bubble':
            plt.plot(lat, den, linewidth=1, c='b', alpha=0.1)
        else:
            plt.plot(lat, den, linewidth=1, c='y', alpha=0.1)
        plt.axis([-20, 20, 3.5, 7])
    return ck


def write_cha_prf_info():
    for year in range(2001, 2005):
        for month in range(1, 13):
            for day in range(1, 32):
                date = str(year) + str(month + 100)[1:3] + str(day + 100)[1:3]
                # print(date)
                try:
                    staticLT(date)
                except:
                    print('error!' + str(date))


zn = bF.magline(50)
zs = bF.magline(-50)
z0 = bF.magline(0)

dlonlsit = []
dltlist = []
if __name__ == '__main__':
    outpath = 'D:/Program/BigCTR/Text/champOrb/'
    write_cha_prf_info()
    # for i in range(17, 24):
    #     print(i)
    #     fout = open('D:\\program\\BigCTR\\LTdevelop\\' + str(i * 1.0) + '.txt', 'w+')
    #     test(i * 1.)
    #     fout.close()
    #     fout = open('D:\\program\\BigCTR\\LTdevelop\\' + str(i + 0.5) + '.txt', 'w+')
    #     test(i + 0.5)
    #     fout.close()
