s = """
234324
235325
364436
3454754
745747
54745745
746435
46457
43636436
34545745
345346
45347
45636346
3467347
"""

nums = []

num = ""
for c in s:
    if c in "1234567890":
        num += c
    elif num:
        nums.append(int(num))
        num = ""


s = s
result = s.split("\n")


sum_ = 0
for i in range(len(result)):
    sum_ = sum_ + int(result[i])

