import math

r = 0.01
c = 10284.5

a = c / (1 + r / 2 * 62 / 184)
b = c / (1 + r * 62 / 365)
print(a)
print(b)

rr = 12.051
rr /= 100
n = 187.5 / 365
d = 10284.5 / (1 + rr) ** n
print(d)

rrr = 5.689
rrr /= 100
nn = 182.5 / 365
e = 10284.5 / (1 + rrr / 2)
print(e)