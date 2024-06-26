import time
import random

p = 28871#25013  200115
a = random.randint(0, p)
b = random.randint(0, p)
while ((((4*a)%p*a)%p*a)%p+((27*b)%p*b)%p)%p == 0:
    a = random.randint(0, p)
    b = random.randint(0, p)

def extended_euclidean_algorithm(a, b):
    """
    Возвращает кортеж из трёх элементов (gcd, x, y), такой, что
    a * x + b * y == gcd, где gcd - наибольший
    общий делитель a и b.

    В этой функции реализуется расширенный алгоритм
    Евклида и в худшем случае она выполняется O(log b).
    """
    s, old_s = 0, 1
    t, old_t = 1, 0
    r, old_r = b, a

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    return old_r, old_s, old_t


def inverse_of(n, p):
    """
    Возвращает обратную величину
    n по модулю p.

    Эта функция возвращает такое целое число m, при котором
    (n * m) % p == 1.
    """
    gcd, x, y = extended_euclidean_algorithm(n, p)
    assert (n * x + p * y) % p == gcd

    if gcd != 1:
        # Или n равно 0, или p не является простым.
        raise ValueError(
            '{} has no multiplicative inverse '
            'modulo {}'.format(n, p))
    else:
        return x % p

def new_point(p1, p2, p):
    if p1 == (0, 0):
        return p2
    elif p2 == (0, 0):
        return p1
    elif p1[0] == p2[0] and p1[1] != p2[1]:
        return (0, 0)

    if p1 == p2:
        m = ((3 * p1[0] ** 2 + (a % p)) * inverse_of(2 * p1[1], p)) % p
    else:
        m = ((p1[1] - p2[1]) * inverse_of(p1[0] - p2[0], p)) % p
    x = (m ** 2 - p1[0] - p2[0]) % p
    y = (p1[1] + m * (x - p1[0])) % p
    return (x, -y % p)


def order(point, p):
    i = 1
    tmp = point
    while tmp != (0, 0):
        tmp = new_point(tmp, point, p)
        i += 1
    return i


points = []
start = time.time()
for x in range(0, p):
    for y in range(0, p):
        if (y ** 2) % p == (x ** 3 + (a % p) * x + (b % p)) % p:
            points.append((x, y))
print("y^2 = x^3 + {0} * x + {1} (mod {2})".format(a % p, b % p, p))
print("Order curve = {0}".format(len(points)))
point = random.choice(points)
print("Order point {0}: {1}".format(point, order(point, p)))
print("Time: {} sec.".format(time.time() - start))
