import numpy as np
import matplotlib.pyplot as plt
from bc3newMergeOrb import Orb, curveKind2, staticdraw
import basicFun as bf
import scipy.signal as signal


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
        dloc = min(abs(lon - loc), abs(lon - loc + 360), abs(lon - loc - 360))
        chose = (year in ['2001'])  # (month in monrange) * (dloc < 45.) * (year in ['2001', '2002'])
        if chose:
            temp = temp + 1
            if cha.name == 'ROCSAT':
                # temp = temp
                roclist.append(cha)
            elif cha.name == 'CHAMP':
                chalist.append(cha)
            else:
                print(cha.name)
        startline = nextline
    # print(temp)
    # staticdraw(chalist, roclist, LT)
    static_season_lon(chalist, LT)
    # plt.savefig(path + 'picture\\' + 'LT=' + str(LT) + season + location + '.png')
    # plt.close()


def static_season_lon(chalist, LT):
    flat = []
    deep = []
    bubble = []
    nosort = []
    for i in range(len(chalist)):
        cha = chalist[i]
        den, lat = [], []
        for i in range(len(cha.data)):
            a = cha.data[i]
            den.append(np.log10(float(a[10])))
            lat.append(float(a[8]) - z0([float(a[9])])[0])
        ck = curveKind2(lat, den)
        doy = bf.orderday(cha.date)
        month = int(cha.date[4:6])
        lon = (cha.midlon + 180) % 360 - 180
        if ck == 'flat':
            flat.append([lon, month, doy])
        elif ck == 'deep':
            deep.append([lon, month, doy])
        elif ck == 'bubble':
            bubble.append([lon, month, doy])
        else:
            nosort.append([lon, month, doy])
    plt.scatter([x[0] for x in flat], [x[2] for x in flat], c='r', s=3)
    plt.scatter([x[0] for x in deep], [x[2] for x in deep], c='g', s=3)
    plt.scatter([x[0] for x in bubble], [x[2] for x in bubble], c='b', s=3)
    # plt.scatter([x[0] for x in nosort], [x[1] for x in nosort], c='k', s=3)
    # static_draw(flat, deep, bubble, nosort)
    # print(len(flat), len(deep), len(bubble), len(nosort))
    # preDrawContourf(flat, deep, bubble, nosort)


def staticbin(alist):
    abin = np.array([[0] * 24] * 12)
    # deepbin = np.array([[0]*12]*12)
    # bubblebin = np.array([[0]*12]*12)
    # nosortbin = np.array([[0]*12]*12)
    for i in range(len(alist)):
        month = int(alist[i][1]) - 1
        lon = int((alist[i][0] + 180.) / 15)
        abin[month][lon] = abin[month][lon] + 1
    return abin


def static_draw(flat, deep, bubble, nosort):
    flatbin = staticbin(flat)
    deepbin = staticbin(deep)
    bubblebin = staticbin(bubble)
    nosortbin = staticbin(nosort)
    perbin = np.array([[-1.] * 24] * 12)
    for i in range(12):
        for j in range(24):
            asum = flatbin[i][j] + deepbin[i][j] + bubblebin[i][j] + nosortbin[i][j]
            if asum != 0:
                # print(deepbin[i][j]/asum)
                perbin[i][j] = (deepbin[i][j] + bubblebin[i][j]) / asum
            else:
                print(i, j)

    # for i in range(12):
    #     perbin[i] = perbin[i]/np.max(perbin[i])

    with open('BubbleAndDeep.txt', 'w') as file:
        for i in range(len(perbin)):
            arr = [format(x, '.3f') for x in perbin[i]]
            lines = ' '.join(arr)
            lines = lines + '\n'
            file.writelines(lines)

            # print(perbin)
            # print(flatbin)
            # print(deepbin)
            # perbin = signal.medfilt2d(perbin, (3, 3))

            # plt.imshow(perbin, cmap='jet', aspect='auto', vmax=0.8)
            # plt.title('bubble&deep')
            # plt.colorbar()
            # plt.yticks(np.arange(0, 12), np.arange(1, 13))
            # plt.xticks(np.arange(0, 25, 2)-0.5, np.arange(-180, 181, 30))
            # plt.axis([-0.5, 23.5, -0.5, 11.5])
            # plt.show()


def preDrawContourf(flat, deep, bubble, nosort):
    x = []
    y = []
    z = []
    x = x + [x[0] for x in flat] + [x[0] for x in deep] + [x[0] for x in bubble] + \
        [x[0] + 360 for x in flat] + [x[0] + 360 for x in deep] + [x[0] + 360 for x in bubble]
    # [x[0] - 360 for x in flat] + [x[0] - 360 for x in deep] + [x[0] - 360 for x in bubble]
    y = y + [x[1] for x in flat] + [x[1] for x in deep] + [x[1] for x in bubble] + \
        [x[1] + 365 for x in flat] + [x[1] + 365 for x in deep] + [x[1] + 365 for x in bubble]
    z = z + [x[0] * 0 for x in flat] + [x[1] * 0 + 1 for x in deep] + [x[1] * 0 + 1 for x in bubble] + \
        [x[0] * 0 for x in flat] + [x[1] * 0 + 1 for x in deep] + [x[1] * 0 + 1 for x in bubble]
    print(z)
    bf.drawcountourf(x, y, z)


def test(LT):
    print(LT)
    path = 'D:\\program\\BigCTR\\LTdevelop\\text_onlyChamp\\'
    fin = []
    for i in range(19, 24):
        fin = fin + bf.readfile(path + format(i * 1.0, '.1f') + '.txt') \
              + bf.readfile(path + format(i - 0.5, '.1f') + '.txt')
    # lenfin = len(fin)
    for i in range(1):
        for j in range(1):
            # plt.figure(figsize=[10, 10], dpi=150)
            # plt.subplots_adjust(hspace=0.1, left=0.1, bottom=0.05, right=0.97, top=0.97)
            sort_month_lon(season[i], location[j], fin, LT, path)
            # plt.subplot(3, 1, 1)
            # plt.title(LT)
            # plt.axis([0, 366, 0, 360])
            # plt.savefig(str(LT)+'.png')
            # plt.close()
            plt.show()


z0 = bf.magline(0)
if __name__ == '__main__':
    for i in range(18, 19):
        # print(i)
        test(i)
        # plt.axis([0, 360, 0, 366])
        # plt.savefig('b.png')
        # plt.close()
