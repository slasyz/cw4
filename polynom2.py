#!/usr/bin/python3
# coding: utf-8

import math


class ZValues():
    def __init__(self, xvalues, x0):
        self.xvalues = xvalues
        self.k = len(xvalues) // 2


    def __getitem__(self, i):
        index = self.k + i
        return self.xvalues[index]


    def z_to_x(self, i):
        #print("{} -> {}".format(i, self.k + i))
        return self.k + i


def get_values(x_list, f): # return [(x0,f0), (x2,f2), ..., (x_(m),f_(m)]
    res = []
    for x in x_list:
        y = f(x)
        res.append((x, y))

    return res


def Df(values, i, num): # список узлов, порядок, номер узла
    if i == 1:
        return values[num + 1][1] - values[num][1]
    else:
        return Df(values, i - 1, num + 1) - Df(values, i - 1, num)


def newton_start(values, x, h, n):
    x0, y0 = values[0]
    t = (x - x0) / h
    P = y0

    for k in range(n):
        a1 = 1
        for j in range(k + 1): a1 *= t - j
        a2 = math.factorial(k + 1)
        a3 = Df(values, k + 1, 0)

        P += (a1/a2) * a3

    return P


def newton_end(values, x, h, n, m):
    xm, ym = values[-1]
    t = (x - xm) / h
    P = ym

    for k in range(n):
        a1 = 1
        for j in range(k + 1): a1 *= t + j
        a2 = math.factorial(k + 1)
        a3 = Df(values, k + 1, m - k - 1)

        P += (a1/a2) * a3

    return P


def gauss_middle(values, x, h, n, m):
    zvalues = ZValues(values, x)

    P = zvalues[0][1]
    t = (x - zvalues[0][0]) / h
    for k in range(n):
        a1 = 1
        for j in range(k + 1):
            a1 *= t + (-1)**j * (j+1)//2
        a2 = math.factorial(k + 1)
        #a3 = Df(zvalues, k + 1, -((k+1)//2))
        a3 = Df(values, k + 1, zvalues.z_to_x(-((k+1)//2)))
        #print("z[{}] or x[{}]".format(-((k+1)//2), zvalues.z_to_x(-((k+1)//2))))

        #print("Очередное слагаемое: Df(zvalues, {}, {})".format(k+1, 1 + 2*((k+1)//2)))
        P += (a1/a2) * a3

    return P


def main():
    a, b = (float(x) for x in input('Введите a и b (a < b): ').split(' '))
    #a, b = 0, 1
    if a >= b:
        print('a долно быть строго меньше b')
        return

    m = int(input('Введите количество узлов в таблице: ')) - 1
    #m = 10
    h = (b-a) / m
    print("Длина отрезка равна {}".format(h))

    n = int(input('Введите степень полинома n (n <= {}): '.format(m)))
    #n = 6
    while (n > m) or (n < 0):
        print('Степень полинома должна быть не больше количества отрезков (и больше нуля).')
        n = int(input('Введите степень полинома n (n <= m): '))

    x_list = []
    for j in range(m + 1):
        x_list.append(a + j * h)


    func = lambda x: 1 - math.e**(-x) + x**2
    values = get_values(x_list, func)
    print('{:>10} | {}'.format('x', 'f(x)'))
    for x, y in values:
        print('{:>10f} | {:<10f}'.format(x, y))


    x0 = float(input('Введите x из интервалов: [{:>.10}, {:>.10}], [{:>.10}, {:>.10}], [{:>.10}, {:>.10}]: '.format(values[0][0], values[1][0], 
                      #values[len(values)//2-1][0], values[len(values)//2][0], 
                      a + (m-1)//2 * h, b - (m-1)//2 * h,
                      values[-2][0], values[-1][0])))
    while not ((values[0][0] <= x0 <= values[1][0]) or values[-2][0] <= x0 <= values[-1][0] or (a + (m-1)//2 * h <= x0 <= b - (m-1)//2 * h)):
        print("Значение x находится вне допустимых интервалов")
        x0 = float(input('Введите x из интервалов: [{:>.10}, {:>.10}], [{:>.10}, {:>.10}], [{:>.10}, {:>.10}]: '.format(values[0][0], values[1][0], 
                          values[len(values)//2-1][0], values[len(values)//2][0], 
                          values[-2][0], values[-1][0])))
    #x0 = 6
    print()


    if values[0][0] <= x0 <= values[1][0]:
        res = newton_start(values, x0, h, n)
        print("Интерполяционная формула Ньютона для начала таблицы")
        print("Значение равно {:.10f}.".format(res))
        print('Фактическая погрешность в данном случае равна {:.10f}.'.format(abs(func(x0) - res)))
    elif values[-2][0] <= x0 <= values[-1][0]:
        res = newton_end(values, x0, h, n, m)
        print("Интерполяционная формула Ньютона для конца таблицы")
        print("Значение равно {:.10f}.".format(res))
        print('Фактическая погрешность в данном случае равна {:.10f}.'.format(abs(func(x0) - res)))
    #elif values[len(values)//2-1][0] <= x0 <= values[len(values)//2][0]:
    elif a + (m-1)//2 * h <= x0 <= b - (m-1)//2 * h:
        res = gauss_middle(values, x0, h, n, m)
        print("Интерполяционная формула Гаусса для середины таблицы")
        print("Значение равно {:.15f}.".format(res))
        print('Фактическая погрешность в данном случае равна {:.15f}.'.format(abs(func(x0) - res)))
    else:
        print("Запрашиваемое значение находится вне допустимых интервалов. Ошибка.")


if __name__ == '__main__':
    main()
