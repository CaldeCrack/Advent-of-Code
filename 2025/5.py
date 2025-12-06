# --- Day 5: Cafeteria ---
# https://adventofcode.com/2025/day/5


def merge_overlap(arr: list[list[int]]) -> list[list[int]]:
    arr.sort()
    res: list[list[int]] = []
    res.append(arr[0])

    for i in range(1, len(arr)):
        last = res[-1]
        curr = arr[i]
        if curr[0] <= last[1]:
            last[1] = max(last[1], curr[1])
        else:
            res.append(curr)

    return res

ranges: list[list[int]] = []
while fresh_range := input():
  range_list = fresh_range.split('-')
  ranges.append([int(range_list[0]), int(range_list[1])])
merged_ranges = merge_overlap(ranges)

fresh_total = 0
while food_id := input():
  if any(r[0] <= int(food_id) <= r[1] for r in merged_ranges):
    fresh_total += 1

print(f'Part 1 solution: {fresh_total}')

total = 0
for r in merged_ranges:
  total += r[1] - r[0] + 1

print(f'Part 2 solution: {total}')
