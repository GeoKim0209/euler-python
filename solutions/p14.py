r"""<p>The following iterative sequence is defined for the set of positive integers:</p>
<ul style="list-style-type:none;">
<li>$n \to n/2$ ($n$ is even)</li>
<li>$n \to 3n + 1$ ($n$ is odd)</li></ul>
<p>Using the rule above and starting with $13$, we generate the following sequence:
$$13 \to 40 \to 20 \to 10 \to 5 \to 16 \to 8 \to 4 \to 2 \to 1.$$</p>
<p>It can be seen that this sequence (starting at $13$ and finishing at $1$) contains $10$ terms. Although it has not been proved yet (Collatz Problem), it is thought that all starting numbers finish at $1$.</p>
<p>Which starting number, under one million, produces the longest chain?</p>
<p class="note"><b>NOTE:</b> Once the chain starts the terms are allowed to go above one million.</p>"""


def collatz(n):
    if n % 2 == 0:
        return n / 2
    else:
        return n * 3 + 1


memo = {}
max_count = 0
max_n = 0
for n in range(1, 10000001):
    initial_n = n
    count = 0
    chain = [initial_n]
    while n != 1:
        n = collatz(n)
        count += 1
        chain.append(n)
        if n in memo:
            count += memo[n]
            break
    if count > max_count:
        max_n = initial_n
        max_count = count

    # Update memo
    for val in chain:
        if val in memo:
            break
        memo[val] = count
        count-=1
print(max_n)
