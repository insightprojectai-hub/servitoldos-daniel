# -*- coding: utf-8 -*-
"""Render de Shorts verticales 1080x1920 (< 60 s).

Uso:  python3 shorts.py <indice|id> [--frames]
Salida: ../shorts/<id>.mp4
"""
import os, sys, math, json, time, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import render as R
from shorts_data import SHORTS
from videos import CHANNEL

W, H = 1080, 1920
R.W, R.H, R.HOR = W, H, 1180
R.OUTRO_TAIL = 0.8
FPS = 30
OUT = os.path.join(HERE, "..", "shorts")

F, text_img, rounded, fit_font, hexc, El = R.F, R.text_img, R.rounded, R.fit_font, R.hexc, R.El

# zona segura de Shorts: arriba ~220 px de interfaz, abajo ~420 px, derecha ~140 px
CX = 500            # centro horizontal del contenido (desplazado a la izquierda de los botones)
X0, X1 = 50, 950    # anchura útil
SUB_Y = 1385        # base de los subtítulos


_orig_split = R.split_sub
R.split_sub = lambda t: _orig_split(t, 30)


def vpanel(pal, y0, y1, x0=X0 - 10, x1=X1 + 10):
    return rounded((x1 - x0, y1 - y0), 36, (8, 4, 20, 205), outline=hexc(pal["a2"], 170), width=3, shadow=True)


def heading(s, pal, size=86):
    f = fit_font("anton", s.upper(), X1 - X0 - 80, size, 44)
    return text_img(s.upper(), f, fill=hexc(pal["a1"]), glow=hexc(pal["a1"], 140), glow_r=12)


def build(scene, pal):
    typ = scene["type"]; s0 = scene["_start"]
    a1, a2 = hexc(pal["a1"]), hexc(pal["a2"])
    els = []

    if typ == "title":
        k = text_img(scene["kicker"], F("bebas", 60), fill=(15, 5, 25, 255), pad=0)
        badge = rounded((k.width + 60, k.height + 26), 22, a1)
        badge.alpha_composite(k, (30, 10))
        els.append(El(badge, CX, 330, s0 + 0.05, "pop", center=True, sfx="pop"))
        f = fit_font("anton", "MMMMMMMM", X1 - X0, 150, 80)
        tt = text_img(scene["title"], f, stroke=6, stroke_fill=(10, 0, 20, 255), glow=a1, glow_r=22, align="center", maxw=X1 - X0)
        els.append(El(tt, CX, 450, s0 + 0.2, "up", 0.5, center=True))
        sub = text_img(scene["sub"], F("xbold", 52), stroke=4, align="center", maxw=X1 - X0)
        els.append(El(sub, CX, 450 + tt.height - 10, s0 + 0.5, "up", center=True))

    elif typ == "stat":
        els.append(El(vpanel(pal, 330, 1200), X0 - 40, 300, s0, "fade", 0.3))
        lab = text_img(scene["label"], fit_font("bebas", scene["label"], X1 - X0 - 60, 90, 50), fill=a2, glow=hexc(pal["a2"], 120))
        els.append(El(lab, CX, 390, s0 + 0.1, "up", center=True))
        f = fit_font("anton", scene["value"], X1 - X0 - 80, 260, 120)
        val = text_img(scene["value"], f, stroke=6, stroke_fill=(10, 0, 20, 255), glow=a1, glow_r=26)
        els.append(El(val, CX, 540, s0 + 0.3, "pop", 0.5, center=True, sfx="pop"))
        sub = text_img(scene["sub"], F("bold", 48), align="center", maxw=X1 - X0 - 80)
        els.append(El(sub, CX, 540 + val.height, s0 + 0.6, "up", center=True))

    elif typ in ("bullets", "checklist"):
        items = scene["items"]; n = len(items)
        step = min(170, (1180 - 470) // n)
        y_end = 470 + step * n + 40
        els.append(El(vpanel(pal, 280, y_end), X0 - 40, 250, s0, "fade", 0.3))
        els.append(El(heading(scene["heading"], pal), X0 + 10, 300, s0 + 0.1, "left"))
        times = R.reveal_times(scene, n)
        fs = 52 if n <= 4 else 46
        for i, it in enumerate(items):
            row = Image.new("RGBA", (X1 - X0 - 20, step), (0, 0, 0, 0))
            d = ImageDraw.Draw(row)
            cy = step // 2
            if typ == "bullets":
                d.ellipse([6, cy - 34, 74, cy + 34], fill=a1)
                num = str(i + 1); nf = F("anton", 44); tw, th, bb = R.text_size(nf, num)
                d.text((40 - tw // 2 - bb[0], cy - th // 2 - bb[1]), num, font=nf, fill=(15, 5, 25, 255))
            else:
                d.rounded_rectangle([6, cy - 32, 70, cy + 32], 14, fill=a2)
                d.line([(20, cy), (34, cy + 15), (58, cy - 16)], fill=(15, 5, 25, 255), width=9)
            txt = text_img(it, F("bold", fs), pad=0, maxw=X1 - X0 - 140)
            row.alpha_composite(txt, (100, max(0, cy - txt.height // 2)))
            els.append(El(row, X0 + 10, 470 + i * step, times[i], "left", sfx="pop"))

    elif typ == "compare":
        els.append(El(heading(scene["heading"], pal, 96), CX, 270, s0 + 0.05, "up", center=True))
        cols = scene["cols"]; n = len(cols)
        cw = X1 - X0
        ch = min(380, (1200 - 420) // n - 30)
        times = R.reveal_times(scene, n)
        colors = [a1, a2, hexc("#ffffff")]
        for i, c in enumerate(cols):
            card = rounded((cw, ch), 30, (8, 4, 20, 225), outline=colors[i % 3], width=4, shadow=True)
            pad = 30
            d = ImageDraw.Draw(card)
            d.rounded_rectangle([pad, pad, pad + cw, pad + 90], 30, fill=colors[i % 3])
            d.rectangle([pad, pad + 50, pad + cw, pad + 90], fill=colors[i % 3])
            t_img = text_img(c["title"], fit_font("bebas", c["title"], cw - 40, 70, 36), fill=(15, 5, 25, 255), pad=0)
            card.alpha_composite(t_img, (pad + (cw - t_img.width) // 2, pad + 45 - t_img.height // 2))
            body_y, body_h = pad + 100, ch - 100
            if c.get("big"):
                b_img = text_img(c["big"], fit_font("anton", c["big"], cw * 0.5, 140, 60), glow=colors[i % 3], glow_r=14, pad=8)
                card.alpha_composite(b_img, (pad + 30, body_y + (body_h - b_img.height) // 2))
                lx, lw = pad + 30 + b_img.width + 20, cw - b_img.width - 70
            else:
                lx, lw = pad + 40, cw - 80
            lines = [text_img(ln, F("bold", 40), maxw=lw, pad=0) for ln in c["lines"]]
            tot = sum(l.height for l in lines) + 20 * (len(lines) - 1)
            y = body_y + (body_h - tot) // 2
            for l in lines:
                card.alpha_composite(l, (int(lx), int(y))); y += l.height + 20
            els.append(El(card, X0 - 30, 420 + i * (ch + 30), times[i], "up", 0.45, sfx="pop"))

    elif typ == "clock":
        rows = scene["rows"]; n = len(rows)
        step = min(190, (1200 - 470) // n)
        els.append(El(vpanel(pal, 280, 470 + step * n + 30), X0 - 40, 250, s0, "fade", 0.3))
        els.append(El(heading(scene["heading"], pal), X0 + 10, 300, s0 + 0.1, "left"))
        times = R.reveal_times(scene, n)
        for i, (place, tm) in enumerate(rows):
            row = Image.new("RGBA", (X1 - X0 - 40, step), (0, 0, 0, 0))
            d = ImageDraw.Draw(row)
            d.line([(0, step - 4), (X1 - X0 - 40, step - 4)], fill=hexc(pal["a2"], 90), width=2)
            p_img = text_img(place, F("bold", 44), pad=0)
            row.alpha_composite(p_img, (0, 14))
            t_img = text_img(tm, fit_font("bebas", tm, X1 - X0 - 60, 76, 40), fill=a1, pad=0)
            row.alpha_composite(t_img, (0, 14 + p_img.height + 6))
            els.append(El(row, X0 + 20, 470 + i * step, times[i], "left", sfx="pop"))

    elif typ == "timeline":
        ev = scene["events"]; n = len(ev)
        y0, y1 = 560, 560 + min(170, 700 // n) * (n - 1)
        els.append(El(vpanel(pal, 280, y1 + 150), X0 - 40, 250, s0, "fade", 0.3))
        els.append(El(heading(scene["heading"], pal), X0 + 10, 300, s0 + 0.1, "left"))
        lx = X0 + 90
        line = Image.new("RGBA", (30, y1 - y0 + 20), (0, 0, 0, 0))
        ImageDraw.Draw(line).rounded_rectangle([9, 0, 21, y1 - y0 + 20], 6, fill=hexc(pal["a2"], 200))
        els.append(El(line, lx - 15, y0 - 10, s0 + 0.2, "fade", 0.5))
        times = R.reveal_times(scene, n)
        for i, (date, lab) in enumerate(ev):
            cy = y0 + (y1 - y0) * (i / max(1, n - 1))
            node = Image.new("RGBA", (X1 - X0, 150), (0, 0, 0, 0))
            d = ImageDraw.Draw(node)
            d.ellipse([lx - X0 - 30, 45, lx - X0 + 30, 105], fill=a1, outline=(255, 255, 255, 255), width=5)
            dt = text_img(date, fit_font("anton", date, 600, 70, 40), fill=(255, 255, 255, 255), glow=a1, glow_r=10, pad=4)
            node.alpha_composite(dt, (lx - X0 + 60, 75 - dt.height + 10))
            lt = text_img(lab, F("bold", 40), maxw=620, pad=0)
            node.alpha_composite(lt, (lx - X0 + 66, 82))
            els.append(El(node, X0, int(cy) - 75, times[i], "left", 0.4, sfx="pop"))

    elif typ == "warning":
        els.append(El(vpanel(pal, 300, 1180), X0 - 40, 270, s0, "fade", 0.3))
        tri = Image.new("RGBA", (300, 270), (0, 0, 0, 0))
        d = ImageDraw.Draw(tri)
        d.polygon([(150, 10), (290, 255), (10, 255)], fill=hexc("#ffcc00"))
        d.polygon([(150, 40), (262, 238), (38, 238)], fill=(20, 10, 0, 255))
        ef = F("anton", 150); tw, th, bb = R.text_size(ef, "!")
        d.text((150 - tw // 2 - bb[0], 150 - th // 2 - bb[1] + 15), "!", font=ef, fill=hexc("#ffcc00"))
        tri = Image.alpha_composite(tri.filter(ImageFilter.GaussianBlur(10)), tri)
        els.append(El(tri, CX, 360, s0 + 0.1, "pop", 0.45, center=True, sfx="pop"))
        tt = text_img(scene["title"], fit_font("anton", scene["title"], X1 - X0 - 60, 96, 50), fill=hexc("#ffcc00"), glow=hexc("#ffcc00", 120), align="center")
        els.append(El(tt, CX, 650, s0 + 0.25, "up", center=True))
        els.append(El(text_img(scene["text"], F("bold", 48), maxw=X1 - X0 - 90, align="center", spacing=14), CX, 650 + tt.height, s0 + 0.5, "up", center=True))

    elif typ == "map":
        els.append(El(vpanel(pal, 280, 1350), X0 - 40, 250, s0, "fade", 0.3))
        els.append(El(heading(scene["heading"], pal), X0 + 10, 290, s0 + 0.1, "left"))
        mp, pins = R.map_image(pal)
        sc = (X1 - X0 - 40) / mp.width
        mp = mp.resize((int(mp.width * sc), int(mp.height * sc)), Image.LANCZOS)
        pins = {k: (int(x * sc), int(y * sc)) for k, (x, y) in pins.items()}
        mx, my = X0 + 20, 420
        els.append(El(mp, mx, my, s0 + 0.15, "fade", 0.5))
        regs = scene["regions"]; n = len(regs)
        times = R.reveal_times(scene, n)
        ends = times[1:] + [scene["_end"]]
        rw = (X1 - X0 - 40) // 2
        rows_n, rows_a = [], []
        for i, r in enumerate(regs):
            for act, store in ((False, rows_n), (True, rows_a)):
                row = Image.new("RGBA", (rw, 84), (0, 0, 0, 0))
                d = ImageDraw.Draw(row)
                if act:
                    d.rounded_rectangle([0, 4, rw, 80], 18, fill=hexc(pal["a1"], 235))
                col = (15, 5, 25, 255) if act else (255, 255, 255, 255)
                d.text((16, 14), str(i + 1), font=F("anton", 40), fill=col if act else a2)
                rt = text_img(r.upper(), fit_font("bebas", r.upper(), rw - 80, 56, 30), fill=col, pad=0)
                row.alpha_composite(rt, (64, 42 - rt.height // 2))
                store.append(row)
        ly = my + mp.height + 20
        for i in range(n):
            e = El(rows_n[i], X0 + 20 + (i % 2) * rw, ly + (i // 2) * 90, times[i], "left", sfx="pop")
            e.dyn = (lambda ti, te, i: (lambda t: rows_a[i] if ti <= t < te else rows_n[i]))(times[i], ends[i], i)
            els.append(e)
        size = mp.size

        def pin_dyn(t):
            im = Image.new("RGBA", size, (0, 0, 0, 0)); d = ImageDraw.Draw(im)
            for i, r in enumerate(regs):
                if t < times[i]:
                    continue
                px, py = pins[r]; active = times[i] <= t < ends[i]
                d.ellipse([px - 13, py - 13, px + 13, py + 13], fill=a1 if active else a2, outline=(255, 255, 255, 255), width=3)
                if active:
                    ph = ((t - times[i]) * 1.4) % 1; Rr = 16 + 50 * ph
                    d.ellipse([px - Rr, py - Rr, px + Rr, py + Rr], outline=hexc(pal["a1"], int(255 * (1 - ph))), width=5)
            return im
        pe = El(Image.new("RGBA", size), mx, my, s0 + 0.15, "fade", 0.3); pe.dyn = pin_dyn
        els.append(pe)
        els.append(El(text_img("Ilustración orientativa · no es el mapa oficial", F("semi", 22), fill=(255, 255, 255, 150), pad=0), mx + 10, my + mp.height - 20, s0 + 0.4, "fade"))

    elif typ == "outro":
        tt = text_img(scene["title"], fit_font("anton", "MMMMMMMM", X1 - X0, 130, 70), stroke=6, stroke_fill=(10, 0, 20, 255), glow=a1, glow_r=22, align="center", maxw=X1 - X0)
        els.append(El(tt, CX, 360, s0 + 0.05, "up", 0.5, center=True))
        els.append(El(text_img(scene["sub"], F("xbold", 54), stroke=4, align="center", maxw=X1 - X0), CX, 360 + tt.height - 10, s0 + 0.3, "up", center=True))
        btn = rounded((620, 140), 70, hexc("#ff1f3d"), shadow=True)
        bt = text_img("SUSCRÍBETE", F("anton", 84), pad=0)
        btn.alpha_composite(bt, (30 + (620 - bt.width) // 2, 30 + (140 - bt.height) // 2 - 6))
        els.append(El(btn, CX, 1060, s0 + 0.5, "pop", 0.5, center=True, sfx="pop"))
    return els


_subc = {}


def sub_img(s):
    if s not in _subc:
        _subc[s] = text_img(s, F("black", 60), stroke=7, stroke_fill=(0, 0, 0, 255), align="center", maxw=X1 - X0, pad=10, spacing=6)
    return _subc[s]


def render(sh, frames_only=False):
    t0 = time.time()
    pal = R.PALETTES[sh["palette"]]
    video = dict(id=sh["id"], palette=sh["palette"], scenes=sh["scenes"])
    bdir, voice, subs, total = R.prepare(video)
    print(f"[{sh['id']}] {total:.1f}s", flush=True)
    bg = R.build_background(pal, seed=len(sh["id"]) * 5)
    wm = text_img(CHANNEL, F("bebas", 48), fill=hexc(pal["a2"]), glow=hexc(pal["a2"], 140), glow_r=8, pad=10)
    scenes = sh["scenes"]
    all_els = [build(sc, pal) for sc in scenes]
    if frames_only:
        ims = []
        for si, sc in enumerate(scenes):
            fr = bg.copy(); R.draw_grid(ImageDraw.Draw(fr), pal, 1.0)
            t = sc["_end"] - 0.5
            for e in all_els[si]:
                e.draw(fr, t, 1.0)
            fr.alpha_composite(wm, ((W - wm.width) // 2, 200))
            for (a, b, s) in subs:
                if a <= sc["_sent_starts"][-1] + 0.1 < b:
                    im = sub_img(s); fr.alpha_composite(im, ((W - im.width) // 2 - 40, SUB_Y))
            ims.append(fr.convert("RGB").resize((360, 640)))
        c = Image.new("RGB", (360 * len(ims), 640))
        for i, im in enumerate(ims):
            c.paste(im, (i * 360, 0))
        p = os.path.join(bdir, "contact.jpg"); c.save(p, quality=85); print(p); return
    sfx = []
    for sc, els in zip(scenes, all_els):
        sfx.append(("whoosh", max(0, sc["_start"] - 0.15)))
        sfx += [("pop", e.t0) for e in els if e.sfx == "pop"]
    wav = os.path.join(bdir, "mix.wav")
    R.build_audio(video, voice, total, sfx, wav)
    os.makedirs(OUT, exist_ok=True)
    out = os.path.join(OUT, sh["id"] + ".mp4")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-i", wav, "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-threads", "2",
           "-c:a", "aac", "-b:a", "192k", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", "-movflags", "+faststart", "-shortest", out]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    rng = np.random.default_rng(3)
    parts = [[rng.uniform(0, W), rng.uniform(0, H), rng.uniform(10, 40), rng.uniform(1, 3)] for _ in range(40)]
    a2 = hexc(pal["a2"])
    si = 0
    for fi in range(int(total * FPS)):
        t = fi / FPS
        while si + 1 < len(scenes) and t >= scenes[si + 1]["_start"] - 0.05:
            si += 1
        frame = bg.copy(); d = ImageDraw.Draw(frame)
        R.draw_grid(d, pal, t)
        for p in parts:
            y = (p[1] - t * p[2]) % H; x = p[0] + 12 * math.sin(t * 0.7 + p[1]); r = p[3]
            d.ellipse([x - r, y - r, x + r, y + r], fill=(a2[0], a2[1], a2[2], 150))
        sc = scenes[si]
        fade = max(0.0, (sc["_end"] - t) / 0.3) if t > sc["_end"] - 0.3 and si + 1 < len(scenes) else 1.0
        for e in all_els[si]:
            e.draw(frame, t, fade)
        dt = t - sc["_start"]
        if 0 <= dt < 0.18 and si > 0:
            frame = Image.alpha_composite(frame, Image.new("RGBA", (W, H), hexc(pal["a1"], int(90 * (1 - dt / 0.18)))))
        frame.alpha_composite(wm, ((W - wm.width) // 2, 200))
        for (a, b, s) in subs:
            if a <= t < b:
                im = sub_img(s); frame.alpha_composite(im, ((W - im.width) // 2 - 40, SUB_Y)); break
        d = ImageDraw.Draw(frame)
        d.rectangle([0, H - 8, int(W * t / total), H], fill=hexc(pal["a1"]))
        proc.stdin.write(frame.convert("RGB").tobytes())
    proc.stdin.close(); proc.wait()
    json.dump(dict(id=sh["id"], duration=total), open(os.path.join(bdir, "meta.json"), "w"))
    print(f"[{sh['id']}] OK {out} {time.time()-t0:.0f}s", flush=True)


if __name__ == "__main__":
    k = sys.argv[1]
    sh = SHORTS[int(k)] if k.isdigit() else next(x for x in SHORTS if x["id"] == k)
    render(sh, frames_only="--frames" in sys.argv)
