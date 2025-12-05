# --- Day 4: Printing Department ---
# https://adventofcode.com/2025/day/4
from copy import deepcopy


grid: list[str] = []
while row := input():
  grid.append(row)
row_size = len(grid[0])
col_size = len(grid)
grid2 = deepcopy(grid)

def clamp(x: int, min_value: int, max_value: int) -> int:
  return max(min_value, min(x, max_value))

def adjacent_rolls(x1: int, y1: int) -> int:
  x0 = clamp(x1 - 1, 0, row_size - 1)
  x2 = clamp(x1 + 1, 0, row_size - 1)
  y0 = clamp(y1 - 1, 0, col_size - 1)
  y2 = clamp(y1 + 1, 0, col_size - 1)

  combs: set[tuple[int, int]] = set()
  combs.add((x0, y0))
  combs.add((x0, y1))
  combs.add((x0, y2))
  combs.add((x1, y0))
  # skip (x1, y1) same value
  combs.add((x1, y2))
  combs.add((x2, y0))
  combs.add((x2, y1))
  combs.add((x2, y2))

  # discard if clamping added same value
  combs.discard((x1, y1))

  adjacents = 0
  for comb in combs:
    if grid[comb[1]][comb[0]] == "@":
      adjacents += 1
  return adjacents

total1 = 0
for x in range(row_size):
  for y in range(col_size):
    if grid[y][x] == "@" and adjacent_rolls(x, y) < 4:
      total1 += 1

print(f'Part 1 solution: {total1}')

total2_prev = -1
total2 = 0
while total2_prev != total2:
  total2_prev = total2
  for x in range(row_size):
    for y in range(col_size):
      if grid[y][x] == "@" and adjacent_rolls(x, y) < 4:
        total2 += 1
        grid2[y] = grid2[y][:x] + 'x' + grid2[y][x + 1:]
  grid = deepcopy(grid2)

print(f'Part 2 solution: {total2}')
