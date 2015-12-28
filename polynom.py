#!/usr/bin/python3
# coding: utf-8

import math

A_cache = {}


def get_values(a, b, m, f): # return [(x0,f0), (x2,f2), ..., (x_(m),f_(m)]
    res = []
    for i in range(m+1):
        x = a + i * (b - a) / m
        y = f(x)
        res.append((x, y))

    return res


def L(values, x_k, x):
    a = phi(values, x_k, x)
    b = phi(values, x_k, x_k)
    return a/b


def phi(values, x_k, x):
    pr = 1
    flag = True

    for dot in values:
        if abs(dot[0] - x_k) < 0.000001:
            flag = False
        else:
            pr *= (x - dot[0])

    if flag:
        pr /= (x - x_k)

    return pr


def lagrange(values, x):
    P = 0
    for i in range(len(values)):
        l_val = L(values, values[i][0], x)
        P += l_val * values[i][1]

    return P


def F(x_list):
    if x_list in A_cache.keys():
        #print(">>> x_list = {}".format(x_list))
        #print(">>> F({}) = {:2f} (cached)".format(x_list, A_cache[x_list]))
        return A_cache[x_list]
    else:
        a1 = F(x_list[1:])
        a2 = F(x_list[:-1])
        a3 = x_list[-1]
        a4 = x_list[0]
        A = (a1 - a2) / (a3 - a4)
        A_cache[x_list] = A

        #print(">>> x_list = {}".format(x_list))
        #print(">>> F({}) = ({:<2f} - {:<2f}) / ({:2f} - {:2f}) = {:2f}".format(x_list, a1, a2, a3, a4, A))
        return A


def newton(values, x):
    x_list = tuple(xk for xk,yk in values)
    for xk,yk in values:
        A_cache[(xk,)] = yk

    P = F((x_list[0],))
    pr = 1

    for i in range(len(x_list)-1):
        #print("{} шаг".format(i))
        #print("Вычисляем: A_({}+1)".format(i))
        #print("Множители: от x_0 до x_{}".format(i, x_list[:i+1]))
        pr *= (x - x_list[i])
        P += F(x_list[:i+2]) * pr

    return P


def main():
    a, b = (float(x) for x in input('Введите a и b (a < b): ').split(' '))
    #a, b = 0.0, 100.0
    if a >= b:
        print('a долно быть строго меньше b')
        return
    m = int(input('Введите m (количество отрезков между a и b): '))
    #m = 5

    func = lambda x: math.tan(x) - x**2/2.0
    values = get_values(a, b, m, f=func)
    print('{:>10} | {}'.format('x', 'f(x)'))
    for x, y in values:
        print('{:>10f} | {:<10f}'.format(x, y))


    n = int(input('Введите степень полинома n (n <= m): '))
    #n = 5
    if n > m:
        print('Степень полинома должна быть не больше количества отрезков.')
        return

    x0 = float(input('Введите x: '))
    #x0 = 16.0
    values_with_distances = [(abs(x-x0), x, y) for x, y in values]
    values_with_distances.sort()
    values_sorted = [(x,y) for d, x, y in values_with_distances][:n+1]

    print()

    res = lagrange(values_sorted, x0)
    print('Значение алгебраического многочлена в форме Лагранжа в точке {}: {}'.format(x0, res))
    #print(res)
    print('Погрешность в данном случае равна {}.'.format(abs(func(x0) - res)))
    print()

    res = newton(values_sorted, x0)
    print('Значение алгебраического многочлена в форме Ньютона в точке {}: {}'.format(x0, res))
    #print(res)
    print('Погрешность в данном случае равна {}.'.format(abs(func(x0) - res)))


if __name__ == '__main__':
    main()
