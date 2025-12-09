# --- Day 9: Movie Theater ---
# https://adventofcode.com/2025/day/9
import sys
from collections import deque


red_tiles = []
while line := input():
  x, y = map(int, line.split(','))
  red_tiles.append((x, y))
n = len(red_tiles)
max_x = max(x for x, _ in red_tiles)
max_y = max(y for _, y in red_tiles)

largest1 = 0
for i in range(n):
  for j in range(i, n):
    w = abs(red_tiles[i][0] - red_tiles[j][0]) + 1
    h = abs(red_tiles[i][1] - red_tiles[j][1]) + 1
    largest1 = max(largest1, w * h)

print(f'Part 1 solution: {largest1}')

xs_set = set()
ys_set = set()

xs_all = [x for x, _ in red_tiles]
ys_all = [y for _, y in red_tiles]
min_x, max_x = min(xs_all), max(xs_all)
min_y, max_y = min(ys_all), max(ys_all)

xs_set.add(min_x - 1); xs_set.add(max_x + 1)
ys_set.add(min_y - 1); ys_set.add(max_y + 1)

for i, (x, y) in enumerate(red_tiles):
  prev_x, prev_y = red_tiles[i - 1]
  xs_set.add(x); xs_set.add(x + 1)
  ys_set.add(y); ys_set.add(y + 1)

  if x == prev_x:
    a = min(y, prev_y)
    b = max(y, prev_y)
    ys_set.add(a); ys_set.add(b + 1)
    xs_set.add(x); xs_set.add(x + 1)
  else:
    a = min(x, prev_x)
    b = max(x, prev_x)
    xs_set.add(a); xs_set.add(b + 1)
    ys_set.add(y); ys_set.add(y + 1)

xs_sorted = sorted(xs_set)
ys_sorted = sorted(ys_set)

W = len(xs_sorted) - 1
H = len(ys_sorted) - 1

xs_index = {v: i for i, v in enumerate(xs_sorted)}
ys_index = {v: i for i, v in enumerate(ys_sorted)}

x_width = [xs_sorted[i+1] - xs_sorted[i] for i in range(W)]
y_height = [ys_sorted[i+1] - ys_sorted[i] for i in range(H)]

x_acc = [0] * (W + 1)
for i in range(W):
  x_acc[i + 1] = x_acc[i] + x_width[i]
y_acc = [0] * (H + 1)
for i in range(H):
  y_acc[i + 1] = y_acc[i] + y_height[i]

graph = [bytearray(W) for _ in range(H)]
for i, (x, y) in enumerate(red_tiles):
  prev_x, prev_y = red_tiles[i - 1]
  if x == prev_x:
    cx = xs_index[x]
    cy0 = ys_index[min(y, prev_y)]
    cy1 = ys_index[max(y, prev_y)]
    for cy in range(cy0, cy1 + 1):
      graph[cy][cx] = 1
  else:
    cy = ys_index[y]
    cx0 = xs_index[min(x, prev_x)]
    cx1 = xs_index[max(x, prev_x)]
    for cx in range(cx0, cx1 + 1):
      graph[cy][cx] = 1

outside = [bytearray(W) for _ in range(H)]
q = deque()
for cx in range(W):
  if graph[0][cx] == 0 and outside[0][cx] == 0:
    outside[0][cx] = 1
    q.append((0, cx))
  if graph[H - 1][cx] == 0 and outside[H - 1][cx] == 0:
    outside[H - 1][cx] = 1
    q.append((H - 1, cx))

for cy in range(H):
    if graph[cy][0] == 0 and outside[cy][0] == 0:
        outside[cy][0] = 1
        q.append((cy, 0))
    if graph[cy][W - 1] == 0 and outside[cy][W - 1] == 0:
        outside[cy][W - 1] = 1
        q.append((cy, W - 1))

dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
while q:
  cy, cx = q.popleft()
  for dy, dx in dirs:
    ny, nx = cy + dy, cx + dx
    if 0 <= ny < H and 0 <= nx < W:
      if graph[ny][nx] == 0 and outside[ny][nx] == 0:
        outside[ny][nx] = 1
        q.append((ny, nx))

for cy in range(H):
  row_g = graph[cy]
  row_out = outside[cy]
  for cx in range(W):
    if row_g[cx] == 0 and row_out[cx] == 0:
      row_g[cx] = 1

ps = [[0] * (W + 1) for _ in range(H + 1)]
for cy in range(H):
  row = graph[cy]
  rsum = 0
  for cx in range(W):
    rsum += row[cx]
    ps[cy + 1][cx + 1] = ps[cy][cx + 1] + rsum

def rect_sum(ps, y1, x1, y2, x2):
  return ps[y2+1][x2+1] - ps[y1][x2+1] - ps[y2+1][x1] + ps[y1][x1]

def rectangle_edges_are_inside_ps(ps, cx1, cy1, cx2, cy2):
  left = min(cx1, cx2)
  right = max(cx1, cx2)
  top = min(cy1, cy2)
  bottom = max(cy1, cy2)

  width_intervals = right - left + 1
  height_intervals = bottom - top + 1

  if rect_sum(ps, top, left, top, right) != width_intervals:
    return False
  if rect_sum(ps, bottom, left, bottom, right) != width_intervals:
    return False
  if rect_sum(ps, top, left, bottom, left) != height_intervals:
    return False
  if rect_sum(ps, top, right, bottom, right) != height_intervals:
    return False
  return True

red_compressed = [(xs_index[x], ys_index[y]) for (x, y) in red_tiles]
largest2 = 0
for i in range(n):
  cx1, cy1 = red_compressed[i]
  for j in range(i+1, n):
    cx2, cy2 = red_compressed[j]

    left = min(cx1, cx2)
    right = max(cx1, cx2)
    top = min(cy1, cy2)
    bottom = max(cy1, cy2)

    true_width = x_acc[right+1] - x_acc[left]
    true_height = y_acc[bottom+1] - y_acc[top]
    area = true_width * true_height

    if area <= largest2:
      continue
    if rectangle_edges_are_inside_ps(ps, cx1, cy1, cx2, cy2):
      largest2 = area

print(f'Part 2 solution: {largest2}')

