from hashlib import sha224
import gmpy2

def gcd(a, b):
    while b:
        tmp = a % b
        a = b
        b = tmp
    return a

def openExp(f):
    e = int(input())
    if 1 < e < f:
        while gcd(f, e) != 1:
            print(f'Число е = {e} должно быть взаимно простым со значением функции Эйлера fi = {f}')
            return openExp(f)
    else:
        print(f'e = {e} должно быть больше единицы и меньше функции Эйлера (f)')
        return openExp(f)
    return e

# def excEuclid(e, f):
#     if not f:
#         return e, 1, 0
#     else:
#         d, x, y = excEuclid(f, e % f)
#     return d, y, x - y * (e // f)

def privateExp(e, f):
    return gmpy2.invert(e, f)

def getKey():
    p, q = map(int, input().split())
    if p == q: return getKey()
    n = p * q
    fi = (p-1)*(q-1)
    e = openExp(fi)
    d = privateExp(e, fi)
    if d > n:
        print("Ошибка!")
    else:
        return e, n, d

def toAscii(m):
    mes = 0
    for i in m:
        mes += ord(i)
    return mes

def decrypt():
    message = open('transfer.txt').read()
    start, length = 0, len(message)
    for i in message:
        start += 1
        if i.isdigit():
            break
    start = (length - start + 1) * -1
    signature = message[start:length]
    message = message.replace(signature, '').strip()
    #
    with open('publickey.txt', 'r') as f:
        pk = f.read().split('\n')
    e, n = int(pk[0]), int(pk[1])
    _m = pow(int(signature), e, n) # прообраз
    m = message.encode('utf-8')
    m = sha224(m).hexdigest()
    m = int(toAscii(m)) # полученное х-з
    return "Подпись верна." if m == _m else "Подпись не верна."



e, n, d = getKey()
# message = input()
message = open("message.txt", "r").read()
m = message.encode('utf-8')
m = sha224(m).hexdigest()
m = toAscii(m)
signature = m ** d % n
with open('transfer.txt', 'w') as f:
	f.write(message + ' ' + str(signature))

with open('publickey.txt', 'w') as f:
    f.write(str(e).strip() + '\n' + str(n).strip())

with open('privatekey.txt', 'w') as f:
    f.write(str(d).strip())
print(decrypt())