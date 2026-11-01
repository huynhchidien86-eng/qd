"""Tạo nhanh file chữ (.ass) theo phong cách đã chốt: chữ nổi bật, mở đầu "cuốn", khung kết nhẹ nhàng.

Dùng trong Python:
    import sys; sys.path.insert(0, "tools")
    from tao_mau import chu_chinh, chu_mo_dau, phu_de
    chu_chinh("video/mau/abc.ass", "ghi chú", (0.3, 4.5, "TIÊU ĐỀ\\NDÒNG 2"),
              [(5, 8, "Ý chính ✔"), ...], ket=30.0, dong_phu="Tên sản phẩm", hop_ten_shop=29.8)
    chu_mo_dau("video/mau/abc-mo-dau.ass", "ghi chú", "NỖI LO?", "HẬU QUẢ!", "CHỮ NHỎ", "SỐ CHỐT",
               co_chu=150, t1=1.3, t2=2.8, het=5.8)
    phu_de("video/mau/abc.srt", [(1.1, 2.9, "Câu nói"), ...])

Mốc thời gian tính theo video gốc (dùng với `edit.py --goc`). Kiểu chữ lấy từ mẫu ống gen.
"""
import re
from pathlib import Path

MAU = Path(__file__).resolve().parent.parent / "video" / "mau"
EV = "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
VANG = r"\N{\c&H0000D7FF&}"  # xuống dòng + chữ vàng
NAY = r"{\fad(200,250)\t(0,200,\fscx110\fscy110)\t(200,380,\fscx100\fscy100)}"
GIAT = r"{\pos(540,820)\t(0,120,\fscx118\fscy118)\t(120,260,\fscx100\fscy100)}"


def _t(t):
    h, r = divmod(max(t, 0), 3600)
    m, s = divmod(r, 60)
    return f"{int(h)}:{int(m):02}:{s:05.2f}"


def _dau(file, ghi_chu):
    head = (MAU / file).read_text(encoding="utf-8").split("[Events]")[0]
    return re.sub(r"^\[Script Info\]\n(;[^\n]*\n)+", f"[Script Info]\n; {ghi_chu}\n", head, flags=re.M)


def chu_chinh(dst, ghi_chu, tieu_de, y_chinh, ket, dong_phu, hop_ten_shop=None):
    """Tiêu đề vàng + các hộp ý chính xanh lá phía trên + khung kết nhẹ nhàng từ giây `ket`."""
    s = _dau("ong-gen-giong.ass", ghi_chu) + EV
    if hop_ten_shop:
        s += f"Dialogue: 0,{_t(0)},{_t(hop_ten_shop)},Brand,,0,0,0,,LINH KIỆN QUỲNH DIỄN\n"
    a, b, txt = tieu_de
    s += (f"Dialogue: 1,{_t(a)},{_t(b)},Title,,0,0,0,,"
          rf"{{\fad(300,200)\t(0,300,\fscx110\fscy110)\t(300,500,\fscx100\fscy100)}}{txt}" "\n")
    for a, b, txt in y_chinh:
        s += f"Dialogue: 1,{_t(a)},{_t(b)},Point,,0,0,0,,{NAY}{txt}\n"
    het = ket + 8
    s += (f"Dialogue: 1,{_t(ket - 0.2)},{_t(het)},Line,,0,0,0,,"
          r"{\an7\pos(0,0)\c&H000000&\1a&HFF&\t(0,700,\1a&H70&)\p1}m 0 0 l 1080 0 l 1080 1920 l 0 1920{\p0}" "\n")
    s += (f"Dialogue: 2,{_t(ket)},{_t(het)},Soft,,0,0,0,,"
          r"{\an5\fad(700,300)\move(540,1430,540,1395,0,700)}Linh Kiện Quỳnh Diễn" "\n")
    s += (f"Dialogue: 2,{_t(ket + 0.3)},{_t(het)},Line,,0,0,0,,"
          r"{\an5\pos(540,1462)\fad(600,300)\fscx0\t(0,700,\fscx100)\p1}m 0 0 l 360 0 l 360 5 l 0 5{\p0}" "\n")
    s += (f"Dialogue: 2,{_t(ket + 0.6)},{_t(het)},Soft2,,0,0,0,,"
          rf"{{\an5\fad(700,300)\move(540,1525,540,1500,0,700)}}{dong_phu}" "\n")
    Path(dst).write_text(s, encoding="utf-8")


def chu_mo_dau(dst, ghi_chu, noi_lo_1, noi_lo_2, chu_nho, so_chot, co_chu, t1, t2, het):
    """Mở đầu: 2 câu nỗi lo (hộp đỏ) đổi lúc t1, chữ chốt vàng rất to từ t2 đến het."""
    head = _dau("ong-gen-mo-dau.ass", ghi_chu).replace("Style: Big,DejaVu Sans,150,", f"Style: Big,DejaVu Sans,{co_chu},")
    s = head + EV
    s += f"Dialogue: 1,{_t(0)},{_t(t1)},Pain,,0,0,0,,{GIAT}{noi_lo_1}\n"
    s += f"Dialogue: 1,{_t(t1)},{_t(t2 - 0.05)},Pain,,0,0,0,,{GIAT}{noi_lo_2}\n"
    s += f"Dialogue: 2,{_t(t2 - 0.05)},{_t(het)},Small,,0,0,0,,{{\\pos(540,700)\\fad(100,0)}}{chu_nho}\n"
    s += (f"Dialogue: 2,{_t(t2)},{_t(het)},Big,,0,0,0,,"
          rf"{{\pos(540,860)\t(0,150,\fscx130\fscy130)\t(150,350,\fscx100\fscy100)}}{so_chot}" "\n")
    Path(dst).write_text(s, encoding="utf-8")


def phu_de(dst, dong):
    """File .srt từ [(bắt đầu, kết thúc, chữ)], mỗi dòng giữ thêm 0.25s."""
    def t(x):
        ms = int(round(x * 1000))
        h, ms = divmod(ms, 3600000)
        m, ms = divmod(ms, 60000)
        s, ms = divmod(ms, 1000)
        return f"{h:02}:{m:02}:{s:02},{ms:03}"
    Path(dst).write_text("\n".join(f"{i}\n{t(a)} --> {t(b + 0.25)}\n{x}\n" for i, (a, b, x) in enumerate(dong, 1)),
                         encoding="utf-8")
