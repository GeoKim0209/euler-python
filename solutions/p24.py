r"""<p>A permutation is an ordered arrangement of objects. For example, 3124 is one possible permutation of the digits 1, 2, 3 and 4. If all of the permutations are listed numerically or alphabetically, we call it lexicographic order. The lexicographic permutations of 0, 1 and 2 are:</p>
<p class="center">012   021   102   120   201   210</p>
<p>What is the millionth lexicographic permutation of the digits 0, 1, 2, 3, 4, 5, 6, 7, 8 and 9?</p>
"""


"""Brainstorm:
Sorting order --> Bring sort algorithm from euler library
Lexicographic Permutation --> Factorial?
set=[0,1,2,3,4,5,6,7,8,9]
Bring "factorial" module?
for i in range(factorial(10)) --> 10digits = 10!

Starting from 0: 0xxxxx... --> 9! --> 362,880
Starting from 1: 1xxxxx... --> 9! --> 362,880
9!*y --> Less than 1 million --> 362880*3 = 1088640 --> Starting number = 2 
...

2013456789 = 274261th num
21xxxxx
22xxxxx
23xxxx
 ...
"""