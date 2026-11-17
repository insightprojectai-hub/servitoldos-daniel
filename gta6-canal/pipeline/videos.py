# -*- coding: utf-8 -*-
"""Guiones de los 10 vídeos del canal.

Cada vídeo es una lista de escenas. Cada escena tiene:
  - type: plantilla visual (title, stat, bullets, checklist, compare, clock,
          timeline, map, warning, outro)
  - say:  frases de la locución (una entrada = una frase = un subtítulo)
  - resto de claves: datos que pinta la plantilla
En bullets/checklist/timeline/map/clock, el elemento i aparece cuando empieza
la frase i+1 (la primera frase es la introducción de la escena).
"""

CHANNEL = "ZONA LEONIDA"

VIDEOS = [
# ---------------------------------------------------------------- 01
dict(
 id="01-hora-lanzamiento",
 palette="sunset",
 title="GTA 6: HORA EXACTA de lanzamiento en España y Latinoamérica (y el truco de Nueva Zelanda)",
 thumb=dict(top="¿A QUÉ HORA", big="SALE GTA 6?", badge="00:00", note="+ TRUCO NUEVA ZELANDA"),
 scenes=[
  dict(type="title", kicker="19 · NOV · 2026", title="¿A QUÉ HORA SALE GTA 6?", sub="España · México · Colombia · Argentina · Chile", say=[
   "Por fin. Después de dos retrasos y casi tres años desde el primer tráiler, GTA 6 sale este jueves, diecinueve de noviembre.",
   "En este vídeo te digo exactamente a qué hora podrás jugar en tu país, qué tienes que tener listo, y si de verdad funciona el famoso truco de Nueva Zelanda.",
   "Quédate hasta el final, porque hay un detalle que mucha gente va a pasar por alto.",
  ]),
  dict(type="stat", value="00:00", label="HORA LOCAL", sub="Jueves 19 de noviembre · PS5 y Xbox Series X|S", say=[
   "Vamos con lo importante. Según el soporte oficial de Rockstar, GTA 6 se desbloquea a medianoche, hora local, el jueves diecinueve de noviembre.",
   "Eso vale tanto para PS5 como para Xbox Series X y Series S.",
   "Es decir, no hay una hora única para todo el mundo: cada país lo desbloquea cuando su reloj marca las doce de la noche.",
  ]),
  dict(type="clock", heading="TU HORA DE DESBLOQUEO", rows=[
     ("España peninsular", "00:00 · noche del mié 18 al jue 19"),
     ("Canarias", "00:00 hora canaria (1 h después)"),
     ("México · Colombia · Perú", "00:00 hora local"),
     ("Argentina · Chile", "00:00 hora local"),
   ], say=[
   "Así queda en cada sitio.",
   "En España peninsular: a las doce de la noche del miércoles al jueves.",
   "En Canarias, también a las doce, pero en su hora, así que una hora más tarde que en la península.",
   "En México, Colombia o Perú, exactamente igual: a medianoche de tu hora local.",
   "Y en Argentina y Chile, lo mismo. Ojo al error típico: no es el jueves por la noche, es la noche del miércoles al jueves.",
  ]),
  dict(type="clock", heading="NUEVA ZELANDA ABRE PRIMERO", rows=[
     ("Nueva Zelanda", "00:00 · jueves 19"),
     ("España", "12:00 · miércoles 18"),
     ("Ciudad de México", "05:00 · miércoles 18"),
     ("Colombia · Perú", "06:00 · miércoles 18"),
     ("Argentina · Chile", "08:00 · miércoles 18"),
   ], say=[
   "Ahora, el truco del que todo el mundo habla. Como el desbloqueo va por hora local, Nueva Zelanda es de los primeros países en llegar a la medianoche.",
   "Cuando allí sean las doce del jueves, en España serán las doce del mediodía del miércoles.",
   "En Ciudad de México, las cinco de la mañana.",
   "En Colombia y Perú, las seis.",
   "Y en Argentina y Chile, las ocho de la mañana. En teoría, hasta doce horas de ventaja desde España.",
  ]),
  dict(type="bullets", heading="EL TRUCO EN XBOX", items=[
     "Precarga el juego al 100 %",
     "Configuración › Sistema › Idioma y ubicación",
     "Ubicación: Nueva Zelanda y reinicia",
     "Después, vuelve a poner tu región",
   ], say=[
   "En Xbox es lo más sencillo, porque puedes cambiar la ubicación de la consola sin crear otra cuenta.",
   "Primero, asegúrate de tener el juego precargado al cien por cien.",
   "Luego ve a Configuración, Sistema, Idioma y ubicación.",
   "Cambia la ubicación a Nueva Zelanda y reinicia la consola.",
   "Y cuando termines, puedes volver a poner tu región sin problema.",
  ]),
  dict(type="warning", title="EN PS5 ES MÁS DIFÍCIL", text="Sony no deja cambiar la región de una cuenta PSN. Necesitarías otra cuenta y comprar el juego otra vez.", say=[
   "En PlayStation la cosa cambia. Sony no permite cambiar el país de una cuenta que ya existe.",
   "Para intentarlo necesitarías una cuenta nueva de Nueva Zelanda y comprar el juego otra vez en esa tienda. Tu copia de España no te sirve.",
  ]),
  dict(type="warning", title="NO ESTÁ GARANTIZADO", text="Ni Rockstar, ni Microsoft, ni Sony lo han confirmado. Pruébalo bajo tu responsabilidad y no pagues a nadie por 'acceso anticipado'.", say=[
   "Y aquí va el detalle importante: nadie ha confirmado que este truco funcione con GTA 6. Ni Rockstar, ni Microsoft, ni Sony.",
   "Ha funcionado con otros juegos, pero depende de cómo se gestione el desbloqueo digital. Tómatelo como un experimento, y desconfía de cualquier web que te pida dinero por jugar antes.",
  ]),
  dict(type="checklist", heading="ANTES DEL JUEVES", items=[
     "Precarga hecha (hasta 212 GB)",
     "Consola en reposo con descargas activas",
     "Conexión estable a medianoche",
     "Y si puedes… el jueves libre",
   ], say=[
   "Mi consejo para que no se te escape nada.",
   "Ten la precarga hecha antes del miércoles.",
   "Deja la consola en reposo con las descargas activadas, para que pille cualquier parche.",
   "Asegúrate de tener buena conexión a la hora del desbloqueo.",
   "Y si puedes, pide el jueves libre. Es broma. O no.",
  ]),
  dict(type="outro", title="¿A QUÉ HORA EMPIEZAS?", sub="Dímelo en comentarios", say=[
   "Cuéntame en los comentarios desde qué país vas a jugar y a qué hora vas a empezar.",
   "Suscríbete y activa la campana, porque esta semana subimos todo lo que necesitas saber de GTA 6. Nos vemos en Leonida.",
  ]),
 ]),
# ---------------------------------------------------------------- 02
dict(
 id="02-standard-vs-ultimate",
 palette="miami",
 title="GTA 6 Standard vs Ultimate: ¿cuál comprar? Precio y TODO lo que incluye cada edición",
 thumb=dict(top="STANDARD", big="vs ULTIMATE", badge="+20 €", note="¿CUÁL COMPRAR?"),
 scenes=[
  dict(type="title", kicker="GUÍA DE COMPRA", title="STANDARD vs ULTIMATE", sub="¿Merecen la pena los 20 € de diferencia?", say=[
   "Vas a comprar GTA 6 y te encuentras con dos ediciones: Standard y Ultimate. Veinte euros de diferencia.",
   "En unos minutos te explico qué trae cada una, qué te regalan por reservar, y cuál te recomiendo según cómo juegues.",
  ]),
  dict(type="compare", heading="PRECIOS EN ESPAÑA", cols=[
     dict(title="STANDARD", big="79,99 €", lines=["Juego completo", "Física y digital", "Bonus de reserva incluido"]),
     dict(title="ULTIMATE", big="99,99 €", lines=["Juego + extras de historia", "Solo digital", "Bonus de reserva incluido"]),
   ], say=[
   "Precios en España: la Standard cuesta setenta y nueve con noventa y nueve euros, y la Ultimate, noventa y nueve con noventa y nueve.",
   "En Estados Unidos son setenta y nueve y noventa y nueve dólares.",
   "Y un detalle importante: la Ultimate solo existe en digital. Si quieres la caja física, solo tienes la Standard.",
   "Eso sí, según se ha anunciado, la versión física no incluye el juego en disco, así que vas a tener que descargarlo igualmente.",
  ]),
  dict(type="bullets", heading="QUÉ AÑADE LA ULTIMATE", items=[
     "Vehículos exclusivos",
     "Negocios y talleres extra",
     "Armas y cosméticos especiales",
     "Se desbloquean durante la historia",
   ], say=[
   "¿Y qué añade la Ultimate? Contenido extra para el modo historia.",
   "Vehículos exclusivos, entre ellos un deportivo clásico.",
   "Varios negocios extra, incluidos talleres de modificación.",
   "Armas y cosméticos especiales.",
   "Y ojo: estos extras se van desbloqueando a medida que avanzas en la historia. No los tienes todos desde el minuto uno.",
  ]),
  dict(type="checklist", heading="BONUS DE RESERVA · AMBAS EDICIONES", items=[
     "Vintage Vice City Pack",
     "Sedán clásico + garaje",
     "Ropa, peinados y patrón de arma",
     "1 mes de GTA+ (compra digital)",
   ], say=[
   "Ahora, el bonus de reserva, que es el mismo en las dos ediciones.",
   "Se llama Vintage Vice City Pack.",
   "Incluye un sedán clásico con su propio garaje.",
   "Ropa, peinados y un patrón exclusivo para armas.",
   "Y si compras en digital antes del veinte de noviembre, también te llevas un mes de GTA plus.",
  ]),
  dict(type="stat", value="+20 €", label="MEJORA A ULTIMATE", sub="Puedes empezar con la Standard y mejorar después", say=[
   "Y una cosa que mucha gente no sabe: si compras la Standard, puedes pasar a la Ultimate más adelante.",
   "Rockstar ha confirmado que hay una mejora a Ultimate en las tiendas de PlayStation y Microsoft. Así que no tienes que decidirlo hoy.",
  ]),
  dict(type="compare", heading="MI RECOMENDACIÓN", cols=[
     dict(title="COMPRA STANDARD SI…", big="", lines=["Quieres la caja física", "Vas a por la historia", "Quieres ahorrar 20 €"]),
     dict(title="COMPRA ULTIMATE SI…", big="", lines=["Juegas en digital", "Quieres todos los extras", "Te sobran esos 20 €"]),
   ], say=[
   "Mi recomendación.",
   "Compra la Standard si quieres la caja física, si solo te interesa la historia o si quieres ahorrar.",
   "Compra la Ultimate si juegas en digital y quieres todos los extras desde el principio.",
   "Y en ningún caso pagues más solo por el bonus de reserva, porque es exactamente el mismo.",
  ]),
  dict(type="outro", title="¿STANDARD O ULTIMATE?", sub="Te leo en comentarios", say=[
   "¿Tú cuál te has pillado, Standard o Ultimate? Déjalo en los comentarios.",
   "Suscríbete para no perderte nada de GTA 6, y nos vemos en el siguiente vídeo.",
  ]),
 ]),
# ---------------------------------------------------------------- 03
dict(
 id="03-tamano-precarga",
 palette="neon",
 title="GTA 6 ocupa 212 GB: cómo PRECARGARLO y hacer sitio en PS5 y Xbox",
 thumb=dict(top="GTA 6 OCUPA", big="212 GB", badge="PRECARGA", note="HAZ SITIO YA"),
 scenes=[
  dict(type="title", kicker="PRECARGA", title="GTA 6 OCUPA 212 GB", sub="Cómo descargarlo ya y hacer sitio en tu consola", say=[
   "Doscientos doce gigas. Eso es lo que te pide GTA 6 para instalarse.",
   "Y si lo dejas para el jueves, vas a llegar tarde. Te enseño cómo precargarlo, cuánto espacio necesitas de verdad, y cómo hacer hueco en tu consola.",
  ]),
  dict(type="stat", value="212 GB", label="ESPACIO LIBRE NECESARIO", sub="Xbox Store muestra hasta 225 GB · deja margen", say=[
   "Rockstar indica que necesitas hasta doscientos doce gigas libres para la precarga.",
   "En la tienda de Xbox, el tamaño máximo de instalación aparece como algo más de doscientos veinticinco.",
   "Mi recomendación: deja al menos doscientos treinta gigas libres, porque las instalaciones necesitan margen para archivos temporales y para el primer parche.",
  ]),
  dict(type="compare", heading="CUÁNTO TE COME GTA 6", cols=[
     dict(title="XBOX SERIES S", big="> 1/2", lines=["512 GB", "≈ 364 GB útiles", "Más de la mitad"]),
     dict(title="PS5 · 825 GB", big="≈ 1/3", lines=["≈ 667 GB útiles", "Casi un tercio", "del espacio"]),
     dict(title="1 TB o más", big="≈ 1/4", lines=["Series X · PS5 Slim", "≈ 800 GB útiles", "Una cuarta parte"]),
   ], say=[
   "Para que te hagas una idea de lo que supone.",
   "En una Xbox Series S, con unos trescientos sesenta y cuatro gigas útiles, GTA 6 se come más de la mitad del disco.",
   "En una PS5 original, con unos seiscientos sesenta y siete gigas útiles, casi un tercio.",
   "Y en consolas de un tera, como la Series X o la PS5 Slim, más o menos una cuarta parte.",
  ]),
  dict(type="bullets", heading="PRECARGA EN PS5", items=[
     "Compra digital en PlayStation Store",
     "Biblioteca › GTA VI › Descargar",
     "Deja la consola en modo reposo",
     "Ajustes › Ahorro de energía › Seguir conectado a internet",
   ], say=[
   "Cómo precargar en PS5.",
   "Si lo has comprado en digital en PlayStation Store, la precarga ya está disponible.",
   "Ve a tu Biblioteca, busca Grand Theft Auto seis y pulsa Descargar.",
   "Luego deja la consola en modo reposo en lugar de apagarla.",
   "Y en los ajustes de ahorro de energía, activa la opción de seguir conectado a internet en reposo, para que descargue mientras duermes.",
  ]),
  dict(type="bullets", heading="PRECARGA EN XBOX", items=[
     "Compra digital en Microsoft Store",
     "Mis juegos y aplicaciones › Cola",
     "Modo de energía: suspensión",
     "Comprueba que llega al 100 %",
   ], say=[
   "En Xbox es muy parecido.",
   "Compra el juego en digital en la tienda de Microsoft y pulsa instalar.",
   "Puedes ver el progreso en Mis juegos y aplicaciones, en la cola de descargas.",
   "Pon el modo de energía en suspensión, para que siga descargando cuando no la uses.",
   "Y antes del miércoles, comprueba que la descarga ha llegado al cien por cien.",
  ]),
  dict(type="checklist", heading="CÓMO HACER SITIO", items=[
     "Borra juegos que no tocas (se reinstalan)",
     "Mueve juegos a un disco USB externo",
     "Elimina capturas y clips de vídeo",
     "Amplía: SSD M.2 (PS5) o tarjeta (Xbox)",
   ], say=[
   "¿No te cabe? Cuatro formas de hacer sitio.",
   "Borra juegos que no tocas. Tus partidas guardadas no se pierden y los puedes volver a instalar cuando quieras.",
   "Mueve juegos a un disco duro USB externo. Ahí puedes guardarlos y devolverlos al interno cuando los necesites.",
   "Elimina capturas y clips de vídeo, que ocupan muchísimo más de lo que crees.",
   "Y si quieres una solución definitiva, amplía: un SSD M punto dos en PS5, o una tarjeta de expansión en Xbox.",
  ]),
  dict(type="warning", title="¿Y SI LO COMPRO EN FÍSICO?", text="Te toca igual: el juego se instala en el almacenamiento interno y necesitas el mismo espacio.", say=[
   "Y si lo compras en físico, no te libras.",
   "El juego tiene que instalarse igualmente en el almacenamiento interno, así que necesitas el mismo espacio. Hazlo antes de que llegue el jueves.",
  ]),
  dict(type="outro", title="¿CUÁNTO ESPACIO TE QUEDA?", sub="Cuéntamelo en comentarios", say=[
   "Dime en los comentarios cuánto espacio te queda libre, que seguro que alguno va justísimo.",
   "Suscríbete y activa la campana para tenerlo todo listo para el lanzamiento. Nos vemos en Leonida.",
  ]),
 ]),
# ---------------------------------------------------------------- 04
dict(
 id="04-gta6-pc",
 palette="cyber",
 title="¿GTA 6 en PC? Cuándo sale y CUIDADO con las descargas falsas",
 thumb=dict(top="¿GTA 6", big="EN PC?", badge="CUIDADO", note="LO QUE ESTÁ CONFIRMADO"),
 scenes=[
  dict(type="title", kicker="PC", title="¿GTA 6 EN PC?", sub="Lo que está confirmado (y lo que no)", say=[
   "Es una de las preguntas más buscadas estos días: ¿se puede jugar a GTA 6 en PC?",
   "La respuesta corta es no. Y la larga te interesa todavía más, porque estos días van a aparecer muchas trampas.",
  ]),
  dict(type="checklist", heading="LO QUE ESTÁ CONFIRMADO", items=[
     "Sale solo en PS5 y Xbox Series X|S",
     "Rockstar no ha anunciado versión de PC",
     "Sin fecha ni requisitos oficiales",
   ], say=[
   "Esto es lo que está confirmado.",
   "GTA 6 sale el diecinueve de noviembre solo en PS5 y en Xbox Series X y Series S.",
   "Rockstar no ha anunciado ninguna versión para PC.",
   "Y no hay ni fecha, ni requisitos mínimos oficiales. Cualquier tabla de requisitos que veas, es inventada.",
  ]),
  dict(type="timeline", heading="LO QUE HIZO ROCKSTAR ANTES", events=[
     ("2013", "GTA V en consolas"),
     ("2015", "GTA V llega a PC"),
     ("2018", "RDR 2 en consolas"),
     ("2019", "RDR 2 llega a PC"),
   ], say=[
   "Si miramos la historia de Rockstar, el patrón está claro.",
   "GTA cinco salió en consolas en septiembre de dos mil trece.",
   "Y no llegó a PC hasta abril de dos mil quince, año y medio después.",
   "Red Dead Redemption dos salió en consolas en octubre de dos mil dieciocho.",
   "Y llegó a PC en noviembre de dos mil diecinueve. Un año de espera.",
  ]),
  dict(type="bullets", heading="LOS RUMORES", items=[
     "Un informe apunta a inicios de 2027",
     "Otros estiman finales de 2027 o 2028",
     "Take-Two: «la noticia vendrá de Rockstar»",
   ], say=[
   "¿Y los rumores?",
   "Un informe basado en fuentes anónimas habla de principios de dos mil veintisiete, pero Rockstar no lo ha confirmado.",
   "Otros análisis, mirando los plazos de antes, estiman finales de dos mil veintisiete o incluso dos mil veintiocho.",
   "Y Take-Two, la empresa matriz, solo ha dicho que cualquier noticia sobre PC vendrá de Rockstar.",
  ]),
  dict(type="warning", title="CUIDADO CON LAS ESTAFAS", text="No existe «GTA 6 PC gratis», ni betas, ni instaladores. Son virus, robos de cuenta o fraudes.", say=[
   "Y ahora, lo más importante de este vídeo.",
   "Estos días vas a ver webs, vídeos y anuncios con GTA 6 para PC gratis, betas filtradas o instaladores milagrosos.",
   "Todo eso es mentira. En el mejor de los casos pierdes el tiempo. En el peor, te instalan un virus o te roban tus cuentas.",
   "Si no viene de Rockstar, de PlayStation o de Xbox, no lo descargues.",
  ]),
  dict(type="bullets", heading="¿Y SIN CONSOLA?", items=[
     "No hay versión en la nube anunciada",
     "La opción más barata: Xbox Series S",
     "O esperar a la versión de PC",
   ], say=[
   "¿Entonces cómo juego si no tengo consola?",
   "A día de hoy, no hay ninguna forma oficial anunciada de jugarlo en la nube.",
   "La opción más barata para jugar desde el día uno es una Xbox Series S, aunque con su poco espacio.",
   "Y si no tienes prisa, toca esperar a la versión de PC, que con toda probabilidad llegará, pero sin fecha.",
  ]),
  dict(type="outro", title="¿ESPERAS AL PC?", sub="¿O te pillas consola?", say=[
   "¿Tú qué vas a hacer: esperar al PC o pillarte una consola? Te leo en comentarios.",
   "Y suscríbete, porque en cuanto Rockstar diga algo de la versión de PC, aquí lo tendrás.",
  ]),
 ]),
# ---------------------------------------------------------------- 05
dict(
 id="05-que-consola",
 palette="sunset2",
 title="GTA 6 a 30 FPS: PS5 vs PS5 Pro vs Xbox Series X|S ¿Qué consola comprar?",
 thumb=dict(top="¿QUÉ CONSOLA", big="PARA GTA 6?", badge="30 FPS", note="PS5 · PRO · SERIES X|S"),
 scenes=[
  dict(type="title", kicker="CONSOLAS", title="¿QUÉ CONSOLA PARA GTA 6?", sub="PS5 · PS5 Pro · Series X · Series S", say=[
   "Si estás pensando en comprarte una consola para GTA 6, o te preguntas si la tuya va a ir bien, este vídeo es para ti.",
   "Te cuento lo que se sabe del rendimiento, los mitos que circulan, y qué consola te recomiendo según tu caso.",
  ]),
  dict(type="stat", value="30 FPS", label="OBJETIVO EN CONSOLAS", sub="Sin modo 60 FPS anunciado", say=[
   "Lo primero: según lo publicado, GTA 6 apunta a treinta fotogramas por segundo en consolas.",
   "Y de momento no hay ningún modo a sesenta anunciado, ni en PS5 Pro.",
   "Rockstar tampoco ha dado cifras oficiales de resolución para cada consola, así que desconfía de las tablas que circulan por redes.",
  ]),
  dict(type="compare", heading="DIFERENCIAS CONOCIDAS", cols=[
     dict(title="PS5 PRO", big="TOP", lines=["Sombras con ray tracing", "Reescalado PSSR", "La más vistosa"]),
     dict(title="PS5 · SERIES X", big="BASE", lines=["La experiencia base", "Tráiler final en PS5", "Sin problemas"]),
     dict(title="SERIES S", big="BÁSICA", lines=["La más barata", "Menor resolución", "Poco espacio"]),
   ], say=[
   "Estas son las diferencias que conocemos.",
   "La PS5 Pro tiene sombras con ray tracing exclusivas y reescalado PSSR. Será la versión más vistosa en consola.",
   "La PS5 normal y la Series X son la experiencia base. Y ojo, el tráiler final se capturó en una PS5 normal, así que pinta muy bien.",
   "La Series S es la más barata, pero se espera menos resolución, y como vimos, va muy justa de espacio.",
  ]),
  dict(type="bullets", heading="MITOS QUE CIRCULAN", items=[
     "«60 FPS en PS5 Pro» › no confirmado",
     "«No sale en Series S» › falso",
     "«Necesitas una tele 4K» › no, pero ayuda",
   ], say=[
   "Vamos con los mitos.",
   "Que va a sesenta en PS5 Pro: no está confirmado. Son rumores y filtraciones.",
   "Que no sale en Series S: falso. Sale en Series S el mismo día.",
   "Que necesitas una tele cuatro K: no. Se va a ver bien en cualquier tele, aunque una buena pantalla con HDR se nota, y mucho.",
  ]),
  dict(type="checklist", heading="MI RECOMENDACIÓN", items=[
     "¿Ya tienes PS5 o Series X? No cambies",
     "¿Quieres lo mejor? PS5 Pro",
     "¿Poco presupuesto? Series S + disco externo",
   ], say=[
   "Mi recomendación.",
   "Si ya tienes una PS5 o una Series X, no cambies de consola. Vas a disfrutarlo igual.",
   "Si quieres la mejor imagen posible y te lo puedes permitir, la PS5 Pro.",
   "Y si vas justo de presupuesto, la Series S cumple, pero cuenta con un disco externo para el resto de juegos.",
  ]),
  dict(type="outro", title="¿EN QUÉ CONSOLA JUEGAS?", sub="Vota en comentarios", say=[
   "¿En qué consola vas a jugar tú? Escríbelo en comentarios y vemos cuál gana.",
   "Suscríbete y activa la campana, que esta semana va a ser muy intensa.",
  ]),
 ]),
# ---------------------------------------------------------------- 06
dict(
 id="06-mapa-leonida",
 palette="ocean",
 title="El MAPA de GTA 6 explicado: las 6 regiones de Leonida",
 thumb=dict(top="EL MAPA DE", big="GTA 6", badge="6 ZONAS", note="LEONIDA EXPLICADA"),
 scenes=[
  dict(type="title", kicker="EL MAPA", title="BIENVENIDO A LEONIDA", sub="Las 6 regiones que conocemos", say=[
   "GTA 6 no pasa solo en Vice City. Pasa en Leonida, un estado entero inspirado en Florida.",
   "Te explico las seis regiones que conocemos, qué esperar de cada una, y un aviso sobre los mapas que vas a ver por internet.",
  ]),
  dict(type="map", heading="LEONIDA", regions=[
     "Vice City", "Leonida Keys", "Grassrivers", "Port Gellhorn", "Ambrosia", "Mount Kalaga",
   ], say=[
   "Vamos región por región.",
   "Vice City. La gran ciudad, inspirada en Miami. Playas, neones, rascacielos y la vida nocturna más loca del juego.",
   "Leonida Keys. Una cadena de islas al sur, inspirada en los Cayos de Florida. Barcos, puentes interminables y aguas turquesa.",
   "Grassrivers. Pantanos al estilo de los Everglades. Hidrodeslizadores, caimanes, y seguramente lo más salvaje del mapa.",
   "Port Gellhorn. Una zona costera venida a menos, con aire de destino turístico de otra época.",
   "Ambrosia. El interior más rural e industrial, con fábricas y pueblos pequeños.",
   "Y Mount Kalaga. Un parque nacional con bosques y montaña, perfecto para escaparse de la ciudad.",
  ]),
  dict(type="warning", title="OJO CON LOS MAPAS «FILTRADOS»", text="Rockstar no ha publicado el mapa completo. Los que circulan son reconstrucciones de fans a partir de los tráilers.", say=[
   "Un aviso importante.",
   "Rockstar no ha publicado todavía el mapa completo. Los mapas detallados que ves por internet son reconstrucciones de la comunidad, hechas a partir de los tráilers.",
   "Algunas son increíbles, pero no son oficiales. Y que conozcamos seis regiones con nombre no significa que sean las únicas.",
  ]),
  dict(type="bullets", heading="QUÉ ESPERAR", items=[
     "Ciudad, pantano, islas y montaña",
     "Agua por todas partes: barcos y aviones",
     "Fauna salvaje en las zonas rurales",
   ], say=[
   "¿Qué podemos esperar?",
   "Muchísima variedad: ciudad, pantano, islas y montaña en un mismo mapa.",
   "Agua por todas partes, así que barcos, motos de agua y aviones van a ser clave para moverse.",
   "Y fauna salvaje en las zonas rurales, que en los tráilers ya se ha dejado ver.",
  ]),
  dict(type="outro", title="¿QUÉ ZONA EXPLORAS PRIMERO?", sub="Te leo en comentarios", say=[
   "¿Cuál es la primera zona que vas a explorar? Yo lo tengo claro: Vice City de noche.",
   "Suscríbete, porque en cuanto salga el juego vamos a recorrer Leonida entera. Nos vemos allí.",
  ]),
 ]),
# ---------------------------------------------------------------- 07
dict(
 id="07-lucia-jason-historia",
 palette="sunset",
 title="Lucía y Jason: TODO lo que sabemos de la historia de GTA 6 (sin spoilers)",
 thumb=dict(top="LUCÍA", big="Y JASON", badge="SIN SPOILERS", note="LA HISTORIA DE GTA 6"),
 scenes=[
  dict(type="title", kicker="HISTORIA · SIN SPOILERS", title="LUCÍA Y JASON", sub="Lo que sabemos antes de jugar", say=[
   "Dos protagonistas, una pareja, y un estado entero en su contra.",
   "Te cuento todo lo que sabemos de Lucía, de Jason y de los personajes que les rodean. Solo con lo que ha mostrado Rockstar, sin spoilers.",
  ]),
  dict(type="bullets", heading="LUCÍA CAMINOS", items=[
     "Protagonista junto a Jason",
     "La vemos salir de prisión en el primer tráiler",
     "Quiere una vida mejor… a su manera",
   ], say=[
   "Empezamos por Lucía Caminos.",
   "Es una de las dos protagonistas, la primera mujer protagonista de un GTA principal en la era moderna.",
   "En el primer tráiler la conocemos en prisión, en el sistema penitenciario de Leonida.",
   "Y todo apunta a que sale con las ideas muy claras: conseguir una vida mejor, aunque sea por el camino difícil.",
  ]),
  dict(type="bullets", heading="JASON DUVAL", items=[
     "Pasado en el ejército",
     "Trabajos turbios en los Keys",
     "Conoce a Lucía y todo cambia",
   ], say=[
   "Jason Duval.",
   "El tráiler final abre con su pasado en el ejército, algo que le ha marcado.",
   "Después lo vemos haciendo trabajos turbios en los Keys para gente poco recomendable.",
   "Y cuando se cruza con Lucía, todo cambia. Para bien y para mal.",
  ]),
  dict(type="bullets", heading="LOS SECUNDARIOS", items=[
     "Cal Hampton · el amigo de Jason",
     "Brian Heder · veterano del contrabando",
     "Boobie Ike · leyenda local de Vice City",
     "Dre'Quan Priest · aspirante a magnate musical",
     "Real Dimez · dúo de raperas",
     "Raul Bautista · atracador experimentado",
   ], say=[
   "Y los secundarios que ya conocemos.",
   "Cal Hampton, el amigo de Jason, un tipo que desconfía de todo.",
   "Brian Heder, un veterano del contrabando en los Keys.",
   "Boobie Ike, toda una leyenda local en Vice City, con negocios en la noche y en la música.",
   "Dre'Quan Priest, un aspirante a magnate de la música que quiere llegar a lo más alto.",
   "Real Dimez, un dúo de raperas en plena subida.",
   "Y Raul Bautista, un atracador con mucha experiencia, de esos que buscan socios con agallas.",
  ]),
  dict(type="checklist", heading="EL TONO DEL JUEGO", items=[
     "Pareja criminal al estilo Bonnie y Clyde",
     "Atracos, persecuciones y redes sociales",
     "Sátira de la Florida moderna",
   ], say=[
   "¿Y el tono de la historia?",
   "Una pareja criminal al más puro estilo Bonnie y Clyde.",
   "Atracos, persecuciones, y unas redes sociales que lo graban y lo comentan todo.",
   "Y la sátira de siempre de Rockstar, esta vez sobre la Florida más loca de internet.",
  ]),
  dict(type="outro", title="¿LUCÍA O JASON?", sub="¿Con quién te quedas?", say=[
   "¿Con quién te quedas, con Lucía o con Jason? Te leo en comentarios.",
   "Suscríbete, y cuando juegues, cuidado con los spoilers. Nos vemos en Leonida.",
  ]),
 ]),
# ---------------------------------------------------------------- 08
dict(
 id="08-historia-espera",
 palette="miami",
 title="De 2013 a 2026: la LARGA espera de GTA 6 en 3 minutos",
 thumb=dict(top="13 AÑOS", big="ESPERANDO", badge="2013→2026", note="LA HISTORIA DE GTA 6"),
 scenes=[
  dict(type="title", kicker="2013 → 2026", title="LA LARGA ESPERA", sub="Cómo hemos llegado hasta GTA 6", say=[
   "Trece años. Eso es lo que ha pasado entre GTA cinco y GTA 6.",
   "Antes de que empieces a jugar, repasamos en pocos minutos cómo hemos llegado hasta aquí: anuncios, filtraciones, tráilers y retrasos.",
  ]),
  dict(type="timeline", heading="DE GTA V AL ANUNCIO", events=[
     ("2013", "Sale GTA V"),
     ("2022", "Rockstar confirma GTA 6"),
     ("2022", "La gran filtración"),
   ], say=[
   "Todo empieza en septiembre de dos mil trece.",
   "Sale GTA cinco, que acabaría convirtiéndose en uno de los productos de entretenimiento más vendidos de la historia.",
   "En febrero de dos mil veintidós, Rockstar confirma por fin que el siguiente GTA está en desarrollo.",
   "Y en septiembre de ese mismo año llega la mayor filtración de su historia: decenas de vídeos de una versión de desarrollo, publicados en internet.",
  ]),
  dict(type="timeline", heading="LOS TRÁILERS", events=[
     ("DIC 2023", "Tráiler 1"),
     ("MAY 2025", "Tráiler 2"),
     ("OCT 2026", "Tráiler final"),
   ], say=[
   "Después llegaron los tráilers.",
   "En diciembre de dos mil veintitrés, el primero, que se publicó antes de tiempo por una filtración y batió récords de visualizaciones.",
   "En mayo de dos mil veinticinco, el segundo, centrado en Jason y Lucía, que volvió a romper récords.",
   "Y en octubre de dos mil veintiséis, el tráiler final de lanzamiento.",
  ]),
  dict(type="timeline", heading="LOS RETRASOS", events=[
     ("2025", "Fecha inicial"),
     ("26 MAY 2026", "Primer retraso"),
     ("19 NOV 2026", "Fecha definitiva"),
   ], say=[
   "Y claro, los retrasos.",
   "La idea original era lanzarlo en dos mil veinticinco.",
   "En mayo de ese año, Rockstar lo retrasó al veintiséis de mayo de dos mil veintiséis.",
   "Y en noviembre de dos mil veinticinco llegó el segundo retraso, a la fecha que por fin ha aguantado: el diecinueve de noviembre de dos mil veintiséis.",
  ]),
  dict(type="stat", value="19.11", label="EL DÍA HA LLEGADO", sub="PS5 · Xbox Series X|S", say=[
   "Y aquí estamos.",
   "Después de trece años, dos retrasos y miles de teorías, GTA 6 ya está en nuestras consolas. Ahora solo queda saber si ha merecido la pena la espera.",
  ]),
  dict(type="outro", title="¿DESDE CUÁNDO ESPERAS?", sub="Cuéntamelo en comentarios", say=[
   "Cuéntame en los comentarios desde cuándo estás esperando este juego. Seguro que hay gente que lleva desde dos mil trece.",
   "Suscríbete, que esto no ha hecho más que empezar.",
  ]),
 ]),
# ---------------------------------------------------------------- 09
dict(
 id="09-antes-de-jugar",
 palette="neon",
 title="10 cosas que tienes que hacer ANTES de empezar a jugar GTA 6",
 thumb=dict(top="HAZ ESTO", big="ANTES DE JUGAR", badge="10", note="GTA 6 · CHECKLIST"),
 scenes=[
  dict(type="title", kicker="CHECKLIST", title="10 COSAS ANTES DE JUGAR", sub="Para exprimir GTA 6 desde el minuto uno", say=[
   "Has esperado años. No lo estropees en el último momento.",
   "Estas son diez cosas que tienes que hacer antes de empezar a jugar a GTA 6, para que la primera partida sea perfecta.",
  ]),
  dict(type="checklist", heading="PREPARA LA CONSOLA", items=[
     "1 · Precarga completa",
     "2 · Modo reposo con internet",
     "3 · 30 GB extra para parches",
     "4 · Mando cargado (y uno de reserva)",
   ], say=[
   "Primero, la consola.",
   "Uno: ten la precarga hecha al cien por cien.",
   "Dos: deja la consola en modo reposo con internet, para que baje cualquier parche sola.",
   "Tres: deja unos treinta gigas extra libres para futuras actualizaciones.",
   "Cuatro: carga el mando. Y si tienes otro, cárgalo también. Créeme.",
  ]),
  dict(type="checklist", heading="PREPARA LA TELE", items=[
     "5 · Activa el modo juego",
     "6 · Calibra el HDR de la consola",
     "7 · Prueba los cascos o el sonido",
   ], say=[
   "Segundo, la pantalla y el sonido.",
   "Cinco: activa el modo juego de tu tele. Reduce el retraso entre el mando y la imagen.",
   "Seis: calibra el HDR desde los ajustes de la consola. Vice City de noche lo merece.",
   "Siete: prueba tus cascos o tu equipo de sonido. Rockstar cuida muchísimo el audio, y la radio es media vida en GTA.",
  ]),
  dict(type="checklist", heading="PREPÁRATE TÚ", items=[
     "8 · Reclama tus bonus de reserva",
     "9 · Silencia palabras para evitar spoilers",
     "10 · Reserva tiempo y no corras",
   ], say=[
   "Y tercero, tú.",
   "Ocho: si reservaste en digital, revisa que tienes el bonus de reserva y tu mes de GTA plus.",
   "Nueve: silencia palabras clave en tus redes sociales. Los spoilers van a volar desde el primer día.",
   "Y diez: resérvate tiempo y no corras la historia. Explora, pierde el tiempo, déjate sorprender. Eso es GTA.",
  ]),
  dict(type="outro", title="¿TE FALTABA ALGUNO?", sub="Comenta tu consejo", say=[
   "¿Se me ha escapado alguno? Déjame tu consejo en los comentarios.",
   "Suscríbete y activa la campana. Nos vemos en Leonida.",
  ]),
 ]),
# ---------------------------------------------------------------- 10
dict(
 id="10-resumen-gta6",
 palette="cyber",
 title="GTA 6 en 3 minutos: TODO lo que tienes que saber antes de jugar",
 thumb=dict(top="GTA 6 EN", big="3 MINUTOS", badge="TODO", note="LO QUE TIENES QUE SABER"),
 scenes=[
  dict(type="title", kicker="RESUMEN", title="GTA 6 EN 3 MINUTOS", sub="Todo lo que tienes que saber antes de jugar", say=[
   "Si solo vas a ver un vídeo antes de jugar a GTA 6, que sea este.",
   "Fecha, precio, tamaño, consolas, mapa, protagonistas y PC. Todo, en menos de tres minutos.",
  ]),
  dict(type="stat", value="19 NOV", label="FECHA DE LANZAMIENTO", sub="00:00 hora local · PS5 y Xbox Series X|S", say=[
   "La fecha: jueves diecinueve de noviembre de dos mil veintiséis.",
   "Se desbloquea a medianoche, hora local de cada país, en PS5 y en Xbox Series X y Series S.",
  ]),
  dict(type="compare", heading="PRECIO", cols=[
     dict(title="STANDARD", big="79,99 €", lines=["Física y digital"]),
     dict(title="ULTIMATE", big="99,99 €", lines=["Solo digital", "Extras de historia"]),
   ], say=[
   "El precio: setenta y nueve con noventa y nueve euros la Standard, y noventa y nueve con noventa y nueve la Ultimate, que solo existe en digital.",
   "Las dos incluyen el bonus de reserva, el Vintage Vice City Pack. Y puedes pasar de Standard a Ultimate más adelante.",
  ]),
  dict(type="stat", value="212 GB", label="TAMAÑO", sub="Precarga disponible desde el 10 de noviembre", say=[
   "El tamaño: hasta doscientos doce gigas. Deja margen, y si no lo has precargado ya, hazlo ahora.",
  ]),
  dict(type="stat", value="30 FPS", label="RENDIMIENTO", sub="PS5 Pro: sombras con ray tracing", say=[
   "El rendimiento: apunta a treinta fotogramas por segundo en todas las consolas.",
   "La PS5 Pro tiene ventajas visuales, como sombras con ray tracing, pero no hay modo a sesenta anunciado.",
  ]),
  dict(type="map", heading="LEONIDA", regions=[
     "Vice City", "Leonida Keys", "Grassrivers", "Port Gellhorn", "Ambrosia", "Mount Kalaga",
   ], say=[
   "El mapa: Leonida, un estado inspirado en Florida, con seis regiones conocidas.",
   "Vice City, la gran ciudad.",
   "Leonida Keys, las islas del sur.",
   "Grassrivers, los pantanos.",
   "Port Gellhorn, la costa.",
   "Ambrosia, el interior.",
   "Y Mount Kalaga, la montaña.",
  ]),
  dict(type="bullets", heading="PROTAGONISTAS", items=[
     "Lucía Caminos",
     "Jason Duval",
     "Una pareja contra todo Leonida",
   ], say=[
   "Los protagonistas.",
   "Lucía Caminos, a la que conocemos saliendo de prisión.",
   "Jason Duval, un exmilitar metido en trabajos turbios.",
   "Juntos, una pareja criminal al estilo Bonnie y Clyde.",
  ]),
  dict(type="warning", title="¿Y EN PC?", text="No hay versión de PC anunciada. Cualquier descarga «gratis» para PC es una estafa.", say=[
   "Y el PC: no hay versión anunciada, ni fecha.",
   "Cualquier web que te ofrezca GTA 6 para PC gratis es una estafa. No lo descargues.",
  ]),
  dict(type="outro", title="¡NOS VEMOS EN LEONIDA!", sub="Suscríbete para más GTA 6", say=[
   "Y esto es todo lo que necesitas saber. En el canal tienes un vídeo dedicado a cada uno de estos temas.",
   "Suscríbete, activa la campana, y disfruta de GTA 6. Nos vemos en Leonida.",
  ]),
 ]),
]
