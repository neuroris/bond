import math

r = 0.05698
m = 1000000
c = 8000
d = 32
t = 92
f = 4

price1 = c / (1 + (r / f) * (d / 92))
price2 = m / (1 + (r / f) * (d / 92))
price = price1 + price2

print(price1)
print(price2)
print(price)