# --- Day 8: Playground ---
# https://adventofcode.com/2025/day/8
import math
from itertools import combinations

type point = tuple[int, int, int]
type pair = tuple[point, point]
type edge = tuple[float, point, point]


junction_boxes: list[point] = []
while coords := input():
  coord_list = coords.split(',')
  junction_boxes.append((int(coord_list[0]), int(coord_list[1]), int(coord_list[2])))

def euclidean_distance(p1: point, p2: point) -> float:
  return math.sqrt(sum([(c1 - c2) ** 2 for c1, c2 in zip(p1, p2)]))

def k_closest_pairs(k: int) -> list[pair]:
  distances: list[tuple[float, pair]] = []
  for p1, p2 in combinations(junction_boxes, 2):
    dist = euclidean_distance(p1, p2)
    distances.append((dist, (p1, p2)))

  distances.sort()
  return [pair for _, pair in distances[:k]]

closest_pairs = k_closest_pairs(1000)
connections: list[set[point]] = []

for a, b in closest_pairs:
  matching = [s for s in connections if a in s or b in s]
  if not matching:
    new_set = {a, b}
    connections.append(new_set)
  else:
    merged = set().union(*matching, {a, b})
    for s in matching:
      connections.remove(s)
    connections.append(merged)

connections.sort(key=len, reverse=True)
total = 1
for circuit in connections[:3]:
  total *= len(circuit)

print(f'Part 1 solution: {total}')

class DSU:
  def __init__(self, nodes):
    self.parent = {n: n for n in nodes}
    self.rank = {n: 0 for n in nodes}

  def find(self, a):
    while self.parent[a] != a:
      self.parent[a] = self.parent[self.parent[a]]
      a = self.parent[a]
    return a

  def union(self, a, b):
    pa = self.find(a)
    pb = self.find(b)

    if pa == pb:
      return False

    if self.rank[pa] < self.rank[pb]:
      pa, pb = pb, pa
    self.parent[pb] = pa

    if self.rank[pa] == self.rank[pb]:
      self.rank[pa] += 1

    return True

# Minimum Spanning Tree
def mst_last_x_product(junction_boxes: list[point]) -> int:
  edges: list[edge] = []
  for p1, p2 in combinations(junction_boxes, 2):
    d = euclidean_distance(p1, p2)
    edges.append((d, p1, p2))

  edges.sort(key=lambda x: x[0])
  dsu = DSU(junction_boxes)
  edges_used = 0
  n = len(junction_boxes)

  last_p1 = last_p2 = (0, 0, 0)
  for _, p1, p2 in edges:
    if dsu.union(p1, p2):
      edges_used += 1
      last_p1, last_p2 = p1, p2

      if edges_used == n - 1:
        break

  return last_p1[0] * last_p2[0]

result = mst_last_x_product(junction_boxes)
print(f'Part 2 solution: {result}')
