#!/usr/bin/python3

import math
from inverse import solve, way2

q = 0

def gamma(n):
    return math.factorial(n)


def P(x, n):
    arr = [1, x]
    for i in range(2, n+1):
        arr.append(((2*i - 1)/i) * x * arr[i - 1] - ((i - 1)/i) * arr[i - 2])
    return arr[n]

def Pd(x, n):
    return (n / (1 - x * x)) * (P(x, n - 1) - x * P(x, n))


def H(x, n):
    arr = [1, 2*x]
    for i in range(2, n+1):
        arr.append(2 * x * arr[i - 1] - 2 * (i - 1) * arr[i - 2])
    return arr[n]

def Hd(x, n):
    return 2 * n * H(x, n - 1)


def L(x, n, alpha):
    arr = [1, alpha + 1 - x]
    for i in range(2, n+1):
        a = i
        b = i - 1 + alpha
        c = 2 * (i - 1) + alpha - x + 1
        arr.append((c * arr[i - 1] - b * arr[i - 2]) / a)

    return arr[n]

def Ld(x, n):
    return - L(x, n - 1, q + 1) # or q+1


def bisect(a, b, s, n):
    for i in range(1, 201):
        m = (a+b)/2
        if s == 1:
            value_m = P(m, n)
            value_r = P(b, n)
            value_l = P(a, n)
        elif s == 4:
            value_m = H(m , n);
            value_r = H(b, n);
            value_l = H(a, n);
        elif s == 5:
            value_m = L(m , n, 0)
            value_r = L(b, n, 0)
            value_l = L(a, n, 0)

        if value_r > value_l:
            if value_m <= 0:
                a = m
            else:
                b = m
        else:
            if value_m < 0:
                b = m
            else:
                a = m
    return a



def get_values(m, f): # return [(x0,f0), (x2,f2), ..., (x_(m),f_(m)]
    a = -1
    b = 1
    m = 10000
    res = []
    for i in range(m+1):
        x = a + i * (b - a) / m
        y = f(x)
        res.append((x, y))

    return res


def main():
    N = int(input('Введите степень многочлена: '))
    print()

    a, b = -1, 1
    k = 0
    m = 10000
    h = (b - a) / m
    x = []

    for i in range(m+1):
        l = a + i * h;
        r = l + h;
        value_r = P(r, N)
        value_l = P(l, N)

        if value_r * value_l < 0:
            k+=1
            x_res = bisect(l, r, 1, N)
            x.append(x_res)


    coef = []
    for i in range(1, N+1):
        coef.append(1 / ((1 - x[i-1]**2) * Pd(x[i-1], N) * Pd(x[i-1], N)))

    print('Корни многочлена Лежандра:')
    for i in range(len(x)):
        print('{:>15.11f}'.format(x[i]))
    print('Коэффициенты квадратурной формулы Гаусса:')
    for i in range(len(coef)):
        print('{:>15.11f}'.format(coef[i]))
    print()

    x = []
    coef = []
    for i in range(1, N+1):
        x.append(math.cos(math.pi*(2*i-1)/(2*N)))
        coef.append(math.pi/N)

    print('Корни многочлена Чебышёва первого рода:')
    for i in range(len(x)):
        print('{:>15.11f}'.format(x[i]))
    print('Коэффициенты квадратурной формулы Мелера:')
    for i in range(len(coef)):
        print('{:>15.11f}'.format(coef[i]))
    print()

    x = []
    coef = []
    for i in range(1, N+1):
        x.append(math.cos(math.pi * i / (N+1)))
        coef.append(math.sin(math.pi*i/(N+1))*math.sin(math.pi*i/(N+1))*math.pi/(N+1))

    print('Корни многочлена Чебышёва второго рода:')
    for i in range(len(x)):
        print('{:>15.11f}'.format(x[i]))
    print('Коэффициенты соответствующей квадратурной формулы:')
    for i in range(len(coef)):
        print('{:>15.11f}'.format(coef[i]))
    print()

    a = -100
    b = 100
    k = 0
    m = 10000
    h = (b-a)/m
    x = []
    coef = []
    for i in range(m):
        l = a + i * h
        r = l + h
        value_r = H(r, N)
        value_l = H(l, N)
        if value_r * value_l < 0:
            x_res = bisect(l, r, 4, N)
            k += 1
            x.append(x_res)

    p = math.sqrt(math.pi)
    p = p * 2**(2*N+1)
    p = p * math.factorial(N)
    for i in range(1, N+1):
        coef.append(p / (Hd(x[i-1], N) * Hd(x[i-1], N)))

    print('Корни многочлена Чебышёва-Эрмита:')
    for i in range(len(x)):
        print('{:>17.11f}'.format(x[i]))
    print('Коэффициенты соответствующей квадратурной формулы:')
    for i in range(len(coef)):
        print('{:>17.11f}'.format(coef[i]))
    print()

    a = 0
    b = 1000
    k = 0
    m = 10000
    h = (b-a) / m
    x = []
    coef = []
    q = 2
    for i in range(m+1):
        l = a + i * h
        r = l + h
        value_r = L(r, N, q)
        value_l = L(l, N, q)
        if value_r * value_l < 0:
            x_res = bisect(l, r, 5, N)
            k += 1
            x.append(x_res)


    x += x[:N-k]
    p = math.factorial(N)
    for i in range(1, N+1):
        coef.append(p / (x[i-1] * Ld(x[i-1], N) * Ld(x[i-1], N)) * gamma(N + 1))

    print('Корни многочлена Чебышёва-Лагерра:')
    for i in range(k):
        print('{:>15.11f}'.format(x[i]))
    print('Коэффициенты соответствующей квадратурной формулы:')
    for i in range(len(coef)):
        print('{:>25.11f}'.format(coef[i]))
    print()



if __name__ == '__main__':
    main()
