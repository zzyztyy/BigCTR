import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx


def read_jro_data(name, path=''):
    with open(path + name, 'r') as file:
        text = file.readlines()
        data = []
        high_set = set()
        time_set = set()
        for i in range(10, len(text)):
            arr = text[i].split()
            if arr[7] == 'missing':
                arr[7] = 'NaN'
            arr = [float(x) for x in arr]
            time = arr[3] + arr[4] / 60. + arr[5] / 3600.
            high = arr[6]
            Ne = arr[7] / 10 ** 12
            # time_num = int((time-17.16)/0.22767+0.1)  # add 0.1 for int to right
            # high_num = int((high-160)/15)
            high_set.add(high)
            time_set.add(time)
            data.append(Ne)
        data = np.array(data).reshape(len(time_set), len(high_set))
        # print(sorted(high_set))
        # print(sorted(time_set))
        # print(len(data), len(high_set), len(time_set))
        return (data), list(sorted(time_set)), list(sorted(high_set))


temp_picked = [[4, 8, 13, 17, 22, 25],
               [1, 4, 6, 10, 13, 17],
               [3, 7, 11, 15, 19, 23]]


def draw_profile(data, xarr, yarr, number=0):
    values = range(6)
    jet = plt.get_cmap('rainbow_r')
    cNorm = colors.Normalize(vmin=0, vmax=values[-1])
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)
    obj = []
    xarr_time = [str(int(x)) + 'h' + str(int((x - int(x)) * 60)) + 'm' for x in xarr]
    for i in range(6):
        colorVal = scalarMap.to_rgba(values[i])
        temp = temp_picked[number][i]
        obj.append(xarr_time[temp])
        plt.plot(data[temp], yarr, c=colorVal, lw=0.5)
        plt.scatter(data[temp], yarr, c=colorVal, marker='o', s=5)
    print(obj)
    plt.legend(obj, loc='upper right')


if __name__ == '__main__':
    file_path = 'Jicamarca\\'
    file_name = ['jro20020611c_59665.txt', 'jro20020909d_59021.txt', 'jro20011113c_59576.txt']

    plt.subplot(1, 3, 1)
    data, time, high = read_jro_data(file_path + file_name[0])
    draw_profile(data, time, high, 0)
    plt.title(file_name[0][3:11])
    plt.xlim([0, 1.2 * 10 ** 0])
    plt.ylabel('Altitude / km')

    plt.subplot(1, 3, 2)
    data, time, high = read_jro_data(file_path + file_name[1])
    draw_profile(data, time, high, 1)
    plt.title(file_name[1][3:11])
    plt.xlim([0, 2 * 10 ** 0])
    plt.xlabel('Ne / 10^12*m^-3')

    plt.subplot(1, 3, 3)
    data, time, high = read_jro_data(file_path + file_name[2])
    draw_profile(data, time, high, 2)
    plt.title(file_name[2][3:11])
    plt.xlim([0, 2.5 * 10 ** 0])

    plt.show()
