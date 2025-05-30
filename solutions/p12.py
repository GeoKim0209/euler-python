# Highly Divisible Triangular Number

r"""<p>The sequence of triangle numbers is generated by adding the natural numbers. So the $7$<sup>th</sup> triangle number would be $1 + 2 + 3 + 4 + 5 + 6 + 7 = 28$. The first ten terms would be:
$$1, 3, 6, 10, 15, 21, 28, 36, 45, 55, \dots$$</p>
<p>Let us list the factors of the first seven triangle numbers:</p>
\begin{align}
\mathbf 1 &amp;\colon 1\\
\mathbf 3 &amp;\colon 1,3\\
\mathbf 6 &amp;\colon 1,2,3,6\\
\mathbf{10} &amp;\colon 1,2,5,10\\
\mathbf{15} &amp;\colon 1,3,5,15\\
\mathbf{21} &amp;\colon 1,3,7,21\\
\mathbf{28} &amp;\colon 1,2,4,7,14,28
\end{align}
<p>We can see that $28$ is the first triangle number to have over five divisors.</p>
<p>What is the value of the first triangle number to have over five hundred divisors?</p>"""

from euler import get_prime_factorization


def get_triangular_number(n):
    return (n * (n + 1)) // 2


def get_num_of_divisors(n):
    """
    Method of getting how many divisors there are in a certain number (n):
    1. Get the prime factorization of n (Ex. 36 = 2^2*3^2)
    2. Then, multiply the exponents of each prime added by 1 (Ex. 36 -> (2+1)*(2+1) -> 9 )
    """
    x = get_prime_factorization(n)
    product = 1
    for v in x.values():
        product = product * (v + 1)
    return product


print(get_num_of_divisors(36))

i = 1
while True:
    x = get_triangular_number(i)
    n = get_num_of_divisors(x)
    if n > 500:
        print(x)
        break
    i += 1
