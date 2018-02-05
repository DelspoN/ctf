def skewer(t):
    return ord(t)-53;
import sys,base64,os,re;password=base64.b64decode("pb24");r=[chr((x+5+y**2)%256) for y,x in enumerate([skewer(x)+7%256 for x in password])];
code='''
#code here
use MIME::Base64;
my $pwd=decode_base64("JASUS");
$pwd=substr($pwd,-3).substr($pwd,0,(length $pwd) -3);
#print $pwd;
use File::Temp qw(tempfile);
($fh, $filename) = tempfile( );
my $code="<".<<'Y';
?php $p='JERKY';echo $flag=$p[0]=='A'?$p[1]=='S'?$p[2]=='S'?$p[3]=='H'?$p[4]=='A'?$p[5]=='I'?$p[6]=='R'?strlen($p)==7?'YES, the flag is: ':0:0:0:0:0:0:0:'NO';
Y
$code =~ s/JERKY/$pwd/g; print $fh $code;print `php ${filename}`;
'''.replace('JASUS',base64.b64encode("".join(r)));


"""
f = open("sub3", 'w')
f.write(code)
f.close()
"""
f = open("sub3", 'r')
code = f.read()
f.close()

print os.popen("perl sub3").read()

"""
import tempfile;
f = tempfile.NamedTemporaryFile(delete=False);f.write(code);f.close();print os.popen("perl "+f.name).read();
"""
