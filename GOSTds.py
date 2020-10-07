from math import sqrt
from hashlib import sha224
from random import randint
import gmpy2

def getP():
    p = int(input("Введите p = "))
    if not isPrime(p):
        print(f"Число {p} должно быть простым")
        return getP()
    return p

def getQ(p):
    q = int(input("Введите q = "))
    if not isPrime(q):
        print(f"Число {q} должно быть простым")
        return getQ(p)
    elif (p-1) % q:
        print(f"Число {q} не является делителем числа {p}")
        return getQ(p)
    return q

def getA(p, q):
    a = int(input("Введите а = "))
    if 1 < a < p-1:
        if a ** q % p == 1:
            return a
        else:
            print(f'{a} должно быть корнем уравнения a^q mod p = 1')
            return getA(p, q)
    else:
        print(f"{a} должно быть > 1 и < {p-1}")
        return getA(p, q)


def isPrime(n):
    return n > 1 and all(n%i for i in range(2, int(sqrt(n)-1)))

def toAscii(m):
    mes = 0
    for i in m:
        mes += ord(i)
    return mes

def getKeys():
    p = getP()
    q = getQ(p)
    a = getA(p, q)
    x = randint(1, q) # закртый ключ
    y = a ** x % p # открытый ключ
    return p, q, a, x, y

def encrypt():
    p, q, a, x, y = getKeys()
    k = 5
    r = (a ** k % p) % q
    message = open("message.txt", "r").read()
    m = message.encode('utf-8')
    m = sha224(m).hexdigest()
    m = toAscii(m)
    s = (k * m + x * r) % q
    with open('transfer.txt', 'w') as f:
        f.write(message + ' ' + str(r) + ' ' + str(s))
    with open('publickey.txt', 'w') as f:
        f.write(str(y) + ' ' + str(p) + ' ' + str(q) + ' ' + str(a))
    with open('privatekey.txt', 'w') as f:
        f.write(str(x))

def decrypt():
    message = open("transfer.txt", "r").read()
    start, length = 0, len(message)
    for i in message:
        start += 1
        if i.isdigit():
            break
    start = (length - start + 1) * -1
    signature = message[start:length]
    message = message.replace(signature, '').strip()
    r, s = map(int, signature.split())
    private_key = int(open("privatekey.txt",'r').read().strip())
    y, p, q, a = map(int, open("publickey.txt", "r").read().strip().split())
    #
    m = message.encode('utf-8')
    m = sha224(m).hexdigest()
    m = toAscii(m)
    w = gmpy2.invert(m, q)
    u1 = w * s % q
    u2 = (q - r) * w % q
    v = ((a ** u1 * y ** u2) % p) % q
    return "Подпись верна." if v == r else "Подпись не верна."

if __name__ == "__main__":
    q = input("Введите 1 для шифрования и 0 для дешифрования: ")
    if q == '1':
        encrypt()
    elif q == '0':
        print(decrypt())
    else:
        print("Неверный ввод!")
