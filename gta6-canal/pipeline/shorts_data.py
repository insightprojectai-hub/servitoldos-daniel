# -*- coding: utf-8 -*-
"""Guiones de los 10 Shorts verticales (uno por vídeo largo, < 60 s)."""

SHORTS = [
dict(id="s01-hora", palette="sunset", long="01-hora-lanzamiento",
 title="¿A qué hora sale GTA 6 en tu país? 🕛 #gta6 #shorts",
 scenes=[
  dict(type="title", kicker="19 · NOV", title="¿A QUÉ HORA SALE GTA 6?", sub="En España y Latinoamérica", say=[
   "¿A qué hora puedes jugar a GTA 6? Te lo digo en menos de un minuto."]),
  dict(type="stat", value="00:00", label="HORA LOCAL", sub="Noche del miércoles 18 al jueves 19", say=[
   "GTA 6 se desbloquea a medianoche, hora local, en PS5 y en Xbox.",
   "Ojo: es la noche del miércoles al jueves, no el jueves por la noche."]),
  dict(type="clock", heading="NUEVA ZELANDA ABRE ANTES", rows=[
   ("Nueva Zelanda", "00:00 · JUE 19"), ("España", "12:00 · MIÉ 18"), ("Ciudad de México", "05:00 · MIÉ 18"), ("Argentina · Chile", "08:00 · MIÉ 18")], say=[
   "Pero hay un truco: Nueva Zelanda es de los primeros países en llegar a medianoche.",
   "Allí se desbloquea el jueves a las doce de la noche.",
   "Que en España son las doce del mediodía del miércoles.",
   "En Ciudad de México, las cinco de la mañana.",
   "Y en Argentina y Chile, las ocho."]),
  dict(type="warning", title="NO ESTÁ GARANTIZADO", text="Xbox: cambia la ubicación a Nueva Zelanda. PS5: necesitas otra cuenta y otra copia.", say=[
   "En Xbox puedes probar a cambiar la ubicación de la consola. En PS5 necesitarías otra cuenta y otra copia.",
   "Y nadie ha confirmado que funcione, así que bajo tu responsabilidad."]),
  dict(type="outro", title="VÍDEO COMPLETO EN EL CANAL", sub="Suscríbete", say=[
   "Tienes el vídeo completo en el canal. Suscríbete, y nos vemos en Leonida."]),
 ]),
dict(id="s02-ediciones", palette="miami", long="02-standard-vs-ultimate",
 title="GTA 6: ¿Standard o Ultimate? No pagues de más 💸 #gta6 #shorts",
 scenes=[
  dict(type="title", kicker="ANTES DE COMPRAR", title="NO PAGUES DE MÁS POR GTA 6", sub="Standard vs Ultimate", say=[
   "Antes de comprar GTA 6, mira esto para no pagar de más."]),
  dict(type="compare", heading="PRECIOS", cols=[
   dict(title="STANDARD", big="79,99 €", lines=["Física y digital"]),
   dict(title="ULTIMATE", big="99,99 €", lines=["Solo digital", "Extras de historia"])], say=[
   "Hay dos ediciones.",
   "La Standard, a setenta y nueve con noventa y nueve euros, en físico o digital.",
   "Y la Ultimate, a noventa y nueve con noventa y nueve, solo en digital, con extras para la historia."]),
  dict(type="checklist", heading="LO QUE CASI NADIE SABE", items=[
   "El bonus de reserva es igual en las dos", "Puedes mejorar a Ultimate después", "Los extras se desbloquean jugando"], say=[
   "Y tres cosas que casi nadie sabe.",
   "El bonus de reserva, el Vintage Vice City Pack, es el mismo en las dos ediciones.",
   "Puedes comprar la Standard y mejorar a Ultimate más adelante.",
   "Y los extras de la Ultimate se van desbloqueando con la historia."]),
  dict(type="outro", title="¿CUÁL TE HAS PILLADO?", sub="Vídeo completo en el canal", say=[
   "¿Tú cuál te has pillado? Vídeo completo en el canal. Suscríbete."]),
 ]),
dict(id="s03-212gb", palette="neon", long="03-tamano-precarga",
 title="GTA 6 ocupa 212 GB 😱 Haz esto YA #gta6 #shorts",
 scenes=[
  dict(type="title", kicker="PRECARGA", title="GTA 6 OCUPA 212 GB", sub="Haz esto antes del jueves", say=[
   "GTA 6 ocupa doscientos doce gigas. Y si no haces esto ya, el jueves no vas a poder jugar."]),
  dict(type="compare", heading="CUÁNTO TE COME", cols=[
   dict(title="SERIES S", big="> 1/2", lines=["Más de la mitad"]),
   dict(title="PS5 825 GB", big="≈ 1/3", lines=["Casi un tercio"])], say=[
   "Para que te hagas una idea.",
   "En una Series S se come más de la mitad del disco.",
   "Y en una PS5 original, casi un tercio."]),
  dict(type="checklist", heading="HAZ ESTO YA", items=[
   "Precarga desde la tienda", "Deja la consola en reposo", "Borra o mueve juegos a un USB"], say=[
   "Así que haz esto ya.",
   "Si lo compraste en digital, precárgalo desde la tienda.",
   "Deja la consola en reposo para que descargue sola.",
   "Y si no te cabe, borra juegos o muévelos a un disco USB externo."]),
  dict(type="outro", title="¿CUÁNTO ESPACIO TE QUEDA?", sub="Vídeo completo en el canal", say=[
   "Tienes la guía completa en el canal. Suscríbete."]),
 ]),
dict(id="s04-pc-estafa", palette="cyber", long="04-gta6-pc",
 title="NO descargues GTA 6 para PC ⚠️ #gta6 #shorts",
 scenes=[
  dict(type="title", kicker="AVISO", title="NO DESCARGUES GTA 6 PARA PC", sub="Te explico por qué", say=[
   "Si ves GTA 6 para PC, no lo descargues. Te explico por qué."]),
  dict(type="checklist", heading="LO CONFIRMADO", items=[
   "Solo PS5 y Xbox Series X|S", "Sin versión de PC anunciada", "Sin fecha ni requisitos"], say=[
   "Esto es lo único confirmado.",
   "GTA 6 sale solo en PS5 y Xbox Series X y Series S.",
   "Rockstar no ha anunciado versión de PC.",
   "Y no hay fecha ni requisitos oficiales."]),
  dict(type="warning", title="ES UNA ESTAFA", text="Las «descargas» de GTA 6 para PC son virus, robos de cuenta o fraudes.", say=[
   "Así que cualquier descarga de GTA 6 para PC es una estafa.",
   "En el mejor caso pierdes el tiempo. En el peor, te roban tus cuentas."]),
  dict(type="timeline", heading="¿CUÁNDO EN PC?", events=[("2013 → 2015", "GTA V"), ("2018 → 2019", "RDR 2")], say=[
   "¿Y cuándo llegará? Rockstar suele tardar entre uno y dos años.",
   "GTA cinco tardó año y medio en llegar a PC.",
   "Y Red Dead Redemption dos, un año."]),
  dict(type="outro", title="COMPÁRTELO", sub="Que no le timen a nadie", say=[
   "Compártelo con quien lo necesite, y suscríbete."]),
 ]),
dict(id="s05-30fps", palette="sunset2", long="05-que-consola",
 title="GTA 6 a 30 FPS… ¿y la PS5 Pro? 🎮 #gta6 #shorts",
 scenes=[
  dict(type="title", kicker="RENDIMIENTO", title="GTA 6 A 30 FPS", sub="¿Y la PS5 Pro?", say=[
   "GTA 6 va a treinta fotogramas por segundo. ¿Y la PS5 Pro?"]),
  dict(type="stat", value="30 FPS", label="EN TODAS LAS CONSOLAS", sub="Sin modo 60 FPS anunciado", say=[
   "Según lo publicado, el objetivo es treinta en todas las consolas.",
   "Y no hay ningún modo a sesenta anunciado, tampoco en PS5 Pro."]),
  dict(type="bullets", heading="ENTONCES…", items=[
   "PS5 Pro: sombras con ray tracing", "PS5 y Series X: la experiencia base", "Series S: más barata, menos resolución"], say=[
   "Entonces, ¿qué cambia?",
   "La PS5 Pro tiene sombras con ray tracing y se verá mejor.",
   "La PS5 y la Series X son la experiencia base, y el tráiler final se grabó en una PS5 normal.",
   "Y la Series S es la más barata, con menos resolución."]),
  dict(type="outro", title="¿EN QUÉ CONSOLA JUEGAS?", sub="Dímelo en comentarios", say=[
   "¿En qué consola vas a jugar tú? Dímelo en comentarios, y suscríbete."]),
 ]),
dict(id="s06-mapa", palette="ocean", long="06-mapa-leonida",
 title="Las 6 regiones del mapa de GTA 6 🗺️ #gta6 #shorts",
 scenes=[
  dict(type="title", kicker="EL MAPA", title="LAS 6 REGIONES DE GTA 6", sub="Bienvenido a Leonida", say=[
   "Estas son las seis regiones de Leonida, el mapa de GTA 6."]),
  dict(type="map", heading="LEONIDA", regions=["Vice City", "Leonida Keys", "Grassrivers", "Port Gellhorn", "Ambrosia", "Mount Kalaga"], say=[
   "Vamos.",
   "Vice City, la gran ciudad inspirada en Miami.",
   "Leonida Keys, las islas del sur.",
   "Grassrivers, los pantanos con caimanes.",
   "Port Gellhorn, la costa venida a menos.",
   "Ambrosia, el interior rural e industrial.",
   "Y Mount Kalaga, bosques y montaña."]),
  dict(type="outro", title="¿CUÁL EXPLORAS PRIMERO?", sub="Comenta tu región", say=[
   "¿Cuál vas a explorar primero? Comenta, y suscríbete."]),
 ]),
dict(id="s07-personajes", palette="sunset", long="07-lucia-jason-historia",
 title="Quién es quién en GTA 6 (sin spoilers) #gta6 #shorts",
 scenes=[
  dict(type="title", kicker="SIN SPOILERS", title="QUIÉN ES QUIÉN EN GTA 6", sub="Los personajes que conocemos", say=[
   "Quién es quién en GTA 6, sin spoilers."]),
  dict(type="bullets", heading="PROTAGONISTAS", items=["Lucía Caminos", "Jason Duval"], say=[
   "Los protagonistas.",
   "Lucía Caminos, a la que conocemos en prisión.",
   "Y Jason Duval, un exmilitar metido en trabajos turbios."]),
  dict(type="bullets", heading="SECUNDARIOS", items=[
   "Cal Hampton", "Brian Heder", "Boobie Ike", "Raul Bautista"], say=[
   "Y algunos secundarios.",
   "Cal Hampton, el amigo de Jason.",
   "Brian Heder, veterano del contrabando en los Keys.",
   "Boobie Ike, leyenda local de Vice City.",
   "Y Raul Bautista, un atracador experimentado."]),
  dict(type="outro", title="¿LUCÍA O JASON?", sub="Vídeo completo en el canal", say=[
   "¿Lucía o Jason? Comenta, y mira el vídeo completo en el canal."]),
 ]),
dict(id="s08-13-anos", palette="miami", long="08-historia-espera",
 title="13 años esperando GTA 6 ⏳ #gta6 #shorts",
 scenes=[
  dict(type="title", kicker="2013 · 2026", title="13 AÑOS ESPERANDO", sub="La historia de GTA 6", say=[
   "Trece años esperando GTA 6. Así hemos llegado hasta aquí."]),
  dict(type="timeline", heading="LA ESPERA", events=[
   ("2013", "Sale GTA V"), ("2022", "Anuncio y filtración"), ("2023", "Tráiler 1"), ("2025", "Tráiler 2"), ("2026", "¡Lanzamiento!")], say=[
   "Repasemos.",
   "En dos mil trece sale GTA cinco.",
   "En dos mil veintidós, Rockstar confirma el siguiente GTA, y llega la mayor filtración de su historia.",
   "En dos mil veintitrés, el primer tráiler bate récords.",
   "En dos mil veinticinco, el segundo tráiler, y dos retrasos.",
   "Y por fin, el diecinueve de noviembre de dos mil veintiséis."]),
  dict(type="outro", title="¿DESDE CUÁNDO ESPERAS?", sub="Dímelo en comentarios", say=[
   "¿Desde cuándo lo estás esperando tú? Comenta, y suscríbete."]),
 ]),
dict(id="s09-antes-jugar", palette="neon", long="09-antes-de-jugar",
 title="Haz esto ANTES de jugar GTA 6 ✅ #gta6 #shorts",
 scenes=[
  dict(type="title", kicker="CHECKLIST", title="HAZ ESTO ANTES DE JUGAR", sub="GTA 6", say=[
   "Haz esto antes de jugar a GTA 6."]),
  dict(type="checklist", heading="5 COSAS", items=[
   "Precarga al 100 %", "Modo juego en la tele", "Calibra el HDR", "Silencia spoilers en redes", "No corras la historia"], say=[
   "Cinco cosas.",
   "Ten la precarga al cien por cien.",
   "Activa el modo juego de tu tele.",
   "Calibra el HDR desde la consola.",
   "Silencia palabras en tus redes para evitar spoilers.",
   "Y no corras la historia. Explora."]),
  dict(type="outro", title="¿TE FALTABA ALGUNA?", sub="Lista completa en el canal", say=[
   "La lista completa de diez está en el canal. Suscríbete."]),
 ]),
dict(id="s10-resumen", palette="cyber", long="10-resumen-gta6",
 title="GTA 6 en 45 segundos ⚡ #gta6 #shorts",
 scenes=[
  dict(type="title", kicker="RESUMEN", title="GTA 6 EN 45 SEGUNDOS", sub="Todo lo que tienes que saber", say=[
   "GTA 6 en cuarenta y cinco segundos."]),
  dict(type="checklist", heading="LO ESENCIAL", items=[
   "19 nov · 00:00 hora local", "PS5 y Xbox Series X|S", "79,99 € · Ultimate 99,99 €", "212 GB", "30 FPS", "Sin versión de PC"], say=[
   "Apunta.",
   "Sale el diecinueve de noviembre a medianoche, hora local.",
   "En PS5 y Xbox Series X y Series S.",
   "Setenta y nueve con noventa y nueve euros, o noventa y nueve con noventa y nueve la Ultimate.",
   "Ocupa doscientos doce gigas.",
   "Va a treinta fotogramas por segundo.",
   "Y no hay versión de PC anunciada."]),
  dict(type="outro", title="¡NOS VEMOS EN LEONIDA!", sub="Suscríbete para más", say=[
   "Suscríbete para más GTA 6. Nos vemos en Leonida."]),
 ]),
]
