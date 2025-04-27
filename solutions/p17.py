# Number Letter Counts

r"""
<p>If the numbers $1$ to $5$ are written out in words: one, two, three, four, five, then there are $3 + 3 + 5 + 4 + 4 = 19$ letters used in total.</p>
<p>If all the numbers from $1$ to $1000$ (one thousand) inclusive were written out in words, how many letters would be used? </p>
<br><p class="note"><b>NOTE:</b> Do not count spaces or hyphens. For example, $342$ (three hundred and forty-two) contains $23$ letters and $115$ (one hundred and fifteen) contains $20$ letters. The use of "and" when writing out numbers is in compliance with British usage.</p>"""


def num_word(n):
    mapping = {
        0: "",
        1: "one",
        2: "two",
        3: "three",
        4: "four",
        5: "five",
        6: "six",
        7: "seven",
        8: "eight",
        9: "nine",
        10: "ten",
        11: "eleven",
        12: "twelve",
        13: "thirteen",
        14: "fourteen",
        15: "fifteen",
        16: "sixteen",
        17: "seventeen",
        18: "eighteen",
        19: "nineteen",
        20: "twenty",
        30: "thirty",
        40: "forty",
        50: "fifty",
        60: "sixty",
        70: "seventy",
        80: "eighty",
        90: "ninety",
    }
    if n <= 20:
        return mapping[n]
    elif 21 <= n <= 99:
        # Ex. n == 23
        # Unit == 3,
        # Ten_digit == 2

        # Twenty-three
        unit = n % 10
        units_word = mapping[unit]  # Units_word == Three
        tens_digit = n // 10
        tens_word = mapping[tens_digit * 10]  # Tens_Word == Twenty
        return tens_word + units_word
    elif 100 <= n <= 999:
        # Ex. n == 123

        # One hundred and twenty-three
        last_two_digits = n % 100
        first_digit = n // 100
        first_digit_word = mapping[first_digit]
        if last_two_digits == 0:
            return first_digit_word + "hundred"
        else:
            last_two_digits_word = num_word(last_two_digits)
            return first_digit_word + "hundred" + "and" + last_two_digits_word


total = 0
for i in range(1, 1000):
    print(num_word(i))
    total += len(num_word(i))
total += len("onethousand")

print(total)
