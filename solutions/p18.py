# Maximum Path Sum I

r"""
<p>By starting at the top of the triangle below and moving to adjacent numbers on the row below, the maximum total from top to bottom is $23$.</p>
<p class="monospace center"><span class="red"><b>3</b></span><br><span class="red"><b>7</b></span> 4<br>
2 <span class="red"><b>4</b></span> 6<br>
8 5 <span class="red"><b>9</b></span> 3</p>
<p>That is, $3 + 7 + 4 + 9 = 23$.</p>
<p>Find the maximum total from top to bottom of the triangle below:</p>
<p class="monospace center">75<br>
95 64<br>
17 47 82<br>
18 35 87 10<br>
20 04 82 47 65<br>
19 01 23 75 03 34<br>
88 02 77 73 07 63 67<br>
99 65 04 28 06 16 70 92<br>
41 41 26 56 83 40 80 70 33<br>
41 48 72 33 47 32 37 16 94 29<br>
53 71 44 65 25 43 91 52 97 51 14<br>
70 11 33 28 77 73 17 78 39 68 17 57<br>
91 71 52 38 17 14 91 43 58 50 27 29 48<br>
63 66 04 68 89 53 67 30 73 16 69 87 40 31<br>
04 62 98 27 23 09 70 98 73 93 38 53 60 04 23</p>
<p class="note"><b>NOTE:</b> As there are only $16384$ routes, it is possible to solve this problem by trying every route. However, <a href="problem=67">Problem 67</a>, is the same challenge with a triangle containing one-hundred rows; it cannot be solved by brute force, and requires a clever method! ;o)</p>"""

import itertools

s = """3
7 4
2 4 6
8 5 9 3"""

s = """75
95 64
17 47 82
18 35 87 10
20 04 82 47 65
19 01 23 75 03 34
88 02 77 73 07 63 67
99 65 04 28 06 16 70 92
41 41 26 56 83 40 80 70 33
41 48 72 33 47 32 37 16 94 29
53 71 44 65 25 43 91 52 97 51 14
70 11 33 28 77 73 17 78 39 68 17 57
91 71 52 38 17 14 91 43 58 50 27 29 48
63 66 04 68 89 53 67 30 73 16 69 87 40 31
04 62 98 27 23 09 70 98 73 93 38 53 60 04 23"""
split_s = s.split("\n")
print(f"{split_s=}")
g = [x.split(" ") for x in split_s]
print(f"{g=}")
final = []
for item in g:
    new_item = [int(x) for x in item]
    final.append(new_item)
print(final)


def compute_sum(triangle, strategy):
    # When triangle = [[3], [7, 4], [2, 4, 6], [8, 5, 9, 3]], and strategy = 'LLR'--> Output: 3+7+2+5 = 17
    index = 0
    sum = triangle[0][0]
    row_index = 0
    for d in strategy:
        # Update sum with the next row's value
        row_index += 1
        if d == "L":
            index += 0
        if d == "R":
            index += 1
        sum = sum + triangle[row_index][index]
    return sum


# NOTE to self: Possibilities of moving: Left or Right --> Left (Index doesn't change), Right(Index increases by 1)
# 2^ Number of moves to reach the end == Num of possibilities (ex. LLL, LRL, LLR.... RRR 8 moves)
# Number of possibilities: 'LLL', 'LLR', 'LRL', 'LRR', 'RLL', 'RLR', 'RRL', 'RRR'
max_sum = 0
max_x = ""
for x in itertools.product("LR", repeat=14):
    current_sum = compute_sum(final, x)
    if current_sum > max_sum:
        max_sum = current_sum
        max_x = x
print(max_x, max_sum)
