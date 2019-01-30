import matplotlib.pyplot as plt
import numpy as np
# import seaborn as sns
from cycler import cycler

from basicFun import get_one_orb, repair_bubble, get_curve_kind


def read_file(lt, what):
    # text = open('D:/Program/BigCTR/Text/text_onlyChamp/a' + str(lt * 1.0 - 0.5) + '.txt').readlines() + \
    text = open('D:/Program/BigCTR/Text/champOrb/' + str(lt * 1.0) + '.txt').readlines()
    temp_line = 0
    # num_ck = {'flat': 0, 'deep': 0, 'bubble': 0, 'error': 0}
    ctrs = []
    while temp_line < len(text):
        cha, temp_line = get_one_orb(text, temp_line)
        # print(temp_line)
        if what == 2:
            if cha.ctr != 0 and cha.ctr != -2:
                if cha.ctr == -1:
                    cha.ctr = 0.95
                else:
                    ctrs.append(cha.ctr)
        elif what == 1:
            draw2(cha)
        # static_lct(cha, num_ck)
    if what == 2:
        return ctrs


def draw(cha):
    mlat0, den0 = cha.mlat_den()
    mlat, den = [], []
    for i in range(len(mlat0)):
        if -27 < mlat0[i] < 27:
            den.append(den0[i])
            mlat.append(mlat0[i])

    if len(mlat) > 5:
        den = np.array(den)
        den_d2 = den[:-2] + den[2:] - 2 * den[1:-1]
        den_rp, den_d2_rp, step = repair_bubble(den, den_d2)

        if len(mlat) < 35:
            color = 'y'
        else:
            if step == 0:
                color = 'r'
            elif step < 5:
                color = 'g'
            else:
                color = 'b'

        plt.figure(figsize=[5, 6])

        plt.subplot(2, 1, 1)
        plt.plot(mlat, den, linewidth=1, linestyle='--', c=color, alpha=0.5)
        plt.scatter(mlat, den, alpha=0.5, c='k', marker='+')

        # den_rp, den_d2_rp, step = repair_bubble(den, den_d2)
        plt.plot(mlat, den_rp, linewidth=1, c=color, alpha=1)
        plt.scatter(mlat, den_rp, alpha=0.5, c='k')
        plt.xlim([-25, 25])

        plt.subplot(2, 1, 2)
        plt.scatter(mlat[1:-1], den_d2, alpha=0.5, c='k', marker='+')
        plt.plot(mlat[1:-1], den_d2, linewidth=1, linestyle='--', c=color, alpha=0.5)
        plt.plot(mlat[1:-1], np.zeros(len(mlat[1:-1])), linewidth=1, c='k', alpha=1)

        plt.scatter(mlat[1:-1], den_d2_rp, alpha=0.5, c='k')
        plt.plot(mlat[1:-1], den_d2_rp, linewidth=1, c=color, alpha=1)
        plt.plot(mlat[1:-1], np.zeros(len(mlat[1:-1])), linewidth=1, c='k', alpha=1)
        plt.xlim([-25, 25])

        plt.subplot(2, 1, 1)
        lct = round(cha.midlt)
        title = color + '_' + cha.date + '_' + str(round(cha.midlt, 2)) + '_' + str(round(cha.midlon, 2))
        plt.title(title)
        # plt.show()
        print(title)
        plt.savefig('D:/Program/BigCTR/Picture/champProfileDiff/' + str(lct) + '/' + title + '.png')
        plt.close()


def draw2(cha):
    mlat0, den0 = cha.mlat_den()
    mlat, den = [], []
    for i in range(len(mlat0)):
        if -27 < mlat0[i] < 27:
            den.append(den0[i])
            mlat.append(mlat0[i])

    if len(mlat) > 35:
        den = np.array(den)
        # den_d2 = den[:-2] + den[2:] - 2 * den[1:-1]
        # den_rp, den_d2_rp, step = repair_bubble(den, den_d2)
        ck = cha.ck
        color = {'flat': 'r', 'deep': 'g', 'bubble': 'b', 'error': 'y', 'loss': 'c'}[ck]

        # plt.plot(mlat, den, linewidth=1, linestyle='--', c=color, alpha=0.5)
        # plt.scatter(mlat, den, alpha=0.5, c='k', marker='+')
        plt.plot(mlat, den, linewidth=1, c=color, alpha=0.1)
        # plt.scatter(mlat, den_rp, alpha=0.5, c='k')
        plt.xlim([-25, 25])
        plt.ylim([3.5, 7])

        title = ck + '_' + cha.date + '_' + str(round(cha.lct, 2)) + '_' + str(round(cha.lon, 2))
        # plt.title(title)
        # plt.show()
        print(title)
        # plt.savefig('D:/Program/BigCTR/Picture/champProfile/' + str(min(23, round(lct))) + '/' + title + '.png')
        # plt.close()


def static_lct(mlat, den, num_ck):
    den = np.array(den)
    # den_d2 = den[:-2] + den[2:] - 2 * den[1:-1]
    # den_rp, den_d2_rp, step = repair_bubble(den, den_d2)
    ck = get_curve_kind(mlat, den)
    num_ck[ck] += 1


def draw_profile():
    tran = [1, 3, 5, 2, 4, 6]
    plt.figure(figsize=[10, 8])
    plt.subplots_adjust(left=0.07, bottom=0.07, right=0.97, top=0.95, hspace=0.3, wspace=0.15)
    for i in range(18, 24):
        plt.subplot(3, 2, tran[i - 18])
        plt.title('LT = ' + str(i), size=10)
        if tran[i - 18] == 5 or tran[i - 18] == 6:
            plt.xlabel('Mlat')
        if tran[i - 18] % 2 == 1:
            plt.ylabel('lg Ne')
    # plt.savefig('LT_develop_ele.png')
    # plt.savefig('LT_develop_ele.eps')
    plt.show()


def static_ctr():
    cmap = plt.get_cmap('rainbow_r')
    c = cycler('color', cmap(np.linspace(0, 1, 6)))
    plt.rcParams["axes.prop_cycle"] = c

    lenth = 20
    nums = []
    num_all = np.zeros(lenth + 2)
    xdot = np.array([10 ** (3.4 * x / lenth) for x in range(-1, lenth + 1)])
    for i in range(18, 24):
        ctrs = read_file(i, 2)
        print(len(ctrs))
        num = np.zeros(lenth + 2)
        for ctr in ctrs:
            temp = int(np.log10(ctr) / 3.4 * lenth)
            # num = num + np.array([1]*(temp+1) + [0]*(lenth+1-temp))
            # num_all = num_all + np.array([1] * (temp + 1) + [0] * (lenth + 1 - temp))
            num[temp] += 1
            num_all[temp] += 1
        b = num.copy()
        nums.append(b)
        # plt.plot(xdot, num/sum(num))
    for i in range(6):
        plt.plot(xdot, num_all / sum(num_all) - nums[i] / sum(nums[i]))
    plt.semilogx()
    # plt.semilogy()
    plt.legend(range(18, 24))
    plt.show()


if __name__ == '__main__':
    static_ctr()
