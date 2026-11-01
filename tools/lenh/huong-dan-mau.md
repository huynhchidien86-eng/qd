# Viết mẫu chữ + lời đọc cho video sản phẩm (repo /home/user/qd)

Bối cảnh: shop linh kiện điện "Linh Kiện Quỳnh Diễn" làm video bán hàng dọc 9:16 từ clip thô.
Công cụ dựng là `tools/edit.py`. Em (agent) KHÔNG dựng video (máy yếu, việc dựng do phiên chính
làm). Việc của em: xem clip, viết 4 file mẫu cho mỗi clip, và trả về 1 dòng lệnh dựng.

ĐỌC TRƯỚC: `/home/user/qd/CLAUDE.md` (luật của chủ shop: phong cách, giọng đọc, cách viết số,
"không nói quá", kết nhẹ nhàng…). Mẫu tham khảo đã làm đạt:
- `video/mau/kep-ac-quy-75a.{ass,loi.txt}`, `video/mau/kep-ac-quy-75a-mo-dau.{ass,loi.txt}`
- `video/mau/phich-cam-p3000w*` ; công cụ tạo file: `tools/tao_mau.py` (chu_chinh, chu_mo_dau)
- Lệnh dựng đợt trước: `tools/lenh/dung-26-35.sh` (hàm `v`).

## Dữ liệu vào
- Clip thô: `/home/user/qd/video/tho/dd/<file>` (MOV quay dọc, có thể 4K, KHÔNG có lời nói,
  chỉ là tay cầm xoay sản phẩm). Bản `.mp4` cùng mã là bản nén của MOV: bỏ qua.
- Lưới 12 khung đều nhau: `/tmp/pt/<file>.jpg` ; thời lượng + phiên âm: `/tmp/pt/<file>.txt`.
- Muốn đọc nhãn/thông số: trích khung lớn, vd
  `ffmpeg -v error -ss 12 -i <clip> -frames:v 1 -vf scale=720:-2 /tmp/<ten>/x.jpg` rồi xem ảnh
  (gộp 3 khung bằng hstack=3 cho đỡ tốn). Đặt file tạm trong thư mục `/tmp/<key>/` riêng.

## Với MỖI clip (mỗi clip = 1 video riêng)
1. Xem lưới + vài khung lớn, đọc nhãn: tên hàng, thương hiệu, công suất, dòng, số lỗ, kích thước…
   CHỈ ghi điều thấy rõ trên nhãn/trong hình. Không đọc rõ thì không ghi số. Không bịa công dụng
   ngoài nhãn (được nói điều hiển nhiên như "dây dài, cuộn gọn" nếu thấy).
   Nếu 2 clip cùng sản phẩm: vẫn làm 2 video nhưng đổi góc nói (hook, ý nhấn) cho khác nhau.
   Nếu clip gần như trùng hệt clip khác (cùng cảnh) hoặc không rõ là hàng gì: bỏ, ghi lý do.
2. Đặt `key` dạng kebab không dấu (vd `o-cam-sopoka-1200w-3lo`). Kiểm tra `ls video/mau/` để
   không trùng tên đã có.
3. Viết `video/mau/<key>.loi.txt`: ~1 câu mỗi 5–6 giây video, câu đầu ở 0.3s, các câu sau neo
   `@giây` khớp lúc cảnh đó hiện; dòng cuối `@ket | Cần …, anh em ghé Linh Kiện Quỳnh Diễn nhé.`
   (chỉ MỘT dấu `|`). Số/đơn vị/chữ Anh viết cách đọc ở vế sau `|` (2200W → "hai nghìn hai trăm
   oát", 10A → "mười am pe", 250V → "hai trăm năm mươi vôn", SOPOKA → "Sô pô ca", ABS → "a bê ét").
   `ket` = thời lượng clip − khoảng 4.5s (câu kết phải đọc xong trước khi clip hết ít nhất 0.5s).
4. Đo độ dài giọng thật (bắt buộc), chạy từ /home/user/qd:
   `python3 -c "import sys;sys.path.insert(0,'tools');from giong_doc import make_voice;make_voice('video/mau/<key>.loi.txt','/tmp/<key>','edge','vi-VN-HoaiMyNeural','+30%')"`
   (tạo thư mục /tmp/<key> trước). Nó in mốc từng câu: câu không được chồng/đẩy lố câu sau quá
   nhiều, và câu kết phải xong trước cuối clip. Sửa đến khi khớp.
5. `video/mau/<key>.ass` bằng `chu_chinh(dst, ghi_chu, (0.3, 4.5, "TIÊU ĐỀ\\NDÒNG 2"),
   [(a,b,"Ý chính ✔"), ...], ket=<ket>, dong_phu="<tên ngắn sp>", hop_ten_shop=<ket-0.2>)`.
   Tiêu đề ≤ 14 ký tự mỗi dòng, ý chính ≤ 24 ký tự (dùng `·` để nối 2 ý, `VANG` để xuống dòng
   chữ vàng). Các ý chính khớp thời gian với câu đọc tương ứng. Không emoji (dùng ✔ ►).
   Nếu clip có chữ sẵn ở phần trên khung hình, ghi chú lại (phiên chính sẽ dời chữ xuống).
6. Hook: `video/mau/<key>-mo-dau.loi.txt` 2 dòng ngắn (nỗi lo? → giải pháp!), tổng ≤ 5.5s khi đọc
   (đo bằng make_voice như trên). `video/mau/<key>-mo-dau.ass` bằng
   `chu_mo_dau(dst, ghi_chu, "NỖI LO 1?", "NỖI LO 2?", "CHỮ NHỎ", "SỐ/TÊN CHỐT", co_chu=150, t1, t2, het)`
   với t1 ≈ giữa câu 1, t2 = lúc câu 2 bắt đầu, het = lúc giọng hook hết + 0.3. Chữ chốt ≤ 8 ký tự
   thì co_chu 150–170, dài hơn thì giảm (120–130) để không tràn 1080px.
7. Chọn 4 mốc cảnh đẹp nhất cho hook (`canh`, giây trong clip gốc, cách nhau, tránh lúc mờ/rung)
   và mốc sfx: `"0.3:whoosh,<lúc mỗi ý chính hiện>:pop,..."`.
8. Nhạc (tên file + âm lượng cố định): pop-rock-quang-cao.mp3 0.148 | running-night.mp3 0.097 |
   promotion.mp3 0.098 | moodmode.mp3 0.153 | vlog-beat.mp3 0.09 | inspiring-acoustic.mp3 0.112.
   Đổi bài giữa các video kề nhau.

## Trả về (tin nhắn cuối, ngắn gọn)
Mỗi clip một dòng đúng định dạng (TÊN là tên file đầu ra không dấu, ngắn):
`v dd/<file> <key> <canh> "<sfx>" <nhac.mp3> <vol> "TÊN - giong doc.mp4"`
Ví dụ: `v dd/03_1iZxHs.mov o-cam-sopoka-1200w 1,8,15,22 "0.3:whoosh,6:pop,12:pop" vlog-beat.mp3 0.09 "O cam SOPOKA 1200W 3 lo - giong doc.mp4"`
Kèm: clip bỏ qua + lý do; ghi chú chữ sẵn trên clip; điều chưa chắc.
Không commit git.

## BỔ SUNG (đợt 2: clip trong /home/user/qd/video/tho/p2/)
- Clip đợt 2 có thể có NGƯỜI NÓI THẬT (review, giới thiệu). Kiểm tra bằng Whisper (medium hoặc small):
  `python3 -c "import sys;sys.path.insert(0,'tools');from edit import load_audio;from faster_whisper import WhisperModel as W;m=W('small',device='cpu',compute_type='int8');[print(f'{s.start:.1f}-{s.end:.1f} {s.text}') for s in m.transcribe(load_audio('CLIP'),language='vi',vad_filter=True,word_timestamps=False)[0]]"`
  Whisper hay bịa "subscribe cho kênh…" khi không có lời: coi như không có lời.
- Clip KHÔNG có lời nói: làm như trên (dòng `v`).
- Clip CÓ người nói thật (đọc CLAUDE.md mục "Video có người nói thật"): giữ giọng thật, không đọc
  máy chồng lên. Làm 5 file: `<key>.srt` (phụ đề lời thật, theo giờ gốc, sửa tay chữ nghe sai,
  không thêm lời người không nói; dùng `tao_mau.phu_de`), `<key>.ass` (chỉ chữ nổi bật phía trên:
  tiêu đề, thông số chính + khung kết từ `ket`, dùng chu_chinh), `<key>-ket.loi.txt` (CHỈ một dòng
  `@ket | Cần …, anh em ghé Linh Kiện Quỳnh Diễn nhé.`, ket = lúc người nói xong hẳn/ sau đoạn
  outro bị bỏ), hook như cũ. Nếu đầu clip có câu thừa/ chết, cuối có outro "Follow/ theo dõi kênh"
  thì bỏ bằng `--bo a-b,c-d` (giây gốc). KHÔNG cắt đoạn đang thao tác/đo. Nhạc: nhân âm lượng ×0.7.
  Dòng trả về dạng: `s p2/<file> <key> <canh> "<sfx>" <nhac> <vol> "TÊN - review.mp4" <extra>`
- Cột cuối `<extra>` (cho cả `v` và `s`, có thể bỏ trống): cờ thêm KHÔNG chứa dấu cách hay dấu nháy
  trong giá trị, ví dụ `--bo 0-1.6,70.6-79.95` hoặc `--day-khung`. Clip quay NGANG: nếu 4K/1080p mà
  sản phẩm ở giữa thì thêm `--day-khung` (cắt đầy khung dọc); 720p trở xuống thì không (nền mờ).
- Ống gen sợi thủy tinh: TUYỆT ĐỐI không dùng chữ/lời "amiang" (kể cả khi người trong clip nói
  "amiang": phụ đề ghi "ống gen sợi thủy tinh"... nhưng không được sửa lời thành ý khác; nếu người
  nói "amiang" thì phụ đề ghi "gen sợi thủy tinh" là chấp nhận được vì cùng sản phẩm). Đã có mẫu
  `video/mau/ong-gen*` từ video IMG_7648: xem để không lặp y hệt. Ghi "chịu tới 600°C", không ghi
  "không cháy".
- File to (4K, hàng trăm MB): trích khung bằng `-ss` trước `-i` cho nhanh; đừng chạy Whisper medium
  trên clip > 3 phút (dùng small).
