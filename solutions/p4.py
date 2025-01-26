maxPalindrome = 0
palindrome = 0
for a in range(100,1000):
    for b in range(100,1000):
        num = a*b
        if str(num) == str(num)[::-1]:
            palindrome = num
        if palindrome > maxPalindrome:
            maxPalindrome = palindrome
            aValue=a
            bValue=b
print(aValue, bValue)
print(maxPalindrome)