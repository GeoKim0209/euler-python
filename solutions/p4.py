# Largest Palindrome Product

"""
<p>A palindromic number reads the same both ways. The largest palindrome made from the product of two $2$-digit numbers is $9009 = 91 \times 99$.</p>
<p>Find the largest palindrome made from the product of two $3$-digit numbers.</p>
"""

max_palindrome = 0
palindrome = 0
for a in range(100, 1000):
    for b in range(100, 1000):
        num = a * b
        if str(num) == str(num)[::-1]:
            palindrome = num
        if palindrome > max_palindrome:
            max_palindrome = palindrome
            a_value = a
            b_value = b
print(a_value, b_value)
print(max_palindrome)
