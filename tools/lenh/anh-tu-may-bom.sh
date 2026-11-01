cd /home/user/qd
P=video/tho/anh/TuMayBom/prep
b(){ k=$1; shift; a=(); for n in "$@"; do a+=($P/$n.jpg); done; python3 tools/anh_video.py "${a[@]}" -o video/tho/anh/$k.mp4 --giay 5.5 > /tmp/tukd/$k.log 2>&1 && echo OK $k || echo FAIL $k; }
b anh-tu-mb-tinh-chi-ba-tri-so 28 55 50 57 39
b anh-tu-mb-tinh-chi-20uf 56 26 60 31 27
b anh-tu-mb-tinh-chi-25uf 61 51 38 37 47
b anh-tu-mb-tinh-chi-30uf 64 58 65 41 42
b anh-tu-mb-tinh-chi-kich-thuoc 62 44 52 54 53
b anh-tu-mb-tinh-chi-hang-san 29 34 46 40 63
b anh-tu-mb-tinh-chi-day-cos 33 36 45 59 30
b anh-tu-mb-tinh-chi-du-loai 25 32 35 48 49
