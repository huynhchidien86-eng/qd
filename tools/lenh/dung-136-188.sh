#!/bin/bash
# Dựng video 136–188 (đợt 3, 01/11: clip còn lại p3/ + video từ ảnh anh/). Clip thô: video/tho/dd/ (thư mục 2 › DÂN DỤNG; Drive id ở
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
# Phần hình video ảnh (video/tho/anh/*.mp4) dựng bằng tools/anh_video.py, ảnh chọn ghi ở dòng đầu mỗi video/mau/anh-*.loi.txt.
v p3/d-kep-ca-sau-6550010194216.mp4 kep-ca-sau-co-lon 1,9,21,42 "0.3:whoosh,6:pop,12:pop,18:pop,27:pop,36:pop,47.5:pop,53.5:pop" pop-rock-quang-cao.mp3 0.148 "136 Kep ca sau co lon - giong doc.mp4"
v p3/d-kep-ca-sau-6550009084280.mp4 kep-ca-sau-co-vua 1,6,18,39 "0.3:whoosh,6:pop,10.5:pop,15:pop,24:pop,30:pop,42:pop" running-night.mp3 0.097 "137 Kep ca sau do den co vua - giong doc.mp4"
v p3/d-kep-ca-sau-6550008580920.mp4 kep-ca-sau-co-nho 1,18,42,54 "0.3:whoosh,6:pop,15:pop,24:pop,33:pop,47.5:pop,53.5:pop" promotion.mp3 0.098 "138 Kep ca sau co nho - giong doc.mp4"
v p3/t-225k-630v.mp4 tu-keo-weidy-cbb21-225k 1,5,15,42 "0.3:whoosh,6:pop,12.5:pop,19:pop,25.5:pop,33:pop" moodmode.mp3 0.153 "139 Tu keo WEIDY CBB21 225K 630V - giong doc.mp4"
v p3/t-6983.mov tu-tinh-chi-hop-vuong-ke 7,16,37,55 "0.3:whoosh,6.5:pop,13.5:pop,20.5:pop,32.3:pop,42.5:pop,49.5:pop,55:pop" vlog-beat.mp3 0.09 "140 Tu Tinh Chi hop vuong du so - giong doc.mp4" "--bo 28.3-31.8"
v p3/v-bang-keo-vang-5774502879793.mp4 bang-keo-vang-ke-kho 8,15,24,36 "0.3:whoosh,6:pop,12:pop,18:pop,24:pop,30:pop,36:pop" inspiring-acoustic.mp3 0.112 "141 Bang keo vang day ke kho - giong doc.mp4"
v p3/h-dong-goi-don-hang-hop-abs.mp4 hop-abs-dong-goi-don-lon 2,18,50,80 "0.3:whoosh,12:pop,23:pop,38:pop,45.5:pop,72:pop,79.5:ding" pop-rock-quang-cao.mp3 0.148 "142 Hop nhua ABS dong goi don lon - giong doc.mp4" "--bo 90.2-93.3"
v p3/h-cnc-1121.mov hop-cnc-kho-khoet-san 12,24,38,60 "0.3:whoosh,8:pop,13:pop,20:pop,32:pop,38.5:pop,46:pop,60:pop,67:pop" running-night.mp3 0.097 "143 Kho hop nhua khoet san lo quat - giong doc.mp4"
s p3/h-so-sanh-2-hop-200x120x75.mp4 hop-200-wanchi-vyanh 3,13,33,46 "1.0:whoosh,11:pop,19.3:pop,30:ding,51.8:pop" promotion.mp3 0.069 "144 So sanh hop 200 WANCHI va VY ANH - review.mp4" "--bo 0-0.9"
s p3/h-hop-dung-pin-xe-dien.mp4 hop-pin-xe-dien-16s 1,12,19,25 "0.9:whoosh,6.8:pop,14.6:pop,20.4:ding" moodmode.mp3 0.107 "145 Hop dung pin xe dien 16S 2P - review.mp4" "--bo 0-0.85,25.92-34.3"
v anh/anh-tu-mb-tinh-chi-ba-tri-so.mp4 anh-tu-mb-tinh-chi-ba-tri-so 2.7,7.7,12.7,17.7 "0.3:whoosh,5.1:pop,10.1:pop,15.1:pop" pop-rock-quang-cao.mp3 0.148 "146 Tu may bom Tinh Chi 20-25-30uF - anh.mp4"
v anh/anh-tu-mb-tinh-chi-20uf.mp4 anh-tu-mb-tinh-chi-20uf 2.7,7.7,12.7,17.7 "0.3:whoosh,5.1:pop,10.1:pop,15.1:pop" running-night.mp3 0.097 "147 Tu Tinh Chi 20uF 450VAC - anh.mp4"
v anh/anh-tu-mb-tinh-chi-25uf.mp4 anh-tu-mb-tinh-chi-25uf 2.7,7.7,12.7,17.7 "0.3:whoosh,5.1:pop,10.1:pop,15.1:pop" promotion.mp3 0.098 "148 Tu Tinh Chi 25uF 450VAC - anh.mp4"
v anh/anh-tu-mb-tinh-chi-30uf.mp4 anh-tu-mb-tinh-chi-30uf 2.7,7.7,12.7,17.7 "0.3:whoosh,5.1:pop,10.1:pop,15.1:pop" moodmode.mp3 0.153 "149 Tu Tinh Chi 30uF 450VAC - anh.mp4"
v anh/anh-tu-mb-tinh-chi-kich-thuoc.mp4 anh-tu-mb-tinh-chi-kich-thuoc 7.7,12.7,17.7,22.7 "0.3:whoosh,5.1:pop,10.1:pop,15.1:pop" vlog-beat.mp3 0.09 "150 Tu may bom Tinh Chi kich thuoc - anh.mp4"
v anh/anh-tu-mb-tinh-chi-hang-san.mp4 anh-tu-mb-tinh-chi-hang-san 2.7,7.7,12.7,22.7 "0.3:whoosh,5.1:pop,10.1:pop,15.1:pop" inspiring-acoustic.mp3 0.112 "151 Tu may bom Tinh Chi hang san - anh.mp4"
v anh/anh-tu-mb-tinh-chi-day-cos.mp4 anh-tu-mb-tinh-chi-day-cos 2.7,7.7,12.7,17.7 "0.3:whoosh,5.1:pop,10.1:pop,15.1:pop" pop-rock-quang-cao.mp3 0.148 "152 Tu may bom Tinh Chi ra san day cos - anh.mp4"
v anh/anh-tu-mb-tinh-chi-du-loai.mp4 anh-tu-mb-tinh-chi-du-loai 2.7,7.7,12.7,17.7 "0.3:whoosh,5.1:pop,10.1:pop,15.1:pop" running-night.mp3 0.097 "153 Tu Tinh Chi du loai 10-30uF - anh.mp4"
v anh/anh-so-nhiet-ksd301-tren-tay.mp4 anh-so-nhiet-ksd301-tren-tay 2.5,7.5,17.5,22.7 "0.3:whoosh,5:pop,10:pop,15:pop" pop-rock-quang-cao.mp3 0.148 "154 So nhiet KSD301 tren tay - anh.mp4"
v anh/anh-so-nhiet-ksd301-can-canh.mp4 anh-so-nhiet-ksd301-can-canh 2.2,6.7,11.2,20.2 "0.3:whoosh,4.5:pop,9:pop,13.5:pop,18:pop" running-night.mp3 0.097 "155 So nhiet KSD301 can canh - anh.mp4"
v anh/anh-so-nhiet-ksd301-60-180-do.mp4 anh-so-nhiet-ksd301-60-180-do 2.2,11.2,15.7,24.7 "0.3:whoosh,4.5:pop,9:pop,13.5:pop,18:pop" promotion.mp3 0.098 "156 So nhiet KSD301 60-180 do - anh.mp4"
v anh/anh-cau-chi-tu-ngat-du-dong.mp4 anh-cau-chi-tu-ngat-du-dong 2.5,7.5,12.5,17.5 "0.3:whoosh,5:pop,10:pop,15:pop" moodmode.mp3 0.153 "157 Cau chi tu ngat du dong - anh.mp4"
v anh/anh-co-bop-tiep-diem-dong.mp4 anh-co-bop-tiep-diem-dong 2.2,11.2,15.7,24.7 "0.3:whoosh,4.5:pop,9:pop,13.5:pop,18:pop" vlog-beat.mp3 0.09 "158 Co bop tiep diem dong - anh.mp4"
v anh/anh-kep-ca-sau-tui-10-doi.mp4 anh-kep-ca-sau-tui-10-doi 2.2,6.7,11.2,24.7 "0.3:whoosh,4.5:pop,9:pop,13.5:pop,18:pop" inspiring-acoustic.mp3 0.112 "159 Kep ca sau tui 10 doi - anh.mp4"
v anh/anh-kep-ca-sau-ngam-rang.mp4 anh-kep-ca-sau-ngam-rang 2.2,11.2,15.7,20.2 "0.3:whoosh,4.5:pop,9:pop,13.5:pop,18:pop" pop-rock-quang-cao.mp3 0.148 "160 Kep ca sau ngam rang - anh.mp4"
v anh/anh-kep-ca-sau-cam-tay.mp4 anh-kep-ca-sau-cam-tay 2.2,6.7,15.7,24.7 "0.3:whoosh,4.5:pop,9:pop,13.5:pop,18:pop" running-night.mp3 0.097 "161 Kep ca sau boc do den - anh.mp4"
v anh/anh-day-nguon-cuon-gon.mp4 anh-day-nguon-cuon-gon 2.5,7.5,12.5,22.7 "0.3:whoosh,5:pop,10:pop,15:pop" promotion.mp3 0.098 "162 Day nguon cuon gon - anh.mp4"
v anh/anh-ru-lo-sopoka-ru3500w-thung.mp4 anh-ru-lo-sopoka-ru3500w-thung 2.5,7.5,12.5,17.5 "0.3:whoosh,5.3:pop,10.3:pop" pop-rock-quang-cao.mp3 0.148 "163 Ru lo SOPOKA RU3500W nguyen thung - anh.mp4"
v anh/anh-o-cam-sopoka-trang-du-mau.mp4 anh-o-cam-sopoka-trang-du-mau 2.2,6.8,11.2,24.7 "0.3:whoosh,4.8:pop,9.3:pop,13.8:pop,18.3:pop" running-night.mp3 0.097 "164 O cam SOPOKA vo trang du mau - anh.mp4"
v anh/anh-o-cam-keo-dai-sopoka-du-loai.mp4 anh-o-cam-keo-dai-sopoka-du-loai 2.2,6.8,15.8,24.7 "0.3:whoosh,4.8:pop,9.3:pop,13.8:pop,18.3:pop" promotion.mp3 0.098 "165 O cam keo dai SOPOKA du loai - anh.mp4"
v anh/anh-o-cam-sopoka-cam-day-dai.mp4 anh-o-cam-sopoka-cam-day-dai 2.5,7.5,12.5,17.5 "0.3:whoosh,5.3:pop,10.3:pop,15.3:pop" moodmode.mp3 0.153 "166 O cam SOPOKA mau cam day dai - anh.mp4"
v anh/anh-day-noi-sopoka-3000w.mp4 anh-day-noi-sopoka-3000w 2.2,11.2,15.8,24.7 "0.3:whoosh,4.8:pop,9.3:pop,13.8:pop,18.3:pop" vlog-beat.mp3 0.09 "167 Day noi nguon SOPOKA 3000W - anh.mp4"
v anh/anh-chao-dui-den.mp4 anh-chao-dui-den 2.2,6.8,15.8,20.2 "0.3:whoosh,4.8:pop,9.3:pop,13.8:pop,18.3:pop" inspiring-acoustic.mp3 0.112 "168 Chao den kem dui - anh.mp4"
v anh/anh-bong-led-sopoka-victolux.mp4 anh-bong-led-sopoka-victolux 2.5,7.5,12.5,17.5 "0.3:whoosh,5.3:pop,10.3:pop,15.3:pop" pop-rock-quang-cao.mp3 0.148 "169 Bong LED SOPOKA Victolux 7-60W - anh.mp4"
v anh/anh-thiet-bi-dien-sopoka.mp4 anh-thiet-bi-dien-sopoka 2.2,6.8,15.8,20.2 "0.3:whoosh,4.8:pop,9.3:pop,13.8:pop,18.3:pop" running-night.mp3 0.097 "170 Thiet bi dien SOPOKA cau dao cong tac - anh.mp4"
v anh/anh-hop-wanchi-du-co.mp4 anh-hop-wanchi-du-co 2.5,7.5,12.5,22.5 "0.3:whoosh,5.3:pop,10.3:pop,15.3:pop" promotion.mp3 0.098 "171 Hop nhua WANCHI du co - anh.mp4"
v anh/anh-hop-wanchi-co-lon.mp4 anh-hop-wanchi-co-lon 2.5,7.5,12.5,17.5 "0.3:whoosh,5.3:pop,10.3:pop,15.3:pop" moodmode.mp3 0.153 "172 Hop nhua WANCHI co lon - anh.mp4"
v anh/anh-bang-keo-vang-bien-ap.mp4 anh-bang-keo-vang-bien-ap 7.75,12.75,17.75,22.75 "0.3:whoosh,5:pop,10:pop,15:pop,20:pop" pop-rock-quang-cao.mp3 0.148 "173 Bang keo vang quan bien ap - anh.mp4"
v anh/anh-bang-keo-vang-du-size.mp4 anh-bang-keo-vang-du-size 2.75,7.75,22.75,27.75 "0.3:whoosh,5:pop,10:pop,15:pop,20:pop" running-night.mp3 0.097 "174 Bang keo vang du size 10-40mm - anh.mp4"
v anh/anh-bang-keo-vang-ban-tho.mp4 anh-bang-keo-vang-ban-tho 2.75,7.75,12.75,22.75 "0.3:whoosh,5:pop,10:pop,15:pop,20:pop" promotion.mp3 0.098 "175 Bang keo vang ban tho - anh.mp4"
v anh/anh-bang-keo-nano-nguyen-cay.mp4 anh-bang-keo-nano-nguyen-cay 2.75,12.75,17.75,27.75 "0.3:whoosh,5:pop,10:pop,15:pop,20:pop" moodmode.mp3 0.153 "176 Bang keo dien Nano nguyen cay - anh.mp4"
v anh/anh-bang-keo-nano-cuon-le.mp4 anh-bang-keo-nano-cuon-le 2.75,7.75,17.75,22.75 "0.3:whoosh,5:pop,10:pop,15:pop,20:pop" vlog-beat.mp3 0.09 "177 Bang keo dien Nano 18mm - anh.mp4"
v anh/anh-bang-keo-nau-chiu-nhiet.mp4 anh-bang-keo-nau-chiu-nhiet 2.75,12.75,17.75,22.75 "0.3:whoosh,5:pop,10:pop,15:pop,20:pop" inspiring-acoustic.mp3 0.112 "178 Bang keo nau chiu nhiet - anh.mp4"
v anh/anh-gen-thuy-tinh-soc-do.mp4 anh-gen-thuy-tinh-soc-do 2.75,7.75,12.75,22.75 "0.3:whoosh,5:pop,10:pop,15:pop" pop-rock-quang-cao.mp3 0.148 "179 Gen soi thuy tinh soc do - anh.mp4"
v anh/anh-ong-gen-thuy-tinh-cuon-tron.mp4 anh-ong-gen-thuy-tinh-cuon-tron 2.75,7.75,17.75,22.75 "0.3:whoosh,5:pop,10:pop,15:pop" running-night.mp3 0.097 "180 Ong gen soi thuy tinh cuon tron - anh.mp4"
v anh/anh-ong-gen-thuy-tinh-ban-det.mp4 anh-ong-gen-thuy-tinh-ban-det 2.75,7.75,12.75,22.75 "0.3:whoosh,5:pop,10:pop,15:pop" promotion.mp3 0.098 "181 Ong gen soi thuy tinh ban to - anh.mp4"
v anh/anh-tu-eun-sung-60uf.mp4 anh-tu-eun-sung-60uf 2.5,16,20.5,25 "0.3:whoosh,4.5:pop,9:pop,13.5:pop,18:pop" pop-rock-quang-cao.mp3 0.148 "182 Tu nhom EUN SUNG 60uF - anh.mp4"
v anh/anh-tu-eun-sung-70-80uf.mp4 anh-tu-eun-sung-70-80uf 2.8,7.8,12.8,17.8 "0.3:whoosh,5:pop,10:pop,15:pop" running-night.mp3 0.097 "183 Tu nhom EUN SUNG 70-80uF - anh.mp4"
v anh/anh-tu-eun-sung-nho-den-lon.mp4 anh-tu-eun-sung-nho-den-lon 2.8,12.8,17.8,22.8 "0.3:whoosh,5:pop,10:pop,15:pop" promotion.mp3 0.098 "184 Tu nhom EUN SUNG nho den lon - anh.mp4"
v anh/anh-tu-eun-sung-so-luong.mp4 anh-tu-eun-sung-so-luong 2.5,7,16,25 "0.3:whoosh,4.5:pop,9:pop,13.5:pop,18:pop" moodmode.mp3 0.153 "185 Tu nhom EUN SUNG so luong - anh.mp4"
v anh/anh-tu-eun-sung-nhan-ro.mp4 anh-tu-eun-sung-nhan-ro 2.8,7.8,12.8,22.8 "0.3:whoosh,5:pop,10:pop,15:pop" vlog-beat.mp3 0.09 "186 Tu nhom EUN SUNG nhan ro - anh.mp4"
v anh/anh-tu-nuintek-day-do-can-canh.mp4 anh-tu-nuintek-day-do-can-canh 2.8,7.8,12.8,17.8 "0.3:whoosh,5:pop,10:pop,15:pop" inspiring-acoustic.mp3 0.112 "187 Tu nhom day do NUINTEK can canh - anh.mp4"
v anh/anh-tu-nuintek-day-do-tri-so.mp4 anh-tu-nuintek-day-do-tri-so 2.5,11.5,20.5,25 "0.3:whoosh,4.5:pop,9:pop,13.5:pop,18:pop" pop-rock-quang-cao.mp3 0.148 "188 Tu nhom day do 15-40uF - anh.mp4"
echo HET
