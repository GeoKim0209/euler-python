def collatz_sequence_length(n, memo):
    if n in memo:
        return memo[n]
    
    if n == 1:
        return 1
    
    if n % 2 == 0:
        next_n = n // 2
    else:
        next_n = 3 * n + 1
    
    memo[n] = 1 + collatz_sequence_length(next_n, memo)
    return memo[n]

def longest_collatz_chain(limit):
    longest_chain = 0
    starting_number = 0
    memo = {}
    
    for i in range(1, limit):
        length = collatz_sequence_length(i, memo)
        if length > longest_chain:
            longest_chain = length
            starting_number = i
    
    return starting_number, longest_chain

if __name__ == "__main__":
    limit = 10000000
    result = longest_collatz_chain(limit)
    print(f"Starting number under {limit} that produces the longest chain: {result[0]}")
    print(f"Length of the chain: {result[1]}")
