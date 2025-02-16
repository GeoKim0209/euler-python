import math


def is_prime(k):
    for i in range(2, int(math.sqrt(k)) + 1):
        if k % i == 0:
            return False
    return True

def get_prime_factorization(n):
    from collections import Counter
    r = []
    while n > 1:
        factor=n
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                # n is divisible by i
                factor=i
                break
        r.append(factor)
        n = n // factor
    return Counter(r)