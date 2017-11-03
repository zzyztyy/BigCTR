import numpy as np
import matplotlib.pyplot as plt
import basicFun as bf
import datetime
import os
# from geo2mag.geo2mag_coord import loopcoord
from scipy.interpolate import interp1d

oschamp = 'D:\\sattelite data\\CHAMP\\CH-ME-2-PLP\\'
osroc = 'D:\\sattelite data\\ROCSAT\\IPEI\\'
def datetran(date, num):
    year = (date[:4])
    month = (date[4:6])
    day = (date[6:])
    champname = year + '\\CH-ME-2-PLP+'+year+'-'+month+'-'+day+'_'+str(num)+'.dat'
    dd = datetime.datetime.strptime(date, "%Y%m%d")
    days = dd.timetuple().tm_yday
    if days < 10:
        rocname = year+'\\'+year[2:4]+'00'+str(days)
    elif days < 100:
        rocname = year+'\\'+year[2:4]+'0'+str(days)
    else:
        rocname = year+'\\'+year[2:4]+str(days)
    rocname = rocname+'.dat'
    return champname, rocname

#GPS0 yy1 mm2 dd3 hh4 mm5 ss6 radius7 lat8 lon9 den10 (Temperature)
def searchCHA(data, state):
    cha = []
    midlon = 0
    midut = 0
    yy = 0
    mm = 0
    dd = 0
    hh = 0
    days=0
    #找到轨道起始位置
    for i in range(state, len(data)):
        a = data[i].split()
        lat = float(a[8])
        if lat>-70 and lat < 70:
            state = i
            break
    a = data[state].split()
    lat = float(a[8])
    #获得轨道
    midlat = 100
    while lat >-70 and lat<70 and state<len(data)-1:
        cha.append(data[state])
        state = state+1
        a = data[state].split()
        lat = float(a[8])
        if abs(lat) < midlat:
            midlat = abs(lat)
            midut = float(a[4])+float(a[5])/60+float(a[6])/3600
            midlon = float(a[9])
            yy = float(a[1])
            mm = float(a[2])
            dd = float(a[3])
            hh = float(a[4])
            days = bf.orderday(str(int(yy))+str(100+int(mm))[1:3]+str(100+int(dd))[1:3])
    midlt = (midut + midlon/15)%24
    if midlt < 17 or midlt > 23:
        cha.clear()
    if len(cha) > 0:
        if bf.isMagstorm(int(yy), int(days), int(hh), value):
            cha.clear()

    return cha, midlon, midut, state

#roc 0Date 1HHMMSS 2LHLMLS 3Vx_rpy 4Vy_rpy 5Vz_rpy  6Vpar  7VperM 8VperZ  9LogN  10Temp 11O+ 12H 13He 14NO 15GLAT 16GLON 17DipLat 18ALT
def searchROC(data, ut, midlon):
    roc=[]
    state = 0
    dtime = 0.8
    for i in range(1, len(data)):
        a = data[i].split()
        utr = float(a[1][:2])+float(a[1][3:5])/60+float(a[1][6:8])/3600
        if utr < ut+dtime and utr>ut-dtime:
            state = i
            break
    a = data[state].split()
    utr = float(a[1][:2]) + float(a[1][3:5]) / 60 + float(a[1][6:8]) / 3600
    while utr < ut+dtime and utr>ut-dtime and state<len(data)-1:
        roc.append(data[state])
        state = state+1
        a = data[state].split()
        utr = float(a[1][:2]) + float(a[1][3:5]) / 60 + float(a[1][6:8]) / 3600

    dstate, mermlat = chaMERroc(roc, midlon)
    roc2 = []
    state = state-dstate
    # mermlat = float(list(loopcoord((merlat, midlon)).mlat)[0])
    # print('mlat='+format(mermlat, '.2f'))
    # print(merlat)

    if abs(mermlat)<20:
        a = data[state].split()
        lat = float(a[15])
        # print(lat)
        while lat > -30 and lat<30 and state>1:
            state = state-1
            a = data[state].split()
            lat = float(a[15])
        # print(lat)
        # print(state)
        for i in range(state, len(data)):
            # print(lat)
            roc2.append(data[i])
            a = data[i].split()
            lat = float(a[15])
            if lat > 31 or lat < -31:
                break
    else:
        roc2.clear()
    return roc2

def chaMERroc(roc, midlon):
    dlon = 100
    state = 0
    diplat = 100
    for i in range(len(roc)):
        a = roc[i].split()
        lon = float(a[16])
        if dlon > abs(lon-midlon):
            dlon = abs(lon - midlon)
            state = i
            # lat = float(a[15])
            diplat = float(a[17])
    return len(roc) - state, diplat

def outtext(cha, roc, midlon, midut):
    chaout = []
    for i in range(len(cha)):
        a = cha[i].split()
        glat = float(a[8])
        glon = float(a[9])
        if glat< zn(glon) and glat>zs(glon):
            chaout.append(cha[i])
    fout.write('CHAMP ' + str(len(chaout)) + ' ' + format(midlon, '.2f') + ' ' + format(midut, '.2f') + '\n')
    fout.write('GPS yy mm dd hh mm ss radius lat lon den (Temperature)\n')
    for i in range(len(chaout)):
        fout.write(chaout[i])

    rocout = []
    for i in range(len(roc)):
        a = roc[i].split()
        diplat = float(a[17])
        #UT LT VperM LogN DipLat
        if abs(diplat)<20:
            b = np.zeros(5)
            b[0] = float(a[1][:2])+float(a[1][3:5])/60+float(a[1][6:8])/3600
            b[1] = float(a[2][:2])+float(a[2][3:5])/60+float(a[2][6:8])/3600
            b[2] = float(a[7])
            b[3] = float(a[9])
            b[4] = float(a[17])
            bout = ''
            for i in range(5):
                bout = bout + format(b[i], '.2f') + ' '
            rocout.append(bout + '\n')
            # fout.write(str(b).replace('[','').replace(']','')+'\n')
    fout.write('ROCSAT ' + str(len(rocout)) + '\n')
    fout.write('UT LT VperM LogN DipLat\n')
    for i in range(len(rocout)):
        fout.write(rocout[i])

def mergeouttext(date):
    num = 1
    while num <= 4:
        champname, rocname = datetran(date, num)
        champfilename = oschamp + champname
        if os.path.exists(champfilename) and os.path.exists(osroc + rocname):
            datacha = bf.readfile(champfilename)
            dataroc = bf.readfile(osroc + rocname)
            state = 18
            midut = 0.01
            while state < len(datacha)-1 and midut>0.001:
                cha, midlon, midut, state = searchCHA(datacha, state)
                # print(state, midut)
                if len(cha) != 0:
                    roc = searchROC(dataroc, midut, midlon)
                    if len(roc) != 0:
                        # print(len(cha))
                        # print(len(roc))
                        outtext(cha, roc, midlon, midut)
            # print(1111)
            num = 5
        else:
            num = num + 1

def test():
    for year in range(2001, 2005):
        for month in range(1, 13):
            for day in range(1, 32):
                date = str(year)+str(month+100)[1:3]+str(day+100)[1:3]
                print(date)
                try:
                    mergeouttext(date)
                except:
                    print('error!')
                    print(date)

value = bf.magstormexcle()

def magline( ns):#input longitude output 40 maglat
    #type of ns is bool,north=true
    if ns:
        f = open("50maglatline.txt", 'r')
    else:
        f = open("-50maglatline.txt", 'r')
    ml = f.readlines()
    y = []
    x = []
    for i in range(len(ml)):
        a = ml[i].split()
        y.append(float(a[0]))
        x.append(float(a[1]))
    z = interp1d(x, y, kind='cubic')
    return z

zn = magline(True)
zs = magline(False)

if __name__ == '__main__':
    fout = open('merged.txt', 'w+')
    test()
    fout.close()
