# --- Day 10: Factory ---
# https://adventofcode.com/2025/day/10
from itertools import combinations, chain


def parse_input(text: str) -> tuple[list[int], list[list[int]], list[int]]:
  new_text = text.replace('] ', '-').replace(' {', '-').split('-')

  lights = [0 if char == '.' else 1 for char in new_text[0].replace('[', '')]

  buttons: list[list[int]] = []
  for button in new_text[1].replace('(', '').replace(')', '').split(' '):
    buttons.append([int(i) for i in button.split(',')])

  joltages = [int(i) for i in new_text[2].replace('}', '').split(',')]
  return lights, buttons, joltages

def get_output(buttons: tuple, length: int) -> list[int]:
  result = [0] * length
  for button in buttons:
    for indicator in button:
      result[indicator] = int(not result[indicator])
  return result

def all_subsets(iterable) -> chain[tuple[list[list[int]]]]:
  return chain(*map(lambda x: combinations(iterable, x), range(1, len(iterable) + 1)))

lights: list[list[int]] = []
buttons: list[list[list[int]]] = []
joltages: list[list[int]] = []
rows = 0
while row := input():
  l, b, j = parse_input(row)
  lights.append(l)
  buttons.append(b)
  joltages.append(j)
  rows += 1

total = 0
for row in range(rows):
  for comb in all_subsets(buttons[row]):
    if get_output(comb, len(lights[row])) == lights[row]:
      total += len(comb)
      break

print(f'Part 1 solution: {total}')
