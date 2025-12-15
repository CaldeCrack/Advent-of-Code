# --- Day 11: Reactor ---
# https://adventofcode.com/2025/day/11
from functools import cache


devices: dict[str, set[str]] = {}
while device := input():
  splitted = device.split(': ')
  key = splitted[0]
  value = set(splitted[1].split(' '))
  devices[key] = value

def find_paths(graph: dict[str, set[str]], start: str, end: str) -> list[list[str]]:
  def dfs(node: str, visited: set[str], path: list[str]) -> list[list[str]]:
    if node == end:
      return [path.copy()]

    paths = []
    visited.add(node)

    for nxt in graph.get(node, []):
      if nxt not in visited:
        path.append(nxt)
        paths.extend(dfs(nxt, visited, path))
        path.pop()

    visited.remove(node)
    return paths

  return dfs(start, set(), [start])

print(f'Part 1 solution: {len(find_paths(devices, 'you', 'out'))}')

def total_part2(graph: dict[str, set[str]]) -> int:
  @cache # online hint
  def dfs(device: str, fft: bool, dac: bool) -> int:
    if device == "out":
      return 1 if fft and dac else 0
    if (outputs := graph.get(device)) is None:
      return 0
    fft = fft or device == "fft"
    dac = dac or device == "dac"
    return sum(dfs(output, fft, dac) for output in outputs)

  return dfs('svr', False, False)

print(f'Part 2 solution: {total_part2(devices)}')
