import matplotlib.pyplot as plt
import numpy as np
from cycler import cycler

from basicFun import get_one_orb, get_curve_kind, repair_bubble, julday, date_tran, orderday


def read_cha(lct, what):
    """
    :param lct: local time
    :param what: 0 for draw single picture, 1 for drawing all profiles, 2 for counting ctrs, 3 for repaired steps
    :return: 0 or 1 counts, 2 ctr list, 3 num_ck dict
    """
    text = open('D:/Program/BigCTR/Text/champOrb/' + str(lct * 1.0) + '.txt').readlines()
    temp_line = 0
    all_lines = len(text)

    if what == 1 or what == 0:
        count = {'flat': 0, 'deep': 0, 'bubble': 0, 'error': 0}
        while temp_line < all_lines:
            cha, temp_line = get_one_orb(text, temp_line)
            if cha.ck != 'loss':
                date = cha.date
                # days = julday(date_tran(date))
                lon = ((cha.midlon + 180) % 360 - 180)
                doy = orderday(date)
                if (152 < doy < 213) and (-45 < lon < -15):
                    plot_profile(cha, what)
                    count[cha.ck] += 1
        print(count)
        return count
    elif what == 2:
        ctrs = []
        while temp_line < all_lines:
            cha, temp_line = get_one_orb(text, temp_line)
            if cha.ctr != 0 and cha.ctr != -2:
                if cha.ctr == -1:
                    pass
                else:
                    ctrs.append(cha.ctr)
        return ctrs
    elif what == 3:
        num_ck = {'flat': [0] * 50, 'deep': [0] * 50, 'bubble': [0] * 50, 'error': [0] * 50}
        while temp_line < len(text):
            cha, temp_line = get_one_orb(text, temp_line)
            mlat, den = cha.mlat_den()
            if len(mlat) > 35:
                static_lct(mlat, den, num_ck)
        return num_ck
    else:
        print("error in 'read_cha'")


def plot_profile(cha, what):
    mlat0, den0 = cha.mlat_den()
    mlat, den = [], []
    for i in range(len(mlat0)):
        if -47 < mlat0[i] < 47:
            den.append(den0[i])
            mlat.append(mlat0[i])

    if len(mlat) > 35:
        color = {'flat': 'g', 'deep': 'r', 'bubble': 'b', 'error': 'y', 'loss': 'c'}[cha.ck]
        plt.xlim([-25, 25])
        plt.ylim([3.5, 7])

        if what == 1:
            plt.plot(mlat, den, alpha=0.1, c=color, lw=1)
        elif what == 0:
            den_rp, step = repair_bubble(mlat, den)
            plt.plot(mlat, den_rp, linewidth=2, linestyle='-', c=color, alpha=0.5)
            # plt.scatter(mlat, den_rp, alpha=0.5, c=color, marker='+')
            plt.plot(mlat, den, linewidth=1, c=color, alpha=0.5, ls='--')
            plt.scatter(mlat, den, alpha=0.5, c=color, s=8)
            # title = cha.ck + '_' + cha.date + '_' + str(round(cha.midlt, 2)) + '_' + str(round(cha.midlon, 2))
            # plt.title(title)
            # plt.show()
            # print(title)
            # plt.savefig(
            #     # 'D:/Program/BigCTR/Picture/champProfile/' + str(min(23, round(cha.midlt))) + '/' + title + '.png')
            #     # 'D:/Program/BigCTR/Picture/champProfileCheck/' + title + '.png')
            #     'picked.png')
            # plt.close()
        else:
            print("error in 'plot_profile'")


def static_lct(mlat, den, num_ck):
    mlat0, den0 = [], []
    for i in range(len(mlat)):
        if -27 < mlat[i] < 27:
            den0.append(den[i])
            mlat0.append(mlat[i])
    den_rp, step = repair_bubble(mlat0, den0)
    ck, ctr = get_curve_kind(mlat0, den0)
    num_ck[ck][step] += 1


def static_ctr(what):
    """
    :param what: 0 for count, 1 for percent
    :return: null
    """
    lenth = 40
    nums = []
    num_all = np.zeros(lenth + 2)
    xdot = np.array([10 ** (3.4 * x / lenth) for x in range(-1, lenth + 1)])
    for i in range(18, 24):
        ctrs = read_cha(i, 2)
        print(len(ctrs))
        num = np.zeros(lenth + 2)
        for ctr in ctrs:
            temp = int(np.log10(ctr) / 3.4 * lenth)
            num = num + np.array([1] * (temp + 1) + [0] * (lenth + 1 - temp))
            num_all = num_all + np.array([1] * (temp + 1) + [0] * (lenth + 1 - temp))
            # num[temp] += 1
            # num_all[temp] += 1
        b = num.copy()
        nums.append(b)
        # plt.plot(xdot, num/sum(num))
    if what == 0:
        for i in range(6):
            plt.plot(xdot, nums[i])
        plt.plot(xdot, num_all, c='k')
        plt.text(1000, num_all[0] * 1, 'Number', fontsize=12)
        plt.ylim([1, num_all[0] * 2])
    else:
        # what == 1
        for i in range(6):
            plt.plot(xdot, nums[i] / nums[i][0])
        plt.plot(xdot, num_all / num_all[0], c='k')
        plt.text(1000, 1, 'Percent', fontsize=12)
        plt.ylim([1 / num_all[0], 2])
    plt.semilogx()
    plt.semilogy()


def draw_ctr():
    plt.figure(figsize=[6, 8], dpi=100)
    cmap = plt.get_cmap('rainbow_r')
    c = cycler('color', cmap(np.linspace(0, 1, 6)))
    plt.rcParams["axes.prop_cycle"] = c
    plt.subplot(2, 1, 1)
    static_ctr(0)
    plt.subplot(2, 1, 2)
    static_ctr(1)
    plt.yticks([1, 0.1, 0.01, 0.001], ['100%', '10%', '1%', '0.1%'])
    plt.xlabel('CTR')
    plt.legend([str(x) for x in range(18, 24)] + ['All'], loc=3)
    plt.show()


def draw_all_profiles():
    tran = [1, 3, 5, 2, 4, 6]
    plt.figure(figsize=[10, 8])
    plt.subplots_adjust(left=0.07, bottom=0.07, right=0.97, top=0.95, hspace=0.3, wspace=0.15)
    for i in range(18, 24):
        plt.subplot(3, 2, tran[i - 18])
        count = read_cha(i, 1)
        print(i)
        for k in count.keys():
            print(k, count[k])
        plt.title('LT = ' + str(i), size=10)
        if tran[i - 18] == 5 or tran[i - 18] == 6:
            plt.xlabel('Mlat')
        if tran[i - 18] % 2 == 1:
            plt.ylabel('lg Ne')
    # plt.savefig('LT_develop_ele.png')
    # plt.savefig('LT_develop_ele.eps')
    plt.show()


def draw_single_profile():
    for lct in range(18, 24):
        count = read_cha(lct, 0)
        print(lct)
        for k in count.keys():
            print(k, count[k])


def draw_num_ck():
    for lct in range(18, 24):
        res = read_cha(lct, 3)
        print(lct)
        for k in res:
            print(k, sum(res[k]))
        plt.plot(res['flat'])
        plt.plot(np.array(res['bubble']) + np.array(res['deep']) + np.array(res['flat']))
        plt.plot(np.array(res['deep']) + np.array(res['flat']))
        plt.axis([0, 50, 0, 50])
        # print(key.ljust(7), ' '.join([str(x).rjust(3) for x in res[key]]))
        plt.savefig('D:/Program/BigCTR/Picture/localtime_ck_num/' + str(lct) + '.jpg')
        plt.close()


def bar_plot():
    arr = [[1026, 19, 0],
           [740, 213, 12],
           [511, 290, 134],
           [501, 243, 225],
           [735, 170, 233],
           [760, 84, 125]]
    arr = np.array(arr).transpose()
    localtime = [18, 19, 20, 21, 22, 23]
    plt.bar(localtime, arr[0] + arr[1] + arr[2], color='b', width=0.5)
    plt.bar(localtime, arr[0] + arr[1], color='r', width=0.5)
    plt.bar(localtime, arr[0], color='g', width=0.5)
    plt.axis([17.1, 23.9, 0, 1400])
    plt.xlabel('Local Time')
    plt.ylabel('Counts')
    plt.text(16.5, 1500, '(b)', fontsize=16)
    plt.legend(['Bubble', 'Deep', 'Flat'])
    plt.show()


def draw_picked_profiles():
    with open('D:/Program/BigCTR/Text/champOrb/picked.txt', 'r') as f:
        texts = f.readlines()
    temp_line = 0
    all_lines = len(texts)
    plt.plot([1], [1], c='r')
    plt.plot([1], [1], c='g')
    plt.plot([1], [1], c='b')
    while temp_line < all_lines:
        cha, temp_line = get_one_orb(texts, temp_line)
        if cha.ck != 'loss':
            plot_profile(cha, 0)
    plt.legend(['Deep', 'Flat', 'Bubble'])
    plt.show()


if __name__ == '__main__':
    # draw_ctr()
    # draw_all_profiles()
    # draw_single_profile()
    # draw_num_ck()
    # bar_plot()
    draw_picked_profiles()
