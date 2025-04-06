r"""<p>Let $d(n)$ be defined as the sum of proper divisors of $n$ (numbers less than $n$ which divide evenly into $n$).<br>
If $d(a) = b$ and $d(b) = a$, where $a \ne b$, then $a$ and $b$ are an amicable pair and each of $a$ and $b$ are called amicable numbers.</p>
<p>For example, the proper divisors of $220$ are $1, 2, 4, 5, 10, 11, 20, 22, 44, 55$ and $110$; therefore $d(220) = 284$. The proper divisors of $284$ are $1, 2, 4, 71$ and $142$; so $d(284) = 220$.</p>
<p>Evaluate the sum of all the amicable numbers under $10000$.</p>"""

# Sum of divisors = (p^0 + p^1 + … + p^m) × (q^0 + q^1 + … + q^n)
from euler import get_prime_factorization

print(get_prime_factorization(220))


def get_sum_of_divisors(n):
    pf = get_prime_factorization(n)
    product = 1
    for prime, exponent in pf.items():
        sum = 0
        for i in range(exponent + 1):
            sum += prime**i
        product *= sum
    return product - n


print(get_sum_of_divisors(284))
