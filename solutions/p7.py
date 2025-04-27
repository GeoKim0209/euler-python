# 10,001st Prime

r"""<p>By listing the first six prime numbers: $2, 3, 5, 7, 11$, and $13$, we can see that the $6$th prime is $13$.</p>
<p>What is the $10\,001$st prime number?</p>
"""

import math


def is_prime(k):
    r"""is $n$ prime?

    - divide n by 2
      - if divisible $\rarr$ not prime
      - else $\rarr$ keep going
    - divide n by 3
      - if divisible $\rarr$ not prime
      - else $\rarr$ keep going
    ...
    - divide n by $\lfloor\sqrt{n}\rfloor$
      - if divisible $\rarr$ not prime
      - else $\rarr$ PRIME!"""
    for i in range(2, int(math.sqrt(k)) + 1):
        if k % i == 0:
            return False
    return True


def find_nth_prime(n):
    prime_count = 0
    k = 2
    while True:
        if is_prime(k):
            prime_count += 1  # K is the ith prime where i = prime_count
            if prime_count == n:
                return k
        k += 1


print(find_nth_prime(10001))
