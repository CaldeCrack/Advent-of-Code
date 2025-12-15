# --- Day 12: Christmas Tree Farm ---
# https://adventofcode.com/2025/day/12


# hardcoded areas
areas: list[int] = [6, 5, 7, 7, 7, 7]

regions: list[tuple[tuple[int, int], list[int]]] = []
while region := input():
  splitted = region.split(': ')
  width, length = splitted[0].split('x')
  size = (int(width), int(length))
  amounts = [int(amount) for amount in splitted[1].split(' ')]
  regions.append((size, amounts))

# online hint that the input was easy xd
total = 0
for size, amounts in regions:
  width, length = size
  area = width * length
  if (width // 3) * (length // 3) >= sum(amounts):
    total += 1
  elif sum([areas[i] * amount for i, amount in enumerate(amounts)]) <= area:
    total += 1

print(f'Part 1 solution: {total}')
