import numpy as np
import matplotlib.pyplot as plt
import time
import datetime

from basicFun import dip_lat

locations = ['American', 'Africa', 'Pacific', 'Asia']


class Prf(object):
    def __init__(self):
        self.season = 'sum'
        self.loc = 'north'
        self.lct = 0
        self.dens = []
        self.alts = []
        self.lons = []
        self.lats = []
        self.mlats = []
        self.year = 0
        self.month = 0
        self.day = 0

    def set_prf(self):
        if self.month in [5, 6, 7, 8]:
            self.season = 'sum'
        elif self.month in [11, 12, 1, 2]:
            self.season = 'win'
        else:
            self.season = 'spr'

        mlat = self.get_mlat()
        if -20 < mlat < -10:
            self.loc = 'south'
        elif -5 < mlat < 5:
            self.loc = 'equator'
        elif 10 < mlat < 20:
            self.loc = 'north'
        else:
            self.loc = 'ignore'

    def get_data(self, den, alt, lon, lat):
        self.dens.append(den)
        self.alts.append(alt)
        self.lons.append(lon)
        self.lats.append(lat)
        self.mlats.append(dip_lat(lat, lon, lat, self.year))

    def get_mlat(self):
        glat = np.median(self.lats)
        glon = np.median(self.lons)
        galt = np.median(self.alts)
        mlat = dip_lat(glat, glon, galt, self.year)
        return mlat

    def draw(self):
        color = {'win': 'b', 'sum': 'r', 'spr': 'g'}
        # plt.plot(self.dens, self.alts, c=color[self.season], lw=1)
        plt.scatter(np.array(self.dens) / 1000000, self.alts, c='', s=10, edgecolors=color[self.season])


def get_one_prf(text_prf):
    # lats = []
    p = Prf()
    for s in text_prf:
        if len(s) > 3:
            if s[:3] == '200':
                a = s.split()
                p.year, p.month, p.day = [int(x) for x in a[0].split('/')]
                # lct = (float(a[2].replace('[', '').replace(',', '')) + float(a[3].replace(']', ''))) / 2
                lct = float(a[3].replace(']', ''))
                p.lct = round(lct, 2)
            else:
                lat, lon, alt, den = [float(x) for x in s.split()]
                p.get_data(den, alt, lon, lat)
                # lats.append(lat)
        else:
            p.set_prf()
    return p


def caltime(date1, date2):
    date1 = time.strptime(date1, "%Y/%m/%d")
    date2 = time.strptime(date2, "%Y/%m/%d")
    date1 = datetime.datetime(date1[0], date1[1], date1[2])
    date2 = datetime.datetime(date2[0], date2[1], date2[2])
    return (date2 - date1).days


def static_date_distribution():
    days_count = []
    with open('D:/Program/BigCTR/Text/occPrfJicamarca.txt', 'r') as f:
        text = f.readlines()
        for s in text:
            if len(s) != 0 and s[:3] == '200':
                # print(s)
                date = s.split()[0]
                days_count.append(caltime('2001/1/1', date))
    print(days_count)
    plt.hist(days_count, bins=400)
    plt.xticks(range(365, 8 * 365 + 1, 365), ['2002/1/1', '2003/1/1', '2004/1/1', '2005/1/1',
                                              '2006/1/1', '2007/1/1', '2008/1/1', '2009/1/1'])
    plt.show()


def sort_lt_year_season_lat():
    prf_dict = {}
    get_prf = False
    with open('D:/Program/BigCTR/Text/occPrf' + location + '.txt', 'r') as f:
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

                    if p.year not in prf_dict:
                        prf_dict[p.year] = {}
                    if round(p.lct) not in prf_dict[p.year]:
                        prf_dict[p.year][round(p.lct)] = []
                    prf_dict[p.year][round(p.lct)].append(p)

                    get_prf = False
            line_num += 1
    return prf_dict


def draw_prf(prf_dict):
    sub_fig = {'south': 1, 'equator': 2, 'north': 3}
    for year in range(2002, 2009):
        for lct in range(18, 24):
            plt.figure(figsize=[12, 6], dpi=75)
            plt.subplot(1, 3, 1)
            plt.subplot(1, 3, 2)
            plt.title(location + str(year) + '/' + str(lct))
            for p in prf_dict[year][lct]:
                if p.loc != 'ignore':
                    plt.subplot(1, 3, sub_fig[p.loc])
                    p.draw()
                    plt.ylim([250, 450])
                    plt.xlim([-0.5, 3])
            plt.subplot(1, 3, 3)
            p1, = plt.plot([], [], c='r')
            p2, = plt.plot([], [], c='b')
            p3, = plt.plot([], [], c='g')
            plt.legend([p1, p2, p3], ['sum', 'win', 'spr'])
            # plt.show()
            plt.savefig('D:/Program/BigCTR/Picture/occPrfStatic/' +
                        location + '_' + str(year) + '_LocalTime=' + str(lct))
            plt.close()


if __name__ == '__main__':
    for location in locations:
        draw_prf(sort_lt_year_season_lat())
