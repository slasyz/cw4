#!/usr/bin/python3

import math
import polynom
import inverse
import integr_runge
import numpy


def main():
    a, b = (float(x) for x in input('Введите a и b (a < b): ').split(' '))
    #a, b = 0.0, 1.0
    if a >= b:
        print('a должно быть строго меньше b')
        return

    m = int(input('Введите m (количество отрезков между a и b): '))
    #m = 100

    func_w = lambda x: abs(x - 0.5)
    func_f = lambda x: math.sin(x)

    # находим моменты весовой функции
    print("Находим моменты весовой функции")
    mu = []
    for k in range(6):
        func = lambda x: func_w(x) * x**k
        values = polynom.get_values(a, b, 2*m, f=func)
        res = integr_runge.sp3(values, func)
        mu.append(res)
        print("µ_{} = {:.10f}".format(k, res))
    print()

    # находим c, d, e
    matrix = [[mu[2], mu[1], mu[0]],
              [mu[3], mu[2], mu[1]],
              [mu[4], mu[3], mu[2]],
             ]
    depvar = [-mu[3], -mu[4], -mu[5]]
    c, d, e = numpy.linalg.solve(matrix, depvar)
    print("Ортогональный многочлен: w_3(x) = x^3 + ({:.4f}) * x^2 + ({:.4f}) * x + ({:.4f})".format(c, d, e))

    # находим корни w3(x) бисекцией
    func_w3 = lambda x: x**3 + c * x**2 + d * x + e

    res = []
    eps = 1e-8
    values = polynom.get_values(a, b, 2*m, f=func_w3)
    for i in range(len(values) - 1):
        res1 = inverse.solve(func_w3, values[i][0], values[i+1][0], eps)
        if res1 is not None:
            res.append(res1)

    i = 0
    while i < len(res) - 1:
        if abs(res[i] - res[i+1]) < eps:
            del res[i]
        else:
            i += 1

    x1, x2, x3 = res
    print("x1 = {:.10f}; x2 = {:.10f}; x3 = {:.10f}".format(x1, x2, x3))

    # находим A1, A2, A3
    matrix = [[1,     1,     1],
              [x1,    x2,    x3],
              [x1**2, x2**2, x3**2]]
    depvar = [mu[0], mu[1], mu[2]]
    A1, A2, A3 = numpy.linalg.solve(matrix, depvar)
    print("A1 = {:.10f}; A2 = {:.10f}; A3 = {:.10f}".format(A1, A2, A3))

    # делаем проверку
    test_value = A1 * x1**5 + A2 * x2**5 + A3 * x3**5
    if abs(test_value - mu[5]) < eps:
        print("Проверка пройдена ({:.10f} = {:.10f}).".format(test_value, mu[5]))

    # вычисляем интеграл
    J = A1 * func_f(x1) + A2 * func_f(x2) + A3 * func_f(x3)
    print("Приближённое значение интеграла (сделанное с помощью КФ типа Гаусса с 3 узлами) от w(x)f(x) по [a,b] равно: {}".format(J))


if __name__ == '__main__':
    main()
