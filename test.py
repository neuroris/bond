import math

r = 10.000
r /= 100
# fv = 1056900
fv = 1028450
# fv = 1056000
f = 2
T = 181
R = 1

# price = fv / ((1 + (r / f) * (R / T)) * (1 + r / f))
# price = fv / ((1 + (r / f) * (R / T)) * 1.05)
price = fv / ((1 + (r / f) * (R / T)) * (1 + r / f))
price2 = 28450 / (1 + (r / f) * (R / T))
price3 = price + price2

print(price / 100)
print(price2 / 100)
print(price3 / 100)