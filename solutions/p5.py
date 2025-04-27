# Smallest Multiple

"""
<p>$2520$ is the smallest number that can be divided by each of the numbers from $1$ to $10$ without any remainder.</p>
<p>What is the smallest positive number that is <strong class="tooltip">evenly divisible</strong> by all of the numbers from $1$ to $20$?</p>

"""

n = 20
while True:
    r = True
    for i in range(1, 21):
        if n % i != 0:
            r = False
            break
    if r:
        print(n)
        break
    n = n + 1
