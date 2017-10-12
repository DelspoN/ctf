import requests
import base64

url = "http://95.85.51.183/"

def get_mal_plain(mal_cipher):
	cookie = dict(user_info="\""+base64.b64encode(mal_cipher)+"\"")

        r = requests.get(url, cookies = cookie)
        response = r.text

        if "UnicodeDecodeError: 'ascii' codec" in response:
		tmp = response.split("decode byte 0x")[1].split(" ")
		return int(tmp[0],16)
	return -1

cipher = "S6rw59a355xp9NJXwMxl0r/ZywhlX6d619xjQ71Q4KQGrDxEQUM8cE+uW93Pb82YIMRLvCdwwkQNY3QyhzWOdg=="
cipher = base64.decodestring(cipher)
block_size = 16
plain = ""

# mal_cipher ^ mal_plain = intermediary
# intermediary ^ iv = plain

for i in range(4):
	for idx in range(block_size):
		for bf in range(0x100):
			mal_cipher = list(cipher[i*block_size:])
			mal_cipher[idx] = chr(bf)
			mal_cipher = ''.join(mal_cipher)

			mal_plain = get_mal_plain(mal_cipher)
			if mal_plain != -1:
				plain += chr(ord(cipher[i*block_size+idx]) ^ ord(mal_cipher[idx]) ^ mal_plain)
				print "plain = {}".format(plain)
				break
"""
plain = {
plain = {"
plain = {"n
plain = {"na
plain = {"nam
plain = {"name
plain = {"name"
plain = {"name":
plain = {"name": 
plain = {"name": "
plain = {"name": "2
plain = {"name": "2"
plain = {"name": "2",
plain = {"name": "2", 
plain = {"name": "2", "
plain = {"name": "2", "s
plain = {"name": "2", "sh
plain = {"name": "2", "sho
plain = {"name": "2", "show
plain = {"name": "2", "show_
plain = {"name": "2", "show_f
plain = {"name": "2", "show_fl
plain = {"name": "2", "show_fla
plain = {"name": "2", "show_flag
plain = {"name": "2", "show_flag"
plain = {"name": "2", "show_flag":
plain = {"name": "2", "show_flag": 
plain = {"name": "2", "show_flag": f
plain = {"name": "2", "show_flag": fa
plain = {"name": "2", "show_flag": fal
plain = {"name": "2", "show_flag": fals
plain = {"name": "2", "show_flag": false
plain = {"name": "2", "show_flag": false}
"""	
