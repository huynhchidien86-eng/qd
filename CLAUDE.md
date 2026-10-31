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
- Stack: FFmpeg, Python 3, `auto-editor` (cắt khoảng lặng), `faster-whisper` (phụ đề).
- Cấu trúc thư mục:
  - `tools/edit.py`: script edit chính (xem `python3 tools/edit.py -h`).
  - `tools/setup.sh`: cài công cụ (chạy đầu mỗi phiên cloud).
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
bash tools/setup.sh                       # cài công cụ (đầu mỗi phiên)
python3 tools/edit.py video/tho/abc.mp4 \
  --cat-lang --phu-de --khung 9:16 \
  --nhac video/assets/nhac.mp3 --logo video/assets/logo.png \
  --tieu-de "Tiêu đề" --mo-dau-ket-thuc --chuan-am
```

Tùy chọn chính: `--tu/--den` (cắt đầu/cuối), `--cat-lang` (bỏ khoảng lặng,
chỉnh bằng `--nguong-lang`, `--le`), `--phu-de` hoặc `--srt file.srt`,
`--khung 9:16|16:9|1:1|4:5`, `--nhac`, `--logo`, `--tieu-de`, `--chuan-am`.

## Quy trình edit video

Khi anh bảo "lấy video thô edit":
1. Chạy `bash tools/setup.sh`.
2. Lấy video thô về `video/tho/` (anh đính kèm file trong chat, hoặc link tải trực tiếp).
3. Chạy `tools/edit.py` theo "phong cách mặc định" bên dưới, trừ khi anh dặn khác.
4. Trích vài khung hình kiểm tra phụ đề/tiêu đề trước khi giao.
5. Gửi file trong `video/xong/` cho anh.

Phong cách mặc định của anh: _chưa chốt — sẽ ghi sau khi edit thử video đầu tiên._

## Ghi nhớ khác

<!-- Bất cứ điều gì anh muốn em nhớ qua các phiên: sở thích, việc cần tránh, ngữ cảnh riêng. -->

- Mạng của môi trường cloud đang **chặn `huggingface.co`**, nên `--phu-de` (tải model
  Whisper) chưa chạy được. Cần thêm `huggingface.co` vào Allowed domains trong cài đặt
  Network access của môi trường. Tạm thời dùng `--srt` với file phụ đề có sẵn.
- Google Drive connector tải file dạng base64 qua hội thoại, chỉ hợp với file nhỏ
  (vài MB). Video lớn nên gửi bằng cách khác.
