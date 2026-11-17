# -*- coding: utf-8 -*-
"""Render completo de un vídeo: locución + música + animación + montaje.

Uso:  python3 render.py <id-o-indice> [--preview]
Salida: ../videos/<id>.mp4 y ../miniaturas/<id>.jpg
"""
import os, sys, json, math, subprocess, time, re, hashlib
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import soundfile as sf
from scipy.signal import resample_poly

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from videos import VIDEOS, CHANNEL
import music

W, H = 1920, 1080
FPS = 30
HOR = 700  # línea del horizonte
OUTRO_TAIL = 2.0
FONT_DIR = os.environ.get("FONT_DIR", "/tmp/claude-0/fonts/")
BUILD = os.environ.get("BUILD_DIR", "/tmp/claude-0/build/")
OUT_VID = os.path.join(HERE, "..", "videos")
OUT_THUMB = os.path.join(HERE, "..", "miniaturas")

PALETTES = {
    "sunset":  dict(sky=[(0, "#0b0221"), (.45, "#3b0a57"), (.78, "#b4236e"), (1, "#ff7b3d")], sun=("#ffd23f", "#ff2e88"), grid="#ff2e88", a1="#ff2e88", a2="#29e7ff", city="#16052a"),
    "sunset2": dict(sky=[(0, "#120018"), (.5, "#5a0f3c"), (.8, "#e2483d"), (1, "#ffb347")], sun=("#fff07a", "#ff4e50"), grid="#ffb347", a1="#ffb347", a2="#ff4e8a", city="#1a0414"),
    "miami":   dict(sky=[(0, "#020b26"), (.5, "#0d3b66"), (.8, "#e84a8a"), (1, "#ffb36b")], sun=("#fff1a8", "#ff5fa2"), grid="#36f1e7", a1="#ff5fa2", a2="#36f1e7", city="#06112a"),
    "neon":    dict(sky=[(0, "#050014"), (.5, "#1d0b47"), (.85, "#5b1fa8"), (1, "#b44cff")], sun=("#c6ff4a", "#ff3cac"), grid="#b44cff", a1="#c6ff4a", a2="#ff3cac", city="#0c0322"),
    "cyber":   dict(sky=[(0, "#00010d"), (.5, "#06173a"), (.85, "#0a4d8c"), (1, "#20c5ff")], sun=("#ffe066", "#ff3b3b"), grid="#20c5ff", a1="#ffe066", a2="#ff3b81", city="#020818"),
    "ocean":   dict(sky=[(0, "#00111c"), (.5, "#003b5c"), (.8, "#1fa3a8"), (1, "#ffd27f")], sun=("#fff3b0", "#ff8c61"), grid="#5ef2d0", a1="#5ef2d0", a2="#ff8c61", city="#00101a"),
}


def hexc(h, a=255):
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)


def mix(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(4))


_fonts = {}


def F(name, size):
    key = (name, size)
    if key not in _fonts:
        if name == "anton":
            f = ImageFont.truetype(FONT_DIR + "Anton-Regular.ttf", size)
        elif name == "bebas":
            f = ImageFont.truetype(FONT_DIR + "BebasNeue-Regular.ttf", size)
        else:
            f = ImageFont.truetype(FONT_DIR + "Montserrat-VF.ttf", size)
            try:
                f.set_variation_by_axes([{"bold": 700, "xbold": 800, "black": 900, "semi": 600}.get(name, 700)])
            except Exception:
                pass
        _fonts[key] = f
    return _fonts[key]


# ------------------------------------------------------------------ fondo
def build_background(pal, seed=7):
    rng = np.random.default_rng(seed)
    # cielo
    ys = np.linspace(0, 1, HOR)
    stops = [(p, np.array(hexc(c)[:3], float)) for p, c in pal["sky"]]
    col = np.zeros((HOR, 3))
    for i, y in enumerate(ys):
        for j in range(len(stops) - 1):
            p0, c0 = stops[j]; p1, c1 = stops[j + 1]
            if p0 <= y <= p1:
                col[i] = c0 + (c1 - c0) * ((y - p0) / (p1 - p0 + 1e-9)); break
    img = np.zeros((H, W, 4), np.uint8)
    img[:HOR, :, :3] = col[:, None, :].astype(np.uint8)
    img[:, :, 3] = 255
    # suelo
    g0 = np.array(hexc(pal["city"])[:3], float) * 0.6
    gy = np.linspace(0, 1, H - HOR)[:, None]
    img[HOR:, :, :3] = (g0 * (1 - gy * 0.5)).astype(np.uint8)[:, None, :]
    base = Image.fromarray(img, "RGBA")
    d = ImageDraw.Draw(base)
    # estrellas
    for _ in range(160):
        x, y = rng.integers(0, W), rng.integers(0, int(HOR * 0.55))
        r = rng.choice([1, 1, 1, 2])
        a = int(rng.integers(90, 230))
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, a))
    # sol con franjas
    R = 270; cx, cy = W // 2, HOR - 150
    sun = Image.new("RGBA", (2 * R, 2 * R), (0, 0, 0, 0))
    sa = np.zeros((2 * R, 2 * R, 4), np.uint8)
    c1, c2 = np.array(hexc(pal["sun"][0])[:3]), np.array(hexc(pal["sun"][1])[:3])
    yy, xx = np.mgrid[0:2 * R, 0:2 * R]
    t = (yy / (2 * R))[..., None]
    sa[..., :3] = (c1 * (1 - t) + c2 * t).astype(np.uint8)
    inside = (xx - R) ** 2 + (yy - R) ** 2 <= R * R
    stripes = np.ones_like(inside)
    for k in range(7):
        y0 = int(R * 1.05 + k * 30); h = 4 + k * 3
        stripes[y0:y0 + h, :] = False
    sa[..., 3] = (inside & stripes) * 255
    sun = Image.fromarray(sa, "RGBA")
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([cx - R - 60, cy - R - 60, cx + R + 60, cy + R + 60], fill=hexc(pal["sun"][1], 120))
    glow = glow.filter(ImageFilter.GaussianBlur(70))
    base = Image.alpha_composite(base, glow)
    base.alpha_composite(sun, (cx - R, cy - R))
    # skyline
    sky = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sky)
    city = hexc(pal["city"])
    x = 250 if W >= 1920 else 30
    while x < W - (250 if W >= 1920 else 30):
        w = int(rng.integers(40, 120)); h = int(rng.integers(50, 300))
        if abs(x - W / 2) < 300:
            h = int(h * 0.7)
        sd.rectangle([x, HOR - h, x + w, HOR], fill=city)
        if rng.random() < 0.3:
            sd.rectangle([x + w // 2 - 2, HOR - h - 30, x + w // 2 + 2, HOR - h], fill=city)
        for wy in range(HOR - h + 12, HOR - 10, 18):
            for wx in range(x + 8, x + w - 8, 16):
                if rng.random() < 0.18:
                    c = hexc(pal["a2"] if rng.random() < 0.3 else "#ffe9a8", int(rng.integers(90, 200)))
                    sd.rectangle([wx, wy, wx + 5, wy + 7], fill=c)
        x += w + int(rng.integers(0, 14))
    base = Image.alpha_composite(base, sky)
    # palmeras
    pal_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pd = ImageDraw.Draw(pal_layer)
    ps = H / 1080 if H > W else 1.0
    draw_palm(pd, 150, H + 20, int(760 * ps), lean=70, color=(5, 2, 12, 255), rng=rng)
    draw_palm(pd, 40, H + 20, int(560 * ps), lean=40, color=(5, 2, 12, 255), rng=rng)
    draw_palm(pd, W - 140, H + 20, int(820 * ps), lean=-80, color=(5, 2, 12, 255), rng=rng)
    base = Image.alpha_composite(base, pal_layer)
    # línea de horizonte brillante
    hl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(hl).rectangle([0, HOR - 2, W, HOR + 2], fill=hexc(pal["grid"], 255))
    hl = hl.filter(ImageFilter.GaussianBlur(6))
    base = Image.alpha_composite(base, hl)
    # viñeta
    vy, vx = np.mgrid[0:H, 0:W]
    dist = np.sqrt(((vx - W / 2) / (W / 2)) ** 2 + ((vy - H / 2) / (H / 2)) ** 2)
    va = np.clip((dist - 0.75) * 300, 0, 170).astype(np.uint8)
    vig = np.zeros((H, W, 4), np.uint8); vig[..., 3] = va
    base = Image.alpha_composite(base, Image.fromarray(vig, "RGBA"))
    return base


def draw_palm(d, x0, y0, height, lean, color, rng):
    top = (x0 + lean, y0 - height)
    pts = []
    for i in range(161):
        t = i / 160
        x = x0 + lean * t * t
        y = y0 - height * t
        pts.append((x, y))
        r = 22 - 12 * t
        d.ellipse([x - r, y - r, x + r, y + r], fill=color)
    tx, ty = top
    for k in range(9):
        ang = -math.pi + k * (math.pi / 8) + rng.uniform(-0.15, 0.15)
        L = rng.uniform(170, 260)
        prev = (tx, ty)
        for s in range(1, 21):
            t = s / 20
            px = tx + math.cos(ang) * L * t
            py = ty + math.sin(ang) * L * t * 0.6 + (L * 0.55) * t * t
            wdt = max(2, int(26 * (1 - t)))
            d.line([prev, (px, py)], fill=color, width=wdt)
            if s % 2 == 0 and t > 0.15:
                for side in (-1, 1):
                    lx = px + side * 10 * (1 - t) * 3
                    ly = py + 22 * (1 - t) + 8
                    d.line([(px, py), (lx, ly)], fill=color, width=3)
            prev = (px, py)
    d.ellipse([tx - 18, ty - 10, tx + 18, ty + 22], fill=color)


def draw_grid(d, pal, t):
    gc = hexc(pal["grid"])
    n = 18
    speed = 0.6
    for i in range(n):
        u = ((i + t * speed) % n) / n
        y = HOR + (H - HOR) * (u ** 2.3)
        c = mix((0, 0, 0, 255), gc, min(1, 0.25 + u * 1.2))
        d.line([(0, y), (W, y)], fill=c, width=max(1, int(1 + u * 3)))
    vx = W / 2
    for k in range(-16, 17):
        xb = vx + k * 260
        d.line([(vx + k * 18, HOR), (xb, H)], fill=mix((0, 0, 0, 255), gc, 0.75), width=2)


# ------------------------------------------------------------------ utilidades de texto
def text_size(font, s):
    b = font.getbbox(s)
    return b[2] - b[0], b[3] - b[1], b


def wrap(font, s, maxw):
    words = s.split()
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if text_size(font, test)[0] <= maxw or not cur:
            cur = test
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines


def text_img(s, font, fill=(255, 255, 255, 255), stroke=0, stroke_fill=(0, 0, 0, 255), glow=None, glow_r=14, pad=30, align="left", maxw=None, spacing=10):
    lines = wrap(font, s, maxw) if maxw else [s]
    asc, desc = font.getmetrics()
    lh = asc + desc
    widths = [text_size(font, l)[0] + 2 * stroke for l in lines]
    tw = max(widths)
    th = lh * len(lines) + spacing * (len(lines) - 1) + 2 * stroke
    im = Image.new("RGBA", (tw + 2 * pad, th + 2 * pad), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for i, l in enumerate(lines):
        lw = widths[i]
        x = pad + (tw - lw) // 2 if align == "center" else pad
        y = pad + i * (lh + spacing)
        d.text((x + stroke, y + stroke), l, font=font, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)
    if glow:
        g = Image.new("RGBA", im.size, (0, 0, 0, 0))
        gd = ImageDraw.Draw(g)
        for i, l in enumerate(lines):
            lw = widths[i]
            x = pad + (tw - lw) // 2 if align == "center" else pad
            y = pad + i * (lh + spacing)
            gd.text((x + stroke, y + stroke), l, font=font, fill=glow, stroke_width=stroke + 6)
        g = g.filter(ImageFilter.GaussianBlur(glow_r))
        im = Image.alpha_composite(g, im)
    return im


def fit_font(name, s, maxw, start, minsize=40):
    size = start
    while size > minsize and text_size(F(name, size), s)[0] > maxw:
        size -= 4
    return F(name, size)


def rounded(size, radius, fill, outline=None, width=0, shadow=False):
    w, h = size
    pad = 30 if shadow else 0
    im = Image.new("RGBA", (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
    if shadow:
        sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).rounded_rectangle([pad, pad + 10, pad + w, pad + h + 10], radius, fill=(0, 0, 0, 150))
        im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(14)))
    ImageDraw.Draw(im).rounded_rectangle([pad, pad, pad + w, pad + h], radius, fill=fill, outline=outline, width=width)
    return im


# ------------------------------------------------------------------ elementos animados
class El:
    def __init__(self, img, x, y, t0, anim="up", dur=0.45, sfx=None, center=False):
        self.img = img
        if center:
            x -= img.width // 2
        self.x, self.y, self.t0, self.anim, self.dur, self.sfx = int(x), int(y), t0, anim, dur, sfx
        self.dyn = None  # función (t) -> img opcional

    def draw(self, frame, t, fade):
        if t < self.t0:
            return
        p = min(1.0, (t - self.t0) / self.dur)
        e = 1 - (1 - p) ** 3
        img = self.dyn(t) if self.dyn else self.img
        x, y = self.x, self.y
        alpha = e * fade
        if self.anim == "up":
            y += int((1 - e) * 50)
        elif self.anim == "left":
            x -= int((1 - e) * 80)
        elif self.anim == "pop" and p < 1:
            s = 0.6 + 0.4 * e + 0.08 * math.sin(e * math.pi)
            nw, nh = max(1, int(img.width * s)), max(1, int(img.height * s))
            img = img.resize((nw, nh), Image.BILINEAR)
            x += (self.img.width - nw) // 2; y += (self.img.height - nh) // 2
        if alpha < 0.999:
            a = img.getchannel("A").point(lambda v: int(v * alpha))
            img = img.copy(); img.putalpha(a)
        frame.alpha_composite(img, (max(0, x), max(0, y)), (max(0, -x), max(0, -y)))


def panel(pal, x0=150, y0=110, x1=W - 150, y1=850):
    return rounded((x1 - x0, y1 - y0), 36, (8, 4, 20, 200), outline=hexc(pal["a2"], 160), width=3, shadow=True)


def heading_img(s, pal, size=92):
    f = fit_font("anton", s.upper(), 1480, size)
    return text_img(s.upper(), f, fill=hexc(pal["a1"]), glow=hexc(pal["a1"], 140), glow_r=12)


def reveal_times(scene, n_items):
    st = scene["_sent_starts"]
    if len(st) >= n_items + 1:
        return [st[i + 1] for i in range(n_items)]
    t0 = scene["_start"] + 0.6
    span = (scene["_end"] - t0) * 0.7
    return [t0 + span * i / max(1, n_items) for i in range(n_items)]


def build_elements(scene, pal):
    typ = scene["type"]; s0 = scene["_start"]
    els = []
    a1, a2 = hexc(pal["a1"]), hexc(pal["a2"])

    if typ == "title":
        k = text_img(scene["kicker"], F("bebas", 58), fill=(15, 5, 25, 255), pad=0)
        badge = rounded((k.width + 60, k.height + 26), 22, a1)
        badge.alpha_composite(k, (30, 10))
        els.append(El(badge, W // 2, 190, s0 + 0.1, "pop", center=True, sfx="pop"))
        f = fit_font("anton", scene["title"], 1650, 170, 90)
        tt = text_img(scene["title"], f, stroke=6, stroke_fill=(10, 0, 20, 255), glow=a1, glow_r=22, align="center", maxw=1650)
        els.append(El(tt, W // 2, 300, s0 + 0.3, "up", 0.6, center=True))
        sub = text_img(scene["sub"], F("xbold", 46), stroke=3, align="center", maxw=1500)
        els.append(El(sub, W // 2, 300 + tt.height - 20, s0 + 0.7, "up", center=True))

    elif typ == "stat":
        els.append(El(panel(pal, 360, 150, W - 360, 880), 330, 120, s0, "fade", 0.35))
        lab = text_img(scene["label"], F("bebas", 80), fill=a2, glow=hexc(pal["a2"], 120))
        els.append(El(lab, W // 2, 190, s0 + 0.15, "up", center=True))
        f = fit_font("anton", scene["value"], 1100, 250, 120)
        val = text_img(scene["value"], f, stroke=6, stroke_fill=(10, 0, 20, 255), glow=a1, glow_r=26)
        els.append(El(val, W // 2, 300, s0 + 0.35, "pop", 0.55, center=True, sfx="pop"))
        sub = text_img(scene["sub"], F("bold", 44), align="center", maxw=1100)
        els.append(El(sub, W // 2, 290 + val.height - 30, s0 + 0.7, "up", center=True))

    elif typ in ("bullets", "checklist"):
        els.append(El(panel(pal), 120, 80, s0, "fade", 0.35))
        els.append(El(heading_img(scene["heading"], pal), 210, 120, s0 + 0.1, "left"))
        items = scene["items"]; n = len(items)
        top, bottom = 300, 830
        step = min(140, (bottom - top) // n)
        fs = 54 if n <= 4 else 46
        times = reveal_times(scene, n)
        for i, it in enumerate(items):
            row = Image.new("RGBA", (1560, step), (0, 0, 0, 0))
            d = ImageDraw.Draw(row)
            cy = step // 2
            if typ == "bullets":
                d.ellipse([10, cy - 34, 78, cy + 34], fill=a1)
                num = str(i + 1)
                nf = F("anton", 44); tw, th, bb = text_size(nf, num)
                d.text((44 - tw // 2 - bb[0], cy - th // 2 - bb[1]), num, font=nf, fill=(15, 5, 25, 255))
            else:
                d.rounded_rectangle([10, cy - 32, 74, cy + 32], 14, fill=a2)
                d.line([(24, cy), (38, cy + 15), (62, cy - 16)], fill=(15, 5, 25, 255), width=9)
            txt = text_img(it, F("bold", fs), pad=0, maxw=1400)
            row.alpha_composite(txt, (110, max(0, cy - txt.height // 2)))
            els.append(El(row, 210, top + i * step, times[i], "left", sfx="pop"))

    elif typ == "compare":
        els.append(El(heading_img(scene["heading"], pal, 96), W // 2, 110, s0 + 0.05, "up", center=True))
        cols = scene["cols"]; n = len(cols)
        gap = 50; total = 1640
        cw = (total - gap * (n - 1)) // n
        ch = 600
        times = reveal_times(scene, n)
        colors = [a1, a2, hexc("#ffffff")]
        def need(c):
            h = 140 + 40
            if c.get("big"):
                h += text_img(c["big"], fit_font("anton", c["big"], cw - 60, 130, 60), pad=10).height + 10
            for ln in c["lines"]:
                h += text_img(ln, F("bold", 40 if n == 2 else 36), align="center", maxw=cw - 50, pad=0).height + 26
            return h
        ch = min(560, max(380, max(need(c) for c in cols)))
        for i, c in enumerate(cols):
            card = rounded((cw, ch), 30, (8, 4, 20, 220), outline=colors[i % 3], width=4, shadow=True)
            pad = 30
            d = ImageDraw.Draw(card)
            d.rounded_rectangle([pad, pad, pad + cw, pad + 110], 30, fill=colors[i % 3])
            d.rectangle([pad, pad + 60, pad + cw, pad + 110], fill=colors[i % 3])
            tf = fit_font("bebas", c["title"], cw - 40, 72, 36)
            t_img = text_img(c["title"], tf, fill=(15, 5, 25, 255), pad=0)
            card.alpha_composite(t_img, (pad + (cw - t_img.width) // 2, pad + 55 - t_img.height // 2))
            y = pad + 140
            if c.get("big"):
                bf = fit_font("anton", c["big"], cw - 60, 130, 60)
                b_img = text_img(c["big"], bf, glow=colors[i % 3], glow_r=16, pad=10)
                card.alpha_composite(b_img, (pad + (cw - b_img.width) // 2, y))
                y += b_img.height + 10
            for ln in c["lines"]:
                l_img = text_img(ln, F("bold", 40 if n == 2 else 36), align="center", maxw=cw - 50, pad=0)
                card.alpha_composite(l_img, (pad + (cw - l_img.width) // 2, y))
                y += l_img.height + 26
            x = (W - total) // 2 + i * (cw + gap) - 30
            els.append(El(card, x, max(240, 520 - ch // 2 - 30), times[i], "up", 0.5, sfx="pop"))

    elif typ == "clock":
        els.append(El(panel(pal), 120, 80, s0, "fade", 0.35))
        els.append(El(heading_img(scene["heading"], pal), 210, 120, s0 + 0.1, "left"))
        rows = scene["rows"]; n = len(rows)
        top = 300; step = min(115, 520 // n)
        times = reveal_times(scene, n)
        for i, (place, tm) in enumerate(rows):
            row = Image.new("RGBA", (1500, step), (0, 0, 0, 0))
            d = ImageDraw.Draw(row)
            d.line([(0, step - 4), (1500, step - 4)], fill=hexc(pal["a2"], 90), width=2)
            p_img = text_img(place, F("bold", 48), pad=0)
            row.alpha_composite(p_img, (0, (step - p_img.height) // 2 - 4))
            tf = fit_font("bebas", tm, 760, 70, 40)
            t_img = text_img(tm, tf, fill=a1, pad=0)
            row.alpha_composite(t_img, (1500 - t_img.width, (step - t_img.height) // 2 - 4))
            els.append(El(row, 210, top + i * step, times[i], "left", sfx="pop"))

    elif typ == "timeline":
        els.append(El(panel(pal), 120, 80, s0, "fade", 0.35))
        els.append(El(heading_img(scene["heading"], pal), 210, 120, s0 + 0.1, "left"))
        ev = scene["events"]; n = len(ev)
        x0, x1, y = 380, W - 380, 560
        line = Image.new("RGBA", (x1 - x0 + 40, 40), (0, 0, 0, 0))
        ImageDraw.Draw(line).rounded_rectangle([0, 14, x1 - x0 + 40, 26], 6, fill=hexc(pal["a2"], 200))
        els.append(El(line, x0 - 20, y - 20, s0 + 0.2, "left", 0.6))
        times = reveal_times(scene, n)
        for i, (date, lab) in enumerate(ev):
            cx = x0 + (x1 - x0) * (i / max(1, n - 1)) if n > 1 else W // 2
            node = Image.new("RGBA", (420, 420), (0, 0, 0, 0))
            d = ImageDraw.Draw(node)
            d.ellipse([180, 180, 240, 240], fill=a1, outline=(255, 255, 255, 255), width=5)
            df = fit_font("anton", date, 400, 76, 40)
            dt = text_img(date, df, fill=(255, 255, 255, 255), glow=a1, glow_r=10, pad=6)
            node.alpha_composite(dt, ((420 - dt.width) // 2, 165 - dt.height))
            lt = text_img(lab, F("bold", 38), align="center", maxw=380, pad=0)
            node.alpha_composite(lt, ((420 - lt.width) // 2, 265))
            els.append(El(node, cx - 210, y - 210, times[i], "pop", 0.45, sfx="pop"))

    elif typ == "warning":
        els.append(El(panel(pal, 200, 170, W - 200, 800), 170, 140, s0, "fade", 0.35))
        tri = Image.new("RGBA", (300, 270), (0, 0, 0, 0))
        d = ImageDraw.Draw(tri)
        d.polygon([(150, 10), (290, 255), (10, 255)], fill=hexc("#ffcc00"))
        d.polygon([(150, 40), (262, 238), (38, 238)], fill=(20, 10, 0, 255))
        ef = F("anton", 150); tw, th, bb = text_size(ef, "!")
        d.text((150 - tw // 2 - bb[0], 150 - th // 2 - bb[1] + 15), "!", font=ef, fill=hexc("#ffcc00"))
        g = tri.filter(ImageFilter.GaussianBlur(10))
        tri = Image.alpha_composite(g, tri)
        els.append(El(tri, 290, 300, s0 + 0.15, "pop", 0.5, sfx="pop"))
        tf = fit_font("anton", scene["title"], 1050, 96, 50)
        els.append(El(text_img(scene["title"], tf, fill=hexc("#ffcc00"), glow=hexc("#ffcc00", 120)), 650, 240, s0 + 0.3, "left"))
        els.append(El(text_img(scene["text"], F("bold", 46), maxw=1000, spacing=14), 650, 400, s0 + 0.55, "up"))

    elif typ == "map":
        els.append(El(panel(pal), 120, 80, s0, "fade", 0.35))
        els.append(El(heading_img(scene["heading"], pal), 210, 110, s0 + 0.1, "left"))
        mp, pins = map_image(pal)
        mx, my = 230, 230
        els.append(El(mp, mx, my, s0 + 0.2, "fade", 0.6))
        regs = scene["regions"]; n = len(regs)
        times = reveal_times(scene, n)
        rows_norm, rows_act = [], []
        for i, r in enumerate(regs):
            for act, store in ((False, rows_norm), (True, rows_act)):
                row = Image.new("RGBA", (660, 92), (0, 0, 0, 0))
                d = ImageDraw.Draw(row)
                if act:
                    d.rounded_rectangle([0, 6, 660, 86], 20, fill=hexc(pal["a1"], 235))
                col = (15, 5, 25, 255) if act else (255, 255, 255, 255)
                nf = F("anton", 44)
                d.text((24, 18), f"{i+1}", font=nf, fill=col if act else a2)
                rt = text_img(r.upper(), F("bebas", 64), fill=col, pad=0)
                row.alpha_composite(rt, (90, 46 - rt.height // 2))
                store.append(row)
        ends = times[1:] + [scene["_end"]]
        for i in range(n):
            e = El(rows_norm[i], 1050, 230 + i * 98, times[i], "left", sfx="pop")
            ti, te = times[i], ends[i]
            e.dyn = (lambda ti, te, i: (lambda t: rows_act[i] if ti <= t < te else rows_norm[i]))(ti, te, i)
            els.append(e)
        # pin pulsante dinámico
        pin_layer_size = (mp.width, mp.height)

        def pin_dyn(t, times=times, ends=ends, pins=pins, regs=regs):
            im = Image.new("RGBA", pin_layer_size, (0, 0, 0, 0))
            d = ImageDraw.Draw(im)
            for i, r in enumerate(regs):
                if t < times[i]:
                    continue
                px, py = pins[r]
                active = times[i] <= t < ends[i]
                rr = 13
                d.ellipse([px - rr, py - rr, px + rr, py + rr], fill=a1 if active else a2, outline=(255, 255, 255, 255), width=3)
                if active:
                    ph = ((t - times[i]) * 1.4) % 1
                    R = 16 + 50 * ph
                    d.ellipse([px - R, py - R, px + R, py + R], outline=hexc(pal["a1"], int(255 * (1 - ph))), width=5)
            return im
        pe = El(Image.new("RGBA", pin_layer_size), mx, my, s0 + 0.2, "fade", 0.3)
        pe.dyn = pin_dyn
        els.append(pe)
        note = text_img("Ilustración orientativa · no es el mapa oficial", F("semi", 24), fill=(255, 255, 255, 150), pad=0)
        els.append(El(note, mx + 20, my + mp.height - 10, s0 + 0.5, "fade"))

    elif typ == "outro":
        f = fit_font("anton", scene["title"], 1600, 140, 70)
        tt = text_img(scene["title"], f, stroke=6, stroke_fill=(10, 0, 20, 255), glow=a1, glow_r=22, align="center", maxw=1600)
        els.append(El(tt, W // 2, 170, s0 + 0.1, "up", 0.6, center=True))
        els.append(El(text_img(scene["sub"], F("xbold", 50), stroke=3), W // 2, 170 + tt.height - 10, s0 + 0.4, "up", center=True))
        btn = rounded((640, 140), 70, hexc("#ff1f3d"), shadow=True)
        bt = text_img("SUSCRÍBETE", F("anton", 84), pad=0)
        btn.alpha_composite(bt, (30 + (640 - bt.width) // 2, 30 + (140 - bt.height) // 2 - 6))
        els.append(El(btn, W // 2 - 80, 600, s0 + 0.8, "pop", 0.5, center=True, sfx="pop"))
        bell = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
        d = ImageDraw.Draw(bell)
        d.pieslice([30, 20, 130, 130], 180, 360, fill=(255, 255, 255, 255))
        d.rectangle([30, 75, 130, 115], fill=(255, 255, 255, 255))
        d.polygon([(18, 125), (142, 125), (130, 105), (30, 105)], fill=(255, 255, 255, 255))
        d.ellipse([66, 122, 94, 148], fill=(255, 255, 255, 255))
        d.ellipse([72, 8, 88, 24], fill=(255, 255, 255, 255))
        els.append(El(bell, W // 2 + 330, 600, s0 + 1.1, "pop", 0.5, sfx="pop"))
    return els


# Leonida estilizada (ilustración propia, NO el mapa oficial)
MAP_POLY = [(0.02, 0.06), (0.30, 0.03), (0.52, 0.08), (0.62, 0.05), (0.80, 0.08), (0.84, 0.20), (0.86, 0.36),
            (0.90, 0.52), (0.93, 0.66), (0.90, 0.80), (0.84, 0.86), (0.76, 0.84), (0.70, 0.76), (0.62, 0.70),
            (0.56, 0.58), (0.52, 0.44), (0.48, 0.30), (0.40, 0.22), (0.28, 0.20), (0.14, 0.22), (0.04, 0.18)]
MAP_PINS = {"Vice City": (0.86, 0.68), "Leonida Keys": (0.58, 0.93), "Grassrivers": (0.72, 0.66),
            "Port Gellhorn": (0.18, 0.13), "Ambrosia": (0.64, 0.30), "Mount Kalaga": (0.42, 0.10)}


def map_image(pal):
    mw, mh = 780, 600
    im = Image.new("RGBA", (mw, mh), (0, 0, 0, 0))
    poly = [(x * mw, y * mh) for x, y in MAP_POLY]
    glow = Image.new("RGBA", (mw, mh), (0, 0, 0, 0))
    ImageDraw.Draw(glow).polygon(poly, outline=hexc(pal["a2"]), width=14)
    im = Image.alpha_composite(im, glow.filter(ImageFilter.GaussianBlur(12)))
    d = ImageDraw.Draw(im)
    d.polygon(poly, fill=(20, 60, 70, 255), outline=hexc(pal["a2"]), width=4)
    # pantano / interior
    d.ellipse([0.60 * mw, 0.58 * mh, 0.80 * mw, 0.74 * mh], fill=(40, 90, 60, 255))
    d.ellipse([0.55 * mw, 0.20 * mh, 0.74 * mw, 0.40 * mh], fill=(55, 75, 70, 255))
    d.ellipse([0.33 * mw, 0.05 * mh, 0.50 * mw, 0.18 * mh], fill=(40, 70, 50, 255))
    # cayos
    for i in range(9):
        t = i / 8
        x = (0.80 - 0.32 * t) * mw; y = (0.88 + 0.06 * math.sin(t * math.pi)) * mh
        d.ellipse([x - 9, y - 5, x + 9, y + 5], fill=(20, 60, 70, 255), outline=hexc(pal["a2"]), width=2)
    pins = {k: (int(x * mw), int(y * mh)) for k, (x, y) in MAP_PINS.items()}
    return im, pins


# ------------------------------------------------------------------ subtítulos
def split_sub(text, maxc=62):
    if len(text) <= maxc:
        return [text]
    parts = re.split(r"(?<=[,.;:?!])\s+", text)
    out, cur = [], ""
    for p in parts:
        if len(cur) + len(p) + 1 <= maxc:
            cur = (cur + " " + p).strip()
        else:
            if cur:
                out.append(cur)
            if len(p) <= maxc:
                cur = p
            else:
                words = p.split(); cur = ""
                for w in words:
                    if len(cur) + len(w) + 1 <= maxc:
                        cur = (cur + " " + w).strip()
                    else:
                        out.append(cur); cur = w
    if cur:
        out.append(cur)
    return out


_subcache = {}


def sub_img(s):
    if s not in _subcache:
        _subcache[s] = text_img(s, F("xbold", 46), stroke=5, stroke_fill=(0, 0, 0, 255), align="center", maxw=1760, pad=10, spacing=6)
    return _subcache[s]


# ------------------------------------------------------------------ montaje
def prepare(video):
    vid = video["id"]
    bdir = os.path.join(BUILD, vid); os.makedirs(bdir, exist_ok=True)
    import tts
    t = 0.3
    voice = []
    subs = []
    reveals = []
    for si, sc in enumerate(video["scenes"]):
        sc["_start"] = t
        t += 0.45
        starts = []
        for k, s in enumerate(sc["say"]):
            key = hashlib.md5((s + str(tts.SID) + str(tts.SPEED)).encode()).hexdigest()[:12]
            fn = os.path.join(bdir, f"s{si:02d}_{k:02d}_{key}.wav")
            if not os.path.exists(fn):
                x, sr = tts.synth(s)
                sf.write(fn, x, sr)
            x, sr = sf.read(fn, dtype="float32")
            x48 = resample_poly(x, 48000, sr).astype(np.float32)
            dur = len(x48) / 48000
            starts.append(t)
            voice.append((t, x48))
            chunks = split_sub(s)
            tot = sum(len(c) for c in chunks)
            ct = t
            for c in chunks:
                cd = dur * len(c) / tot
                subs.append((ct, ct + cd, c))
                ct += cd
            t += dur + 0.32
        t += 0.35
        if sc["type"] == "outro":
            t += OUTRO_TAIL
        sc["_sent_starts"] = starts
        sc["_end"] = t
    total = t + 0.2
    return bdir, voice, subs, total


def build_audio(video, voice, total, sfx_times, path):
    N = int(total * 48000) + 48000
    v = np.zeros(N, np.float32)
    for st, x in voice:
        i = int(st * 48000); v[i:i + len(x)] += x[: N - i]
    v /= (np.max(np.abs(v)) + 1e-9); v *= 0.92
    m = music.track(video["palette"], total + 1, seed=len(video["id"]))
    m = np.pad(m, (0, max(0, N - len(m))))[:N]
    k = int(0.35 * 48000)
    c = np.concatenate([[0.0], np.cumsum((np.abs(v) > 0.02).astype(np.float64))])
    idx = np.arange(N)
    lo = np.clip(idx - k // 2, 0, N); hi = np.clip(idx + k // 2, 0, N)
    act = ((c[hi] - c[lo]) / k).astype(np.float32)
    act = np.clip(act * 4, 0, 1)
    gain = 0.20 - 0.13 * act
    out = v + m * gain
    wh, pp = music.whoosh(), music.pop()
    for kind, tt in sfx_times:
        snd = wh * 0.22 if kind == "whoosh" else pp * 0.10
        i = int(tt * 48000)
        if i < N:
            out[i:i + len(snd)] += snd[: N - i]
    out /= (np.max(np.abs(out)) + 1e-9); out *= 0.95
    sf.write(path, out[: int(total * 48000)], 48000, subtype="PCM_16")


def render(video, preview=False):
    t_start = time.time()
    pal = PALETTES[video["palette"]]
    bdir, voice, subs, total = prepare(video)
    print(f"[{video['id']}] duración {total:.1f}s", flush=True)
    bg = build_background(pal, seed=len(video["id"]) * 3)
    wm = text_img(CHANNEL, F("bebas", 44), fill=hexc(pal["a2"]), glow=hexc(pal["a2"], 140), glow_r=8, pad=10)
    scenes = video["scenes"]
    all_els = []
    sfx_times = []
    for sc in scenes:
        els = build_elements(sc, pal)
        all_els.append(els)
        sfx_times.append(("whoosh", max(0, sc["_start"] - 0.15)))
        for e in els:
            if e.sfx == "pop":
                sfx_times.append(("pop", e.t0))
    wav = os.path.join(bdir, "mix.wav")
    build_audio(video, voice, total, sfx_times, wav)
    os.makedirs(OUT_VID, exist_ok=True)
    out = os.path.join(OUT_VID, video["id"] + (".preview" if preview else "") + ".mp4")
    nframes = int(total * FPS)
    step = 1
    if preview:
        step = 3
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS / step), "-i", "-",
           "-i", wav, "-c:v", "libx264", "-preset", "medium" if not preview else "ultrafast", "-crf", "20", "-pix_fmt", "yuv420p",
           "-threads", os.environ.get("X264_THREADS", "2"),
           "-c:a", "aac", "-b:a", "192k", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", "-movflags", "+faststart", "-shortest", out]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    rng = np.random.default_rng(3)
    parts = [[rng.uniform(0, W), rng.uniform(0, H), rng.uniform(10, 40), rng.uniform(1, 3)] for _ in range(45)]
    a2 = hexc(pal["a2"])
    si = 0
    for fi in range(0, nframes, step):
        t = fi / FPS
        while si + 1 < len(scenes) and t >= scenes[si + 1]["_start"] - 0.05:
            si += 1
        frame = bg.copy()
        d = ImageDraw.Draw(frame)
        draw_grid(d, pal, t)
        for p in parts:
            y = (p[1] - t * p[2]) % H
            x = p[0] + 12 * math.sin(t * 0.7 + p[1])
            r = p[3]
            d.ellipse([x - r, y - r, x + r, y + r], fill=(a2[0], a2[1], a2[2], 150))
        sc = scenes[si]
        fade = 1.0
        if t > sc["_end"] - 0.3:
            fade = max(0.0, (sc["_end"] - t) / 0.3)
        for e in all_els[si]:
            e.draw(frame, t, fade)
        # flash de transición
        dt = t - sc["_start"]
        if 0 <= dt < 0.18 and si > 0:
            fl = Image.new("RGBA", (W, H), hexc(pal["a1"], int(90 * (1 - dt / 0.18))))
            frame = Image.alpha_composite(frame, fl)
        frame.alpha_composite(wm, (40, 24))
        for (a, b, s) in subs:
            if a <= t < b:
                im = sub_img(s)
                frame.alpha_composite(im, ((W - im.width) // 2, 1030 - im.height))
                break
        d = ImageDraw.Draw(frame)
        d.rectangle([0, H - 6, int(W * t / total), H], fill=hexc(pal["a1"]))
        proc.stdin.write(frame.convert("RGB").tobytes())
        if fi % (FPS * 20) == 0:
            print(f"[{video['id']}] {t:6.1f}/{total:.1f}s  ({time.time()-t_start:.0f}s)", flush=True)
    proc.stdin.close(); proc.wait()
    meta = dict(id=video["id"], duration=total, subs=subs,
                chapters=[(sc["_start"], sc.get("title") or sc.get("heading") or sc["type"]) for sc in scenes])
    with open(os.path.join(bdir, "meta.json"), "w") as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)
    print(f"[{video['id']}] OK {out} en {time.time()-t_start:.0f}s", flush=True)
    return meta


def thumbnail(video):
    pal = PALETTES[video["palette"]]
    bg = build_background(pal, seed=len(video["id"]) * 3)
    d = ImageDraw.Draw(bg); draw_grid(d, pal, 0.3)
    # oscurecer
    ov = np.zeros((H, W, 4), np.uint8)
    xs = np.linspace(1, 0, W)[None, :]
    ov[..., 3] = (np.clip(xs * 1.2, 0, 1) * 170).astype(np.uint8)
    im = Image.alpha_composite(bg, Image.fromarray(ov, "RGBA"))
    th = video["thumb"]
    top = text_img(th["top"], fit_font("anton", th["top"], 1250, 170, 80), stroke=8, stroke_fill=(0, 0, 0, 255), pad=10)
    big = text_img(th["big"], fit_font("anton", th["big"], 1450, 290, 120), fill=hexc("#ffe14d"), stroke=12, stroke_fill=(0, 0, 0, 255), glow=hexc(pal["a1"], 220), glow_r=24, pad=20)
    im.alpha_composite(top, (90, 120))
    im.alpha_composite(big, (70, 120 + top.height - 40))
    bt = text_img(th["badge"], fit_font("anton", th["badge"], 520, 130, 60), pad=0)
    badge = rounded((bt.width + 80, bt.height + 50), 30, hexc("#ff1f3d"), outline=(255, 255, 255, 255), width=6, shadow=True)
    badge.alpha_composite(bt, (70, 50))
    badge = badge.rotate(6, expand=True, resample=Image.BICUBIC)
    im.alpha_composite(badge, (W - badge.width - 60, 60))
    note = text_img(th["note"], F("anton", 84), fill=(15, 5, 25, 255), pad=0)
    band = rounded((note.width + 80, note.height + 40), 16, hexc(pal["a2"]))
    band.alpha_composite(note, (40, 14))
    im.alpha_composite(band, (90, H - band.height - 80))
    os.makedirs(OUT_THUMB, exist_ok=True)
    out = os.path.join(OUT_THUMB, video["id"] + ".jpg")
    im.convert("RGB").resize((1280, 720), Image.LANCZOS).save(out, quality=92)
    return out


if __name__ == "__main__":
    key = sys.argv[1]
    v = VIDEOS[int(key)] if key.isdigit() else next(x for x in VIDEOS if x["id"] == key)
    if "--thumb" in sys.argv:
        print(thumbnail(v)); sys.exit()
    if "--frames" in sys.argv:  # capturas de prueba
        pal = PALETTES[v["palette"]]
        bdir, voice, subs, total = prepare(v)
        bg = build_background(pal, seed=len(v["id"]) * 3)
        for si, sc in enumerate(v["scenes"]):
            fr = bg.copy(); draw_grid(ImageDraw.Draw(fr), pal, 1.0)
            t = sc["_end"] - 0.5
            for e in build_elements(sc, pal):
                e.draw(fr, t, 1.0)
            for (a, b, s) in subs:
                if a <= sc["_sent_starts"][-1] + 0.1 < b:
                    im = sub_img(s); fr.alpha_composite(im, ((W - im.width) // 2, 1030 - im.height))
            fr.convert("RGB").resize((960, 540)).save(os.path.join(bdir, f"frame{si:02d}.jpg"))
        print(bdir); sys.exit()
    render(v, preview="--preview" in sys.argv)
    thumbnail(v)
