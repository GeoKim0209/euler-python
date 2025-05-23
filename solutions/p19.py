# Counting Sundays

r"""
<p>You are given the following information, but you may prefer to do some research for yourself.</p>
<ul><li>1 Jan 1900 was a Monday.</li>
<li>Thirty days has September,<br />
April, June and November.<br />
All the rest have thirty-one,<br />
Saving February alone,<br />
Which has twenty-eight, rain or shine.<br />
And on leap years, twenty-nine.</li>
<li>A leap year occurs on any year evenly divisible by 4, but not on a century unless it is divisible by 400.</li>
</ul><p>How many Sundays fell on the first of the month during the twentieth century (1 Jan 1901 to 31 Dec 2000)?</p>"""


def get_n_days_after(year, month, day, n):
    year_after = year
    month_after = month
    day_after = day + n
    maximum_day = get_maximum_day(month)
    if month == 2 and is_leap_year(year):
        maximum_day += 1
    if day_after > maximum_day:
        if month_after == 12:
            year_after += 1
            month_after = 1
        else:
            month_after += 1
        day_after -= maximum_day

    return year_after, month_after, day_after


def is_leap_year(year):
    if year % 100 == 0:
        if year % 400 == 0:
            return True
        else:
            return False
    elif year % 4 == 0:
        return True
    else:
        return False


def get_maximum_day(month):
    if month in [9, 4, 6, 11]:
        return 30
    elif month in [1, 3, 5, 7, 8, 10, 12]:
        return 31
    elif month == 2:
        return 28


year = 1901
month = 1
day = 1
count = 0
while year < 2001:
    year, month, day = get_n_days_after(year, month, day, 7)
    if day == 1:
        count += 1
print(count)
