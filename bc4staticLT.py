import numpy as np
import matplotlib.pyplot as plt
from bc3newMergeOrb import Orb, staticdraw, draw
import basicFun as bf


def getoneOrb(text, startline):
    cha = Orb()
    # nextline = startline
    a = text[startline].split()
    # print(text[startline])
    cha.name = a[0]
    cha.lenth = int(a[1])
    cha.date = a[2]
    cha.midlon = float(a[3])
    cha.midut = float(a[4])
    cha.midlt = float(a[5])
    for i in range(cha.lenth):
        a = text[startline + i + 2].split()
        cha.insert([float(x) for x in a])
    nextline = startline + cha.lenth + 2
    # print(text[startline+cha.lenth+2])
    return cha, nextline


season = ['sum', 'spr', 'win']
location = ['Eur', 'Asi', 'Pac', 'Ame']


def sort_month_lon(season, location, fin, LT, path):
    monrange = []
    if season == 'sum':
        monrange = ['05', '06', '07', '08']
    elif season == 'win':
        monrange = ['01', '02', '11', '12']
    elif season == 'spr':
        monrange = ['03', '04', '09', '10']
    else:
        print(season)

    loc = np.NAN
    if location == 'Eur':
        loc = 15
    elif location == 'Asi':
        loc = 105
    elif location == 'Pac':
        loc = 195
    elif location == 'Ame':
        loc = 285
    else:
        print(location)

    startline = 0
    chalist = []
    roclist = []
    temp = 0
    while startline < len(fin):
        cha, nextline = getoneOrb(fin, startline)
        month = cha.date[4:6]
        year = cha.date[:4]
        lon = cha.midlon % 360
        chose = (month in monrange) * (abs(lon - loc) < 45.) * (year in ['2003', '2004'])
        if chose:
            temp = temp + 1
            if cha.name == 'ROCSAT':
                roclist.append(cha)
            elif cha.name == 'CHAMP':
                chalist.append(cha)
            else:
                print(cha.name)
        startline = nextline
    # print(temp)
    staticdraw(chalist, roclist, LT)
    plt.savefig(path + 'LT=' + str(LT) + season + location + '.png')
    plt.close()


def test(LT):
    print(LT)
    path = 'D:\\program\\BigCTR\\LTdevelop\\'
    fin = bf.readfile(path + 'text\\' + format(LT * 1.0, '.1f') + '.txt') \
          + bf.readfile(path + 'text\\' + format(LT - 0.5, '.1f') + '.txt')
    # lenfin = len(fin)
    for i in range(3):
        for j in range(4):
            plt.figure(figsize=[10, 10], dpi=150)
            plt.subplots_adjust(hspace=0.1, left=0.1, bottom=0.05, right=0.97, top=0.97)
            sort_month_lon(season[i], location[j], fin, LT, path)


if __name__ == '__main__':
    for i in range(18, 24):
        # print(i)
        test(i)
