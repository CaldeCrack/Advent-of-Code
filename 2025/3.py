# --- Day 3: Lobby ---
# https://adventofcode.com/2025/day/3


def max_joltage(bank: str, amount: int) -> int:
  stack: list[int] = []
  for i, char in enumerate(bank):
    while len(stack) and int(char) > stack[-1] and len(stack) + len(bank[i:]) > amount:
      stack.pop()
    if len(stack) < amount:
      stack.append(int(char))

  return int("".join([str(i) for i in stack]))

total1 = 0
total2 = 0
while bank := input():
  total1 += max_joltage(bank, 2)
  total2 += max_joltage(bank, 12)

print(f'Part 1 solution: {total1}')
print(f'Part 2 solution: {total2}')
