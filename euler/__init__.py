import math


def is_prime(k):
    """Utility Function that helps the user check if the inputted number is prime or composite."""
    for i in range(2, int(math.sqrt(k)) + 1):
        if k % i == 0:
            return False
    return True


def get_prime_factorization(n):
    from collections import Counter

    r = []
    while n > 1:
        factor = n
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                # n is divisible by i
                factor = i
                break
        r.append(factor)
        n = n // factor
    return Counter(r)


def get_sum_of_divisors(n):
    # Sum of divisors = (p^0 + p^1 + … + p^m) × (q^0 + q^1 + … + q^n)
    pf = get_prime_factorization(n)
    product = 1
    for prime, exponent in pf.items():
        sum = 0
        for i in range(exponent + 1):
            sum += prime**i
        product *= sum
    return product - n
