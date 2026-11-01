# Video từ ẢNH sản phẩm (đợt 3) — đọc thêm /tmp/brief.md (luật chung, cách đo giọng, định dạng dòng `v`)

Danh sách ảnh theo thư mục Drive: `/tmp/anh/<Nhóm>.txt` (mỗi dòng: `<drive id>\t<tên file>`).
1. Tải ảnh nhóm của em vào `/home/user/qd/video/tho/anh/<Nhóm>/` (tạo thư mục):
   `curl -sSL -o "<thư mục>/<tên an toàn>" "https://drive.usercontent.google.com/download?id=<ID>&export=download&confirm=t"`
   Bỏ file .HEIC/.PNG bảng giá; kiểm tra file tải về đúng là ảnh (`file x.jpg`), nếu là HTML (chưa chia sẻ) thì ghi lại, bỏ qua.
2. Xem ảnh bằng tờ ghép: `ffmpeg -v error -i "<thư mục>/%*.jpg"` khó dùng; nên dùng python + PIL hoặc ffmpeg từng ảnh
   `-vf scale=200:-2` rồi `tile`. Ảnh xem nhỏ, đọc nhãn thì mở ảnh lớn riêng.
3. CHỈ dùng ảnh chụp thật sản phẩm. BỎ: ảnh AI ("Gemini_Generated", "ChatGPT Image"), ảnh quảng cáo đã chèn nhiều chữ
   / bảng giá / ảnh của shop khác (logo lạ), ảnh mờ. Ảnh có ít chữ của chính shop (QUYNDIEN) dùng được nếu đẹp.
4. Chia ảnh thành video: mỗi video 1 sản phẩm/ 1 mẫu (hoặc 1 nhóm "đủ loại"), 4–7 ảnh khác nhau, không dùng lại cùng
   ảnh ở 2 video. Số video: theo lượng ảnh tốt, mỗi video phải có góc nói riêng (mẫu/ dòng/ trị số khác nhau).
5. Dựng phần hình: `cd /home/user/qd && python3 tools/anh_video.py <ảnh theo thứ tự lời đọc> -o video/tho/anh/<key>.mp4 --giay <G>`
   G = 4.5–5.5 (tổng ≈ 25–35s). Ảnh vuông/ngang thì chữ nổi bật đặt trên, phụ đề dưới (anh_video tự để nền mờ).
   Xem mẫu đã làm: `video/mau/hop-wanchi-170*` (CLAUDE.md mục "Video từ ảnh").
6. Viết 4 file mẫu như brief (lời đọc chỉ nói điều thấy trên nhãn/ảnh hoặc tên thư mục/tên file ảnh ghi rõ, vd
   "Tụ Đề Kapa Tinh Chi 100..." → hiệu Tinh Chi). Mốc `@giây` khớp lúc ảnh tương ứng hiện (ảnh i bắt đầu ≈ i*(G-0.5)).
   Hook `canh`: lấy giữa mỗi ảnh (tránh lúc chuyển cảnh). Đo giọng bằng make_voice như brief.
7. Trả về dòng: `v anh/<key>.mp4 <key> <canh> "<sfx>" <nhac> <vol> "TÊN - anh.mp4"`
Không commit git, không dựng bằng edit.py.
