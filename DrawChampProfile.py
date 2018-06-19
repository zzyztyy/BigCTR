import matplotlib.pyplot as plt
from bc3newMergeOrb import curveKind2
from bc4staticLT import getoneOrb


def read_file(lt):
    text = open('LTdevelop\\text_OnlyChamp\\a' + str(lt * 1.0 - 0.5) + '.txt').readlines() + \
           open('LTdevelop\\text_OnlyChamp\\a' + str(lt * 1.0) + '.txt').readlines()
    temp_line = 0
    while temp_line < len(text):
        cha, temp_line = getoneOrb(text, temp_line)
        draw(cha)


def draw(cha):
    mlat, den = cha.mlat_den()
    if len(mlat) > 5:
        ck = curveKind2(mlat, den)
        # plt.plot(lat, 10**np.array(den), linewidth=1, c='k', alpha=1)
        # plt.xlim(-20, 20)
        # plt.show()
        if ck == 'flat':
            plt.plot(mlat, den, linewidth=1, c='r', alpha=0.075)
        elif ck == 'deep':
            plt.plot(mlat, den, linewidth=1, c='g', alpha=0.075)
        elif ck == 'bubble':
            plt.plot(mlat, den, linewidth=1, c='b', alpha=0.075)
        else:
            plt.plot(mlat, den, linewidth=1, c='y', alpha=0.075)
        plt.axis([-20, 20, 3.5, 7])


if __name__ == '__main__':
    tran = [1, 3, 5, 2, 4, 6]
    plt.figure(figsize=[12, 9])
    plt.subplots_adjust(left=0.07, bottom=0.07, right=0.97, top=0.95, hspace=0.2, wspace=0.15)
    for i in range(18, 24):
        plt.subplot(3, 2, tran[i - 18])
        plt.title('LT = ' + str(i), size=10)
        if tran[i - 18] == 5 or tran[i - 18] == 6:
            plt.xlabel('Mlat')
        if tran[i - 18] % 2 == 1:
            plt.ylabel('logNe')
        read_file(i)
    plt.savefig('LT_develop_ele.png')
    plt.savefig('LT_develop_ele.eps')
    # plt.show()
