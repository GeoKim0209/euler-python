r"""<p>Using <a href="resources/documents/0022_names.txt">names.txt</a> (right click and 'Save Link/Target As...'), a 46K text file containing over five-thousand first names, begin by sorting it into alphabetical order. Then working out the alphabetical value for each name, multiply this value by its alphabetical position in the list to obtain a name score.</p>
<p>For example, when the list is sorted into alphabetical order, COLIN, which is worth $3 + 15 + 12 + 9 + 14 = 53$, is the $938$th name in the list. So, COLIN would obtain a score of $938 \times 53 = 49714$.</p>
<p>What is the total of all the name scores in the file?</p>"""


def get_alphabet_score(name: str):
    total = 0
    for i in name:
        total += ord(i.upper()) - 64
    return total


with open("solutions/names.txt", "r") as f:
    text = f.readlines()[0]

text = text.split(",")
print(len(text))
print(text[:100])
names = []
for i in text:
    i = i.replace('"', "")
    names.append(i)

names = sorted(names)

total = 0
for i, name in enumerate(names):
    total += (i + 1) * get_alphabet_score(name)

print(total)
