# Multiples of 3 or 5

"""
<p>If we list all the natural numbers below $10$ that are multiples of $3$ or $5$, we get $3, 5, 6$ and $9$. The sum of these multiples is $23$.</p>
<p>Find the sum of all the multiples of $3$ or $5$ below $1000$.</p>
"""

x = 0
for i in range(1, 1000):
    if i % 15 == 0:
        x = x + i
    elif i % 5 == 0:
        x = x + i
    elif i % 3 == 0:
        x = x + i
print(x)
