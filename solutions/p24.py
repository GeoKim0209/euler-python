# Lexicographic Permutations

r"""<p>A permutation is an ordered arrangement of objects. For example, 3124 is one possible permutation of the digits 1, 2, 3 and 4. If all of the permutations are listed numerically or alphabetically, we call it lexicographic order. The lexicographic permutations of 0, 1 and 2 are:</p>
<p class="center">012   021   102   120   201   210</p>
<p>What is the millionth lexicographic permutation of the digits 0, 1, 2, 3, 4, 5, 6, 7, 8 and 9?</p>
"""

"""
Brainstorm:
Sorting order --> Bring sort algorithm from euler library
Lexicographic Permutation --> Factorial?
set=[0,1,2,3,4,5,6,7,8,9]
Bring "factorial" module?
for i in range(factorial(10)) --> 10digits = 10!

Starting from 0: 0xxxxx... --> 9! --> 362,880
Starting from 1: 1xxxxx... --> 9! --> 362,880
9!*y --> Less than 1 million --> 362880*3 = 1088640 --> Starting number = 2 
...

2013456789 = 725761th num = 2*(9!) + 1
2098765431 = 
2103456789 = 766081th num = 2*(9!) + 1*8! + 1
2198765430 =
2301456789 = 806401th num = 2*(9!) + 2*8! + 1

2401356789 = 846721th num = 2*(9!) + 3*8! + 1
2501346789 = 887041th num = 2*(9!) + 4*8! + 1
2601345789 = 927361th num = 2*(9!) + 5*8! + 1
2701345689 = 967681th num = 2*(9!) + 6*8! + 1

2710345689 = 972721th num = 2*(9!) + 6*8! + 1*7! + 1
...
2780|134569 = 997921th num = 2*(9!) + 6*8! + 6*7! + 1
2783|014569 = 999361th num = 2*(9!) + 6*8! + 6*7! + 2*6! + 1
27839|01456 = 999961th num = 2*(9!) + 6*8! + 6*7! + 2*6! + 5*5! + 1
278391|0456 = 999985th num = 2*(9!) + 6*8! + 6*7! + 2*6! + 5*5! + 1*4! + 1
2783915|046 = 999997th num = 2*(9!) + 6*8! + 6*7! + 2*6! + 5*5! + 1*4! + 2*3! + 1
2783915064
2783915406
2783915460
"""
