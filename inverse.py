#!/usr/bin/python3
# coding: utf-8


import polynom
import math
from numpy import sign


def get_polynom_value(values, x0, n):
    values_with_distances = [(abs(x-x0), x, y) for x, y in values]
    values_with_distances.sort()
    values_sorted = [(x,y) for d, x, y in values_with_distances][:n+1]

    return polynom.lagrange(values_sorted, x0)


def way1(values, F, n):
    values = [(y, x) for x,y in values]

    return get_polynom_value(values, F, n)


def solve(func, a, b, eps):
    #print("Поиск на интервале от {} до {}".format(a, b))

    if sign(func(a)) == sign(func(b)):
        return None

    if abs(func(a)) < eps: 
        return a
    if abs(func(b)) < eps: 
        return b

    dx = b - a
    xi = (b + a) / 2


    while abs(func(xi)) > eps:
        dx = dx / 2
        xi = a + dx

        if sign(func(a)) != sign(func(xi)):
            b = xi
        else: 
            a = xi

    return xi


    """xi = (a + b) / 2
    if func(xi) < eps:
        return [xi,]
    if abs(a - b) < eps:
        return []

    res = solve(func, a, xi, eps) + solve(func, xi, b, eps)
    return res"""



def way2(values, F, n):
    eps = 1e-8

    a = values[0][0]
    b = values[-1][0]

    res = []

    for i in range(len(values)-1):
        res1 = solve(lambda x: get_polynom_value(values, x, n) - F, values[i][0], values[i+1][0], eps)
        if res1 is not None:
            res.append(res1)

    i = 0
    while i < len(res) - 1:
        if abs(res[i] - res[i+1]) < eps:
            del res[i]
        else:
            i += 1

    return res

    #return solve(lambda x: get_polynom_value(values, x, n) - F, a, b, eps)


def main():
    a, b = (float(x) for x in input('Введите a и b (a < b): ').split(' '))
    #a, b = 0.0, 100.0
    if a >= b:
        print('a должно быть строго меньше b')
        return
    m = int(input('Введите m (количество отрезков между a и b): '))
    #m = 10

    #func = lambda x: math.cos(x) - x**2/2.0
    func = lambda x: math.sin(x) + x**2/2
    values = polynom.get_values(a, b, m, f=func)
    print('{:>10} | {}'.format('x', 'f(x)'))
    for x, y in values:
        print('{:>10f} | {:<10f}'.format(x, y))


    n = int(input('Введите степень полинома n (n <= {}): '.format(m)))
    #n = 5
    if n > m:
        print('Степень полинома должна быть не больше количества отрезков.')
        return


    F = float(input('Введите F: '))
    #F = 5.0
    print()

    res = way1(values, F, n)
    print('Решение задачи обратного интерполирования первым способом: {}'.format(res))
    print('Модуль невязки равен: {:.10f}'.format(abs(func(res) - F)))
    print()

    res = way2(values, F, n)
    print('Решение задачи обратного интерполирования вторым способом: найдено {} корней.'.format(len(res)))
    for el in res:
        print('Корень: {:.10f}; модуль невязки: {:.10f}.'.format(el, abs(func(el) - F)))
    #print('Решение задачи обратного интерполирования вторым способом: {}'.format(res))
    #print('Модуль невязки равен: {}'.format(abs(func(res) - F)))



if __name__ == '__main__':
    main()
