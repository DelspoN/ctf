file ./morph
b *(0x555555554AE9)
b *(0x555555554b35)
r `python -c 'print "3"*23'`

set $argv1 = *(char **)($rax + 8)
set $cnt = 0
c
while($cnt < 23)
set $pos = *($rax + 9)
set $flag = *(*(byte **)$rax + 5)
set *($argv1+$pos) = $flag
printf "[%d] %c %s\n", $pos, $flag, $argv1
c
set $cnt = $cnt + 1
end
