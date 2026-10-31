"""Giọng đọc tiếng Việt (text-to-speech) + phụ đề khớp theo câu.

File lời đọc (.txt), mỗi dòng một câu:
    # dòng bắt đầu bằng # là ghi chú
    Fe sắt silic EI 0.5mm | Phe sắt si líc E I, dày không phẩy năm li
    @9 Lá tôn silic mỏng, từ thẩm tốt.
- "chữ hiển thị | lời đọc": phụ đề hiện vế trái, giọng đọc vế phải (đọc số, viết tắt).
- "@9" ở đầu dòng: câu này bắt đầu không sớm hơn giây thứ 9 (khớp với cảnh).

Engine:
- edge: giọng Microsoft Edge (vi-VN-HoaiMyNeural nữ, vi-VN-NamMinhNeural nam), cần mạng
  tới speech.platform.bing.com.
- espeak: giọng máy offline (espeak-ng), chỉ để chạy thử.
"""
import asyncio
import os
import re
import ssl
import subprocess
from pathlib import Path

GAP = 0.25  # nghỉ giữa hai câu (giây)
START = 0.3  # câu đầu bắt đầu sau (giây)
MAX_WORDS = 8  # mỗi dòng phụ đề tối đa bao nhiêu chữ


def parse_script(path):
    lines = []
    for raw in Path(path).read_text(encoding="utf-8").splitlines():
        raw = raw.strip()
        if not raw or raw.startswith("#"):
            continue
        at = None
        m = re.match(r"@([\d.]+)\s+(.*)", raw)
        if m:
            at, raw = float(m.group(1)), m.group(2)
        shown, _, spoken = raw.partition("|")
        lines.append({"at": at, "shown": shown.strip(), "spoken": (spoken or shown).strip()})
        # "| lời đọc" (vế trái rỗng): chỉ đọc, không hiện phụ đề.
    return lines


def tts_edge(text, out, voice, rate, pitch="+0Hz"):
    import edge_tts
    from edge_tts import communicate

    # edge-tts chỉ tin chứng chỉ của certifi; nạp thêm CA của máy (proxy công ty/cloud).
    cafile = os.environ.get("SSL_CERT_FILE") or os.environ.get("REQUESTS_CA_BUNDLE")
    if cafile and Path(cafile).exists():
        communicate._SSL_CTX.load_verify_locations(cafile)
    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
    asyncio.run(edge_tts.Communicate(text, voice, rate=rate, pitch=pitch, proxy=proxy).save(str(out)))


def tts_espeak(text, out, rate):
    speed = int(160 * (1 + int(rate.rstrip("%")) / 100))
    subprocess.run(["espeak-ng", "-v", "vi", "-s", str(speed), "-w", str(out), text], check=True)


def audio_len(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", str(path)], capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


def srt_time(t):
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def split_chunks(text):
    """Chia câu dài thành các dòng phụ đề ngắn, ưu tiên ngắt ở dấu phẩy."""
    chunks, cur = [], []
    for part in re.split(r"(?<=[,.;!?])\s+", text):
        words = part.split()
        if cur and len(cur) + len(words) > MAX_WORDS:
            chunks.append(cur)
            cur = []
        if len(words) > MAX_WORDS:
            n = -(-len(words) // MAX_WORDS)  # số dòng cần, chia đều cho cân
            size = -(-len(words) // n)
            chunks += [words[i:i + size] for i in range(0, len(words), size)]
        else:
            cur += words
    if cur:
        chunks.append(cur)
    return [" ".join(c) for c in chunks]


def make_voice(script, tmp, engine="edge", voice="vi-VN-HoaiMyNeural", rate="+0%", pitch="+0Hz"):
    """Tạo giọng đọc. Trả về (file wav giọng đọc, file srt, thời lượng)."""
    tmp = Path(tmp)
    lines = parse_script(script)
    t = START
    clips, subs = [], []
    for i, line in enumerate(lines):
        clip = tmp / f"voice_{i}.{'mp3' if engine == 'edge' else 'wav'}"
        if engine == "edge":
            tts_edge(line["spoken"], clip, voice, rate, pitch)
        else:
            tts_espeak(line["spoken"], clip, rate)
        length = audio_len(clip)
        if line["at"] is not None:
            t = max(t, line["at"])
        clips.append((clip, t))
        # Thời gian từng dòng phụ đề chia theo số ký tự.
        chunks = split_chunks(line["shown"]) if line["shown"] else []
        total_chars = sum(len(c) for c in chunks)
        ct = t
        for c in chunks:
            d = length * len(c) / total_chars
            subs.append((ct, ct + d, c))
            ct += d
        print(f"  {t:5.1f}s +{length:4.1f}s  {line['shown']}")
        t += length + GAP

    srt = tmp / "voice.srt"
    srt.write_text("\n".join(f"{i}\n{srt_time(a)} --> {srt_time(b)}\n{c}\n"
                             for i, (a, b, c) in enumerate(subs, 1)), encoding="utf-8")
    wav = tmp / "voice.wav"
    inputs, graph = [], []
    for i, (clip, start) in enumerate(clips):
        inputs += ["-i", str(clip)]
        ms = int(start * 1000)
        graph.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={ms}|{ms}[c{i}]")
    graph.append("".join(f"[c{i}]" for i in range(len(clips)))
                 + f"amix=inputs={len(clips)}:normalize=0:dropout_transition=0[out]")
    subprocess.run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", ";".join(graph),
                    "-map", "[out]", str(wav)], check=True)
    end = t - GAP
    print(f"Giọng đọc: {len(lines)} câu, dài {end:.1f}s")
    return wav, srt, end
