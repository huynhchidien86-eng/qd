#!/bin/bash
# Dựng 10 video 26–35 (đợt 01/11). Video thô tải theo video/danh-sach-tiep-thi.md.
cd "$(dirname "$0")/../.."
E="python3 tools/edit.py"; M=video/mau; N=video/assets/nhac; B=video/xong/ban-cuoi
T="--khung 9:16 --phu-de-cao 60 --chuan-am --studio --goc --nen-am-luong 0"
run(){ $E "$@" 2>&1 | grep -E "^Video |^Giọng đọc:|^Mở đầu|^Xong|rror|Traceback|SIGKILL"; }
v(){ src=$1; key=$2; canh=$3; sfx=$4; nhac=$5; vol=$6; out=$7
  run video/tho/$src $T --chu $M/$key.ass --giong $M/$key.loi.txt --sfx "$sfx" \
    --mo-dau $M/$key-mo-dau.ass --mo-dau-giong $M/$key-mo-dau.loi.txt --mo-dau-canh $canh \
    --nhac $N/$nhac --nhac-am-luong $vol -o "$B/$out"; }
v c03-ios-163015.mov kep-ac-quy-75a 1,12,22,33 "0.3:whoosh,7:pop,13:pop,19:pop,26:pop,32:pop" pop-rock-quang-cao.mp3 0.148 "26 Kep ac quy 75A - giong doc.mp4"
v c04-ios-163056.mov kep-ac-quy-50a 2,14,28,40 "0.3:whoosh,8:pop,15:pop,22:pop,30:pop,38:pop" running-night.mp3 0.097 "27 Kep ac quy 50A - giong doc.mp4"
v c05-ios-163138.mov kep-100a-thep 2,20,33,48 "0.3:whoosh,8:pop,16:pop,24:pop,32:pop,42:pop" promotion.mp3 0.098 "28 Kep 100A thep - giong doc.mp4"
v c06-ios-075442.mov hop-abs-170x70-khoan-san 3,15,27,38 "0.3:whoosh,6.5:pop,12:pop,19:pop,25:pop,31:pop,37:pop" moodmode.mp3 0.153 "29 Hop nhua ABS 170x70 khoan san - giong doc.mp4"
v c08-1117.mp4 vit-nhon-m4 1,8,15,22 "0.3:whoosh,6:pop,12:pop,17.5:pop" vlog-beat.mp3 0.09 "30 Vit nhon M4 15-40mm - giong doc.mp4"
v c09-202505021714.mp4 hop-xanh-nap-trong 2,12,22,35 "0.3:whoosh,6:pop,12:pop,19:pop,26:pop" inspiring-acoustic.mp3 0.112 "31 Hop nhua xanh nap trong - giong doc.mp4"
v c10-202505021633.mp4 hop-den-78x50x30 1,8,18,28 "0.3:whoosh,6:pop,12:pop,18:pop,24:pop" moodmode.mp3 0.153 "32 Hop nhua den 78x50x30 - giong doc.mp4"
v c11-202505021630.mp4 hop-den-tai-bat-vit 1,9,17,24 "0.3:whoosh,5.5:pop,11:pop,16.5:pop,21:pop" vlog-beat.mp3 0.09 "33 Hop nhua den co tai bat vit - giong doc.mp4"
v c14-202601151430.mp4 nhom-thanh-dai-co 2,10,20,28 "0.3:whoosh,6:pop,12:pop,19:pop,26:pop" running-night.mp3 0.097 "34 Nhom tan nhiet thanh dai (co) - giong doc.mp4"
v d01-p3000w.mp4 phich-cam-p3000w 1,4,8,12 "0.3:whoosh,5:pop,9.5:pop" pop-rock-quang-cao.mp3 0.148 "35 Phich cam P3000W - giong doc.mp4"
echo HET
