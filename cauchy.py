#!/usr/bin/python3


import math
import copy


class IndexedArray():
    def __init__(self):
        self.values = [0]*1003

    def __getitem__(self, i):
        return self.values[i + 2]

    def __setitem__(self, i, value):
        self.values[i + 2] = value


class IndexedArray2():
    def __init__(self):
        self.values = []
        for i in range(1003):
            self.values.append(IndexedArray())

    def __getitem__(self, ij):
        i, j = ij
        return self.values[i+2][j+2]

    def __setitem__(self, ij, value):
        i, j = ij
        self.values[i + 2][j + 2] = value


def Df(values, i, num): # список узлов, порядок, номер узла
    if i == 1:
        return values[num + 1][1] - values[num][1]
    else:
        return Df(values, i - 1, num + 1) - Df(values, i - 1, num)


def taylor(x, x0, func):
    #s = 0
    #for k in range(5):
    #    s += func(x0)**k / math.factorial(k) * (x - x0)**k
    #return (9/48 * math.exp(-x0) + 33/48 * math.cos(x0) - 7/48 * math.sin(x0)) * (x - x0)

    return (1/2 * math.exp(-x0) + math.sin(x0)/2 + math.cos(x0)/2) + \
        (-1/2 * math.exp(-x0) + math.cos(x0)/2 - math.sin(x0)/2) * (x - x0) + \
        (1/4 * math.exp(-x0) - math.sin(x0)/4 - math.cos(x0)/4) * (x - x0)**2 + \
        (-1/12 * math.exp(-x0) - math.cos(x0)/12 + math.sin(x0)/12) * (x - x0)**3 + \
        (1/48 * math.exp(-x0) + math.sin(x0)/48 + math.cos(x0)/48) * (x-x0)**4

    #return
    #return s


def eta(values_y, k, f, h):
    return h * f(values_y[k][0], values_y[k][1])


def adams(values_y, f, h, N, x0):
    values_eta = copy.deepcopy(values_y)
    for i in range(len(values_eta)):
        values_eta[i][1] = eta(values_y, i, f, h)
        #values_eta[i][1] = h * f(values_y[i][0], values_y[i][1])

    for k1 in range(3, N+1):
        k = k1 - 1
        xk1 = x0 + k1 * h
        #print(Df(values_eta, 1, k - 1 + 2))
        yk1 = values_y[k + 2][1] + \
                values_eta[k + 2][1] + \
                1/2     * Df(values_eta, 1, k - 1 + 2) + \
                5/12    * Df(values_eta, 2, k - 2 + 2) + \
                3/8     * Df(values_eta, 3, k - 3 + 2) + \
                251/720 * Df(values_eta, 4, k - 4 + 2)

        """yk1 = values_y[k + 2][1] + \
                1901/30 * 1/(4*3*2)  * values_eta[k - 0 + 2][1] + \
                1387/60 * (-1)/(3*2) * values_eta[k - 1 + 2][1] + \
                218/15 * 1/(2*2)     * values_eta[k - 2 + 2][1] + \
                637/60 * (-1)/(3*2)  * values_eta[k - 3 + 2][1] + \
                251/30 * 1/(4*3*2)   * values_eta[k - 4 + 2][1]"""
        values_y.append([xk1, yk1])
        values_eta.append([xk1, eta(values_y, k1 + 2, f, h)])


def rk(values_y, f, h, N, x0):
    for k in range(1, N+1):
        xk, yk = values_y[k + 1]
        xk1 = xk + h
        k1 = h * f(xk, yk)
        k2 = h * f(xk + h / 2, yk + k1 / 2)
        k3 = h * f(xk + h / 2, yk + k2 / 2)
        k4 = h * f(xk1, yk + k3)

        yk1 = yk + 1/6 * (k1 + 2 * k2 + 2 * k3 + k4)
        values_y.append([xk1, yk1])


def euler(values_y, f, h, N, x0):
    for k in range(1, N+1):
        xk, yk = values_y[k + 1]
        xk1 = xk + h
        yk1 = yk + f(xk, yk)

        values_y.append([xk1, yk1])


def eulerb(values_y, f, h, N, x0):
    for k in range(1, N+1):
        xk, yk = values_y[k + 1]
        xk1 = xk + h
        yk1 = yk + h * f(xk + h/2, yk + h/2 * f(xk, yk))

        values_y.append([xk1, yk1])


def eulerc(values_y, f, h, N, x0):
    for k in range(1, N+1):
        xk, yk = values_y[k + 1]
        xk1 = xk + h
        yk1 = yk + h/2 * (f(xk, yk) + f(xk1, yk + h * f(xk, yk)))

        values_y.append([xk1, yk1])


def main():
    h = float(input('Введите h: '))
    #h = 0.1
    x0 = float(input('Введите x0: '))
    #x0 = 0
    y0 = float(input('Введите y0: '))
    #y0 = 1
    N = int(input('Введите N: '))
    #N = 10

    f = lambda x, y: -y + math.cos(x)
    y_cauchy = lambda x: 0.5 * math.exp(-x) + math.sin(x)/2 + math.cos(x)/2

    y_exact = []
    print('Находим точные значения в точках:')
    print("{:>10s} | {:<10s}".format('x', 'y_cauchy(x)'))
    for k in range(-2, N+1):
        xk = x0 + k*h
        yk = y_cauchy(xk)
        y_exact.append(yk)
        print("{:>10.5f} | {:<10.5f}".format(xk, yk))
    print()

    y_taylor = []
    print('Находим приближённые решения (с помощью ряда Тейлора) в точках и погрешности:')
    print("{:>10s} | {:<15.10s} | {:<15.10s}".format('x', 'y_tayl(x)', 'abs(y_cauchy - y_n)'))
    for k in range(-2, 3):
        xk = x0 + k*h
        yk = taylor(xk, x0, y_cauchy)
        y_taylor.append(yk)
        print("{:>10.5f} | {:<15.10f} | {:<15.10f}".format(xk, yk, abs(yk - y_exact[k+2])))
    print()

    print('Находим приближённые решения (с помощью метода Адамса 4 порядка):')
    print("{:>10s} | {:<10s}".format('x', 'y_adams(x)'))
    values_y_adams = [[x0 + k * h, y_taylor[k+2]] for k in range(-2, 3)]
    adams(values_y_adams, f, h, N, x0)
    for k in range(3, N+1):
        xk = x0 + k*h
        yk = values_y_adams[k+2][1]
        print("{:>10.5f} | {:<10.5f}".format(xk, yk))
    print('Абсолютная погрешность для последнего значения равна: {:.10f}'.format(abs(values_y_adams[-1][1] - y_exact[-1])))
    print()

    print('Находим приближённые решения (с помощью метода Рунге-Кутта 4 порядка):')
    print("{:>10s} | {:<10s}".format('x', 'y_rk(x)'))
    values_y_rk = [[x0 + k * h, y_taylor[k+2]] for k in range(-2, 1)]
    rk(values_y_rk, f, h, N, x0)
    for k in range(1, N+1):
        xk = x0 + k*h
        yk = values_y_rk[k+2][1]
        print("{:>10.5f} | {:<10.5f}".format(xk, yk))
    print('Абсолютная погрешность для последнего значения равна: {:.10f}'.format(abs(values_y_rk[-1][1] - y_exact[-1])))
    print()

    print('Находим приближённые решения (с помощью метода Эйлера):')
    print("{:>10s} | {:<10s}".format('x', 'y_euler(x)'))
    values_y_euler = [[x0 + k * h, y_taylor[k+2]] for k in range(-2, 1)]
    euler(values_y_euler, f, h, N, x0)
    for k in range(1, N+1):
        xk = x0 + k*h
        yk = values_y_euler[k+2][1]
        print("{:>10.5f} | {:<10.5f}".format(xk, yk))
    print('Абсолютная погрешность для последнего значения равна: {:.10f}'.format(abs(values_y_euler[-1][1] - y_exact[-1])))
    print()

    print('Находим приближённые решения (с помощью усовершенствованного метода Эйлера):')
    print("{:>10s} | {:<10s}".format('x', 'y_eulerb(x)'))
    values_y_eulerb = [[x0 + k * h, y_taylor[k+2]] for k in range(-2, 1)]
    eulerb(values_y_eulerb, f, h, N, x0)
    for k in range(1, N+1):
        xk = x0 + k*h
        yk = values_y_eulerb[k+2][1]
        print("{:>10.5f} | {:<10.5f}".format(xk, yk))
    print('Абсолютная погрешность для последнего значения равна: {:.10f}'.format(abs(values_y_eulerb[-1][1] - y_exact[-1])))
    print()

    print('Находим приближённые решения (с помощью метода Эйлера-Коши):')
    print("{:>10s} | {:<10s}".format('x', 'y_eulerc(x)'))
    values_y_eulerc = [[x0 + k * h, y_taylor[k+2]] for k in range(-2, 1)]
    eulerc(values_y_eulerc, f, h, N, x0)
    for k in range(1, N+1):
        xk = x0 + k*h
        yk = values_y_eulerc[k+2][1]
        print("{:>10.5f} | {:<10.5f}".format(xk, yk))
    print('Абсолютная погрешность для последнего значения равна: {:.10f}'.format(abs(values_y_eulerc[-1][1] - y_exact[-1])))
    print()


if __name__ == '__main__':
    main()
