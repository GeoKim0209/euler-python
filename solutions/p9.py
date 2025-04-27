# Special Pythagorean Triplet

r"""<p>A Pythagorean triplet is a set of three natural numbers, $a \lt b \lt c$, for which,
$$a^2 + b^2 = c^2.$$</p>
<p>For example, $3^2 + 4^2 = 9 + 16 = 25 = 5^2$.</p>
<p>There exists exactly one Pythagorean triplet for which $a + b + c = 1000$.<br>Find the product $abc$.</p>"""

for a in range(1, 500):
    for b in range(a + 1, 500):
        c = 1000 - a - b
        if a**2 + b**2 == c**2:
            print("The Pythagorean triplet is:", a, b, c)
            print("The product abc is:", a * b * c)
            break
