r"""<p>In the $20 \times 20$ grid below, four numbers along a diagonal line have been marked in red.</p>
<p class="monospace center">
08 02 22 97 38 15 00 40 00 75 04 05 07 78 52 12 50 77 91 08<br>
49 49 99 40 17 81 18 57 60 87 17 40 98 43 69 48 04 56 62 00<br>
81 49 31 73 55 79 14 29 93 71 40 67 53 88 30 03 49 13 36 65<br>
52 70 95 23 04 60 11 42 69 24 68 56 01 32 56 71 37 02 36 91<br>
22 31 16 71 51 67 63 89 41 92 36 54 22 40 40 28 66 33 13 80<br>
24 47 32 60 99 03 45 02 44 75 33 53 78 36 84 20 35 17 12 50<br>
32 98 81 28 64 23 67 10 <span class="red"><b>26</b></span> 38 40 67 59 54 70 66 18 38 64 70<br>
67 26 20 68 02 62 12 20 95 <span class="red"><b>63</b></span> 94 39 63 08 40 91 66 49 94 21<br>
24 55 58 05 66 73 99 26 97 17 <span class="red"><b>78</b></span> 78 96 83 14 88 34 89 63 72<br>
21 36 23 09 75 00 76 44 20 45 35 <span class="red"><b>14</b></span> 00 61 33 97 34 31 33 95<br>
78 17 53 28 22 75 31 67 15 94 03 80 04 62 16 14 09 53 56 92<br>
16 39 05 42 96 35 31 47 55 58 88 24 00 17 54 24 36 29 85 57<br>
86 56 00 48 35 71 89 07 05 44 44 37 44 60 21 58 51 54 17 58<br>
19 80 81 68 05 94 47 69 28 73 92 13 86 52 17 77 04 89 55 40<br>
04 52 08 83 97 35 99 16 07 97 57 32 16 26 26 79 33 27 98 66<br>
88 36 68 87 57 62 20 72 03 46 33 67 46 55 12 32 63 93 53 69<br>
04 42 16 73 38 25 39 11 24 94 72 18 08 46 29 32 40 62 76 36<br>
20 69 36 41 72 30 23 88 34 62 99 69 82 67 59 85 74 04 36 16<br>
20 73 35 29 78 31 90 01 74 31 49 71 48 86 81 16 23 57 05 54<br>
01 70 54 71 83 51 54 69 16 92 33 48 61 43 52 01 89 19 67 48<br></p>
<p>The product of these numbers is $26 \times 63 \times 78 \times 14 = 1788696$.</p>
<p>What is the greatest product of four adjacent numbers in the same direction (up, down, left, right, or diagonally) in the $20 \times 20$ grid?</p>"""


def print_grid(grid):
    for row in grid:
        print(" ".join(row))


def multiply_list(s: list):
    # multiply_list(["11","7"]) -> 77
    product = 1
    for i in s:
        product = product * int(i)
    return product


string = """08 02 22 97 38
49 49 99 40 17
81 49 31 73 55
52 70 95 23 04
22 31 16 71 51"""

row_strings = string.split("\n")
grid = []
for row_string in row_strings:
    grid.append(row_string.split())
print_grid(grid)


# Attempt to find the greatest products of two adjacent numbers horizontally
max_value = 0
n = 2
for k in range(len(grid)):
    s = grid[k]
    for i in range(len(s)):
        try:
            if multiply_list(s[i : i + n]) > max_value:
                max_value = multiply_list(s[i : i + n])
                print(max_value, s[i : i + n])
        except:
            pass

# Attempt to find the greatest products of two adjacent numbers vertically
max_value = 0
n = 2
for k in range(len(grid)):
    s = grid[k]
    for i in range(len(s)):
        try:
            pair = [grid[x][i] for x in range(k, k + n)]
            if multiply_list(pair) > max_value:
                max_value = multiply_list(pair)
                print(max_value, pair)
        except:
            pass

# Attempt to find the greatest products of two adjacent numbers up-right
max_value = 0
n = 5
for k in range(len(grid)):
    s = grid[k]
    for i in range(len(s)):
        # Move from Index(1,1) to Index(0,2)
        # (4,0)->(3,1)->(2,2)->(1,3)->(0,4)
        # (k-0,i+0)->(k-1,i+1)->...-> (k-(n-1),i+(n-1))
        try:
            pair = []
            for x in range(n):
                assert k - x >= 0
                pair.append(grid[k - x][i + x])
            if multiply_list(pair) > max_value:
                max_value = multiply_list(pair)
                print(max_value, pair)
        except:
            pass
