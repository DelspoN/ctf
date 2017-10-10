from pwn import *
from z3 import *

def dec2ter(dec):
	s = Solver()
	max = get_len(dec)
	x = list()
	equation=0
	for i in range(max+1):
		x.append(Int('x['+str(i)+']'))
		s.add(x[i]<=1, x[i]>=-1)
		equation += x[i]*pow(3,max-i)
	s.add(x[0] != 0)
	s.add(equation == dec)

	if s.check() != sat:
		return "not sat"

	result = ""
	m = s.model()

	for i in range(len(m.decls())):
		result += str(m[x[i]])
	result = result.replace("-1","T")
	return result

def get_len(dec):
	if dec < 0:
		dec = dec * -1
	for i in range(10):
		if dec % pow(3,i) == dec:
			max = i
			break
	return max

def ter2dec(ter):
	result = 0
	ter = list(ter)
	for i in range(len(ter)):
		if ter[i] == 'T':
			ter[i] = '-1'
		result += int(ter[i])*(pow(3,len(ter)-i-1))
	return result

p = remote("159.203.38.169", 5672)
print p.recvline()

while True:
	prob = p.recv().strip()
	print prob
	
	arg = prob.split(" + ")
	a = ter2dec(arg[0])
	b = ter2dec(arg[1])
	res = dec2ter(a+b)
	print res
	p.sendline(res)

p.interactive()
