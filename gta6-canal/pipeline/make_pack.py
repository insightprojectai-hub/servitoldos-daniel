# -*- coding: utf-8 -*-
"""Genera PUBLICACION.md (títulos, descripciones con capítulos, etiquetas,
horario) y la carpeta guiones/ a partir de videos.py + meta.json del render."""
import os, json, re
from videos import VIDEOS, CHANNEL

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
BUILD = os.environ.get("BUILD_DIR", "/tmp/claude-0/build/")

SCHEDULE = {
    "01-hora-lanzamiento":   "MIÉRCOLES 18 · 10:00 (recomendado) — si no, jueves 19 · 00:05",
    "10-resumen-gta6":  "Jueves 19 · 00:05",
    "09-antes-de-jugar":     "Jueves 19 · 00:10",
    "03-tamano-precarga":    "Jueves 19 · 08:00",
    "06-mapa-leonida":       "Jueves 19 · 10:00",
    "07-lucia-jason-historia": "Jueves 19 · 12:00",
    "05-que-consola":        "Jueves 19 · 14:00",
    "02-standard-vs-ultimate": "Jueves 19 · 16:00",
    "04-gta6-pc":            "Jueves 19 · 18:00",
    "08-historia-espera":    "Jueves 19 · 20:00",
}

TAGS_BASE = ["gta 6", "gta vi", "grand theft auto 6", "gta 6 español", "gta 6 lanzamiento", "leonida", "vice city", "rockstar games", "gta6"]
TAGS = {
    "01-hora-lanzamiento": ["cuando sale gta 6", "gta 6 hora de lanzamiento", "gta 6 a que hora sale", "gta 6 nueva zelanda", "como jugar gta 6 antes", "gta 6 españa", "gta 6 mexico"],
    "02-standard-vs-ultimate": ["gta 6 precio", "gta 6 ediciones", "gta 6 ultimate edition", "gta 6 standard edition", "gta 6 reserva", "gta 6 bonus reserva", "comprar gta 6"],
    "03-tamano-precarga": ["gta 6 precarga", "gta 6 tamaño", "gta 6 cuanto ocupa", "como descargar gta 6 en ps5", "gta 6 212 gb", "gta 6 xbox series s"],
    "04-gta6-pc": ["gta 6 pc", "cuando sale gta 6 para pc", "como jugar gta 6 en pc", "como jugar gta 6 sin consola", "gta 6 pc fecha", "gta 6 requisitos pc"],
    "05-que-consola": ["gta 6 30 fps", "gta 6 ps5 pro", "gta 6 xbox series s", "que consola comprar para gta 6", "gta 6 60 fps", "gta 6 ps5"],
    "06-mapa-leonida": ["gta 6 mapa", "gta 6 leonida", "gta 6 map", "gta 6 regiones", "gta 6 vice city mapa"],
    "07-lucia-jason-historia": ["gta 6 lucia", "jason gta 6", "gta 6 personajes", "gta 6 historia", "lucia caminos", "jason duval"],
    "08-historia-espera": ["gta 6 historia", "gta 6 trailer", "gta 6 retraso", "gta 6 filtracion", "gta 6 trailer 3"],
    "09-antes-de-jugar": ["gta 6 consejos", "gta 6 antes de jugar", "gta 6 ajustes", "gta 6 hdr", "gta 6 spoilers"],
    "10-resumen-gta6": ["gta 6 todo lo que sabemos", "gta 6 resumen", "gta 6 info", "gta 6 news", "gta 6 detalles"],
}

DISCLAIMER = ("Canal de fans no oficial. Sin afiliación con Rockstar Games ni Take-Two Interactive. "
              "Grand Theft Auto y GTA son marcas de Take-Two Interactive. Ilustraciones, música y locución originales del canal "
              "(voz sintética). Información recopilada de fuentes públicas a 17/11/2026; puede cambiar.")


def ts(s):
    s = int(s)
    return f"{s//60}:{s%60:02d}"


def main():
    os.makedirs(os.path.join(ROOT, "guiones"), exist_ok=True)
    md = ["# Paquete de publicación — canal GTA 6\n",
          f"Canal: **{CHANNEL}** (nombre provisional, cámbialo si quieres: también aparece como marca de agua en `pipeline/videos.py`).\n",
          "Horario en hora peninsular española. Sube los vídeos como **programados** en YouTube Studio para que salgan solos.\n",
          "\n## Orden y horario\n", "| # | Vídeo | Duración | Publicar |", "|---|---|---|---|"]
    order = list(SCHEDULE.keys())
    metas = {}
    for v in VIDEOS:
        mp = os.path.join(BUILD, v["id"], "meta.json")
        metas[v["id"]] = json.load(open(mp)) if os.path.exists(mp) else None
    for vid in order:
        v = next(x for x in VIDEOS if x["id"] == vid)
        m = metas[vid]
        md.append(f"| {vid[:2]} | {v['title'].replace('|', '\\|')} | {ts(m['duration']) if m else '?'} | {SCHEDULE[vid]} |")
    md.append("")
    for v in VIDEOS:
        m = metas[v["id"]]
        md.append(f"\n---\n\n## {v['id']}\n")
        md.append(f"- **Archivo:** `videos/{v['id']}.mp4`  ·  **Miniatura:** `miniaturas/{v['id']}.jpg`")
        md.append(f"- **Publicar:** {SCHEDULE[v['id']]}\n")
        md.append(f"**Título**\n\n```\n{v['title']}\n```\n")
        hook = v["scenes"][0]["say"][0] + " " + v["scenes"][0]["say"][1]
        chapters = ""
        if m:
            seen = set(); ch = []
            for (t, name), scx in zip(m["chapters"], v["scenes"]):
                name = (scx.get("label") if scx["type"] == "stat" else name).strip()
                if sum(c.isupper() for c in name) > sum(c.islower() for c in name):
                    low = name.lower()
                    i = next((k for k, ch_ in enumerate(low) if ch_.isalpha()), 0)
                    name = low[:i] + low[i].upper() + low[i + 1:]
                    for pn in ["Leonida", "GTA", "Vice City", "Xbox", "PS5", "PC", "Lucía", "Jason", "Duval", "Caminos",
                               "España", "Nueva Zelanda", "Standard", "Ultimate", "Rockstar", "GB", "Series", "Pro", "TV"]:
                        name = re.sub(r"\b" + re.escape(pn.lower()) + r"\b", pn, name, flags=re.I)
                if name in seen:
                    continue
                seen.add(name)
                ch.append([0 if not ch else t, name])
            # YouTube: capítulos de al menos 10 s
            ends = [c[0] for c in ch[1:]] + [m["duration"]]
            ok = [c for c, e in zip(ch, ends) if e - c[0] >= 10 or c is ch[0]]
            chapters = "\n".join(f"{ts(t)} {n}" for t, n in ok)
        tags = TAGS_BASE + TAGS.get(v["id"], [])
        desc = (f"{hook}\n\n"
                f"⏱️ Capítulos\n{chapters}\n\n"
                f"🔔 Suscríbete para tenerlo todo de GTA 6 desde el día 1.\n\n"
                f"#GTA6 #GTAVI #Leonida\n\n{DISCLAIMER}")
        md.append(f"**Descripción**\n\n```\n{desc}\n```\n")
        md.append(f"**Etiquetas** (pegar en YouTube Studio)\n\n```\n{', '.join(tags)}\n```\n")
        # guion
        g = [f"# {v['title']}\n", f"Paleta: {v['palette']} · Miniatura: {v['thumb']}\n"]
        for i, sc in enumerate(v["scenes"]):
            name = sc.get("title") or sc.get("heading") or sc["type"]
            start = f" — {ts(sc_start(m, i))}" if m else ""
            g.append(f"\n## Escena {i+1}: {name} ({sc['type']}){start}\n")
            extra = {k: val for k, val in sc.items() if k not in ("type", "say") and not k.startswith("_")}
            if extra:
                g.append("**En pantalla:** " + json.dumps(extra, ensure_ascii=False) + "\n")
            g.append("**Locución:**\n")
            for s in sc["say"]:
                g.append(f"> {s}\n")
        open(os.path.join(ROOT, "guiones", v["id"] + ".md"), "w").write("\n".join(g))
    open(os.path.join(ROOT, "PUBLICACION.md"), "w").write("\n".join(md))
    # subtítulos .srt
    os.makedirs(os.path.join(ROOT, "subtitulos"), exist_ok=True)
    for v in VIDEOS:
        m = metas[v["id"]]
        if not m:
            continue
        out = []
        for i, (a, b, s) in enumerate(m["subs"], 1):
            out.append(f"{i}\n{srt(a)} --> {srt(b)}\n{s}\n")
        open(os.path.join(ROOT, "subtitulos", v["id"] + ".srt"), "w").write("\n".join(out))
    print("ok")


def sc_start(m, i):
    return m["chapters"][i][0]


def srt(t):
    h = int(t // 3600); mi = int(t % 3600 // 60); s = t % 60
    return f"{h:02d}:{mi:02d}:{int(s):02d},{int((s % 1) * 1000):03d}"


if __name__ == "__main__":
    main()


def shorts_pack():
    from shorts_data import SHORTS
    md = ["# Shorts verticales — publicación\n",
          "Formato 1080×1920, menos de 60 s. Cada Short va media hora después de su vídeo largo.",
          "En YouTube Studio, al subir cada Short, usa **«Vídeo relacionado»** para enlazar su vídeo largo: es lo que más tráfico manda al vídeo completo.\n",
          "| Short | Duración | Vídeo largo relacionado | Publicar |", "|---|---|---|---|"]
    body = []
    for s in SHORTS:
        mp = os.path.join(BUILD, s["id"], "meta.json")
        dur = json.load(open(mp))["duration"] if os.path.exists(mp) else 0
        when = SCHEDULE[s["long"]]
        if when.startswith("MIÉRCOLES"):
            when = "Miércoles 18 · 10:30"
        else:
            hh, mm = when.split("· ")[1].split(":")
            m = int(hh) * 60 + int(mm) + 30
            when = f"Jueves 19 · {m // 60:02d}:{m % 60:02d}"
        md.append(f"| `shorts/{s['id']}.mp4` | {ts(dur)} | `{s['long']}` | {when} |")
        hook = s["scenes"][0]["say"][0]
        desc = (f"{hook}\n\nVídeo completo en el canal 👉 (enlázalo como «Vídeo relacionado»)\n\n"
                f"#GTA6 #GTAVI #Leonida #shorts\n\n{DISCLAIMER}")
        body += [f"\n---\n\n## {s['id']}\n", f"**Título**\n\n```\n{s['title']}\n```\n", f"**Descripción**\n\n```\n{desc}\n```\n"]
    open(os.path.join(ROOT, "PUBLICACION_SHORTS.md"), "w").write("\n".join(md + body))
    print("shorts ok")


if __name__ == "__main__":
    shorts_pack()
