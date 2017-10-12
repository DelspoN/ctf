import requests
import base64

url = "http://95.85.51.183/"

def get_mal_plain(mal_cipher, position):
	cookie = dict(user_info="\""+base64.b64encode(mal_cipher)+"\"")

        r = requests.get(url, cookies = cookie)
        response = r.text

	if "UnicodeDecodeError: 'ascii' codec" in response:
		tmp = response.split("decode byte 0x")[1].split(" ")
		if int(tmp[3].replace(':','')) == position:
			return int(tmp[0], 16)
	return -1

cipher = "S6rw59a355xp9NJXwMxl0r/ZywhlX6d619xjQ71Q4KQGrDxEQUM8cE+uW93Pb82YIMRLvCdwwkQNY3QyhzWOdg=="
cipher = base64.decodestring(cipher)
plain		= '{"name": "2", "show_flag": false}'
mal_plain_text  = '{"name": "2", "show_flag": true }'
mal_cipher_text = ''
block_size = 16

# plain ^ iv = intermediary
# intermediary ^ mal_plain = mal_cipher

mal_cipher = list("\x00"*16 + cipher[16:])
for i in range(16, 32):
	mal_cipher[i] = chr(ord(plain[i]) ^ ord(cipher[i]) ^ ord(mal_plain_text[i]))
mal_cipher = ''.join(mal_cipher)

for idx in range(block_size):
	for bf in range(0x100):
		mal_plain = get_mal_plain(mal_cipher,idx)
		if mal_plain != -1:
			mal_cipher = list(mal_cipher)
			mal_cipher[idx] = chr(ord(mal_cipher[idx]) ^ mal_plain ^ ord(mal_plain_text[idx]))
			mal_cipher = ''.join(mal_cipher)
			print "[{}] mal_cipher = {}".format(idx, mal_cipher.encode("hex"))
			print base64.b64encode(mal_cipher)
			break
		mal_cipher = list(mal_cipher)
                mal_cipher[idx] = chr(bf)
                mal_cipher = ''.join(mal_cipher)

"""
[0] mal_cipher = dd000000000000000000000000000000bfd9cb08655fa77ad7dc6351ae49f6e106ac3c4441433c704fae5bddcf6fcd9820c44bbc2770c2440d63743287358e76
3QAAAAAAAAAAAAAAAAAAAL/ZywhlX6d619xjUa5J9uEGrDxEQUM8cE+uW93Pb82YIMRLvCdwwkQNY3QyhzWOdg==
[1] mal_cipher = dd7e0000000000000000000000000000bfd9cb08655fa77ad7dc6351ae49f6e106ac3c4441433c704fae5bddcf6fcd9820c44bbc2770c2440d63743287358e76
3X4AAAAAAAAAAAAAAAAAAL/ZywhlX6d619xjUa5J9uEGrDxEQUM8cE+uW93Pb82YIMRLvCdwwkQNY3QyhzWOdg==
[2] mal_cipher = dd7e7700000000000000000000000000bfd9cb08655fa77ad7dc6351ae49f6e106ac3c4441433c704fae5bddcf6fcd9820c44bbc2770c2440d63743287358e76
3X53AAAAAAAAAAAAAAAAAL/ZywhlX6d619xjUa5J9uEGrDxEQUM8cE+uW93Pb82YIMRLvCdwwkQNY3QyhzWOdg==
[3] mal_cipher = dd7e771c000000000000000000000000bfd9cb08655fa77ad7dc6351ae49f6e106ac3c4441433c704fae5bddcf6fcd9820c44bbc2770c2440d63743287358e76
3X53HAAAAAAAAAAAAAAAAL/ZywhlX6d619xjUa5J9uEGrDxEQUM8cE+uW93Pb82YIMRLvCdwwkQNY3QyhzWOdg==
[4] mal_cipher = dd7e771ca20000000000000000000000bfd9cb08655fa77ad7dc6351ae49f6e106ac3c4441433c704fae5bddcf6fcd9820c44bbc2770c2440d63743287358e76
3X53HKIAAAAAAAAAAAAAAL/ZywhlX6d619xjUa5J9uEGrDxEQUM8cE+uW93Pb82YIMRLvCdwwkQNY3QyhzWOdg==
[5] mal_cipher = dd7e771ca22300000000000000000000bfd9cb08655fa77ad7dc6351ae49f6e106ac3c4441433c704fae5bddcf6fcd9820c44bbc2770c2440d63743287358e76
3X53HKIjAAAAAAAAAAAAAL/ZywhlX6d619xjUa5J9uEGrDxEQUM8cE+uW93Pb82YIMRLvCdwwkQNY3QyhzWOdg==
[6] mal_cipher = dd7e771ca223fe000000000000000000bfd9cb08655fa77ad7dc6351ae49f6e106ac3c4441433c704fae5bddcf6fcd9820c44bbc2770c2440d63743287358e76
3X53HKIj/gAAAAAAAAAAAL/ZywhlX6d619xjUa5J9uEGrDxEQUM8cE+uW93Pb82YIMRLvCdwwkQNY3QyhzWOdg==
[7] mal_cipher = dd7e771ca223fefd0000000000000000bfd9cb08655fa77ad7dc6351ae49f6e106ac3c4441433c704fae5bddcf6fcd9820c44bbc2770c2440d63743287358e76
3X53HKIj/v0AAAAAAAAAAL/ZywhlX6d619xjUa5J9uEGrDxEQUM8cE+uW93Pb82YIMRLvCdwwkQNY3QyhzWOdg==
[8] mal_cipher = dd7e771ca223fefd0600000000000000bfd9cb08655fa77ad7dc6351ae49f6e106ac3c4441433c704fae5bddcf6fcd9820c44bbc2770c2440d63743287358e76
3X53HKIj/v0GAAAAAAAAAL/ZywhlX6d619xjUa5J9uEGrDxEQUM8cE+uW93Pb82YIMRLvCdwwkQNY3QyhzWOdg==
[9] mal_cipher = dd7e771ca223fefd06bd000000000000bfd9cb08655fa77ad7dc6351ae49f6e106ac3c4441433c704fae5bddcf6fcd9820c44bbc2770c2440d63743287358e76
3X53HKIj/v0GvQAAAAAAAL/ZywhlX6d619xjUa5J9uEGrDxEQUM8cE+uW93Pb82YIMRLvCdwwkQNY3QyhzWOdg==
[10] mal_cipher = dd7e771ca223fefd06bddb0000000000bfd9cb08655fa77ad7dc6351ae49f6e106ac3c4441433c704fae5bddcf6fcd9820c44bbc2770c2440d63743287358e76
3X53HKIj/v0GvdsAAAAAAL/ZywhlX6d619xjUa5J9uEGrDxEQUM8cE+uW93Pb82YIMRLvCdwwkQNY3QyhzWOdg==
[11] mal_cipher = dd7e771ca223fefd06bddb3a00000000bfd9cb08655fa77ad7dc6351ae49f6e106ac3c4441433c704fae5bddcf6fcd9820c44bbc2770c2440d63743287358e76
3X53HKIj/v0Gvds6AAAAAL/ZywhlX6d619xjUa5J9uEGrDxEQUM8cE+uW93Pb82YIMRLvCdwwkQNY3QyhzWOdg==
[12] mal_cipher = dd7e771ca223fefd06bddb3a59000000bfd9cb08655fa77ad7dc6351ae49f6e106ac3c4441433c704fae5bddcf6fcd9820c44bbc2770c2440d63743287358e76
3X53HKIj/v0Gvds6WQAAAL/ZywhlX6d619xjUa5J9uEGrDxEQUM8cE+uW93Pb82YIMRLvCdwwkQNY3QyhzWOdg==
[13] mal_cipher = dd7e771ca223fefd06bddb3a59900000bfd9cb08655fa77ad7dc6351ae49f6e106ac3c4441433c704fae5bddcf6fcd9820c44bbc2770c2440d63743287358e76
3X53HKIj/v0Gvds6WZAAAL/ZywhlX6d619xjUa5J9uEGrDxEQUM8cE+uW93Pb82YIMRLvCdwwkQNY3QyhzWOdg==
[14] mal_cipher = dd7e771ca223fefd06bddb3a5990a400bfd9cb08655fa77ad7dc6351ae49f6e106ac3c4441433c704fae5bddcf6fcd9820c44bbc2770c2440d63743287358e76
3X53HKIj/v0Gvds6WZCkAL/ZywhlX6d619xjUa5J9uEGrDxEQUM8cE+uW93Pb82YIMRLvCdwwkQNY3QyhzWOdg==
[15] mal_cipher = dd7e771ca223fefd06bddb3a5990a41ebfd9cb08655fa77ad7dc6351ae49f6e106ac3c4441433c704fae5bddcf6fcd9820c44bbc2770c2440d63743287358e76
3X53HKIj/v0Gvds6WZCkHr/ZywhlX6d619xjUa5J9uEGrDxEQUM8cE+uW93Pb82YIMRLvCdwwkQNY3QyhzWOdg==

Hello 2
Flag: KLCTFFDA616A6DAF4E63A9F7B55B43124E548
"""
