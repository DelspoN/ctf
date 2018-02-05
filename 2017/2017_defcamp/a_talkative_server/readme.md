# [2017_DefCamp] \[Web] A talkative server

```
Some servers have no sense of verbosity limit. They'll blurb out anything, including passwords, secrets, and flags... oops!

Flag format: DCTF{32_bytes_in_hex}
```

### Solution

주어진 링크에 접속해보면 약 11기가 만큼 응답을 해줍니다. 여기서 flag를 뽑아야 합니다.

```
$ http --stream https://a-talkative-server.dctf-quals-17.def.camp/image.php | strings
IHDR
sRGB
gAMA
pHYs
IDATx^
G>[2
y%[W
$x	^
i_wk
TpI]
* x=
_P{G
 x	^
,+0R
"5yzM
]jF6
`^rq
"3uz
W\&x
KIfw
kejHW,wc"
?\)x
J95F
.l*8
^&x	^
}Tj[
C%x]vj>r`
'.x}<
0xEf
M9`{
f'={
5M	^
].x]n
:FJ]
z8m<R
- x	^
#x-8
YSY"
w7"x
Vkd"
>5xu
>(x=
lR[l
vmkW{
Nbp-
)xew
:Y=}
3ZG#
zDSF
+xuL
la{Yc
6'-|
%x	^
%x	^
p6kO
TN:qw
%x	^
!x	^
%x	^
*x	^
%x	^
%x	^
%x	^
~.9i`~
YvFj
DnC<
^;bwZ
Wrow
l,|}M
_fG;
vcH5U+V;
ivl3
d}_Vf}
|/x	^
+xeW
{aEN
E[Vf
i_vk
?2c`
UUR!ZaS
X$ x-
X$ x-
X$ x-
X$ x-
X$ x-
X$ x-
X$ x-
X$ x-
X$ x-
X$ x-
X$ x-
X$ x-
X$ x-
X$ x-
X$ x-
X$ x-
X$ x-
X$ x-
X$ x-
X$ x-
X$ x-
X$ x-
X$ x-
e'kY%d
U~wl
j_6>
RS[a
^.0{
O]|Z
%6>;
^%	>
M],x-
-<'^
E3uq_
j#uqGP
$xM>
+ x]wn
RH=`
U|![
~S)Y
";hIG
{.NG2
\\# x
8&[I-"
jk`]k
Jq	^
#(x9
B^|I
0Ct,
U-xe
X$ x-
X$ x-
X$ x-
X$ x-
X$ x-
X$ x-
.&@`
HGGn#
hjpG
Hfw$x	^
kj;J
5iN5K
qLuT$
>k;J
&x	^
;:<k
Gf'r
*0Uc
&{}</
A"SS
l|un
<	^5
dZS[
JMA	K
XjKp
%0K@
z&@   x
^o3U
 P- xU
X  x-@
& xM
Z%@`
_( x}
!P) xUjj
_/ x}}	
|}7r
! x9
 @`#
X+ x5~
( x}
^=j>C
T.$@
$ x}
L ' x
SFbV*
^&xuL
 P$P
& x}
3RaSG3 x}Sm
. xM'
N`RB
W`RB
 0]@
"#@`
rm_&
v!xm
SQdT
^%e6{
^_RM
G#rT$x	^
++&x	^G
F:~~9{
kp}	.
Wp"j
p_{"
%x	^
YaSWN
N?rt
FwZW
iYVF
wD'^N
?5]80
!x	^
9i`N
M'^N
xmo5
6flc
R-l/~n
FwSG
^}Mm
+'^N
Ucv*
/nj7~
^5v$r'^
=q/<
%x	^
M	^}U7
Wp.j
IEND
DCTF{
1542
879e
00fd
fffg
8794
348a
i like trains
9ea1
ab24
e12a
bba1
sbax
4dea
314a
8787
542a
ea10
951d
b794
```

`Flag format: DCTF{32_bytes_in_hex}`라고 했으니 hex 값만 골라서 형식에 맞게 flag를 작성해줍니다.

`DCTF{1542879e00fd8794348a9ea1ab24e12abba14dea314a8787542aea10951db794}`