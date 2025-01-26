r"""<p>By listing the first six prime numbers: $2, 3, 5, 7, 11$, and $13$, we can see that the $6$th prime is $13$.</p>
<p>What is the $10\,001$st prime number?</p>
"""
def is_prime(k):
    return True

def find_nth_prime(n):
    prime_count = 0
    k=2
    while True:
        if is_prime(k):
            prime_count += 1  #K is the ith prime where i = prime_count
            if prime_count == n:
                return k
        k += 1

print(find_nth_prime(4))

if __name__ == "__main__":
    answers = [
        (1, 2),
        (2, 3),
        (3, 5),
        (4, 7),
        (5, 11),
        (6, 13),
        (7, 17),
        (8, 19),
        (9, 23),
        (10, 29),
        (20, 71),
        (40, 173),
        (80, 409),
        (100, 541),
    ]
for i, (n, expected) in enumerate(answers):
        result = find_nth_prime(n)
        if result != expected:
             print(f"""
Failed for {n=}:
    ith prime should be {expected} but find_nth_prime({n}) returned {result}
""")
