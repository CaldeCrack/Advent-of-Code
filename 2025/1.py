# --- Day 1: Secret Entrance ---
# https://adventofcode.com/2025/day/1

dial = 50
total_zeros = 0
total_passes = 0

while rot_str := input():
  direction = 1 if rot_str[0] == "R" else -1
  distance = int(rot_str[1:])

  for step in range(1, distance + 1):
    pos = (dial + step * direction) % 100
    if pos == 0:
      total_passes += 1
  dial = (dial + distance * direction) % 100

  if dial == 0:
    total_zeros += 1

print(f'Part 1 solution: {total_zeros}')
print(f'Part 2 solution: {total_passes}')
