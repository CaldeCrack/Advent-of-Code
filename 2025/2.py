# --- Day 2: Gift Shop ---
# https://adventofcode.com/2025/day/2


def invalid_id(id: str) -> bool:
  if len(id) % 2:
    return False

  half = len(id) // 2
  return id[:half] == id[half:]

def get_factors(number: int) -> list[int]:
  return [i for i in range(1, number) if number % i == 0]

def split_string_into_chunks(text: str, chunk_size: int):
  return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

def invalid_id2(id: str) -> bool:
  factors = get_factors(len(id))

  for factor in factors:
    if len(set(split_string_into_chunks(id, factor))) == 1:
      return True

  return False

def sum_of_invalid_ids(id_range: str, invalid_func) -> int:
  sum = 0
  lower, upper = id_range.split("-")
  for id in range(int(lower), int(upper) + 1):
    if invalid_func(str(id)):
      sum += id
  return sum

id_ranges = input().split(",")
total1 = 0
total2 = 0
for id_range in id_ranges:
  total1 += sum_of_invalid_ids(id_range, invalid_id)
  total2 += sum_of_invalid_ids(id_range, invalid_id2)

print(f'Part 1 solution: {total1}')
print(f'Part 2 solution: {total2}')
