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
  (công dụng, đặc điểm, size, cam kết) trong hộp đen mờ ở dưới; cuối video hộp xanh
  lá "LINH KIỆN QUỲNH DIỄN ► ĐẶT HÀNG NGAY!".
- Nội dung chữ lấy từ mô tả sản phẩm anh gửi, viết ngắn gọn từng ý.
- Video sản phẩm thường không có lời nói, nên không dùng `--cat-lang`.
- Anh muốn có **giọng đọc kèm phụ đề**. Lời đọc viết từ mô tả sản phẩm, ~7 câu cho
  video 30s, dòng cuối "Linh Kiện Quỳnh Diễn. Đặt hàng ngay!". Số, đơn vị, từ tiếng Anh
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
- Giọng mặc định: **vi-VN-HoaiMyNeural** (nữ). Lời đọc phải vừa độ dài video; nếu dài
  hơn thì tăng `--toc-do` (Fe silic 32s dùng `+12%`), đừng để giữ khung cuối quá lâu.
- Kiểm tra giọng đọc: chạy Whisper nghe lại video (dùng `load_audio` trong `edit.py`).
