#!/usr/bin/env python
# -*- coding: cp936 -*-
import numpy as np
import matplotlib.pyplot as plt
import basicFun as bf
from champ3 import search_orbit
from scipy.interpolate import interp1d
import datetime
import os

#champ 0GPS 1YYYY 2MM 3DD 4hh 5mm 6ss.ssss 7radius 8latitude 9longitude 10electron
#roc 0Date 1HHMMSS 2LHLMLS 3Vx_rpy 4Vy_rpy 5Vz_rpy  6Vpar  7VperM 8VperZ  9LogN  10Temp 11O+ 12H 13He 14NO 15GLAT 16GLON 17DipLat 18ALT

def datatran(date, num):
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

oschamp = 'D:\\sattelite data\\CHAMP\\CH-ME-2-PLP\\'
osroc = 'D:\\sattelite data\\ROCSAT\\IPEI\\'
magstovalue = bf.magstormexcle()
def daypic(date):
    num = 1
    while num <= 4:
        champname, rocname = datatran(date, num)
        champfilename = oschamp+champname
        # print(champfilename)
        if os.path.exists(champfilename):
            # datachamp = bf.readfile(champfilename)
            datachamp = bf.readfilenomagstorm(champfilename, date, magstovalue)
            dataroc = bf.readfile(osroc+rocname)
            # print(datachamp)
            state = 0
            temp = 0
            timetemp = 7.9
            plt.figure(figsize=[10, 10], dpi=300)
            plt.subplots_adjust(hspace=0.1, left=0.1, bottom=0.05, right=0.97, top=0.97)
            titleloctime = []
            legendlon = []
            # while state < len(datachamp):
            title = date
            while state < len(datachamp):
                # print(state)
                orb = search_orbit(datachamp, state)
                if len(orb) > 1:
                    # print(orb)
                    state = int(float(orb[len(orb)-1]))
                else:
                    # print(orb)
                    break
                if orb[int(len(orb)/2)][4] > timetemp:
                    # temp = 0
                    if temp != 0:
                        ptitle = title+' LT='+format(np.array(titleloctime).mean(), '.2f')+'h'
                        titleloctime.clear()
                        plt.title(ptitle)
                        plt.subplot(3, 1, 3)
                        plt.legend(legendlon, loc='lower right')
                        legendlon.clear()
                        plt.savefig('D:\\program\\picBigCTR\\'+title+'_'+str(int((timetemp+0.2)/8)) +'.png')
                    plt.close()

                    timetemp = timetemp + 8.
                    plt.figure(figsize=[10, 10], dpi=300)
                    plt.subplots_adjust(hspace=0.1, left=0.1, bottom=0.05, right=0.97, top=0.97)
                    temp=0
                else:
                    dtemp, aloctime, alon = draw(orb, dataroc, temp, timetemp)
                    if dtemp == 1:
                        titleloctime.append(aloctime)
                        legendlon.append(alon)
                    temp = temp + dtemp

            # print(titleloctime)

            if temp != 0:
                ptitle = title + ' LT=' + format(np.array(titleloctime).mean(), '.2f') + 'h'
                titleloctime.clear()
                plt.title(ptitle)
                plt.subplot(3, 1, 3)
                plt.legend(legendlon, loc='lower right')
                legendlon.clear()
                plt.savefig('D:\\program\\picBigCTR\\'+title+'_'+str(int((timetemp+0.2)/8)) + '.png')
            plt.close()
            num = 5
        else:
            num = num+1


def sort2(l1, l2):  # 按l2大小为l1排序
    l3 = []
    for i in range(len(l1)):
        l3.append([l1[i], l2[i]])
    # print(l3)
    c = sorted(l3, key=lambda x: x[1])
    for i in range(len(l1)):
        l1[i] = c[i][0]
    return l1

def merge(orb, roc):
    middot = orb[int(len(orb)/2)]
    midlon = float(middot[9])
    midlt = (middot[4]+middot[5]/60.+middot[6]/3600.+middot[9]/15.) % 24
    lat = []
    dlt = []
    lgN = []
    vpm = []
    lon = []
    for i in range(1, len(roc)):
        a = roc[i].split()
        if min(abs(float(a[16])-midlon), abs(float(a[16])+360-midlon), abs(float(a[16])-360-midlon)) < 12.5:
            lt = float(a[2][:2])+float(a[2][3:5])/60+float(a[2][6:8])/3600
            adlt = (midlt - lt) % 24
            if adlt > 12:
                adlt = adlt - 24
            if abs(adlt) < 1:
                lat.append(float(a[15]))
                lon.append(float(a[16]))
                dlt.append(lt)
                lgN.append(float(a[9]))
                vpm.append(float(a[7]))
    lgN = sort2(lgN, lat)
    lon = sort2(lon, lat)
    dlt = sort2(dlt, lat)
    vpm = sort2(vpm, lat)
    lat = sort2(lat, lat)
    return lat, lon, dlt, lgN, vpm


cmap = ['Greys', 'Blues', 'Reds', 'PuRd', 'Greens', 'autumn']
color = ['k', 'b', 'r', 'purple', 'g', 'y']
def draw(orbit, roc, temp, timetemp):
    mlat = list()
    den = list()
    middot = orbit[int(len(orbit) / 2)]
    midlon = float(middot[9])
    midmlat = bf.magline(0)(float(midlon))
    midlt = (middot[4] + middot[5] / 60. + middot[6] / 3600. + middot[9] / 15.) % 24
    # print(midlt)
    if midlt > 17. and midlt < 23. and float(middot[4]) < timetemp:
        # print(midlt)
        plt.subplot(3, 1, 3)
        plt.xlabel('MagLat')
        plt.ylabel('CHAMP lgNe')
        plt.axis([-50, 50, 2, 7])
        for i in range(len(orbit) - 1):
            a = orbit[i]
            mlat.append(a[8]-midmlat)
            den.append(a[10])
        plt.plot(mlat, np.log10(den), linewidth=1, c=color[temp])
        plt.subplot(3, 1, 2)
        plt.ylabel('Vpm')
        plt.axis([-50, 50, -150, 150])
        mlatr, dlt, lgN, vpm = merge(orbit, roc)
        # print(dlt)
        plt.scatter(mlatr, vpm, s=0.1, c=dlt, cmap=cmap[temp], vmax=1, vmin=0.75, marker='o')
        plt.plot(mlatr, vpm, linewidth=0.3, c=color[temp], alpha=0.25)
        plt.subplot(3, 1, 1)
        plt.ylabel('ROCSAT lgNe')
        plt.axis([-50, 50, 4, 7])
        plt.scatter(mlatr, lgN, s=0.1, c=dlt, cmap=cmap[temp], vmax=1, vmin=0.75, marker='.')
        plt.plot(mlatr, lgN, linewidth=0.3, c=color[temp], alpha=0.25)
        # print(midlt)
        return 1, midlt, midlon
    return 0, midlt, midlon

def daytext(date):
    num = 1
    while num <= 4:
        champname, rocname = datatran(date, num)
        champfilename = oschamp + champname
        if os.path.exists(champfilename) and os.path.exists(osroc + rocname):
            fout = open('mergedOrb\\'+date+'.txt', 'w+')
            datachamp = bf.readfilenomagstorm(champfilename, date, magstovalue)
            dataroc = bf.readfile(osroc + rocname)
            state = 0
            temp = 0
            while state < len(datachamp):
                orb = search_orbit(datachamp, state)
                if len(orb) > 1:
                    state = int(float(orb[len(orb) - 1]))
                else:
                    break

                dtemp, latr, lonr, lt, lgN, Vpm = outtext(orb, dataroc)
                if dtemp == 1:
                    fout.write('CHAMP '+str(len(orb))+'\n')
                    fout.write('GPS yy mm dd hh mm ss radius lat lon den (Temperature)\n')
                    for i in range(len(orb)-1):
                        a = str(orb[i]).replace('[', '').replace(']', '').replace(',', ' ').replace('\n', ' ')
                        fout.write(a+'\n')
                    fout.write('ROCSAT '+str(len(latr))+'\n')
                    fout.write('lat lon dlt lgN Vpm\n')
                    for i in range(len(latr)):
                        fout.write(str(latr[i])+' '+str(lonr[i])+' '+str(lt[i])+' '+str(lgN[i])+' '+str(Vpm[i])+'\n')
                temp = temp + dtemp

            fout.close()
            if temp == 0:
                os.remove('mergedOrb\\'+date+'.txt')
            num = 5
        else:
            num = num + 1

def outtext(orbit, roc):
    middot = orbit[int(len(orbit) / 2)]
    midlon = float(middot[9])
    midmlat = bf.magline(0)(float(midlon))
    midlt = (middot[4] + middot[5] / 60. + middot[6] / 3600. + middot[9] / 15.) % 24
    if midlt > 17. and midlt < 23.:
        latr, lonr, lt, lgN, vpm = merge(orbit, roc)
        if len(latr) == 0:
            return 0, [], [], [], [], []
        else:
            if midmlat<latr[0]-0 or midmlat > latr[len(latr)-1]+0:
                return 0, [], [], [], [], []
            else:
                return 1, latr, lonr, lt, lgN, vpm
    return 0, [], [], [], [], []

if __name__ == '__main__':
    for year in range(2001, 2005):
        for month in range(1, 13):
            for day in range(1, 32):
                date = str(year)+str(month+100)[1:3]+str(day+100)[1:3]
                try:
                    daytext(date)
                except:
                    print(date)
