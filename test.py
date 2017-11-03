import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import basicFun as bf

def xiangtu():
    k = 1
    vy0 = np.arange(-10, 10, 2)
    vx0 = 2
    x = np.arange(-1500, 1501) / 200
    x1 = 1
    c = 0.5*k*x1*x1+vy0
    ax = plt.subplot(111, projection='3d')  # 创建一个三维的绘图工程
    for i in range(len(vy0)):
        vy = -k * x * x / 2 + c[i]
        vx = np.sqrt(vy0[i]*vy0[i]+vx0*vx0-vy*vy)
        # vx = np.sqrt(vx0 * vx0 - p * p / 4 * x * x * (x * x - 4 / p * vy0[i]))
        ax.scatter(list(x)+list(x), list(vx)+list(-vx), list(vy)+list(vy), s=1)
        # ax.scatter(x, -vx, vy, s=1)
        ax.set_xlabel('x')
        ax.set_ylabel('vx')
        ax.set_zlabel('vy')
        # plt.scatter(list(x)+list(x), list(-vx)+list(vx), s=0.1)
    # plt.legend(vy0)
    # plt.xlabel('x')
    # plt.ylabel('vx')
    # plt.plot(np.random.rand(100))
    plt.show()

def jifen():
    m = np.arange(1, 10000)/10000
    # x = list(m)+list([1])
    x = []
    # gama = np.arange(-9, 10)/10+0.1
    # a = float(format(1/(1+1/gama),'.2f'))

    # print(a)
    a = [0.45, 0.42, 0.39, 0.35, 0.3, 0.25, 0.2, 0.1, -0.1, -0.3, -0.5]
    u = m*m
    sum = []

    for i in range(len(a)):
        temp = 0
        sum.append(0)
        y = (1 - u / a[i]) / np.sqrt((1 / a[i] - 1) ** 2 - (1 - u / a[i]) ** 2)*abs(a[i])/a[i]
        # plt.plot(m, y)
        # for j in range(len(y)):
        #     temp = temp+y[j]*0.0001
        #     sum.append(temp)
        #     xtemp = m[j]
        #     x.append(xtemp)
        # x.append(1)
        # for j in range(len(y)):
        #     temp = temp - y[len(y)-j-1]*0.0001
        #     sum.append(-temp+2*sum[len(y)])
        #     xtemp = m[len(m)-j-1]
        #     x.append(xtemp)
        # for j in range(len(y)):
        #     temp = temp + y[j]*0.0001
        #     sum.append(temp+2*sum[len(y)])
        #     xtemp = m[j]
        #     x.append(-xtemp)
        # for j in range(len(y)):
        #     temp = temp + y[len(y)-j-1]*0.0001
        #     sum.append(temp+2*sum[len(y)])
        #     xtemp = m[len(m)-j-1]
        #     x.append(-xtemp)
        plt.plot(m, y)
        # sum.clear()
        # x.clear()
    plt.legend(a)
    plt.axis([0, 1.5, -2, 2])
    plt.title('Slope')
    plt.plot(range(-1, 2), np.arange(-1, 2) * 0, linewidth=1, c='k', linestyle='--')
    plt.plot(np.arange(-4, 2) * 0 + 1, range(-4, 2), linewidth=1, c='k', linestyle='--')
    plt.plot(np.arange(-4, 2) * 0 - 1, range(-4, 2), linewidth=1, c='k', linestyle='--')
    plt.show()

#GPS0 yy1 mm2 dd3 hh4 mm5 ss6 radius7 lat8 lon9 den10 (Temperature)
def toobig():
    data = bf.readfile('D:\\sattelite data\\CHAMP\\CH-ME-2-PLP\\toobig\\CH-ME-2-PLP+2002-02-27_1.dat')
    lat = []
    den = []
    lon = []
    ut = 0
    i=19
    while i in range(18, int(len(data)/2)-1):
        i=i+1
        a = (data[2*i]+data[2*i+1]).split()
        print(a)
        while float(a[8])>-70 and float(a[8])<70 and i<int(len(data)/2)-1:
            lat.append(float(a[8]))
            den.append(np.log10(float(a[10])))
            i = i+1
            a = (data[2 * i] + data[2 * i + 1]).split()
            ut = float(a[4])
        if len(lat)>0:
            if lat[0]<0 and ut>16 and ut<=24:
                plt.plot(lat, den)
                lon.append(float(a[9]))
                # plt.show()
            lat.clear()
            den.clear()
    plt.legend(lon)

if __name__ == '__main__':
    toobig()
    plt.ylim(2, 7)
    plt.show()
