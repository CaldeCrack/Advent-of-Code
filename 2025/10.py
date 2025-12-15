# --- Day 10: Factory ---
# https://adventofcode.com/2025/day/10
from itertools import combinations, chain
from functools import cache


def parse_input(text: str) -> tuple[list[int], list[list[int]], list[int]]:
  new_text = text.replace('] ', '-').replace(' {', '-').split('-')

  lights = [0 if char == '.' else 1 for char in new_text[0].replace('[', '')]

  buttons: list[list[int]] = []
  for button in new_text[1].replace('(', '').replace(')', '').split(' '):
    buttons.append([int(i) for i in button.split(',')])

  joltages = [int(i) for i in new_text[2].replace('}', '').split(',')]
  return lights, buttons, joltages

def get_output(buttons: tuple, length: int) -> list[int]:
  result = [0] * length
  for button in buttons:
    for indicator in button:
      result[indicator] = int(not result[indicator])
  return result

def all_subsets(iterable) -> chain[tuple[list[list[int]]]]:
  return chain(*map(lambda x: combinations(iterable, x), range(1, len(iterable) + 1)))

lights: list[list[int]] = []
buttons: list[list[list[int]]] = []
joltages: list[list[int]] = []
rows = 0
while row := input():
  l, b, j = parse_input(row)
  lights.append(l)
  buttons.append(b)
  joltages.append(j)
  rows += 1

total = 0
for row in range(rows):
  for comb in all_subsets(buttons[row]):
    if get_output(comb, len(lights[row])) == lights[row]:
      total += len(comb)
      break

print(f'Part 1 solution: {total}')

# credits to Y0UR-U5ERNAME in GitHub
# I didn't wanted to implement a solver xd

def solve(l, b):
  l = sum(j << c for c, j in enumerate(l))
  b = [sum((1 << j) for j in i) for i in b]

  @cache
  def rsolve(l, idx=0):
    if l == 0: return 0
    if idx == len(b): return len(b) + 1
    return min(rsolve(l, idx + 1), 1 + rsolve(l ^ b[idx], idx + 1))
  return rsolve(l)

def poss(s, n, B, x, idx=0):
  if s == 0: yield x; return
  Bidx0, Bidx1 = B[idx]
  g = (min(x[k] for k in B[j][1]) for j in range(idx, len(B)))
  upper = min(next(g), *(x[k] for k in Bidx1))
  if n == 1:
    if s <= upper: yield tuple(x[k] - s*Bidx0[k] for k in range(len(x)))
  else:
    lower = max(0, s - sum(g))
    for i in range(min(s, upper), lower-1, -1):
      for j in poss(s - i, n - 1, B, tuple(x[k] - i*Bidx0[k] for k in range(len(x))), idx + 1): yield j

def solve2(r, b):
  lenr = len(r)
  lenb = len(b)
  b.sort(key=len, reverse=True)
  ba = [tuple(int(j in i) for j in range(lenr)) for i in b]
  ids = [frozenset(j for j in range(lenb) if ba[j][i]) for i in range(lenr)]
  out = min((sum(r), *(r[c] + r[d] for c in range(lenr-1) for d in range(c + 1, lenr) if set(range(lenb)) <= (ids[c] | ids[d]))))

  def rsolve2(x, z, s):
    nonlocal out
    y, idsy = min(((i, s & ids[i]) for i in range(lenr) if x[i]), key=lambda w: (len(w[1]), -x[w[0]]))
    newz = z + x[y]
    news = s - ids[y]
    for a in poss(x[y], len(idsy), [(ba[j], b[j]) for j in idsy], x):
      ids2a = {frozenset(): 0}
      if any(ids2a.setdefault(news & ids[i], a[i]) != a[i] for i in range(lenr)): continue
      #if any(i < j and ids2a[i] > ids2a[j] for i, j in product(ids2a, 2)): continue
      if (Z:=newz + max(vals := ids2a.values())) >= out: continue
      if len(ids2a) <= 2 or not any(vals): out = Z; continue
      rsolve2(a, newz, news)
  rsolve2(r, 0, frozenset(range(lenb)))
  return out

count2 = 0
for i in range(rows):
  count2 += solve2(joltages[i], buttons[i])

print(f'Part 2 solution: {count2}')
