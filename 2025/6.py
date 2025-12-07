# --- Day 6: Trash Compactor ---
# https://adventofcode.com/2025/day/6
from functools import reduce


math_hm_num: list[list[str]] = []
math_hm: list[str] = []
while row := input():
  math_hm_num.append([x for x in row.split(' ') if x])
  math_hm.append(row)

total1 = 0
for col in range(len(math_hm_num[0])):
  if math_hm_num[-1][col] == "+":
    subtotal = 0
    for i in range(len(math_hm_num) - 1):
      subtotal += int(math_hm_num[i][col])
    total1 += subtotal
  elif math_hm_num[-1][col] == "*":
    subtotal = 1
    for i in range(len(math_hm_num) - 1):
      subtotal *= int(math_hm_num[i][col])
    total1 += subtotal

print(f'Part 1 solution: {total1}')

total2 = 0
numbers: list[int] = []
for col in reversed(range(len(math_hm[0]))):
  number: list[str] = []
  for row in range(len(math_hm)):
    curr = math_hm[row][col]
    if row == len(math_hm) - 1:
      new_number = ''.join(number)
      if new_number == '':
        number.clear()
        continue
      numbers.append(int(new_number))

    if curr == ' ':
      continue
    elif curr == '+':
      total2 += sum(numbers)
      numbers.clear()
    elif curr == '*':
      total2 += reduce(lambda x, y: x * y, numbers, 1)
      numbers.clear()
    else:
      number.append(curr)

print(f'Part 2 solution: {total2}')
