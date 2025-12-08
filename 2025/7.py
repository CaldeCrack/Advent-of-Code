# --- Day 7: Laboratories ---
# https://adventofcode.com/2025/day/7


def clamp(x: int, min_value: int, max_value: int) -> int:
  return max(min_value, min(x, max_value))

diagram: list[str] = []
while row := input():
  diagram.append(row)
row_len = len(diagram[0])

def get_splits() -> int:
  beam_indexes: set[int] = set({diagram[0].find('S')})
  total = 0
  for row in diagram[1:]:
    new_indexes: set[int] = set()
    for i in beam_indexes:
      if row[i] == '^':
        new_indexes.add(clamp(i - 1, 0, row_len - 1))
        new_indexes.add(clamp(i + 1, 0, row_len - 1))
        total += 1
      else:
        new_indexes.add(i)
    beam_indexes = new_indexes
  return total

print(f'Part 1 solution: {get_splits()}')

def get_timelines() -> int:
  beam_positions: dict[int, int] = {diagram[0].find('S'): 1}

  for row in diagram[1:]:
    new_positions: dict[int, int] = {}

    for beam_i, count in beam_positions.items():
      cell = row[beam_i]

      if cell == '^':
        left = clamp(beam_i - 1, 0, row_len - 1)
        right = clamp(beam_i + 1, 0, row_len - 1)

        new_positions[left] = new_positions.get(left, 0) + count
        new_positions[right] = new_positions.get(right, 0) + count
      else:
        new_positions[beam_i] = new_positions.get(beam_i, 0) + count

    beam_positions = new_positions

  return sum(beam_positions.values())

print(f'Part 2 solution: {get_timelines()}')
