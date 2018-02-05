FLAG=-fPIC -pie -D_FORTIFY_SOURCE=2 -fstack-protector --param ssp-buffer-size=4 -Wl,-z,relro,-z,now -Os -std=c++11 -m32
all:
	$(CXX) -o calc_patched calc_patched.cpp $(FLAG)
	strip -s calc_patched
