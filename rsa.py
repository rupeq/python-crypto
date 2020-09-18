def gcd(x, y): # алгоритм Евклида
    while y:
        gcd = x % y
        x, y = y, gcd
    return x

def euler(x): #
    r = 0
    for i in range(1, x):
        if gcd(x, i) == 1:
            r += 1
    return r

p, q = map(int, input().split())
n = p * q
fn = (p - 1) * (q - 1)

e = int(input("Введите открытый ключ: "))

if not gcd(fn, e) == 1:
    print("Числа fn и e не взаимно простые!")
else:
    d = e ** ((euler(euler(n))) - 1) % fn

    m = input("Введите сообщение: ")
    mas = [ord(letter) for letter in m]
    print(mas)

    cypher = [m ** e % n for m in mas]
    decypher = [chr(c ** d % n) for c in cypher]
    print(f"""Вы ввели: {m}
    Зашифрованно: {cypher}
    Расшифрованно: {decypher}""")