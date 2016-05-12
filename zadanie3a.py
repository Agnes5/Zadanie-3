import sys

if len(sys.argv) != 8: sys.exit("Blad: za malo argumentow")

a = int(sys.argv[1])
b = int(sys.argv[2])
c = int(sys.argv[3])
d = int(sys.argv[4])
e = int(sys.argv[5])
f = int(sys.argv[6])
g = int(sys.argv[7])


if a > 0 and (((b > a and c > b) or d <= c) and (e%a == 0 or (f*b > 20 or g < 5))):
	print 1
else:
	print 0
