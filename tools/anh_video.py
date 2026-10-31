#!/usr/bin/env python3
"""Ghép nhiều ảnh thành video dọc 9:16: mỗi ảnh zoom/lia chậm (Ken Burns), chuyển cảnh mượt.

Ví dụ:
    python3 tools/anh_video.py video/anh/ong-gen/*.jpg -o video/tho/ong-gen-anh.mp4 --giay 3.5

Kết quả có rãnh âm thanh im lặng, dùng tiếp với tools/edit.py (chữ, giọng đọc, hiệu ứng...).
"""
import argparse
import subprocess
import tempfile
from pathlib import Path

W, H, FPS = 1080, 1920, 30
# Lần lượt: zoom vào, zoom ra, lia trái→phải, lia phải→trái (z, x, y theo on = khung số mấy).
MOVES = [
    ("1+0.15*on/{n}", "iw/2-iw/zoom/2", "ih/2-ih/zoom/2"),
    ("1.15-0.15*on/{n}", "iw/2-iw/zoom/2", "ih/2-ih/zoom/2"),
    ("1.12", "(iw-iw/zoom)*on/{n}", "ih/2-ih/zoom/2"),
    ("1.12", "(iw-iw/zoom)*(1-on/{n})", "ih/2-ih/zoom/2"),
]
TRANSITIONS = ["fade", "slideleft", "circleopen", "smoothup", "fadewhite", "wiperight"]


def run(cmd):
    print("$", " ".join(str(c) for c in cmd), flush=True)
    subprocess.run([str(c) for c in cmd], check=True)


def clip(img, dst, seconds, move):
    n = int(seconds * FPS)
    z, x, y = (m.format(n=n) for m in MOVES[move % len(MOVES)])
    # Ảnh không đúng khung dọc: nền là chính ảnh đó làm mờ, ảnh gốc nằm giữa.
    graph = (f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
             f"boxblur=30:5,eq=brightness=-0.08[bg];"
             f"[0:v]scale={W}:{H}:force_original_aspect_ratio=decrease[fg];"
             f"[bg][fg]overlay=(W-w)/2:(H-h)/2,scale={W * 2}:{H * 2},"
             f"zoompan=z='{z}':x='{x}':y='{y}':d=1:s={W}x{H}:fps={FPS},"
             f"trim=end_frame={n},setpts=N/{FPS}/TB,format=yuv420p[v]")
    run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-framerate", FPS, "-i", img,
         "-filter_complex", graph, "-map", "[v]", "-c:v", "libx264", "-preset", "veryfast",
         "-crf", "16", dst])


def main():
    p = argparse.ArgumentParser(description="Ghép ảnh thành video dọc")
    p.add_argument("images", nargs="+", help="các file ảnh, theo thứ tự hiện")
    p.add_argument("-o", "--output", required=True)
    p.add_argument("--giay", type=float, default=3.5, help="mỗi ảnh hiện bao nhiêu giây")
    p.add_argument("--chuyen", type=float, default=0.5, help="thời gian chuyển cảnh (giây)")
    args = p.parse_args()

    with tempfile.TemporaryDirectory() as tmp:
        clips = []
        for i, img in enumerate(args.images):
            c = Path(tmp) / f"c{i}.mp4"
            clip(img, c, args.giay, i)
            clips.append(c)
        inputs = [x for c in clips for x in ("-i", c)]
        graph, last, offset = [], "0:v", 0.0
        for i in range(1, len(clips)):
            offset += args.giay - args.chuyen
            out = f"x{i}"
            graph.append(f"[{last}][{i}:v]xfade=transition={TRANSITIONS[(i - 1) % len(TRANSITIONS)]}:"
                         f"duration={args.chuyen}:offset={offset:.3f}[{out}]")
            last = out
        total = args.giay * len(clips) - args.chuyen * (len(clips) - 1)
        graph.append(f"anullsrc=r=48000:cl=stereo,atrim=duration={total:.3f}[a]")
        vmap = f"[{last}]" if len(clips) > 1 else "0:v"
        run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", ";".join(graph),
             "-map", vmap, "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
             "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", args.output])
    print(f"Xong: {args.output} ({total:.1f}s, {len(clips)} ảnh)")


if __name__ == "__main__":
    main()
