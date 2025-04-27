# Largest Prime Factor

"""<p>The prime factors of $13195$ are $5, 7, 13$ and $29$.</p>
<p>What is the largest prime factor of the number $600851475143$?</p>"""

import math
from collections import Counter

r = []
n = 600851475143
while n > 1:
    factor = n
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            # n is divisible by i
            factor = i
            break
    r.append(factor)
    n = n // factor


print(Counter(r))
