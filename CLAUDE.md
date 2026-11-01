# Bộ nhớ Diên

File này là **bộ nhớ dài hạn** của repo `qd`. Claude Code tự động đọc nó ở đầu mỗi
phiên làm việc, nên mọi thứ ghi ở đây sẽ được nhớ lại lần sau. Ngoài file này ra,
Claude **không** nhớ gì giữa các phiên.

Muốn bổ sung: anh sửa trực tiếp file này, hoặc bảo em "ghi vào bộ nhớ ...".

## Người dùng

- Xưng hô: **anh** = người dùng (Diên), **em** = Claude.
- Ngôn ngữ trả lời: **tiếng Việt**.
- GitHub: `huynhchidien86-eng`
- Repo chính: `huynhchidien86-eng/qd`

## Dự án

<!-- Anh điền: repo này dùng để làm gì, stack/ngôn ngữ, cấu trúc thư mục. -->

- Mục đích: **edit video tự động**. Anh đưa video thô, em edit bằng FFmpeg + Python
  rồi trả video hoàn chỉnh.
- Stack: FFmpeg, Python 3, `auto-editor` (cắt khoảng lặng), `faster-whisper` (phụ đề),
  `edge-tts` (giọng đọc tiếng Việt), `espeak-ng` (giọng máy để chạy thử).
- Cấu trúc thư mục:
  - `tools/edit.py`: script edit chính (xem `python3 tools/edit.py -h`).
  - `tools/giong_doc.py`: tạo giọng đọc + phụ đề khớp từ file lời đọc `.txt`.
  - `tools/tao_mau.py`: tạo nhanh file chữ `.ass` (chữ nổi bật + khung kết nhẹ nhàng, mở đầu cuốn) và
    phụ đề `.srt` theo phong cách đã chốt: `chu_chinh()`, `chu_mo_dau()`, `phu_de()`.
  - `tools/anh_video.py`: ghép nhiều ảnh thành video dọc (zoom/lia chậm + chuyển cảnh),
    rồi đưa vào `edit.py` để thêm chữ, giọng đọc, hiệu ứng như video thường.
  - `video/mau/`: mẫu chữ (`.ass`) và lời đọc (`.loi.txt`) theo từng sản phẩm.
  - `tools/setup.sh`: cài công cụ. Tự chạy đầu mỗi phiên cloud nhờ hook
    `.claude/hooks/session-start.sh` (khai báo trong `.claude/settings.json`).
  - `video/tho/`: video thô (không đưa lên git).
  - `video/xong/`: video đã edit (không đưa lên git).
  - `video/assets/`: logo, nhạc nền, font dùng chung.

## Quy ước làm việc

<!-- Ví dụ: code style, cách đặt tên commit, cách chạy test trước khi push. -->

- Nhánh phát triển đặt tên dạng `claude/<mô-tả>`.
- Pull request mở ở dạng **draft**.
- _Các quy ước khác: chưa có._

## Lệnh hay dùng

<!-- Ví dụ: npm test, make build, ./scripts/dev.sh -->

```bash
bash tools/setup.sh                       # cài công cụ (hook đã tự chạy, chỉ cần khi lỗi)
python3 tools/edit.py video/tho/abc.mp4 \
  --cat-lang --phu-de --khung 9:16 \
  --nhac video/assets/nhac.mp3 --logo video/assets/logo.png \
  --tieu-de "Tiêu đề" --mo-dau-ket-thuc --chuan-am
```

Tùy chọn chính: `--tu/--den` (cắt đầu/cuối), `--cat-lang` (bỏ khoảng lặng,
chỉnh bằng `--nguong-lang`, `--le`), `--phu-de` hoặc `--srt file.srt`,
`--khung 9:16|16:9|1:1|4:5`, `--nhac`, `--logo`, `--tieu-de`, `--chu file.ass`
(nhiều đoạn chữ theo thời gian), `--chuan-am`, `--giong loi.txt` (giọng đọc + phụ đề;
kèm `--giong-doc vi-VN-HoaiMyNeural|vi-VN-NamMinhNeural`, `--toc-do +10%`,
`--nen-am-luong 0.25`, `--phu-de-cao 60`, `--giong-engine espeak` để chạy thử).

Video sản phẩm có giọng đọc (mẫu Fe silic):
```bash
python3 tools/edit.py video/tho/IMG_5312.MOV --khung 9:16 \
  --chu video/mau/fe-silic-ei-giong.ass --giong video/mau/fe-silic-ei.loi.txt \
  --phu-de-cao 60 --mo-dau-ket-thuc --chuan-am
```

## Quy trình edit video

Khi anh bảo "lấy video thô edit":
1. Kiểm tra công cụ đã cài (hook tự chạy `tools/setup.sh`; nếu thiếu thì chạy tay).
2. Lấy video thô về `video/tho/` (anh đính kèm file trong chat, hoặc link tải trực tiếp).
3. Chạy `tools/edit.py` theo "phong cách mặc định" bên dưới, trừ khi anh dặn khác.
4. Trích vài khung hình kiểm tra phụ đề/tiêu đề trước khi giao.
5. Gửi file trong `video/xong/` cho anh.

## Thương hiệu của anh

- Tên shop: **Linh Kiện Quỳnh Diễn**. Logo ghi **QUYNDIEN Electronic**: hình con chip
  mạch điện màu xanh lá, chữ QUYNDIEN xanh lá đậm, chữ "Electronic" xanh đen, nền trắng.
- Màu thương hiệu: xanh lá `#22B526` (trong file ASS viết `&H0026B522`), điểm nhấn
  chữ vàng `#FFD700` (`&H0000D7FF`).
- File logo: _chưa có trong repo_. Khi có, lưu ở `video/assets/logo-quyndien.png` và
  thêm `--logo video/assets/logo-quyndien.png` khi edit.
- Mặt hàng: linh kiện điện tử, lõi biến áp (Fe silic EI…). Video đăng bán hàng.

## Phong cách mặc định (video sản phẩm)

Chốt từ video đầu tiên (IMG_5312, Fe silic EI). Mẫu ở `video/mau/fe-silic-ei.ass`.
- Khung dọc 9:16 (1080x1920), giữ độ dài gốc, mờ dần đầu/cuối, `--chuan-am`.
- Chữ chạy theo thời gian bằng file ASS (`--chu`): tên shop trong hộp xanh lá cố định
  ở trên; tiêu đề sản phẩm lớn màu vàng viền đen 4 giây đầu; mỗi 4–5 giây một ý chính
  (công dụng, đặc điểm, size, cam kết) trong hộp đen mờ ở dưới; cuối video là khung kết
  nhẹ nhàng (xem "Kết thúc kêu gọi nhẹ nhàng" bên dưới), **không** dùng hộp "ĐẶT HÀNG NGAY!".
- Nội dung chữ lấy từ mô tả sản phẩm anh gửi, viết ngắn gọn từng ý.
- Video sản phẩm thường không có lời nói, nên không dùng `--cat-lang`.
- Anh muốn có **giọng đọc kèm phụ đề**. Lời đọc viết từ mô tả sản phẩm, ~7 câu cho
  video 30s, dòng cuối là lời mời nhẹ nhàng (xem "Kết thúc" bên dưới). Số, đơn vị, từ tiếng Anh
  viết theo cách đọc ở vế sau dấu `|` (0.5mm → "không phẩy năm li", inverter → "in vớt tơ").
  Bản có giọng đọc dùng mẫu chữ `*-giong.ass` (bỏ hộp ý chính, tiêu đề đưa lên trên).
- Font: DejaVu Sans (có đủ dấu tiếng Việt). Font này không có emoji; dùng ✔ ► thay emoji.

## Ghi nhớ khác

<!-- Bất cứ điều gì anh muốn em nhớ qua các phiên: sở thích, việc cần tránh, ngữ cảnh riêng. -->

- Video thô ở Google Drive: `MAKETING/MEDIA/Video Tài/VIDEO` (folder id
  `1DjeP_fG4AjUrYxNTPAv1yit1A2GVlxXY`). Tìm file bằng Drive connector, rồi tải bằng:
  `curl -sSL -o video/tho/<tên> "https://drive.usercontent.google.com/download?id=<FILE_ID>&export=download&confirm=t"`.
  File phải được chia sẻ "Bất kỳ ai có đường liên kết", nếu không sẽ tải về trang đăng nhập (HTML).
- Môi trường cloud "Default" đã mở mạng cho `drive.google.com`, `drive.usercontent.google.com`,
  `huggingface.co`, `*.hf.co` (model Whisper), `speech.platform.bing.com` (giọng đọc).
  Cả `--phu-de` và `--giong` đều chạy được.
- Không tải video qua Drive connector (base64 quá nặng), dùng curl như trên.
- Anh chê giọng espeak "nghe kỳ": **không giao video dùng giọng espeak**. Chưa có giọng
  thật thì làm bản chữ chạy, không giọng đọc.
- Video đã làm: IMG_5312 (Fe silic EI), ổ cắm siêu tải 6000W (Drive id
  `1ov4emmpEYuPNuk_oB421OYpu5i6tmzIP`, mẫu `video/mau/o-cam-6000w.*`).
- Giọng mặc định: **vi-VN-HoaiMyNeural** (nữ), **tốc độ `+30%`, cao giọng `+0Hz`** (mặc định trong
  `edit.py`). Anh muốn giọng **thật, tự nhiên, cuốn hút**. ĐÃ BỊ CHÊ: `+50%` + nâng cao giọng `+6Hz`
  nghe "éo éo như con nít"; tốc độ thường (+0%) thì "buồn ngủ". Không tăng tốc quá +35%, không nâng
  cao giọng. Giọng qua `VOICE_FX` (nén nhẹ, ấm, rõ chữ vừa phải, không chói).
- **KHÔNG tăng tốc cả video** (`--nhanh` để 1.0; tùy chọn vẫn còn nhưng anh không thích). Video người
  nói thật giữ tốc độ gốc.
- Lời đọc phải vừa độ dài video. Câu kết (lời mời nhẹ nhàng) neo bằng `@giây` trùng lúc
  khung kết trong file `.ass` hiện ra.
- Ổ cắm 6000W là hàng thương hiệu **SOPOKA** (đọc "Sô pô ca").
- Ống gen sợi thủy tinh: anh đồng ý **không dùng chữ "amiang"** (amiang = asbestos, chất
  độc) trong video; kích thước ghi Ø2–10mm. Mẫu `video/mau/ong-gen*` (Drive id
  `1lzwhDqIbZ2mvtNnYZLoQRP_6_xvpFuCn`).
- Ảnh ống gen có sẵn trên Drive: "Ống gen Amiang HD.jpg", "Ống gen Amiang 1..8 HD.jpg" (mỗi ảnh
  một thư mục riêng, chưa chia sẻ lúc 31/10).
- **Nơi lưu video đã edit**: Drive `MAKETING/AFFILIATE HÀNG TOP/VIDEO ĐÃ EDIT (Claude)` (folder id
  `1UknrR5cUuxUuMqtidoY3ke0p5yG3s3Ii`). Em **không tự upload được** (Drive connector chỉ nhận file nhỏ
  qua base64): đặt tên file dạng `NN Tên sản phẩm - kiểu.mp4` trong `video/xong/ban-cuoi/`, gửi anh
  bằng SendUserFile, anh tải về rồi kéo vào thư mục. Máy cloud bị xoá sau phiên: video chưa gửi
  anh là mất (nhưng làm lại được từ repo vì lệnh + mẫu đã lưu).
- Đã gửi bản cuối: 01 Fe silic EI, 02 Ổ cắm SOPOKA 6000W, 03 Tụ CBB 60uF, 04 Ống gen sợi thủy tinh,
  05 Hộp nhựa WANCHI KW-CN-170. Cả 5 đã theo kiểu mở đầu cuốn + kết nhẹ nhàng (01–03 làm lại 31/10).
  Ngày 01/11 làm thêm 06–10 từ VIDEO THÔ: 06 Hộp WANCHI 200x120x75 IGBT, 07 Hộp WANCHI 168x92x56 (2 video
  người nói thật), 08 Hộp WANCHI 130x68x44, 09 Biến áp âm ly 12A 35V đôi, 10 Bulong M6x100 kèm tán (giọng
  đọc, tắt tiếng gốc bằng `--nen-am-luong 0`). Mẫu `video/mau/<tên>.*`; lệnh trong commit "5 video 06–10".
- Video 4K: `edit.py` tự thu về 1080p trước khi dựng (trước đó phần mở đầu cắt 4 cảnh từ 4K làm máy
  hết bộ nhớ, tiến trình bị kill). Dựng nhiều video dài thì chạy nền (`run_in_background`).
- **File trùng tên khác nhau trong VIDEO THÔ**: nhiều file bulong cùng dung lượng đến từng byte nhưng tên
  khác (vd "M3x10.MOV" = "M3x12 (4).mov" = "M3x20.mov"). Xem nội dung, không tin tên file.
- 01/11 làm thêm 11–15 (bulong/ốc vít, giọng đọc, tắt tiếng gốc): 11 Ốc M3 đủ size (ghép 5 clip), 12 M3x12,
  13 M3x15, 14 M4x10 đầu dù, 15 M6x120. Mẫu `video/mau/oc-vit-*`, `oc-m4x10-dau-du*`, `bulong-m6x120*`.
  Số đo thước kẹp không rõ đo phần nào thì không đọc số (chỉ M6x120 ghi "thân dài 120mm" vì thấy rõ trên thước).
- 01/11 làm thêm 16–25 (lệnh dựng: `tools/lenh/dung-16-25.sh`): 16 Hộp Wanchi 200 trắng, 17 Hộp Wanchi 168
  bản Volume, 20 Nhôm 8 lá dài 5 tấc, 21 Khuôn biến áp 50x100, 22 Khuôn 32x50 (5 video người nói thật);
  18 Nhôm 2 tầng 7 cánh, 19 Nhôm 2 tầng 10 cánh, 23 Ổ cắm SOPOKA MAX 2200W (file "10A4"), 24 Nhôm thanh dài
  (file "1108"), 25 IGBT 40T120 MagnaChip mổ thử (giọng đọc). Bỏ qua "400UF", "800uf 11", "240-6": quảng cáo
  người dẫn AI đã dựng xong. Video 14 dựng lại vì câu kết bị đọc 2 lần.
- 01/11 làm thêm **100 video 36–135** (lệnh: `tools/lenh/dung-36-135.sh`, danh sách Drive id `tools/lenh/dd-list.txt`,
  `p2-list.txt`): 36–89 từ thư mục 2 › DÂN DỤNG mã 03–32 (mỗi clip .MOV = 1 video, hàng SOPOKA: ổ cắm, phích, cầu dao,
  bóng, đui, chao đèn…); 90–135 từ TỤ (kẹo CBB22, bếp từ MKP-X2, khởi động, nhôm EUN SUNG, máy bơm), VẬT LIỆU (giấy
  cách điện, băng keo vàng/Nano, sò nhiệt KSD301, gen sợi thủy tinh), dây nguồn, ru lô, HỘP NHỰA › CNC (VY ANH 170x95x70),
  ống gen (thư mục cũ "Gen Amiang"). Bỏ: "Dây bus 3 pin lớn.mp4", "Cầu chì Aotu 20A.mp4" (quảng cáo dựng sẵn), IMG_7647
  (trùng 7646). "Câu chi aotu 15A.mp4" thực ra là cầu chì KUOYUH 5A.
- Cách làm đợt lớn: mỗi nhóm clip giao 1 subagent viết mẫu theo `tools/lenh/huong-dan-mau.md`, phiên chính dựng
  tuần tự (máy 4 nhân, ~5–8 phút/video). Video có người nói thật mà nói "amiang" thì cắt đúng chữ đó bằng `--bo`
  (lấy mốc bằng Whisper word_timestamps); phụ đề lời thật có "chống cháy/không cháy" thì bỏ dòng đó (không sửa lời).
- 01/11 đợt 3 (anh chọn "clip còn lại + ảnh" vì clip thô đã gần hết): **video 136–188** (lệnh `tools/lenh/dung-136-188.sh`):
  10 từ clip còn lại (`tools/lenh/p3-list.txt`) + 43 video ghép ảnh (`video/tho/anh/`, cách làm `tools/lenh/huong-dan-anh.md`,
  Drive id ảnh theo thư mục `tools/lenh/anh-ids/`). Ảnh AI (Gemini/ChatGPT), banner nhiều chữ, ảnh shop khác: bỏ. Tụ khởi động,
  gen co nhiệt, giấy cách điện, tụ bếp từ/kẹo: gần như không có ảnh thật. Bỏ "h-vy-anh.mov" (video nội bộ có thông tin khách).
  Clip/ảnh thô Drive coi như ĐÃ DÙNG HẾT: đợt sau cần anh quay thêm.
- **Phụ đề phải hiện chữ chuẩn** (SOPOKA, 3000W, 15A, 250V, 1µF), cách đọc ("Sô pô ca", "ba nghìn oát") chỉ để ở vế sau `|`.
  Dòng lời đọc không có `|` thì phụ đề hiện y lời đọc: 01/11 phải dựng lại 17 video vì lỗi này. Rà trước khi dựng:
  `grep -n "^[^|#]*\(oát\|am pe\|vôn\|Sô pô\|Uan chi\|micro\)" video/mau/*.loi.txt | grep -v mo-dau`.
- Ảnh có chữ in sẵn ở phần dưới (vd "2 CON") thì nâng phụ đề: thêm `--phu-de-cao 430`.
- Lưu lệnh dựng mỗi đợt thành script trong `tools/lenh/` để phiên sau chạy lại được.
- Câu kết dạng `@giây | lời`: chỉ MỘT dấu `|` (viết 2 dấu thì trước đây máy đọc câu kết 2 lần; nay
  `giong_doc.py` chỉ đọc vế cuối).
- Video ngang 720p: dùng khung nền mờ (không `--day-khung`, vì cắt đầy sẽ mờ hình); chữ nổi bật đặt
  trên, phụ đề dưới phần video.
- Video không có mô tả: lời đọc/chữ **chỉ nói điều thấy trong video hoặc người trong video nói**; số đo
  đọc không rõ thì không ghi số. Video đã edit sẵn có lời đọc gốc của shop: lấy thông tin từ lời đó.
  Mỗi video có `video/mau/<sp>-mo-dau.{ass,loi.txt}`; lệnh dựng xem commit "Làm lại 3 video".
- **Thư mục video + ảnh thô thứ 2** (anh gửi 01/11): Drive folder `1QJFZkPZ3CNZeW3pEtAn0IhuPWe4c6Wfs`
  (link https://drive.google.com/drive/folders/1QJFZkPZ3CNZeW3pEtAn0IhuPWe4c6Wfs), chia theo nhóm hàng:
  - `ĐÓNG CẮT & KẾT NỐI` `1v4cMxYI-gvAqRUX6ifgk7ylXAsQKFW4j` (thư mục con: Cò Bóp, Dây Bus…)
  - `VẬT LIỆU CÁCH ĐIỆN & CHỊU NHIỆT` `1mtZGURWDcG860jc5c9BpiD5suQG3wK6h` (con: Giấy Cách Điện…)
  - `THIẾT BỊ & PHỤ KIỆN ĐIỆN DÂN DỤNG` `1I1VpE953j0pfN0I7fe7ZuuIs4hATKBmu`: ~100 file đánh số 01–32 (số = mã
    sản phẩm), mỗi số có .MOV gốc + .mp4 nhẹ + ảnh JPG. Dùng bản .MOV gốc. Số 02 = ổ cắm SOPOKA 6000W (đã làm).
  - `HỘP NHỰA` `1oGE3oLlNjd3tHldxAO6sfROPNcosmqEp` (con: WANCHI…)
  - `CÁC LOẠI TỤ` `1YIldSPTEOxbN2NkaWeiusGdObifL5-vQ`
  Liệt kê bằng Drive connector (`parentId = '<id>'`, kết quả dài thì đọc file JSON bằng python).
- **Thư mục video chính để "làm dần"**: `MAKETING/AFFILIATE HÀNG TOP/VIDEO THÔ` (đổi tên từ "VIDEO Tiep thi" 31/10; đã chia sẻ).
  Danh sách + mã Drive + trạng thái: `video/danh-sach-tiep-thi.md`. Làm xong video nào thì
  đánh dấu ✅ ở đó. Video quay ngang 4K: dùng `--day-khung` (cắt đầy khung dọc).
- **Cắt dư thừa nhưng KHÔNG mất đoạn quan trọng**: chỉ cắt câu nói thừa, "ờ, à", đoạn đầu/cuối chết,
  outro "Follow"/"bấm theo dõi kênh" (thay bằng khung kết nhẹ nhàng). **Không cắt, không tua** đoạn
  đang có hành động dù im lặng (đo, chờ đồng hồ, nạp, xả tụ, thao tác tay). ĐÃ BỊ CHÊ: `--cat-ngap` +
  `--tua` trên video tụ làm mất đoạn đo/xả. Chỉ dùng `--cat-ngap` khi video là người nói liên tục
  (không thao tác), và xem lại danh sách đoạn cắt nó in ra trước khi dựng. Không chắc thì giữ.
- **Luôn bật `--studio`**: ánh sáng sáng mịn kiểu studio (khử nhiễu, sáng, tương phản, ấm nhẹ, nét).
- Video có người nói + câu kết bằng giọng đọc: dùng cả `--srt` (phụ đề lời thật) và `--giong` (file chỉ
  có dòng `@giây | câu kết`); giọng thật giữ nguyên âm lượng. Mẫu `video/mau/tu-60uf-ket.loi.txt`.
- Video tụ (bản hiện tại): dựng thẳng từ `video3.mov` với `--goc --bo "0-1.6,70.6-79.95"` (chỉ bỏ câu
  thừa đầu + outro), dùng các file theo giờ gốc `video/mau/tu-60uf-goc.{srt,ass}`, `tu-60uf-ket-goc.loi.txt`
  (lệnh đầy đủ trong commit "Giọng tự nhiên").
- Whisper hay "bịa" câu "subscribe cho kênh…" khi video không có lời: coi như không có lời nói.
- Mẹo cho anh: chia sẻ cả thư mục VIDEO "Bất kỳ ai có đường liên kết" một lần là mọi file
  trong đó tải được.
- **Video có người nói thật** (review, đo thử): giữ giọng thật, không chèn giọng đọc máy.
  Cách làm (mẫu `video/mau/tu-60uf.*`, video tụ 60uF Drive id `1q0GcPUEDSoqlOPzqQiPHntoJ5U4T8WqU`):
  1. `--bo` bỏ tiếng thừa, `--tua` tua nhanh đoạn chờ (vd chờ đồng hồ đo), `--chi-dung` để
     xem bản dựng.
  2. Whisper (`medium`) lấy thời điểm câu nói, **sửa tay** chữ nghe sai vào file `.srt`
     (60 OF → 60µF, tụ nhôn → tụ nhôm). Không thêm lời người nói không nói.
  3. File `.ass` chỉ có chữ nổi bật phía trên (tiêu đề, thông số, kết quả đo, CTA trước outro).
  4. Video của anh thường đã có logo QUYNDIEN trên tường và outro "Follow" ở cuối: không cần
     hộp tên shop.
- **Đổi nền (tách nền AI)**: đã thử `rembg` trên video cầm tay, kết quả hỏng (mất tay, sản
  phẩm thành bóng mờ). Không làm; khuyên anh quay tại bàn thợ thật.
- **Hiệu ứng** (anh thích có): `--mo-dau file.ass` đoạn mở đầu "tình huống" 3.5s trước
  video (khung đầu làm mờ + câu hỏi triệu chứng + chốt "CÓ THỂ DO …", mẫu
  `video/mau/tu-60uf-mo-dau.ass`; tiếng vút/pop đã khớp mốc 0 / 0.7 / 1.4 / 2.2s);
  `--zoom "a-bxZ@cx,cy"` phóng to mượt (dùng zoompan; tìm tâm bằng khung hình có lưới,
  đừng zoom đoạn video gốc đã quay cận); `--chop t` chớp sáng; `--sfx "t:whoosh|ding|pop"`.
  Thường: pop khi hộp chữ hiện, ding + chớp khi ra kết quả đo, whoosh lúc mở/CTA.
  Lệnh mẫu video tụ: xem lịch sử commit "hiệu ứng" hoặc dùng lại các mốc trong `tu-60uf.ass`.
- **Mở đầu (hook) phải "cuốn"** (anh chê kiểu ảnh tĩnh làm mờ là chưa cuốn). Mặc định dùng:
  `--mo-dau-canh t1,t2,t3,t4` (4 cảnh thật đẹp nhất cắt nhanh, zoom giật mỗi cảnh) +
  `--mo-dau-giong hook.loi.txt` (giọng đọc ngay giây đầu, 2 câu ngắn: nỗi lo → giải pháp, tổng
  ≤ ~5.5s) + file `.ass` chữ to: câu nỗi lo chữ trắng hộp đỏ, con số chốt chữ vàng rất to.
  Mẫu: `video/mau/ong-gen-mo-dau.*`. Không nói quá thông số (ghi "chịu tới 600°C", không ghi
  "không cháy").
- **Kết thúc kêu gọi nhẹ nhàng, tinh tế** (anh không thích hộp to "ĐẶT HÀNG NGAY!"): nền tối mờ
  dần, tên shop "Linh Kiện Quỳnh Diễn" mờ dần trượt nhẹ lên, gạch xanh mảnh, một dòng phụ nhỏ
  về sản phẩm; giọng đọc kiểu "Cần …, anh em ghé Linh Kiện Quỳnh Diễn nhé." (dòng lời đọc
  dạng `@giây | lời` = chỉ đọc, không hiện phụ đề). Mẫu: cuối `video/mau/ong-gen-giong.ass`.
- **Video từ ảnh** (mẫu hộp nhựa WANCHI KW-CN-170, `video/mau/hop-wanchi-170*`): ảnh anh gửi trong
  chat được lưu ở thư mục `images/` của phiên (đường dẫn hiện trong tin nhắn) → copy vào
  `video/tho/<sp>/`, sắp thứ tự khớp lời đọc → `tools/anh_video.py --giay <lời đọc/số ảnh + 0.5>`
  → `edit.py` như video thường (mở đầu `--mo-dau-canh` lấy giữa mỗi ảnh, tránh lúc chuyển cảnh).
  Ảnh vuông thì chữ nổi bật đặt trên ảnh, phụ đề dưới ảnh.
- Cách đọc thương hiệu: **WANCHI = "Wan-chi"**; trong lời đọc viết `Uan chi` (viết "Wan chi" máy đọc
  thành "Quang chi"). Kiểm tra cách đọc lạ: tạo vài cách viết, cho Whisper nghe lại, chọn cái đúng.
- **Tình huống minh họa bằng hình thật** (máy bơm, máy lạnh hỏng…): em không tự tạo được
  video thật. Cần anh quay thêm clip 3–5s ở xưởng, hoặc mở mạng tới kho video miễn phí.
- **Nhạc nền** (luôn ghép): anh bỏ file nhạc (miễn bản quyền) vào Drive `MAKETING/AFFILIATE HÀNG TOP/NHẠC NỀN (Claude)`
  (folder id `1ZKZViats-94aZGUR2FLOmVSgqL2d7RxW`; cần chia sẻ "Bất kỳ ai có đường liên kết").
  Đã chia sẻ (31/10), 13 bài Pixabay. Tải bằng curl vào `video/assets/nhac/` (không đưa lên git).
  `--nhac file --nhac-am-luong X`: nhạc ghép ở bước cuối cho **cả video kể cả mở đầu**, tự nhỏ khi có
  giọng (sidechain ducking). Ghép nhạc cho video đã dựng: `add_music()` trong `edit.py`.
  Âm lượng: đo `mean_volume` của bài (volumedetect 60s đầu), X = 10^((đích − mean)/20), đích −30 dB
  (video giọng đọc) / −33 dB (video người nói thật).
  Đã chọn: 01 Fe silic = vlog-beat, 02 Ổ cắm = pop-rock-quang-cao, 03 Tụ = promotion,
  04 Ống gen = running-night, 05 Hộp WANCHI = moodmode. Bài có trong thư mục (id Drive):
  vlog-beat `1tdjFEXZYxx_ytFzU6VXiT7YvBU5NMsbd`, pop-rock-commercial `1O8CveRqADT48_J-jLdtI_8HQkvCfE6Uh`,
  music-promotion `1kszHdV-8UeE8VQShN-444c80hgQVImwC`, moodmode `1HX5ANIwxm3iQs1GW3juAFZ2MYs8bNixF`,
  running-night `171R-OO--RY-vJ4fFWFvn8H3QXYWITPpI`, inspiring-acoustic `1st6Tv1u5j7qtszhSVI_-etteW2LKSN1f`,
  cinematic-trailer-intro `16ysWCevhU0tbwfeL10Xi674cm09YTnxI`, cinematic `1sUFXWGWFsK0FB0abDvnVBk-vCjNTuav2`,
  perfect-beauty `1n8JmbNnNFqbbDKuJ5P-PH3OT124M7arg`, moment-of-peace `1xuyFMbaw01eLY_xCH9W-ks4TcOL6kLj_`,
  latin-salsa `18qkxq83uJBeAk3qQjwhcdYTy5abObHgP`, halloween-spooky (không hợp) `1Bcbt2azcDct-sp9HA2mPao2LAAymIHks`.
- Kiểm tra giọng đọc: chạy Whisper nghe lại video (dùng `load_audio` trong `edit.py`).
