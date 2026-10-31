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
- Giọng mặc định: **vi-VN-HoaiMyNeural** (nữ), **tốc độ `+25%`, cao giọng `+4Hz`**
  (anh chê tốc độ thường "nghe buồn ngủ"; đây là mặc định trong `edit.py`).
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
  Mỗi video có `video/mau/<sp>-mo-dau.{ass,loi.txt}`; lệnh dựng xem commit "Làm lại 3 video".
- **Thư mục video chính để "làm dần"**: `MAKETING/AFFILIATE HÀNG TOP/VIDEO Tiep thi` (đã chia sẻ).
  Danh sách + mã Drive + trạng thái: `video/danh-sach-tiep-thi.md`. Làm xong video nào thì
  đánh dấu ✅ ở đó. Video quay ngang 4K: dùng `--day-khung` (cắt đầy khung dọc).
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
- **Nhạc nền**: anh bỏ file nhạc (miễn bản quyền) vào Drive `MAKETING/AFFILIATE HÀNG TOP/NHẠC NỀN (Claude)`
  (folder id `1ZKZViats-94aZGUR2FLOmVSgqL2d7RxW`; cần chia sẻ "Bất kỳ ai có đường liên kết").
  Em liệt kê bằng Drive connector (`parentId = '<id>'`), tải bằng curl vào `video/assets/nhac/`
  (không đưa nhạc lên git). Dùng `--nhac file --nhac-am-luong 0.12`; video có giọng đọc/người nói
  để nhạc nhỏ (0.08–0.12) cho không lấn giọng.
- Kiểm tra giọng đọc: chạy Whisper nghe lại video (dùng `load_audio` trong `edit.py`).
