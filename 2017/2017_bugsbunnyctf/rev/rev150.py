from z3 import *

s = Solver()

a = []
for i in range(20):
	a.append(Int('a['+str(i)+']'))
	s.add(a[i]>=0)
	s.add(a[i]<10)

s.add(a[15] + a[4] == 10)
s.add(a[1] * a[18] == 2)
s.add(a[15] / a[9] == 1)
s.add(a[5] - a[17] == -1)
s.add(a[15] - a[1] == 5)
s.add(a[1] * a[10] == 18)
s.add(a[8] + a[13] == 14)
s.add(a[18] * a[8] == 5)
s.add(a[4] * a[11] == 0)
s.add(a[8] + a[9] == 12)
s.add(a[12] - a[19] == 1)
s.add(a[9] % a[17] == 7)
s.add(a[14] * a[16] == 40)
s.add(a[7] - a[4] == 1)
s.add(a[6] + a[0] == 6)
s.add(a[2] - a[16] == 0)
s.add(a[4] - a[6] == 1)
s.add(a[0] % a[5] == 4)
s.add(a[5] * a[11] == 0)
s.add(a[10] % a[15] == 2)
s.add(a[11] / a[3] == 0)
s.add(a[14] - a[13] == -4)
s.add(a[18] + a[19] == 3)
s.add(a[3] + a[17] == 9)

print s.check()

flag = []
for i in range(20):
	flag.append('')

m = s.model()
for d in m.decls():
	flag[int(d.name()[2:-1])] = str(m[d])
print "".join(flag)
