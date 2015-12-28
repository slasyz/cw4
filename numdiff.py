#!/usr/bin/python3

import math
import polynom


def diff1_calculate(values, h):
    res = []
    y = [y for x,y in values]

    for i in range(2):
        r = (-3*y[i] + 4*y[i+1] - y[i+2]) / (2*h)
        res.append(r)

    for i in range(2, len(values)):
        #print("3 * {:.4f} - 4 * {:.4f} + {:.4f}".format(y[i], y[i-1], y[i-2]))
        r = ( 3*y[i] - 4*y[i-1] + y[i-2]) / (2*h)
        res.append(r)

    return res


def diff2_calculate(values, h):
    res = [None,]
    y = [y for x,y in values]

    for i in range(1, len(values)-1):
        r = (y[i+1] - 2*y[i] + y[i-1]) / h**2
        res.append(r)

    res.append(None)
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
    diff1 = lambda x: math.exp(-x) + 2*x
    diff2 = lambda x: -math.exp(-x) + 2
    values = polynom.get_values(a, b, m, f=func)
    diff1_values = diff1_calculate(values, h)
    diff2_values = diff2_calculate(values, h)
    print('{:>15} | {:>15} | {:>15} | {:>20} | {:>15} | {:>20}'.format('x', 'f(x)', 'f\'(x)чд', '|f\'(x)т - f\'(x)чд|', 'f\'\'(x)чд', '|f\'\'(x)т - f\'\'(x)чд|'))
    print('-'*(15*4+20*2+5*3+3))
    for i in range(len(values)):
        x, y = values[i]
        fx = diff1_values[i]
        fxx = diff2_values[i]
        d1 = abs(diff1(x) - fx)

        if fxx is not None:
            d2 = abs(diff2(x) - fxx)
            print('{:> 15.6} | {:> 15.6f} | {:> 15.6f} | {:> 20.6f} | {:> 15.10f} | {:> 20.15f}'.format(x, y, fx, d1, fxx, d2))
        else:
            print('{:> 15.6} | {:> 15.6f} | {:> 15.6f} | {:> 20.6f} | {:>15.6} | {:>20.6}'.format(x, y, fx, d1, '', ''))




if __name__ == '__main__':
    main()
