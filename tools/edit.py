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


def retime(src, dst, cuts, speeds):
    """Bỏ các đoạn trong cuts [(a, b)], tua nhanh các đoạn trong speeds [(a, b, x)]. Giây gốc."""
    total = duration(src)
    marks = {0.0, total}
    for a, b in cuts:
        marks |= {a, b}
    for a, b, _ in speeds:
        marks |= {a, b}
    points = sorted(m for m in marks if 0 <= m <= total)
    graph, n = [], 0
    for a, b in zip(points, points[1:]):
        if b - a < 0.02 or any(ca <= a and b <= cb for ca, cb in cuts):
            continue
        x = next((sx for sa, sb, sx in speeds if sa <= a and b <= sb), 1.0)
        tempo, chain = x, []
        while tempo > 2.0:  # atempo tối đa 2 lần mỗi bước
            chain.append("atempo=2.0")
            tempo /= 2.0
        chain.append(f"atempo={tempo:.4f}")
        graph.append(f"[0:v]trim={a}:{b},setpts=(PTS-STARTPTS)/{x}[v{n}]")
        graph.append(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,{','.join(chain)}[a{n}]")
        n += 1
    graph.append("".join(f"[v{i}][a{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=1[v][a]")
    run(["ffmpeg", "-y", "-v", "error", "-i", src, "-filter_complex", ";".join(graph),
         "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
         "-c:a", "aac", "-b:a", "192k", dst])


SFX_DIR = Path(tempfile.gettempdir()) / "qd_sfx"


def sfx_file(kind):
    """Tạo (một lần) tiếng hiệu ứng bằng ffmpeg: whoosh (vút), ding, pop."""
    SFX_DIR.mkdir(exist_ok=True)
    out = SFX_DIR / f"{kind}.wav"
    if not out.exists():
        src = {
            "whoosh": ("anoisesrc=d=0.45:c=pink:a=0.6",
                       "highpass=f=600,lowpass=f=5000,afade=t=in:d=0.2,afade=t=out:st=0.2:d=0.25,volume=0.7"),
            "ding": ("sine=f=1568:d=0.9",
                     "volume='exp(-5*t)':eval=frame,aecho=0.6:0.4:60:0.3,volume=0.6"),
            "pop": ("sine=f=700:d=0.12", "afade=t=out:d=0.12,volume=0.6"),
        }[kind]
        run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", src[0], "-af", src[1],
             "-ar", "48000", "-ac", "2", out])
    return out


def make_hook(main, ass, seconds, dst):
    """Đoạn mở đầu: khung hình đầu làm mờ + tối, chữ tình huống từ file ASS, tiếng vút."""
    w, h = video_size(main)
    # Tiếng: vút lúc mở, pop cho câu thứ 2, 3, vút lúc chốt (khớp mẫu *-mo-dau.ass).
    hits = [(0.0, "whoosh"), (0.7, "pop"), (1.4, "pop"), (2.2, "whoosh")]
    sfx_in = [x for _, k in hits for x in ("-i", sfx_file(k))]
    sfx_graph = "".join(f"[{i + 1}:a]aformat=sample_rates=48000:channel_layouts=stereo,"
                        f"adelay={int(t * 1000)}|{int(t * 1000)}[s{i}];" for i, (t, _) in enumerate(hits))
    sfx_mix = "".join(f"[s{i}]" for i in range(len(hits)))
    run(["ffmpeg", "-y", "-v", "error", "-i", main, *sfx_in, "-filter_complex",
         f"[0:v]trim=end_frame=1,loop=loop=-1:size=1,trim=duration={seconds},setpts=N/30/TB,"
         f"fps=30,scale={w}:{h},boxblur=25:3,eq=brightness=-0.25,"
         f"subtitles='{escape_filter_path(ass)}',format=yuv420p[v];"
         f"anullsrc=r=48000:cl=stereo,atrim=duration={seconds}[sil];{sfx_graph}"
         f"[sil]{sfx_mix}amix=inputs={len(hits) + 1}:duration=first:normalize=0[a]",
         "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
         "-c:a", "aac", "-b:a", "192k", dst])


def concat(parts, dst, args):
    graph = "".join(f"[{i}:v]fps=30,setsar=1[v{i}];[{i}:a]aformat=sample_rates=48000:"
                    f"channel_layouts=stereo[a{i}];" for i in range(len(parts)))
    graph += "".join(f"[v{i}][a{i}]" for i in range(len(parts))) + f"concat=n={len(parts)}:v=1:a=1[v][a]"
    inputs = [x for p in parts for x in ("-i", p)]
    run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", graph, "-map", "[v]", "-map", "[a]",
         "-c:v", "libx264", "-preset", args.preset, "-crf", str(args.crf), "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", dst])


def parse_ranges(text, with_speed=False):
    """'35-43.4x3,15.6-20.5x2' -> [(35, 43.4, 3), ...]; '0-1.6' -> [(0, 1.6)]."""
    out = []
    for item in filter(None, (text or "").split(",")):
        rng, _, x = item.partition("x")
        a, b = (float(v) for v in rng.split("-"))
        out.append((a, b, float(x or 2)) if with_speed else (a, b))
    return out


def cut_silence(src, dst, threshold, margin):
    run(["auto-editor", src, "--edit", f"audio:threshold={threshold}",
         "--margin", margin, "--progress", "none", "--no-open", "-o", dst])


def srt_time(t):
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def load_audio(path):
    """Đọc âm thanh bằng ffmpeg (16kHz mono) cho Whisper, tránh lệ thuộc phiên bản PyAV."""
    import numpy as np
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-vn", "-ac", "1", "-ar", "16000",
                          "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32)


def transcribe(src, srt_path, model_name, lang):
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        sys.exit("Thiếu faster-whisper. Chạy: bash tools/setup.sh")
    print(f"Đang nhận dạng giọng nói (model {model_name})...", flush=True)
    model = WhisperModel(model_name, device="cpu", compute_type="int8")
    segments, _ = model.transcribe(load_audio(src), language=lang, vad_filter=True)
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


def frame_chain(args, w, h):
    """Bộ lọc đưa video về khung mới. Trả về (bộ lọc hoặc None, rộng, cao)."""
    if args.khung and args.day_khung:
        # Cắt đầy khung mới (không nền mờ), giữ phần giữa; hợp với video quay ngang độ phân giải cao.
        _, out_w, out_h = frame_filter(args.khung, w, h)
        return (f"scale={out_w}:{out_h}:force_original_aspect_ratio=increase,"
                f"crop={out_w}:{out_h}:(iw-{out_w})*{args.day_khung_x}:(ih-{out_h})/2", out_w, out_h)
    if args.khung:
        return frame_filter(args.khung, w, h)
    return None, w, h


def make_hook_cut(src, args, ass, dst, tmp):
    """Mở đầu "cuốn": cắt nhanh các cảnh thật (zoom giật mỗi lần chuyển), giọng đọc ngay giây đầu,
    chữ to từ file ASS. Cảnh lấy tại các mốc --mo-dau-canh (giây trong video sau bỏ/tua)."""
    from giong_doc import make_voice
    times = [float(t) for t in args.mo_dau_canh.split(",")]
    voice_end = 0.0
    if args.mo_dau_giong:
        hv, _, voice_end = make_voice(args.mo_dau_giong, tmp / "hookvoice", args.giong_engine,
                                      args.giong_doc, args.toc_do, args.cao_giong)
    total = max(args.mo_dau_giay, voice_end + 0.3)
    seg = total / len(times)
    w, h = video_size(src)
    f, out_w, out_h = frame_chain(args, w, h)
    graph = []
    for i, t in enumerate(times):
        # Zoom giật: 1.22 -> 1.0 trong 0.35s đầu mỗi cảnh.
        graph.append(f"[0:v]trim=start={t}:duration={seg:.3f},setpts=PTS-STARTPTS,"
                     f"{f + ',' if f else ''}"
                     f"zoompan=z='max(1,1.22-0.63*it)':d=1:fps=30:s={out_w}x{out_h}"
                     f":x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2',setsar=1[c{i}]")
    graph.append("".join(f"[c{i}]" for i in range(len(times)))
                 + f"concat=n={len(times)}:v=1:a=0,eq=contrast=1.08:saturation=1.15,"
                 f"subtitles='{escape_filter_path(ass)}',format=yuv420p[v]")
    inputs = ["-i", src]
    hits = [(i * seg, "whoosh" if i == 0 else "pop") for i in range(len(times))]
    mix = []
    for i, (t, k) in enumerate(hits):
        inputs += ["-i", sfx_file(k)]
        graph.append(f"[{i + 1}:a]aformat=sample_rates=48000:channel_layouts=stereo,"
                     f"adelay={int(t * 1000)}|{int(t * 1000)}[s{i}]")
        mix.append(f"[s{i}]")
    if args.mo_dau_giong:
        inputs += ["-i", hv]
        graph.append(f"[{len(hits) + 1}:a]aformat=sample_rates=48000:channel_layouts=stereo[hv]")
        mix.append("[hv]")
    graph.append(f"anullsrc=r=48000:cl=stereo,atrim=duration={total:.3f}[sil]")
    graph.append(f"[sil]{''.join(mix)}amix=inputs={len(mix) + 1}:duration=first:normalize=0,"
                 f"loudnorm=I=-14:TP=-1.5:LRA=11[a]")
    run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", ";".join(graph),
         "-map", "[v]", "-map", "[a]", "-t", f"{total:.3f}", "-c:v", "libx264", "-preset", "veryfast",
         "-crf", "18", "-c:a", "aac", "-b:a", "192k", dst])
    print(f"Mở đầu: {total:.1f}s, {len(times)} cảnh")


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

    f, out_w, out_h = frame_chain(args, w, h)
    if f:
        vchain.append(f)
    for a, b_, z, cx, cy in args.zoom_list:
        # Phóng to mượt (0.4s vào, 0.4s ra) quanh điểm (cx, cy) tính theo tỉ lệ khung.
        k = f"clip(min((it-{a})/0.4,({b_}-it)/0.4),0,1)"  # it = thời điểm khung vào
        zf = f"(1+{z - 1:.3f}*{k})"
        vchain.append(f"zoompan=z='{zf}':d=1:fps=30:s={out_w}x{out_h}"
                      f":x='min(max(iw*{cx}-iw/zoom/2,0),iw-iw/zoom)'"
                      f":y='min(max(ih*{cy}-ih/zoom/2,0),ih-ih/zoom)'")
    for t in args.flash_list:
        vchain.append(f"drawbox=color=white@0.55:t=fill:enable='between(t,{t},{t + 0.12})'")
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
    if args.sfx_list:
        labels = []
        for i, (t, kind) in enumerate(args.sfx_list):
            inputs += ["-i", sfx_file(kind)]
            ms = int(t * 1000)
            graph.append(f"[{idx}:a]aformat=sample_rates=48000:channel_layouts=stereo,"
                         f"adelay={ms}|{ms}[sfx{i}]")
            labels.append(f"[sfx{i}]")
            idx += 1
        graph.append(f"[{alast}]{''.join(labels)}amix=inputs={len(labels) + 1}:duration=first:"
                     f"dropout_transition=0:normalize=0[asfx]")
        alast = "asfx"
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
    p.add_argument("--bo", help="bỏ các đoạn (giây gốc), vd 0-1.6,70-72")
    p.add_argument("--tua", help="tua nhanh các đoạn (giây gốc), vd 35-43.4x3,15.6-20.5x2")
    p.add_argument("--chi-dung", action="store_true", help="chỉ làm bước bỏ/tua rồi lưu, để soạn phụ đề")
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
    p.add_argument("--toc-do", default="+25%", help="tốc độ đọc, vd +25%% hoặc -5%%")
    p.add_argument("--cao-giong", default="+4Hz", help="độ cao giọng, vd +4Hz cho giọng tươi hơn")
    p.add_argument("--nen-am-luong", default="0.25", help="âm lượng tiếng gốc khi có giọng đọc (0-1)")
    p.add_argument("--phu-de-cao", type=int, help="khoảng cách phụ đề tới đáy (thang 288, mặc định 24)")
    p.add_argument("--khung", help="tỉ lệ khung mới, vd 9:16, 16:9, 1:1")
    p.add_argument("--day-khung", action="store_true", help="cắt đầy khung mới thay vì nền mờ hai bên")
    p.add_argument("--day-khung-x", type=float, default=0.5, help="vị trí cắt ngang 0 (trái) – 1 (phải)")
    p.add_argument("--nhac", help="file nhạc nền")
    p.add_argument("--nhac-am-luong", default="0.15", help="âm lượng nhạc nền (0-1)")
    p.add_argument("--logo", help="file logo PNG, đặt góc trên bên phải")
    p.add_argument("--chu", help="file .ass chứa các đoạn chữ hiện theo thời gian (xem video/mau/)")
    p.add_argument("--tieu-de", help="chữ tiêu đề hiện ở đầu video")
    p.add_argument("--tieu-de-giay", type=float, default=3.0, help="tiêu đề hiện bao nhiêu giây")
    p.add_argument("--mo-dau-ket-thuc", action="store_true", help="hiệu ứng mờ dần đầu/cuối")
    p.add_argument("--chuan-am", action="store_true", help="chuẩn hoá âm lượng kiểu YouTube/TikTok")
    p.add_argument("--zoom", help="phóng to: 'bắt đầu-kết thúc x mức @ tâm x,y', vd 34-38x1.8@0.56,0.45;...")
    p.add_argument("--chop", help="chớp sáng tại các giây, vd 34.1,45.5")
    p.add_argument("--sfx", help="tiếng hiệu ứng 'giây:loại', loại = whoosh|ding|pop, vd 0.2:whoosh,34.1:ding")
    p.add_argument("--mo-dau", help="file .ass cho đoạn mở đầu tình huống (thời gian tính từ 0)")
    p.add_argument("--mo-dau-giay", type=float, default=3.5, help="độ dài đoạn mở đầu")
    p.add_argument("--mo-dau-canh", help="mở đầu cắt nhanh từ cảnh thật tại các giây, vd 2.5,9.5,13")
    p.add_argument("--mo-dau-giong", help="file lời đọc cho đoạn mở đầu (đọc ngay giây đầu)")
    p.add_argument("--crf", type=int, default=20, help="chất lượng (thấp = đẹp hơn, nặng hơn)")
    p.add_argument("--preset", default="medium", help="tốc độ nén x264")
    p.add_argument("--giu-srt", action="store_true", help="lưu file .srt cạnh video kết quả")
    args = p.parse_args()

    if args.chu:
        args.chu = Path(args.chu).resolve()
    args.zoom_list = []
    for item in filter(None, (args.zoom or "").split(";")):
        rng, _, rest = item.partition("x")
        z, _, center = rest.partition("@")
        cx, cy = (float(v) for v in (center or "0.5,0.5").split(","))
        a, b = (float(v) for v in rng.split("-"))
        args.zoom_list.append((a, b, float(z), cx, cy))
    args.flash_list = [float(t) for t in filter(None, (args.chop or "").split(","))]
    args.sfx_list = [(float(t), k) for t, k in
                     (i.split(":") for i in filter(None, (args.sfx or "").split(",")))]
    src = Path(args.input).resolve()
    if not src.exists():
        sys.exit(f"Không thấy file: {src}")
    dst = Path(args.output) if args.output else ROOT / "video/xong" / f"{src.stem}_edit.mp4"
    dst.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        cur = src
        if args.bo or args.tua:
            retime(cur, tmp / "0_retime.mp4", parse_ranges(args.bo), parse_ranges(args.tua, True))
            cur = tmp / "0_retime.mp4"
            print(f"Bỏ/tua: còn {duration(cur):.1f}s")
        if args.tu or args.den:
            trim(cur, tmp / "1_trim.mp4", args.tu, args.den)
            cur = tmp / "1_trim.mp4"
        if args.cat_lang:
            before = duration(cur)
            cut_silence(cur, tmp / "2_cut.mp4", args.nguong_lang, args.le)
            cur = tmp / "2_cut.mp4"
            print(f"Cắt lặng: {before:.1f}s -> {duration(cur):.1f}s")
        if args.chi_dung:
            shutil.copy(cur, dst)
            print(f"\nXong bước dựng: {dst} ({duration(dst):.1f}s)")
            return
        srt = None
        voice, voice_end = None, 0.0
        if args.giong:
            from giong_doc import make_voice
            voice, srt, voice_end = make_voice(args.giong, tmp, args.giong_engine,
                                               args.giong_doc, args.toc_do, args.cao_giong)
        elif args.srt:
            srt = tmp / "subs.srt"
            shutil.copy(args.srt, srt)
        elif args.phu_de:
            srt = tmp / "subs.srt"
            transcribe(cur, srt, args.model, args.ngon_ngu)
        if args.mo_dau:
            body = tmp / "body.mp4"
            render(cur, body, args, srt, voice, voice_end)
            if args.mo_dau_canh:
                (tmp / "hookvoice").mkdir(exist_ok=True)
                make_hook_cut(cur, args, Path(args.mo_dau).resolve(), tmp / "hook.mp4", tmp)
            else:
                make_hook(body, Path(args.mo_dau).resolve(), args.mo_dau_giay, tmp / "hook.mp4")
            concat([tmp / "hook.mp4", body], dst, args)
        else:
            render(cur, dst, args, srt, voice, voice_end)
        if srt and args.giu_srt:
            shutil.copy(srt, dst.with_suffix(".srt"))

    print(f"\nXong: {dst} ({duration(dst):.1f}s, {dst.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
