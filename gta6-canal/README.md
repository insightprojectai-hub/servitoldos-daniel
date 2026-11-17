# Canal GTA 6 — 10 vídeos listos para el lanzamiento (19/11/2026)

Todo lo necesario para abrir el canal el día que sale GTA 6:

| Carpeta | Qué hay |
|---|---|
| `videos/` | Los 10 vídeos finales en MP4 1080p 30 fps (voz, música, animaciones, subtítulos incrustados) |
| `miniaturas/` | Una miniatura 1280×720 por vídeo |
| `subtitulos/` | Subtítulos `.srt` (súbelos también a YouTube: ayudan al SEO) |
| `guiones/` | Guion completo de cada vídeo, escena por escena |
| `PUBLICACION.md` | Título, descripción con capítulos, etiquetas y hora de publicación de cada vídeo |
| `pipeline/` | Código que genera todo (para editar un guion y volver a renderizar) |

## Qué busca la gente (investigación, 17/11/2026)

Datos de vidIQ (búsquedas en YouTube) + noticias de lanzamiento:

- **«gta 6»**: ~32 M búsquedas/mes, +236 %. En España, ~1 M/mes.
- Lo que más crece: **gameplay** (+408 %), **ps5** (+455 %), **30 fps** (+1098 %), **pc** (+302 %), **mapa** (+244 %), **release date** (+247 %), **lucia** (+126 %), **xbox series s**.
- Preguntas en español con más volumen: *cómo jugar GTA 6 antes*, *Nueva Zelanda*, *cuándo sale GTA 6 (para PC)*, *cómo jugar GTA 6 en PC / sin consola*, *cómo descargar GTA 6 en PS5*, *qué consola comprar*, *cómo comprar GTA 6 barato*.

De ahí salen los 10 temas:

1. Hora exacta de lanzamiento + truco de Nueva Zelanda
2. Standard vs Ultimate (precio y contenido)
3. Tamaño (212 GB) y precarga
4. ¿GTA 6 en PC? + aviso de estafas
5. ¿Qué consola? (30 FPS, PS5 Pro, Series S)
6. El mapa: las 6 regiones de Leonida
7. Lucía, Jason y los secundarios (sin spoilers)
8. La larga espera 2013 → 2026
9. 10 cosas que hacer antes de jugar
10. Resumen: todo lo que hay que saber

## Datos usados (y su fiabilidad)

Confirmado por Rockstar / tiendas: lanzamiento 19/11/2026 a las 00:00 **hora local** en PS5 y Xbox Series X|S · Standard 79,99 € / Ultimate 99,99 € (solo digital) · mejora de Standard a Ultimate disponible · Vintage Vice City Pack en ambas ediciones + 1 mes de GTA+ en compras digitales anteriores al 20/11 · hasta 212 GB · precarga desde el 10/11 · sin versión de PC anunciada.

Presentado como **no confirmado** en los vídeos: truco de Nueva Zelanda, 60 FPS en PS5 Pro, fecha de PC (rumores 2027–2028), mapa completo.

## Cómo está hecho

Todo se generó en local, sin coste y sin material de Rockstar:

- **Voz:** Kokoro TTS (voz `em_alex`, español) con sherpa-onnx.
- **Música y efectos:** synthwave sintetizada por código (sin derechos de autor).
- **Imágenes y animación:** gráficos propios estilo synthwave/Vice City dibujados por código (sin logos, capturas ni personajes oficiales, para evitar reclamaciones de copyright).
- **Montaje:** Python + FFmpeg.

Para regenerar un vídeo después de cambiar su guion en `pipeline/videos.py`:

```bash
cd gta6-canal/pipeline
python3 render.py 02-standard-vs-ultimate   # vídeo + miniatura
python3 make_pack.py                        # actualiza PUBLICACION.md, guiones y .srt
```

Necesita: `pip install sherpa-onnx==1.12.40 soundfile scipy pillow numpy`, FFmpeg, el modelo
`kokoro-multi-lang-v1_0` y las fuentes Anton, Bebas Neue y Montserrat (rutas en `render.py` / `tts.py`).
