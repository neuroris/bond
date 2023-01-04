import math

discount_rate = 5.481
t = 4
d = 302
f = 4
future_value = 1051000
r = discount_rate / 100

dcv1 = future_value / ((1 + r) ** (d / 365))
dcv2 = future_value / ((1 + r / f) ** (d / 365 * f))

print(dcv1)
print(dcv2)