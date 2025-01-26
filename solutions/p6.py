"""
<p>The sum of the squares of the first ten natural numbers is,</p>
$$1^2 + 2^2 + ... + 10^2 = 385.$$
<p>The square of the sum of the first ten natural numbers is,</p>
$$(1 + 2 + ... + 10)^2 = 55^2 = 3025.$$
<p>Hence the difference between the sum of the squares of the first ten natural numbers and the square of the sum is $3025 - 385 = 2640$.</p>
<p>Find the difference between the sum of the squares of the first one hundred natural numbers and the square of the sum.</p>
"""


def f(n):
    x = 0
    y = 0
    for i in range(1, n + 1):
        x = x + i**2
    print(x)

    for i in range(1, n + 1):
        y = y + i
    print(y**2)

    print(y**2 - x)


f(100)
