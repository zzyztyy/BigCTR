import datetime
import os

import matplotlib.pyplot as plt
import numpy as np
# from geo2mag.geo2mag_coord import loopcoord
from scipy.interpolate import interp1d

import basicFun as bf


# ut0 lt1 Vpm2 lgN3 Diplat4 glat5 glon6
class Orb(object):
    def __init__(self):
        self.name = 'not define'
        self.lenth = 0
        self.data = []
        self.midlon = 0.
        self.midut = 0.
    def insert(self, a):
        self.data.append(a)
    def latden(self):
        xtemp = 0
        ytemp = 0
        alldata = self.data
        if self.name == 'CHAMP':
            xtemp = 8
            ytemp = 10
            # alldata = [x.split() for x in alldata]
        elif self.name == 'ROCSAT':
            xtemp = 4
            ytemp = 3
        else:
            print('Error')
        lat = [float(x[xtemp]) for x in alldata]
        den = [float(x[ytemp]) for x in alldata]
        plt.plot(lat, den)
        plt.show()
    def clear(self):
        self.data.clear()
    def outtext(self):
        fout.write(self.name+' '+str(self.lenth)+' '+format(self.midlon, '.2f')+' '+format(self.midut, '.2f')+'\n')
        if self.name == 'CHAMP':
            fout.write('GPS yy mm dd hh mm ss radius lat lon den (Temperature)\n')
        elif self.name == 'ROCSAT':
            fout.write('ut lt Vpm lgN Diplat glat glon\n')
        for i in range(self.lenth):
            outstr = str(self.data[i]).replace('[', '').replace(']', '').replace(',', ' ').replace('\n', '')
            outstr = outstr.replace("'", '')
            fout.write(outstr + '\n')

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
    cha = Orb()
    cha.name = 'CHAMP'
    #找到轨道起始位置
    for i in range(state, len(data)):
        a = data[i].split()
        lat, lon = float(a[8]), float(a[9])
        if lat > zs([lon])[0] and lat < zn([lon])[0]:
            state = i
            break
    a = data[state].split()
    lat, lon = float(a[8]), float(a[9])
    #获得轨道
    while lat > zs([lon])[0] and lat < zn([lon])[0] and state < len(data)-1:
        state = state+1
        a = data[state].split()
        cha.insert(a)
        lat = float(a[8])
        lon = float(a[9])
    #获取参量
    if len(cha.data)>0:
        datatemp = cha.data
        cha.midlon = np.median([float(x[9]) for x in datatemp])
        cha.midut = np.median([float(x[4])+float(x[5])/60+float(x[6])/3600 for x in datatemp])
        midlt = (cha.midut + cha.midlon / 15) % 24
        # print(cha.midlon, cha.midut, midlt)
        yy, mm, dd = float(a[1]), float(a[2]), float(a[3])
        hh = np.median([float(x[4]) for x in datatemp])
        days = bf.orderday(str(int(yy)) + str(100 + int(mm))[1:3] + str(100 + int(dd))[1:3])
        if midlt < 17 or midlt > 23:
            cha.clear()
        if bf.isMagstorm(int(yy), int(days), int(hh), value):
            cha.clear()
    cha.lenth = len(cha.data)
    return cha, state+1

#roc 0Date 1HHMMSS 2LHLMLS 3Vx_rpy 4Vy_rpy 5Vz_rpy  6Vpar  7VperM 8VperZ  9LogN  10Temp 11O+ 12H 13He 14NO 15GLAT 16GLON 17DipLat 18ALT
def searchROC(data, state):
    roc = Orb()
    roc.name = 'ROCSAT'
    # 寻找轨道起点
    for i in range(state, len(data)):
        a = data[i].split()
        diplat = float(a[17])
        if diplat <= 20. and diplat >= -20.:
            state = i
            break
    a = data[state].split()
    diplat = float(a[17])
    #获得轨道
    while state < len(data)-1 and diplat > -20. and diplat < 20.:
        a = data[state].split()
        b = [0]*7
        b[0] = round(float(a[1][:2]) + float(a[1][3:5]) / 60 + float(a[1][6:8]) / 3600, 2) #ut
        b[1] = round(float(a[2][:2]) + float(a[2][3:5]) / 60 + float(a[2][6:8]) / 3600, 2) #lt
        b[2] = float(a[7]) #Vpm
        b[3] = float(a[9]) #lgN
        b[4] = float(a[17]) #Diplat
        b[5] = float(a[15]) #glat
        b[6] = float(a[16]) #glon
        roc.insert(b)
        state = state+1
        diplat = b[4]
    if len(roc.data) > 0:
        datatemp = roc.data
        roc.midlon = np.median([float(x[6]) for x in datatemp])
        roc.midut = np.median([float(x[0]) for x in datatemp])
        midlt = (roc.midut + roc.midlon / 15) % 24
        if midlt < 0 or midlt > 24:
            roc.clear()
    roc.lenth = len(roc.data)
    return roc, state+15

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
            cmidlt = (cha.midut + cha.midlon/15.)%24
            rmidlt = (roc.midut + roc.midlon/15.)%24
            dlt = min(abs(cmidlt-rmidlt), abs(cmidlt-rmidlt+24), abs(cmidlt-rmidlt-24))
            dlon = min(abs(cha.midlon-roc.midlon), abs(cha.midlon-roc.midlon+360), abs(cha.midlon-roc.midlon-360))
            # if dlon < dlontemp:
            #     dlontemp = dlon
            if dlt < dlttemp:
                dlttemp = dlt
                dlontemp =dlon
                rocout = roc
        # dlonlsit.append(dlontemp)
        # dltlist.append(dlttemp)
        if dlttemp < 1. and dlontemp < 45:
            cha.outtext()
            rocout.outtext()
            dlonlsit.append(0)

def mergeouttext(date):
    num = 1
    while num <= 4:
        champname, rocname = datetran(date, num)
        champfilename = oschamp + champname
        if os.path.exists(champfilename) and os.path.exists(osroc + rocname):
            datacha = bf.readfile(champfilename)
            dataroc = bf.readfile(osroc + rocname)
            chalist = []
            roclist = []
            #CHAMP
            state = 18
            while state < len(datacha)-1:
                cha, state = searchCHA(datacha, state)
                if cha.lenth != 0:
                    chalist.append(cha)
                    # cha.latden()
            num = 5
            #ROCSAT
            state = 2
            while state < len(dataroc)-1:
                roc, state = searchROC(dataroc, state)
                if roc.lenth > 0:
                    roclist.append(roc)
                    # roc.latden()
            #merge
            chaMERroc(chalist, roclist)
        else:
            num = num + 1

value = bf.magstormexcle()

def test():
    for year in range(2001, 2005):
        for month in range(1, 13):
            for day in range(1, 33):
                date = str(year)+str(month+100)[1:3]+str(day+100)[1:3]
                # print(date)
                try:
                    mergeouttext(date)
                except:
                    print('error!'+str(date))

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

dlonlsit = []
dltlist = []
if __name__ == '__main__':
    fout = open('merged45.txt', 'w+')
    test()
    # plt.subplot(2, 1, 1)
    # plt.scatter(range(len(dlonlsit)), dlonlsit, s=1)
    # # plt.ylim(0, 20)
    # plt.subplot(2, 1, 2)
    # plt.scatter(range(len(dltlist)), dltlist, s=1)
    # # plt.ylim(0, 6)
    # plt.show()
    fout.close()
    print(len(dlonlsit))
