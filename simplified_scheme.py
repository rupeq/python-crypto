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

    return min(secret_key)

def aSide(n, secret_key):
    print(secret_key)
    r = randint(0, n-1)
    x = r * r % n
    bit = bSide(bit=True)

    if bit == 0:
        print(x, "bit 0")
        return bSide(n=n, r=r, x=x)
    elif bit == 1:
        y = r * secret_key % n
        print(y, "bit 1")
        return bSide(n=n, y=y, x=x)

def bSide(n=0, bit=False, x=0, y=0, r=0, secret_key = 0):

    if bit:
        return randint(0, 1)

    if r:
        _x = r * r % n

        print(_x, "r")
        if x == _x:
            return True

    if y:
        _x = y * y * secret_key % n

        print(_x, "y")
        if x == _x:
            return True

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
        k = getK()
        open_keys = getV(n, k, [])
        secret_key = getS(open_keys, n, [])
        flag = aSide(n, secret_key)
        result.append(f"yes") if flag else result.append(f"no")
        t -= 1

    counter =0

    for element in result:
        if element == "yes":
            counter += 1
    if counter > t // 2:
        print("Сторона Б удовлетворена!")
    else:
        print("Сторона Б неудовлетворена!")