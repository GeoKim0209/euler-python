# Summation of Primes

r"""<p>The sum of the primes below $10$ is $2 + 3 + 5 + 7 = 17$.</p>
<p>Find the sum of all the primes below two million.</p>"""

from euler import is_prime

x = 0
for i in range(2, 2000001):
    if is_prime(i):
        x = x + i
print(x)
