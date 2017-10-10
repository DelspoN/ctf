# [2017_Can-CWIC] \[Prog] Tri it 0

## Key words

- Balanced ternary
- z3 solver

##Problem

```
Can you math some numbers?

nc 159.203.38.169 5672

Note: Give the results to the server, not in the input box bellow.
```

## Analysis

```
# nc 159.203.38.169 5672
Read https://en.wikipedia.org/wiki/Balanced_ternary
1T0 + TT11T
```

ternary는 3진법을 의미하고 balanced ternary는 -1을 이용하여 조금 더 효율적인 3진법인 것 같습니다.

주어진 문제를 파싱하여 balanced ternary 값을 10진수로 변환한 후 계산하여 다시 balanced ternary로 정답을 보내주면 됩니다.

## Code

```python
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
```

ternary to decimal을 구현하는데 수학적인 머리가 안돌아가서 z3 solver를 사용했습니다.