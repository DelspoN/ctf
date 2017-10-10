# [2017_Kaspersky] \[Reversing] Backdoor Pi

## Problem

```
We are doing an project for a school competition in which we need to use a Raspberry Pi to make an IOT prototype. We received SD cards from the professor, and because we lost ours we asked another group to give us a copy of their card, I know it’s been modified because the original hash doesn’t match. Could you please investigate and tell me if everything is ok? Here is some parts of the file system:

FLAG FORMAT: KLCTF{flag}

download this file: https://s3.eu-central-1.amazonaws.com/klctf/fs.zip
```

라즈베리파이 파일시스템 내의 백도어를 분석하는 문제입니다.

## Solution

```
total 84
drwxr-xr-x   2 root root 4096 Oct  5 17:11 bin
drwxr-xr-x   2 root root 4096 Dec 21  2013 boot
drwxr-xr-x   3 root root 4096 Oct  5 18:07 dev
drwxr-xr-x 102 root root 4096 Oct  5 18:07 etc
drwxr-xr-x   3 root root 4096 Oct  5 18:07 home
drwxr-xr-x   3 root root 4096 Oct  5 18:07 lib
drwx------   2 root root 4096 Dec 21  2013 lost+found
drwxrwxr-x  13 root root 4096 Oct  5 18:10 __MACOSX
drwxr-xr-x   4 root root 4096 Oct  5 18:07 media
drwxr-xr-x   2 root root 4096 Oct 18  2013 mnt
drwxr-xr-x   3 root root 4096 Oct  5 18:07 opt
drwxr-xr-x   2 root root 4096 Oct 18  2013 proc
drwx------   4 root root 4096 Oct  5 18:07 root
drwxr-xr-x   8 root root 4096 Oct  5 18:07 run
drwxr-xr-x   2 root root 4096 Jan  1  1970 sbin
drwxr-xr-x   2 root root 4096 Jun 20  2012 selinux
drwxr-xr-x   2 root root 4096 Dec 21  2013 srv
drwxr-xr-x   2 root root 4096 Oct 13  2013 sys
drwxrwxrwx   4 root root 4096 Oct  5 18:07 tmp
drwxr-xr-x  10 root root 4096 Oct  5 18:05 usr
drwxr-xr-x  11 root root 4096 Oct  5 18:07 var
```

라즈베리파이 파일시스템입니다. 여기서 백도어를 찾아야하는데 백도어라면 `crontab`을 사용하지 않았을까하는 삘이 왔습니다.

```
# grep -r crontab ./
Binary file ./usr/bin/crontab matches
./usr/share/perl5/HTML/Tree/Scanning.pod:consider a program that you could use (suppose it's crontabbed) to
./usr/sbin/deluser:    if (system("crontab -l $user >/dev/null 2>&1") == 0) {
./usr/sbin/deluser:      # crontab -l returns 1 if there is no crontab
./usr/sbin/deluser:      my $crontab = &which('crontab');
./usr/sbin/deluser:      &systemcall($crontab, "-r", $user);
./usr/sbin/deluser:      s_print (gtx("Removing crontab ...\n"));
Binary file ./usr/sbin/cron matches
./etc/default/cron:# only be changed via PAM or from within the crontab; see crontab(5).
./etc/group:crontab:x:102:
./etc/mime.types:text/x-crontab
./etc/crontab:# /etc/crontab: system-wide crontab
./etc/crontab:# Unlike any other crontab you don't have to run the `crontab'
./etc/crontab:# that none of the other crontabs do.
./etc/gshadow:crontab:!::
./etc/group-:crontab:x:102:
./etc/gshadow-:crontab:!::
./root/.viminfo:'0  4  0  /var/spool/cron/crontabs/pi
./root/.viminfo:'1  15  0  /etc/crontab
./root/.viminfo:-'  4  0  /var/spool/cron/crontabs/pi
./root/.viminfo:-'  1  0  /var/spool/cron/crontabs/pi
./root/.viminfo:-'  15  0  /etc/crontab
./root/.viminfo:-'  1  0  /etc/crontab
./root/.viminfo:-'  15  0  /etc/crontab
./root/.viminfo:-'  1  0  /etc/crontab
./root/.viminfo:> /var/spool/cron/crontabs/pi
./root/.viminfo:> /etc/crontab
Binary file ./home/pi/.bash_history matches
./var/lib/dpkg/available-old: specified in a crontab. By default, users may also create crontabs of
./var/lib/dpkg/status: /etc/crontab 8f111d100ea459f68d333d63a8ef2205
./var/lib/dpkg/status: specified in a crontab. By default, users may also create crontabs of
./var/lib/dpkg/available: specified in a crontab. By default, users may also create crontabs of
./var/lib/dpkg/info/vim-runtime.md5sums:2b0da23191f9b149762433bb90133b79  usr/share/vim/vim73/syntax/crontab.vim
./var/lib/dpkg/info/vim-runtime.list:/usr/share/vim/vim73/syntax/crontab.vim
./var/lib/dpkg/info/bash-completion.list:/usr/share/bash-completion/completions/crontab
./var/lib/dpkg/info/cron.md5sums:98693a03c8852af0646f50bd667f364f  usr/bin/crontab
./var/lib/dpkg/info/cron.md5sums:4692e137b0c9475417d10397ccb742a7  usr/share/doc/cron/examples/crontab2english.pl
./var/lib/dpkg/info/cron.md5sums:eacc514acff30adb73adfb79d515f453  usr/share/man/man1/crontab.1.gz
./var/lib/dpkg/info/cron.md5sums:24f8f49753d4f38abdcfef50edf1f6b5  usr/share/man/man5/crontab.5.gz
./var/lib/dpkg/info/cron.conffiles:/etc/crontab
./var/lib/dpkg/info/bash-completion.md5sums:678edd99ba10bfbd8771d92c5251c78a  usr/share/bash-completion/completions/crontab
./var/lib/dpkg/info/cron.postinst:# Add group for crontabs
./var/lib/dpkg/info/cron.postinst:getent group crontab > /dev/null 2>&1 || addgroup --system crontab
./var/lib/dpkg/info/cron.postinst:# Fixup crontab binary for new group 'crontab'.
./var/lib/dpkg/info/cron.postinst:if ! dpkg-statoverride --list /usr/bin/crontab > /dev/null ; then
./var/lib/dpkg/info/cron.postinst:    dpkg-statoverride --update --add root crontab 2755 /usr/bin/crontab
./var/lib/dpkg/info/cron.postinst:# Fixup crontab , directory and files for new group 'crontab'.
./var/lib/dpkg/info/cron.postinst:if [ -d $crondir/crontabs ] ; then
./var/lib/dpkg/info/cron.postinst:    chown root:crontab $crondir/crontabs
./var/lib/dpkg/info/cron.postinst:    chmod 1730 $crondir/crontabs
./var/lib/dpkg/info/cron.postinst:    cd $crondir/crontabs
./var/lib/dpkg/info/cron.postinst:    ls -1 | xargs -r -n 1 --replace=xxx  chown 'xxx:crontab' 'xxx'
./var/lib/dpkg/info/cron.list:/usr/share/man/man1/crontab.1.gz
./var/lib/dpkg/info/cron.list:/usr/share/man/man5/crontab.5.gz
./var/lib/dpkg/info/cron.list:/usr/share/doc/cron/examples/crontab2english.pl
./var/lib/dpkg/info/cron.list:/usr/bin/crontab
./var/lib/dpkg/info/cron.list:/var/spool/cron/crontabs
./var/lib/dpkg/info/cron.list:/etc/crontab
./var/lib/dpkg/statoverride:root crontab 2755 /usr/bin/crontab
./var/lib/dpkg/status-old: /etc/crontab 8f111d100ea459f68d333d63a8ef2205
./var/lib/dpkg/status-old: specified in a crontab. By default, users may also create crontabs of
./var/spool/cron/crontabs/b4ckd00r_us3r:# (/tmp/crontab.80NKS4/crontab installed on Wed Oct  4 19:28:12 2017)
./var/spool/cron/crontabs/b4ckd00r_us3r:# (Cron version -- $Id: crontab.c,v 2.13 1994/01/17 03:20:37 vixie Exp $)
./var/spool/cron/crontabs/pi:# (/tmp/crontab.80NKS4/crontab installed on Wed Oct  4 19:28:12 2017)
./var/spool/cron/crontabs/pi:# (Cron version -- $Id: crontab.c,v 2.13 1994/01/17 03:20:37 vixie Exp $)
```

`./var/spool/cron/crontabs/b4ckd00r_us3r`에 있는 백도어의 crontab을 발견했습니다.

```
# DO NOT EDIT THIS FILE - edit the master and reinstall.
# (/tmp/crontab.80NKS4/crontab installed on Wed Oct  4 19:28:12 2017)
# (Cron version -- $Id: crontab.c,v 2.13 1994/01/17 03:20:37 vixie Exp $)
# m h  dom mon dow   command
@reboot python /bin/back
```

backdoor는 `/bin/back`에 있었습니다.

```
# file back
back: python 2.7 byte-compiled
```

python으로 컴파일된 바이너리입니다.

```python
# uncompyle6 back.pyc
# uncompyle6 version 2.12.0
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: back.py
# Compiled at: 2017-10-05 17:09:10
import sys
import os
import time
from flask import Flask
from flask import request
from flask import abort
import hashlib

def check_creds(user, pincode):
    if len(pincode) <= 8 and pincode.isdigit():
        val = '{}:{}'.format(user, pincode)
        key = hashlib.sha256(val).hexdigest()
        if key == '34c05015de48ef10309963543b4a347b5d3d20bbe2ed462cf226b1cc8fff222e':
            return 'Congr4ts, you found the b@ckd00r. The fl4g is simply : {}:{}'.format(user, pincode)
    return abort(404)


app = Flask(__name__)

@app.route('/')
def hello():
    return '<h1>HOME</h1>'


@app.route('/backdoor')
def backdoor():
    user = request.args.get('user')
    pincode = request.args.get('pincode')
    return check_creds(user, pincode)


if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=3333)
# okay decompiling back.pyc
```

pyc 디컴파일러를 사용하여 디컴파일 하면 위와 같은 코드가 나옵니다.



이제 flag를 브루트포싱하여 맞춰줘야 합니다.

```
ls
sudo useradd b4ckd00r_us3r
cat /etc/passwd
```

`.bash_history`에서 `b4ckd00r_us3r`를 확인할 수 있었고, pincode는 아래의 코드를 이용하여 브루트포싱해줍니다.

```python
import hashlib

user = "b4ckd00r_us3r"
pincode_base = 12171337

while True:
	pincode = str(pincode_base)
	print pincode
	if len(pincode) <= 8:
		val = '{}:{}'.format(user, pincode)
		key = hashlib.sha256(val).hexdigest()
		if key == '34c05015de48ef10309963543b4a347b5d3d20bbe2ed462cf226b1cc8fff222e':
			print val
			break
        	pincode_base += 1
	else:
		break
print "completed"
```



##Result

````
# python ex.py 
12171337
b4ckd00r_us3r:12171337
completed
````

flag = `KLCTF{b4ckd00r_us3r:12171337}`