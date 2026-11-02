#!/bin/bash
# Dựng video 189–233 (đợt 4, 02/11: clip mới trong VIDEO THÔ, tools/lenh/p4-list.txt + ảnh còn lại). Clip thô: video/tho/dd/ (thư mục 2 › DÂN DỤNG; Drive id ở
# tools/lenh/dd-list.txt, tên file = 2 số mã + "_" + 6 ký tự đầu id + .mov) và video/tho/p2/ (tụ, hộp CNC,
# ống gen, vật liệu; tools/lenh/p2-list.txt: id + tên file). Tải bằng curl như CLAUDE.md.
# v = giọng đọc máy (tắt tiếng gốc); s = người nói thật (giữ giọng, phụ đề .srt, câu kết đọc máy).
cd "$(dirname "$0")/../.."
E="python3 tools/edit.py"; M=video/mau; N=video/assets/nhac; B=video/xong/ban-cuoi
T="--khung 9:16 --phu-de-cao 60 --chuan-am --studio --goc --nen-am-luong 0"
v(){ src=$1; key=$2; canh=$3; sfx=$4; nhac=$5; vol=$6; out=$7
  $E video/tho/$src $T --chu $M/$key.ass --giong $M/$key.loi.txt --sfx "$sfx" \
    --mo-dau $M/$key-mo-dau.ass --mo-dau-giong $M/$key-mo-dau.loi.txt --mo-dau-canh $canh \
    --nhac $N/$nhac --nhac-am-luong $vol $8 -o "$B/$out"; }
s(){ src=$1; key=$2; canh=$3; sfx=$4; nhac=$5; vol=$6; out=$7
  $E video/tho/$src --khung 9:16 --phu-de-cao 60 --chuan-am --studio --goc --chu $M/$key.ass --srt $M/$key.srt \
    --giong $M/$key-ket.loi.txt --sfx "$sfx" --mo-dau $M/$key-mo-dau.ass --mo-dau-giong $M/$key-mo-dau.loi.txt \
    --mo-dau-canh $canh --nhac $N/$nhac --nhac-am-luong $vol $8 -o "$B/$out"; }
v p4/n-5200-1943.mp4 so-toshiba-c5200-a1943 2,10,22,37 "0.3:whoosh,6:pop,13:pop,17:pop,29:pop,36:pop" pop-rock-quang-cao.mp3 0.148 "189 So Toshiba C5200 A1943 mo thu - giong doc.mp4"
v p4/n-5241626264413.mp4 loi-ei-silic-can-ky 1.2,6.3,13.8,24 "0.3:whoosh,6:pop,11:pop,17:pop,21:pop" running-night.mp3 0.097 "190 Loi ton silic EI len can - giong doc.mp4"
v p4/n-5295299094983.mp4 hop-chong-nuoc-nap-trong-xoay 1,6,11,16 "0.3:whoosh,5:pop,10:pop" promotion.mp3 0.098 "191 Hop nhua nap trong - giong doc.mp4"
v p4/n-5305448679023.mp4 dong-ho-bao-pin-ac-quy-usb 6,15,24,40 "0.3:whoosh,7:pop,12:pop,19:pop,27:pop,35:pop,40:pop" moodmode.mp3 0.153 "192 Dong ho bao pin ac quy USB - giong doc.mp4"
v p4/n-5331509475315.mp4 von-ke-led-xanh-3-so 7,17,36,46 "0.3:whoosh,7:pop,12:pop,22:pop,33:pop,42:pop,48:pop" vlog-beat.mp3 0.09 "193 Von ke LED xanh 3 so - giong doc.mp4"
v p4/n-5472261141554.mp4 keo-dan-tong-hop-tan-phu 0.6,4,8,13 "0.3:whoosh,5:pop" inspiring-acoustic.mp3 0.112 "194 Keo dan tong hop Tan Phu - giong doc.mp4"
v p4/n-5736674433627.mp4 o-cam-ac-c14-cau-chi-cong-tac 2,6.4,9.3,14 "0.3:whoosh,5:pop,9:pop" pop-rock-quang-cao.mp3 0.148 "195 O cam nguon cau chi cong tac - giong doc.mp4"
v p4/n-6150557802584.mp4 kep-ca-sau-thep-han-day 2.4,12,41,51 "0.3:whoosh,6:pop,12:pop,17:pop,27:pop,41:pop,48:pop" running-night.mp3 0.097 "196 Kep ca sau thep han day - giong doc.mp4"
v p4/n-6151992212798.mp4 mach-sac-ac-quy-12v-6a 2,14.9,28,41 "0.3:whoosh,7:pop,13:pop,19:pop,25:pop,31:pop,37:pop" promotion.mp3 0.098 "197 Mach sac ac quy 12V 6A - giong doc.mp4"
v p4/n-6156193567333.mp4 kep-ac-quy-100a-dong 3,11,23,41 "0.3:whoosh,6:pop,10:pop,16:pop,25:pop,36:pop,42:pop" moodmode.mp3 0.153 "198 Kep ac quy 100A dong - giong doc.mp4"
v p4/n-4931596754378.mp4 son-cach-dien-thife-chiet-chai 1,6,10,13 "0.3:whoosh,5:pop" vlog-beat.mp3 0.09 "199 Son cach dien chiet chai - giong doc.mp4"
v p4/n-4931596716144.mp4 son-cach-dien-thife-rot-chai 0.4,2.4,4.5,7 "0.3:whoosh" inspiring-acoustic.mp3 0.112 "200 Son cach dien THIFE chai le - giong doc.mp4"
s p4/n-5299154518695.mp4 mach-sac-tu-dong-20a-dau-day 8,70,133,165 "0.3:whoosh,10.3:pop,46.9:pop,58:pop,82:pop,91:pop,130.2:pop,137.4:pop,150.3:pop,168.1:pop" running-night.mp3 0.068 "201 Mach sac tu dong 20A dau day - review.mp4" "--bo 179.9-188.41"
v anh/anh2-kep-ca-sau-hai-co.mp4 anh2-kep-ca-sau-hai-co 2.75,7.75,12.75,22.75 "0.3:whoosh,5:pop,10:pop,15:pop,20:pop" running-night.mp3 0.097 "202 Kep ca sau 2 co lon nho - anh.mp4"
v anh/anh2-gen-thuy-tinh-soc-xanh.mp4 anh2-gen-thuy-tinh-soc-xanh 2.75,12.75,17.75,22.75 "0.3:whoosh,5:pop,10:pop,15:pop" moodmode.mp3 0.153 "203 Gen soi thuy tinh soc xanh - anh.mp4"
v anh/anh2-gen-thuy-tinh-bo-so-luong.mp4 anh2-gen-thuy-tinh-bo-so-luong 2.75,7.75,22.75,27.75 "0.3:whoosh,5:pop,10:pop,15:pop,20:pop" vlog-beat.mp3 0.09 "204 Gen soi thuy tinh nguyen bo - anh.mp4"
v anh/anh2-so-nhiet-ksd301-75-165-do.mp4 anh2-so-nhiet-ksd301-75-165-do 2.75,12.75,22.75,27.75 "0.3:whoosh,5:pop,10:pop,15:pop,20:pop" pop-rock-quang-cao.mp3 0.148 "205 So nhiet KSD301 75-165 do - anh.mp4" "--phu-de-cao 430"
v anh/anh2-phich-cam-chong-vo-sopoka.mp4 anh2-phich-cam-chong-vo-sopoka 2.2,6.7,11.2,20.2 "0.3:whoosh,4.8:pop,9.3:pop,13.8:pop,18.3:pop" promotion.mp3 0.098 "206 Phich cam chong vo SOPOKA - anh.mp4"
v anh/anh2-phich-sopoka-be-goc-va-thang.mp4 anh2-phich-sopoka-be-goc-va-thang 2.5,7.5,12.5,17.5 "0.3:whoosh,5.3:pop,10.3:pop,15.3:pop" inspiring-acoustic.mp3 0.112 "207 Phich SOPOKA be goc va thang - anh.mp4"
v anh/anh2-o-cam-sopoka-chon-theo-cho.mp4 anh2-o-cam-sopoka-chon-theo-cho 2.2,6.7,20.2,24.7 "0.3:whoosh,4.8:pop,9.3:pop,13.8:pop,18.3:pop,22.8:pop" vlog-beat.mp3 0.09 "208 O cam SOPOKA du kieu chon theo cho - anh.mp4"
s p4/ee5520-ho-nam.mp4 ferrite-ee5520-ho-nam 5,9,16,37 "0.6:whoosh,5.6:pop,10.5:pop,14.4:pop,19.8:pop,27.6:pop" promotion.mp3 0.069 "209 Loi ferrite E55-20 ho khuon nam - review.mp4"
s p4/ee5520-ho-dung.mp4 ferrite-ee5520-ho-dung 6,13,17,32 "0.7:whoosh,6:pop,8.3:pop,13.3:pop,20.7:pop,28.6:pop" moodmode.mp3 0.107 "210 Loi ferrite E55-20 ho khuon dung 11 chan - review.mp4"
s p4/ferrite-e4220-dung-6-6.mp4 ferrite-e4220-dung-6-6 6,14,25,41 "0.5:whoosh,8.8:pop,14.9:pop,24:pop,30.6:pop" vlog-beat.mp3 0.063 "211 Loi ferrite E42-20 khit khuon dung 6 chan - review.mp4"
s p4/ferrite-e4220-ho-nam.mp4 ferrite-e4220-ho-nam 6,10,39,43 "0.7:whoosh,8.2:pop,17.8:pop,31.4:pop,36.8:pop" inspiring-acoustic.mp3 0.078 "212 Loi ferrite E42-20 ho khuon nam - review.mp4"
s p4/ferrite-e4220-nam.mp4 ferrite-e4220-nam 2,25,38,43 "1:whoosh,5.9:pop,9.9:pop,16.9:pop,19.4:pop,29.4:pop" pop-rock-quang-cao.mp3 0.104 "213 Bo ferrite E42-20 khit khuon nam 8 chan - review.mp4"
s p4/ferrite-e4220-dung-9-9.mp4 ferrite-e4220-dung-9-9 2,19,24,41 "0.5:whoosh,5.6:pop,13.7:pop,22.3:pop,24.4:pop,31.7:pop" running-night.mp3 0.068 "214 Loi ferrite E42-20 khuon dung 9 chan - review.mp4"
s p4/ferrite-e5520-nam.mp4 ferrite-e5520-nam 5,16,31,35 "1.2:whoosh,6.3:pop,11.4:pop,16.2:pop,23.7:pop,33.7:pop" promotion.mp3 0.069 "215 Bo ferrite E55-20 khit khuon nam - review.mp4"
s p4/ferrite-e5520-dung.mp4 ferrite-e5520-dung 6,21,33,37 "0.7:whoosh,5.3:pop,13.3:pop,18.1:pop,22.9:pop,28:pop" moodmode.mp3 0.107 "216 Bo ferrite E55-20 khuon dung 11 chan - review.mp4"
v p4/ferrite-e5540-nam.mp4 ferrite-e5540-nam 5,15,27,48 "0.3:whoosh,6:pop,13:pop,18.5:pop,25:pop,33:pop,41:pop,47:pop" pop-rock-quang-cao.mp3 0.148 "217 Loi ferrite E5540 khuon nam - giong doc.mp4"
s p4/ferrite-e5540-ho-nam.mp4 ferrite-e5540-ho-nam 1,5,15,48 "0.3:whoosh,7.9:pop,13.4:pop,19.1:ding,25.7:pop,31.5:pop,39.6:pop" running-night.mp3 0.068 "218 Loi ferrite E5540 ho khuon nam - review.mp4"
s p4/ferrite-e5540-dung.mp4 ferrite-e5540-dung 5,14,24,52 "0.3:whoosh,5:pop,11.2:pop,19.1:pop,27.7:pop,35.3:pop" promotion.mp3 0.069 "219 Loi ferrite E5540 khit khuon dung - review.mp4"
s p4/ferrite-e5540-ho-dung.mp4 ferrite-e5540-ho-dung 15,20,30,51 "0.3:whoosh,6.6:pop,13:pop,20.9:ding,30.2:pop,37.6:pop,44.5:pop" moodmode.mp3 0.107 "220 Loi ferrite E5540 ho khuon dung - review.mp4"
s p4/ferrite-ec60-nam.mp4 ferrite-ec60-nam 4,9,26,43 "0.3:whoosh,2.6:pop,6.3:ding,12.8:pop,22:pop,37.5:pop,40.6:pop" vlog-beat.mp3 0.063 "221 Loi ferrite EC60 khuon nam - review.mp4"
s p4/ferrrite-e6527-nam.mp4 ferrite-e6527-nam 4,13,35,44 "0.3:whoosh,7.6:pop,11.6:pop,15.3:ding,22.7:pop,31.1:pop,36:pop" inspiring-acoustic.mp3 0.078 "222 Loi ferrite E6527 khuon nam - review.mp4"
s p4/ferrite-e70.mp4 ferrite-e70 5,10,35,54 "0.3:whoosh,5.2:pop,13.6:ding,22.8:pop,32.9:pop,40.4:pop" pop-rock-quang-cao.mp3 0.104 "223 Loi ferrite E70 khuon nam - review.mp4"
s p4/xuyen-31mm.mp4 ferrite-xuyen-31mm 4,6,12,22 "0.3:whoosh,3.2:pop,5.2:ding,8.3:pop,10.8:pop,16.5:pop" running-night.mp3 0.068 "224 Loi xuyen ferrite 31mm - review.mp4"
s p4/xuyen-36mm.mp4 ferrite-xuyen-36mm 3,13,20,33 "0.3:whoosh,5.4:pop,10:ding,19:pop,24:pop,28.7:pop" promotion.mp3 0.069 "225 Loi xuyen ferrite 36mm - review.mp4"
s p4/xuyen-63mm.mp4 ferrite-xuyen-63mm 1,8,30,41 "0.3:whoosh,3.9:pop,7.9:ding,28.5:pop,35.5:pop" moodmode.mp3 0.107 "226 Loi xuyen ferrite 63mm - review.mp4"
v p4/chiec-vecni.mp4 chiet-vecni-chai-nho 1,4,8,12.5 "0.3:whoosh,4.8:pop" pop-rock-quang-cao.mp3 0.148 "227 Vecni chiet le chai nho - giong doc.mp4"
v p4/keo-ab-tan-phu.mp4 keo-dan-tan-phu 1,4,9,13.8 "0.3:whoosh,5:pop" running-night.mp3 0.097 "228 Keo dan tong hop Tan Phu (2) - giong doc.mp4"
v p4/look-quat-stato-quat.mp4 stato-quat-day-dong 1,8,15,25 "0.3:whoosh,6:pop,11:pop,17:pop" promotion.mp3 0.098 "229 Stato quat day dong - giong doc.mp4"
v p4/fesilic.mp4 la-fe-silic-e-i-nguyen-thung 2,5,21,27 "0.3:whoosh,6:pop,12:pop,19:pop,26:pop,32:pop" moodmode.mp3 0.153 "230 La Fe silic E-I nguyen thung - giong doc.mp4" "--bo 43-45.1 --day-khung"
s p4/20250108-075507000-ios.mov kep-ac-quy-o-to-500a 4.5,10.5,22.5,28.5 "0.3:whoosh,5:pop,14:pop,21:pop" vlog-beat.mp3 0.063 "231 Kep ac quy o to 500A - review.mp4"
s p4/keo-vecni-trang-nhung-ba.mp4 vecni-pha-xang-nhung-bien-ap 2,20,35,52 "0.3:whoosh,6.8:pop,10:pop,16.3:pop,24.6:pop,33:pop,43:pop" inspiring-acoustic.mp3 0.078 "232 Pha vecni nhung bien ap - review.mp4" "--bo 55-161.42"
s p4/keo-vecni-trang-nhung-ba.mp4 vecni-trang-nhung-bien-ap-xung 70,85,118,145 "55.3:whoosh,65.5:pop,90:pop,113.7:pop,117.8:pop,138:ding,146:pop" pop-rock-quang-cao.mp3 0.104 "233 Vecni trang nhung bien ap xung - review.mp4" "--bo 0-55"
echo HET
