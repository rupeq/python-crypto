from random import randint
from math import gcd, sqrt

def isPrime(x):
    if x == 1:
        return False
    if x <= 3:
        return True
    if x % 2 == 0 or x % 3 == 0:
        return False
    for i in range(5, x // 2 + 1):
        if x % i == 0:
            return False
    return True

def findPrimefactors(s, n):
    while n%2 == 0:
        s.add(2)
        n //= 2
    for i in range(3, int(sqrt(n)), 2):
        while n%i==0:
            s.add(i)
            n //= i
    if n > 2:
        s.add(n)
def power(x, y, p):
    res = 1
    x %= p
    while y:
        if y&1: # нечетно
            res = (res * x) % p
        y = y >> 1
        x = (x * x) % p
    return res

def findPrimitive(n):
    s = set()
    if not isPrime(n):
        return f"{n} не простое число!"
    fi = n - 1
    findPrimefactors(s, fi)
    for r in range(2, fi+1):
        flag = False
        for i in s:
            if (power(r, fi // i, n) == 1):
                flag = True
                break
        if not flag:
            return r, fi

    return "Первичный корень не найден"

def cipher(m, y, fi, result_ab=[]):
    for i in m:
        k = randint(2, fi)
        a = g ** k % p
        b = y ** k * i % p
        result_ab.append((a, b))
    return result_ab

def decipher(c, decipher = []):
    for a, b in c:
        t = b*a**(p-1-x) % p
        decipher.append(chr(t+1039))
    return decipher

if __name__ == "__main__":
    message = [ord(letter)-1039 for letter in input("Введите шифруемое сообщение: ")]
    print(f"Открытое сообщение {message}")
    p = int(input("Введите простое число p = "))
    result_ab = []

    if not isPrime(p):
        print(f"Число {p} не простое!")
    else:
        g, fi = findPrimitive(p)
        ans = input(f"Выбрано число g = {g}. Хотите выбрать другое? (да/нет)? ")
        while ans != "нет":
            g = int(input("Число g = "))
            break
        x = int(input(f"Введите x, меньшее {p} = "))
        y = g ** x % p
        c = cipher(message, y, fi)
        print(f"Зашифрованное сообщение {c}")
        d = decipher(c)
        d = "".join(d)
        print(f"Расшифрованное сообщение: {d}")