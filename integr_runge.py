#!/usr/bin/python3

import math
import polynom


def sp1(values, func):
    res = 0

    for i in range(len(values)-1):
        a = values[i][0]
        b = values[i+1][0]

        res += (b-a) * func((a+b)/2)

    return res


def sp2(values, func):
    res = 0

    for i in range(len(values)-1):
        a = values[i][0]
        b = values[i+1][0]

        res += (b-a) / 2 * (func(a) + func(b))

    return res


def sp3(values, func):
    res = 0

    for i in range(len(values)-1):
        a = values[i][0]
        b = values[i+1][0]

        res += (b-a) / 6 * (func(a) + 4*func((a+b)/2) + func(b))

    return res


def main():
    a, b = (float(x) for x in input('Введите a и b (a < b): ').split(' '))
    #a, b = 0.0, 1.0
    if a >= b:
        print('a должно быть строго меньше b')
        return
    m = int(input('Введите m (количество отрезков между a и b): '))
    #m = 10

    h = (b - a) / m

    func = lambda x: 1 - math.exp(-x) + x**2
    #integr_func = lambda a1, b1: (b1 + math.exp(-b1) + b1**3/3) - (a1 + math.exp(-a1) + a1**3/3)
    integr_func = lambda x: x + math.exp(-x) + x**3/3
    #func = lambda x: x**3 + x**2 + x + 1
    #integr_func = lambda x: x**4/4 + x**3/3 + x**2/2 + x

    integr = lambda a1, b1: integr_func(b1) - integr_func(a1)

    values = polynom.get_values(a, b, m, f=func)
    J = integr(a, b)
    print('{:>10} | {}'.format('x', 'f(x)'))
    #for x, y in values:
    #    print('{:>10f} | {:<10f}'.format(x, y))
    print('Интеграл по [a,b] равен {}'.format(J))
    print()

    Jh = sp1(values, func)
    print('Формула средних прямоугольников: {:<.15f}'.format(Jh))
    print('Фактическая погрешность: {:<.15f}'.format(abs(Jh - J)))
    Jh = sp2(values, func)
    print('Формула трапеций: {:<.15f}'.format(Jh))
    print('Фактическая погрешность: {:<.15f}'.format(abs(Jh - J)))
    Jh = sp3(values, func)
    print('Формула Симпсона: {:<.15f}'.format(Jh))
    print('Фактическая погрешность: {:<.15f}'.format(abs(Jh - J)))


if __name__ == '__main__':
    main()
