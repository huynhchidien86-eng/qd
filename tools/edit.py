#!/usr/bin/env python3
"""Edit video tự động: cắt khoảng lặng, phụ đề, đổi khung, nhạc nền, logo, tiêu đề.

Ví dụ:
    python3 tools/edit.py video/tho/abc.mp4 --cat-lang --phu-de --khung 9:16 \
        --nhac video/assets/nhac.mp3 --logo video/assets/logo.png --tieu-de "Vlog Đà Lạt"

Kết quả mặc định nằm ở video/xong/<tên>_edit.mp4.
"""
import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FONT = "DejaVu Sans"
FONT_FILE = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
# Kích thước chuẩn cho các nền tảng phổ biến.
STANDARD_SIZES = {"9:16": (1080, 1920), "16:9": (1920, 1080), "1:1": (1080, 1080), "4:5": (1080, 1350)}


def run(cmd):
    print("$", " ".join(str(c) for c in cmd), flush=True)
    subprocess.run([str(c) for c in cmd], check=True)


def video_size(path):
    """Kích thước khung hình sau khi xoay (video iPhone quay dọc lưu kèm góc xoay)."""
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
         "stream=width,height:stream_side_data=rotation", "-of", "json", str(path)],
        capture_output=True, text=True, check=True).stdout
    st = json.loads(out)["streams"][0]
    w, h = st["width"], st["height"]
    rotation = next((int(d["rotation"]) for d in st.get("side_data_list", []) if "rotation" in d), 0)
    return (h, w) if abs(rotation) % 180 == 90 else (w, h)


def duration(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(path)], capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


def trim(src, dst, start, end):
    cmd = ["ffmpeg", "-y", "-v", "error"]
    if start:
        cmd += ["-ss", start]
    if end:
        cmd += ["-to", end]
    run(cmd + ["-i", src, "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
               "-c:a", "aac", "-b:a", "192k", dst])


def cut_silence(src, dst, threshold, margin):
    run(["auto-editor", src, "--edit", f"audio:threshold={threshold}",
         "--margin", margin, "--progress", "none", "--no-open", "-o", dst])


def srt_time(t):
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def transcribe(src, srt_path, model_name, lang):
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        sys.exit("Thiếu faster-whisper. Chạy: bash tools/setup.sh")
    print(f"Đang nhận dạng giọng nói (model {model_name})...", flush=True)
    model = WhisperModel(model_name, device="cpu", compute_type="int8")
    segments, _ = model.transcribe(str(src), language=lang, vad_filter=True)
    lines = []
    for i, seg in enumerate(segments, 1):
        lines.append(f"{i}\n{srt_time(seg.start)} --> {srt_time(seg.end)}\n{seg.text.strip()}\n")
    srt_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Phụ đề: {len(lines)} câu -> {srt_path}")


def frame_filter(ratio, w, h):
    """Đưa video về tỉ lệ khung mới: nền mờ phía sau, video gốc ở giữa."""
    if ratio in STANDARD_SIZES:
        out_w, out_h = STANDARD_SIZES[ratio]
    else:
        rw, rh = (int(x) for x in ratio.split(":"))
        # Giữ cạnh dài của video gốc làm chuẩn, làm tròn về số chẵn.
        long_side = max(w, h)
        if rw >= rh:
            out_w, out_h = long_side, int(long_side * rh / rw) // 2 * 2
        else:
            out_w, out_h = int(long_side * rw / rh) // 2 * 2, long_side
    return (f"split[a][b];"
            f"[a]scale={out_w}:{out_h}:force_original_aspect_ratio=increase,"
            f"crop={out_w}:{out_h},boxblur=20:5[bg];"
            f"[b]scale={out_w}:{out_h}:force_original_aspect_ratio=decrease[fg];"
            f"[bg][fg]overlay=(W-w)/2:(H-h)/2"), out_w, out_h


def escape_filter_path(p):
    return str(p).replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'")


def render(src, dst, args, srt, voice=None, voice_end=0.0):
    w, h = video_size(src)
    video_len = duration(src)
    # Giọng đọc dài hơn video thì giữ khung hình cuối cho đến hết lời.
    total = max(video_len, voice_end + 0.8) if voice else video_len
    inputs = ["-i", src]
    vchain = []
    out_w, out_h = w, h

    if total > video_len + 0.01:
        vchain.append(f"tpad=stop_mode=clone:stop_duration={total - video_len:.3f}")
        print(f"Giọng đọc dài hơn video: giữ khung cuối thêm {total - video_len:.1f}s")

    if args.khung:
        f, out_w, out_h = frame_filter(args.khung, w, h)
        vchain.append(f)
    if srt:
        # libass tính cỡ chữ theo khung chuẩn cao 288, không theo pixel thật.
        size = 11 if out_h > out_w else 18
        margin = args.phu_de_cao if args.phu_de_cao is not None else 24
        style = (f"FontName={FONT},FontSize={size},Bold=1,PrimaryColour=&H00FFFFFF,"
                 f"OutlineColour=&H00000000,BorderStyle=1,Outline=1.5,MarginV={margin}")
        vchain.append(f"subtitles='{escape_filter_path(srt)}':force_style='{style}'")
    if args.chu:
        # File ASS tự định kiểu chữ, vị trí, thời gian nên không ép style.
        vchain.append(f"subtitles='{escape_filter_path(args.chu)}'")
    if args.tieu_de:
        # Cỡ chữ vừa chiều ngang khung (ký tự rộng khoảng 0.65 cỡ chữ).
        fontsize = min(out_h // 14, int(out_w * 0.9 / (0.65 * max(len(args.tieu_de), 1))))
        text = args.tieu_de.replace("\\", "\\\\").replace("'", "’").replace(":", "\\:")
        vchain.append(
            f"drawtext=fontfile={FONT_FILE}:text='{text}':fontsize={fontsize}:"
            f"fontcolor=white:borderw=3:bordercolor=black:x=(w-tw)/2:y=h/6:"
            f"enable='lt(t,{args.tieu_de_giay})':"
            f"alpha='if(lt(t,{args.tieu_de_giay}-0.5),1,({args.tieu_de_giay}-t)/0.5)'")

    graph = [f"[0:v]{','.join(vchain) if vchain else 'null'}[v0]"]
    vlast = "v0"
    idx = 1
    if args.logo:
        inputs += ["-i", args.logo]
        lw = out_w // 8
        graph.append(f"[{idx}:v]scale={lw}:-1[logo]")
        graph.append(f"[{vlast}][logo]overlay=W-w-{out_w // 40}:{out_w // 40}[v1]")
        vlast = "v1"
        idx += 1
    if args.mo_dau_ket_thuc:
        fade = 0.6
        graph.append(f"[{vlast}]fade=t=in:d={fade},fade=t=out:st={max(0, total - fade)}:d={fade}[v2]")
        vlast = "v2"

    alast = "0:a"
    if voice:
        # Tiếng gốc nhỏ lại làm nền cho giọng đọc.
        inputs += ["-i", voice]
        graph.append(f"[0:a]volume={args.nen_am_luong},apad[orig]")
        graph.append(f"[orig][{idx}:a]amix=inputs=2:duration=first:dropout_transition=0:normalize=0[av]")
        alast = "av"
        idx += 1
    if args.nhac:
        inputs += ["-stream_loop", "-1", "-i", args.nhac]
        graph.append(f"[{idx}:a]volume={args.nhac_am_luong},"
                     f"afade=t=out:st={max(0, total - 2)}:d=2[bgm]")
        graph.append(f"[{alast}][bgm]amix=inputs=2:duration=first:dropout_transition=0:normalize=0[a1]")
        alast = "a1"
        idx += 1
    if args.chuan_am:
        graph.append(f"[{alast}]loudnorm=I=-14:TP=-1.5:LRA=11[a2]")
        alast = "a2"
    amap = f"[{alast}]" if alast != "0:a" else "0:a?"

    run(["ffmpeg", "-y", "-v", "error", "-stats", *inputs,
         "-filter_complex", ";".join(graph), "-map", f"[{vlast}]", "-map", amap,
         "-t", f"{total:.3f}", "-c:v", "libx264", "-preset", args.preset, "-crf", str(args.crf),
         "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
         "-movflags", "+faststart", dst])


def main():
    p = argparse.ArgumentParser(description="Edit video tự động")
    p.add_argument("input", help="video thô")
    p.add_argument("-o", "--output", help="file kết quả (mặc định video/xong/<tên>_edit.mp4)")
    p.add_argument("--tu", help="bắt đầu từ thời điểm, vd 00:00:05")
    p.add_argument("--den", help="kết thúc ở thời điểm, vd 00:03:20")
    p.add_argument("--cat-lang", action="store_true", help="tự cắt khoảng lặng")
    p.add_argument("--nguong-lang", default="0.04", help="ngưỡng âm lượng coi là lặng (0-1)")
    p.add_argument("--le", default="0.2s", help="giữ lại bao nhiêu quanh chỗ có tiếng")
    p.add_argument("--phu-de", action="store_true", help="tạo phụ đề và gắn vào video")
    p.add_argument("--srt", help="dùng file phụ đề .srt có sẵn thay vì tự nhận dạng")
    p.add_argument("--model", default="small", help="model Whisper: tiny/base/small/medium/large-v3")
    p.add_argument("--ngon-ngu", default="vi", help="ngôn ngữ lời nói")
    p.add_argument("--giong", help="file lời đọc .txt: tạo giọng đọc + phụ đề khớp (xem tools/giong_doc.py)")
    p.add_argument("--giong-engine", default="edge", choices=["edge", "espeak"],
                   help="edge = giọng Microsoft (cần mạng), espeak = giọng máy để chạy thử")
    p.add_argument("--giong-doc", default="vi-VN-HoaiMyNeural",
                   help="vi-VN-HoaiMyNeural (nữ) hoặc vi-VN-NamMinhNeural (nam)")
    p.add_argument("--toc-do", default="+0%", help="tốc độ đọc, vd +10%% hoặc -5%%")
    p.add_argument("--nen-am-luong", default="0.25", help="âm lượng tiếng gốc khi có giọng đọc (0-1)")
    p.add_argument("--phu-de-cao", type=int, help="khoảng cách phụ đề tới đáy (thang 288, mặc định 24)")
    p.add_argument("--khung", help="tỉ lệ khung mới, vd 9:16, 16:9, 1:1")
    p.add_argument("--nhac", help="file nhạc nền")
    p.add_argument("--nhac-am-luong", default="0.15", help="âm lượng nhạc nền (0-1)")
    p.add_argument("--logo", help="file logo PNG, đặt góc trên bên phải")
    p.add_argument("--chu", help="file .ass chứa các đoạn chữ hiện theo thời gian (xem video/mau/)")
    p.add_argument("--tieu-de", help="chữ tiêu đề hiện ở đầu video")
    p.add_argument("--tieu-de-giay", type=float, default=3.0, help="tiêu đề hiện bao nhiêu giây")
    p.add_argument("--mo-dau-ket-thuc", action="store_true", help="hiệu ứng mờ dần đầu/cuối")
    p.add_argument("--chuan-am", action="store_true", help="chuẩn hoá âm lượng kiểu YouTube/TikTok")
    p.add_argument("--crf", type=int, default=20, help="chất lượng (thấp = đẹp hơn, nặng hơn)")
    p.add_argument("--preset", default="medium", help="tốc độ nén x264")
    p.add_argument("--giu-srt", action="store_true", help="lưu file .srt cạnh video kết quả")
    args = p.parse_args()

    if args.chu:
        args.chu = Path(args.chu).resolve()
    src = Path(args.input).resolve()
    if not src.exists():
        sys.exit(f"Không thấy file: {src}")
    dst = Path(args.output) if args.output else ROOT / "video/xong" / f"{src.stem}_edit.mp4"
    dst.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        cur = src
        if args.tu or args.den:
            trim(cur, tmp / "1_trim.mp4", args.tu, args.den)
            cur = tmp / "1_trim.mp4"
        if args.cat_lang:
            before = duration(cur)
            cut_silence(cur, tmp / "2_cut.mp4", args.nguong_lang, args.le)
            cur = tmp / "2_cut.mp4"
            print(f"Cắt lặng: {before:.1f}s -> {duration(cur):.1f}s")
        srt = None
        voice, voice_end = None, 0.0
        if args.giong:
            from giong_doc import make_voice
            voice, srt, voice_end = make_voice(args.giong, tmp, args.giong_engine,
                                               args.giong_doc, args.toc_do)
        elif args.srt:
            srt = tmp / "subs.srt"
            shutil.copy(args.srt, srt)
        elif args.phu_de:
            srt = tmp / "subs.srt"
            transcribe(cur, srt, args.model, args.ngon_ngu)
        render(cur, dst, args, srt, voice, voice_end)
        if srt and args.giu_srt:
            shutil.copy(srt, dst.with_suffix(".srt"))

    print(f"\nXong: {dst} ({duration(dst):.1f}s, {dst.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
