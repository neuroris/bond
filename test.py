import math

r = 3.629
r /= 100
# fv = 1056900
m = 1000000
# c = 65270.7
c = 65200
n = 0
f = 1
T = 365
R = 1

price1 = m / ((1 + (r / f) * (R / T)) * ((1 + r / f) ** n))
price2 = c / ((1 + (r / f) * (R / T)) * ((1 + r / f) ** n))

price = price1 + price2
print(price / 100)

a = 10890
dcv = a / (1 + 0.0325 * 1)
print(dcv)

