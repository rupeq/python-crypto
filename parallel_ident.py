from random import randint
import gmpy2
from math import sqrt, factorial

def genN(a, b):
    return a * b

def getK():
    return randint(2, 4)

def getR():
    return randint(3, 50)

def isPrime(n):
    if (factorial(n-1)+1) % n!=0:
        return False
    else:
        return True

def QR(modulus, a):
    QR = 0
    for b in range(1,((modulus-1)//2) + 1):
        if (b ** 2) % modulus == a:
            QR = 1
        try:
            gmpy2.invert(a, n)
        except ZeroDivisionError:
            QR = 0
    return 1 if QR == 1 else 0

def getV(n, k, open_key = []):
    while len(open_key) != k:
        var = randint(3, 50)
        v = QR(n, var)
        if v == 1 and var not in open_key:
            open_key.append(var)
    return open_key

def getS(open_key, n, secret_key=[]):
    for v in open_key:
        s = sqrt(gmpy2.invert(v, n))
        if s not in secret_key:
            secret_key.append(int(s))
    return secret_key

def aSide(n, secret_key=[], r=0, binary=[]):
    if r == 0:
        r = randint(10, 30)
        if r > n:
            return aSide(n)
        return r * r % n, r
    tmp, temp = [], 1
    for s, b in zip(secret_key, binary):
        tmp.append(s ** b)
    for s in tmp:
        temp *= s
    return r * temp % n

def bSide(open_key=[], y=0, r=0, binary=[]):
    if y == 0:
        result = []
        for _ in range(0, k):
            result.append(randint(0, 1))
        return result
    tmp, temp = [], 1
    for v, b in zip(open_key, binary):
        tmp.append(v ** b)
    for v in tmp:
        temp *= v
    return y * y * temp % n

if __name__ == '__main__':
    flag = True
    while flag:
        a = int(input("Введите число а = "))
        b = int(input("Введите число b = "))
        if (isPrime(a) and isPrime(b)):
            flag = False
        else:
            print("Числа должны быть простыми!")
    t = int(input("Сколько раз повторить протокол проверки? "))
    result = []
    while t:
        n = genN(a, b)
        flag = True
        while flag:
            k = getK()
            open_keys = getV(n, k, [])
            secret_keys = getS(open_keys, n, [])
            if len(secret_keys) > 1 and len(open_keys) > 1:
                flag = False
        x, r = aSide(n)
        binary = bSide(k)
        y = aSide(n, secret_keys, r, binary)
        _x = bSide(open_keys, y, r, binary)
        result.append(f"yes") if x == _x else result.append(f"no")
        t -= 1
    counter =0
    for element in result:
        if element == "yes":
            counter += 1
    if counter > t // 2:
        print("Сторона Б удовлетворена!")
    else:
        print("Сторона Б неудовлетворена!")