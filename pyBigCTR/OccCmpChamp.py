import numpy as np
import matplotlib.pyplot as plt
import os

from pyGeoMagApex import dipLat

from StaticOccPrf import get_one_prf, Prf, caltime
from basicFun import dip_lat


def cmp_occ_plp():
    files = ['D:/Program/BigCTR/Text/occPrfAfrica.txt', 'D:/Program/BigCTR/Text/occPrfAmerican.txt',
             'D:/Program/BigCTR/Text/occPrfAsia.txt', 'D:/Program/BigCTR/Text/occPrfPacific.txt']
    for file in files:
        get_prf = False
        with open(file, 'r') as f:
            text = f.readlines()
            text_prf = []
            line_num = 0
            while line_num < len(text):
                s = text[line_num]
                # print(s)
                if len(s) > 3:
                    if s[:3] == '200':
                        get_prf = True
                    text_prf.append(s)
                else:
                    if get_prf:
                        text_prf.append(s)
                        p = get_one_prf(text_prf)
                        text_prf.clear()

                        mlat = p.get_mlat()
                        if -10 < mlat < 10:
                            champ_orb = get_champ_orb(p.year, p.month, p.day, np.median(p.lons), p.lct)
                            draw_occ_plp(champ_orb, p)

                        get_prf = False
                line_num += 1


def get_champ_orb(year, month, day, lon, lct):
    path = 'D:/SpaceScienceData/CHAMP/CH-ME-2-PLP/'
    file_a = path + str(year) + '/' + 'CH-ME-2-PLP+' + str(year) + '-' + str(month).zfill(2) + '-' + str(day).zfill(2)
    file_bs = ['_1.dat', '_2.dat', '_3.dat', '_4.dat']
    get_file = False
    i = 0
    while not get_file and i < 4:
        get_file = os.path.exists(file_a + file_bs[i])
        i += 1

    orb = {'lat': [], 'lon': [], 'alt': [], 'den': [], 'mlat': []}
    if get_file:
        file = file_a + file_bs[i - 1]
        with open(file, 'r') as f:
            text = f.readlines()
            for s in text:
                if s[0] != '#':
                    a = s.split()
                    try:
                        hh, mm, ss, ra, lat, clon, den = [float(x) for x in a[4:11]]
                    except:
                        print(s, file)
                    dlct = (hh + mm / 60 + ss / 3600 + lon / 15 - lct) % 24
                    if min(abs(dlct - 24), dlct) < 0.5:
                        dlon = (clon - lon) % 360
                        if min(dlon, abs(dlon - 360)) < 12.5:
                            mlat = dip_lat(lat, clon, ra - 6371, year)
                            if -15 < mlat < 15:
                                orb['lat'].append(lat)
                                orb['lon'].append(clon)
                                orb['alt'].append(ra - 6371)
                                orb['den'].append(den)
                                orb['mlat'].append(dip_lat(lat, clon, ra - 6371, year))
    return orb


def draw_occ_plp(champ_orb, one_prf):
    if len(champ_orb['lat']) > 20:
        cmap = 'jet'
        plt.scatter(champ_orb['mlat'], champ_orb['alt'], c=champ_orb['den'], marker='o', s=10, cmap=cmap)
        plt.scatter(one_prf.mlats, one_prf.alts, c=one_prf.dens, marker='s', s=10, cmap=cmap, vmin=0)
        # plt.ylim([250, 450])
        ymax = np.max(champ_orb['alt'])
        plt.axis([-15, 15, ymax - 80, ymax + 20])
        title = '__'.join([str(x) for x in [one_prf.year, one_prf.month,
                                            one_prf.day, one_prf.lct, round(float(np.median(one_prf.lons)), 2)]])
        plt.title(title)
        plt.colorbar()
        plt.savefig('D:/Program/BigCTR/Picture/cmp_occ_plp/lowLat/' + title + '.png')
        # plt.show()
        plt.close()


if __name__ == '__main__':
    cmp_occ_plp()
