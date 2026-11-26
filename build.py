#!/usr/bin/env python3
"""Builds the static site for thedivproject.com into ./site (EN at /, ES at /es/)."""
import json, os, shutil, html

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, 'docs')  # GitHub Pages serves this folder
WEB = os.path.join(ROOT, 'src', 'images')

# ---- Settings you may change ----
AVAILABLE_OFFICES = 2
EMAIL = 'info@thedivproject.com'
MAPS = 'https://goo.gl/maps/zZpvHULTJyQvUufR8'
IG = 'https://www.instagram.com/thedivproject/'

IMAGES = {
    'hero': 'hero.jpg', 'living': 'living.jpg', 'office': 'office.jpg', 'office2': 'office2.jpg',
    'conf': 'conf.jpg', 'garden': 'garden.jpg', 'garden2': 'garden2.jpg', 'coffee': 'coffee.jpg',
    'kitchen': 'kitchen.jpg', 'hall': 'hall.jpg', 'sign': 'sign.jpg', 'mail': 'mail.jpg',
    'openoffice': 'openoffice.jpg', 'og': 'og.jpg', 'og_es': 'og-es.jpg',
}

ICONS = {
    'wifi': 'M2 9a15 15 0 0 1 20 0M5 12.5a10 10 0 0 1 14 0M8.5 16a5 5 0 0 1 7 0M12 19.5h.01',
    'clock': 'M12 3a9 9 0 1 0 0 18a9 9 0 1 0 0-18M12 7v5l3 2',
    'cal': 'M4 6h16v14H4zM4 10h16M8 3v5M16 3v5',
    'table': 'M3 10h18M6 10v9M18 10v9M8 6h8',
    'cup': 'M5 8h11v6a5 5 0 0 1-5 5h-1a5 5 0 0 1-5-5zM16 10h2a2 2 0 0 1 0 4h-2M8 3v2M12 3v2',
    'fork': 'M7 3v8a2 2 0 0 0 2 2v8M11 3v8M15 3c-1.5 2-2 4-2 7h3v11',
    'mail': 'M3 6h18v12H3zM3 7l9 6l9-6',
    'car': 'M5 16v-4l2-5h10l2 5v4zM5 16v2M19 16v2M8 13h.01M16 13h.01',
    'sofa': 'M4 11V8a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v3M3 11h4v4h10v-4h4v6H3zM5 17v2M19 17v2',
    'star': 'M12 3l2.6 5.6L20 9.3l-4 4l1 5.7L12 16.3L7 19l1-5.7l-4-4l5.4-.7z',
}

REVIEWS = [
    ('Excellent place to work. Management was very easy to work with. The facilities are well designed and clean.', 'Abbas Jessa'),
    ('Easy to park and walk to your office. Lots of trees around the property and comfortable social areas.', 'Santiago Rojas'),
    ('Good amenities, lot of parking spaces, always good coffee and snacks, and reasonable prices, close to everything!', 'Anji Ismail'),
]

T = {
'en': dict(
    lang='en', path='/', other='es/', home='./', other_label='ES',
    title='The Div Project — Coworking & private offices in South Miami',
    desc='A one-story house turned coworking in South Miami: private offices, a conference room and a garden. Open 24/7, free parking, month-to-month terms.',
    nav=['The house', "What's included", 'Spaces', 'FAQ'], book='Book a visit',
    mail_subject='Visit request — The Div', mail_body='Hi! I would like to schedule a visit to The Div.%0D%0A%0D%0AName:%0D%0AWhat I need (office / conference room / other):%0D%0APreferred dates:%0D%0A',
    avail=lambda n: '1 private office available' if n == 1 else f'{n} private offices available',
    h1='A house<br>to work in.',
    hero_p='Private offices, a conference room and a garden in South Miami. Open 24/7, free parking, one month at a time.',
    explore='Explore the house',
    strip=[('Available now', lambda n: f'{n} offices'), ('Address', '5798 SW 68 St'), ('Access', '24/7'), ('Terms', 'Month to month')],
    intro_h='A one-story house turned coworking — natural light, a living room, a garden, and an office door that’s yours.',
    intro_p='Home base for freelancers, small teams, therapists, consultants and remote workers who want somewhere calmer than an office tower. Flexible, relaxed, and balanced between work and life.',
    tour_k='Sheet 01 — The house', tour_h='Walk through<br>the house.', tour_p='Seven rooms, one front door. Pick a room to look inside.',
    rooms=[
        ('garden2', 'Garden', 'Picnic tables under the trees — for lunch, calls in the fresh air, or a break between meetings.'),
        ('living', 'Living room', 'Sofas, plants and big windows. Where members take a break or meet clients informally.'),
        ('coffee', 'Kitchen & coffee', 'Equipped kitchenette and coffee bar. Coffee, tea, water and snacks are free for members.'),
        ('office', 'Private offices', 'Lockable offices with electric standing desks, ergonomic chairs, natural light and blinds you control.'),
        ('conf', 'Conference room', 'Seats 6 with a screen for presentations and video calls. Members get 2 hours a month included.'),
        ('hero', 'Entrance', '24/7 electronic access with your phone and fingerprint. Mail is handed to you directly.'),
        ('sign', 'Parking', 'Free parking for members and guests, right at the house.'),
    ],
    inc_k="What's included", inc_h='One rent.<br>Everything in it.',
    inc_p='Focus on your work — the internet, the coffee, the cleaning and the mail are taken care of.',
    items=[('wifi', 'Fast Wi-Fi', 'Secure and uninterrupted.'), ('clock', '24/7 access', 'Get in with your phone and fingerprint.'),
           ('cal', 'Flexible terms', 'One month in advance, no long lease.'), ('table', 'Conference room', '2 hours a month included.'),
           ('cup', 'Coffee, tea & snacks', 'Free for every member.'), ('fork', 'Kitchenette', 'Fully equipped, use it any time.'),
           ('mail', 'Mailbox', 'Your mail, handed to you directly.'), ('car', 'Free parking', 'For members and guests.'),
           ('sofa', 'Common areas', 'A living room and a garden.'), ('star', 'Events', 'We like to keep it social.')],
    band=[('openoffice', 'Shared office with desks'), ('kitchen', 'Kitchenette counter with stools'), ('mail', 'Member mailboxes')],
    spaces_h='Choose your space',
    spaces=[
        ('office2', 'Private office', True, 'Your own lockable office, all amenities included. One month in advance.', 'Ask about availability', 'Private office'),
        ('conf', 'Conference room', False, 'Seats 6, screen ready. Members get 2 hours a month; anyone can book it by the hour.', 'Ask about booking', 'Conference room'),
        ('garden', 'Host in the garden', False, 'Have an idea for a pop-up, workshop or small gathering? The garden is open for it — tell us what you have in mind.', 'Pitch your idea', 'Garden event idea'),
    ],
    available_n=lambda n: f'{n} available',
    rev_k='Sheet 02 — Reviews', rev_h='From our members', rev_badge='on Google · 20 reviews', rev_src='Google review',
    faq_h='Good<br>questions.',
    faqs=[
        ('How do I book a visit?', f'Tap “Book a visit” anywhere on this page or email {EMAIL}, and we’ll set a time.'),
        ('How much does it cost?', 'It depends on the office and how long you need it. Send us a request and we’ll reply with current availability and rates.'),
        ('Is there a long-term contract?', 'No. Terms are month to month — one month of rent in advance.'),
        ('Can I come in at night or on weekends?', 'Yes. Members have 24/7 electronic access with their phone and fingerprint.'),
        ('Is parking included?', 'Yes, free parking for members and their guests.'),
        ('Can I use the conference room?', 'Every member gets 2 hours a month of conference room time.'),
        ('Can I get my mail here?', 'Yes. Members have a postal box and mail is handed to them directly.'),
    ],
    visit_h='Come see<br>the house.', visit_p='Leave us a note and we’ll set up a visit.',
    visit_btn='Request a visit →', visit_small=f'Tell us what you need — we’ll reply with availability and rates.',
    addr='5798 SW 68th Street<br>South Miami, FL 33143', maps='Google Maps', menu='Menu', skip='Skip to content',
    tour_room='Room',
),
'es': dict(
    lang='es', path='/es/', other='../', home='../', other_label='EN',
    title='The Div Project — Coworking y oficinas privadas en South Miami',
    desc='Una casa de un piso convertida en coworking en South Miami: oficinas privadas, sala de reuniones y jardín. Abierto 24/7, estacionamiento gratis, mes a mes.',
    nav=['La casa', 'Qué incluye', 'Espacios', 'Preguntas'], book='Agenda una visita',
    mail_subject='Solicitud de visita — The Div', mail_body='¡Hola! Me gustaría agendar una visita a The Div.%0D%0A%0D%0ANombre:%0D%0AQué necesito (oficina / sala de reuniones / otro):%0D%0AFechas preferidas:%0D%0A',
    avail=lambda n: '1 oficina privada disponible' if n == 1 else f'{n} oficinas privadas disponibles',
    h1='Una casa<br>para trabajar.',
    hero_p='Oficinas privadas, una sala de reuniones y un jardín en South Miami. Abierto 24/7, estacionamiento gratis y mes a mes.',
    explore='Conoce la casa',
    strip=[('Disponibles hoy', lambda n: f'{n} oficinas'), ('Dirección', '5798 SW 68 St'), ('Acceso', '24/7'), ('Términos', 'Mes a mes')],
    intro_h='Una casa de un piso convertida en coworking: luz natural, una sala, un jardín y una oficina con puerta propia.',
    intro_p='El lugar para freelancers, equipos pequeños, terapeutas, consultores y trabajadores remotos que buscan algo más tranquilo que una torre de oficinas. Flexible, relajado y con balance entre el trabajo y la vida.',
    tour_k='Plano 01 — La casa', tour_h='Recorre<br>la casa.', tour_p='Siete espacios, una sola puerta. Elige uno para verlo por dentro.',
    rooms=[
        ('garden2', 'Jardín', 'Mesas bajo los árboles para almorzar, hacer llamadas al aire libre o descansar entre reuniones.'),
        ('living', 'Sala', 'Sofás, plantas y ventanales. Donde los miembros toman un descanso o se reúnen con clientes de forma informal.'),
        ('coffee', 'Cocina y café', 'Cocina equipada y barra de café. Café, té, agua y snacks gratis para los miembros.'),
        ('office', 'Oficinas privadas', 'Oficinas con llave, escritorios eléctricos de pie, sillas ergonómicas, luz natural y cortinas que tú controlas.'),
        ('conf', 'Sala de reuniones', 'Para 6 personas, con pantalla para presentaciones y videollamadas. Los miembros tienen 2 horas al mes incluidas.'),
        ('hero', 'Entrada', 'Acceso electrónico 24/7 con tu teléfono y huella. Te entregamos el correo directamente.'),
        ('sign', 'Estacionamiento', 'Estacionamiento gratis para miembros e invitados, en la misma casa.'),
    ],
    inc_k='Qué incluye', inc_h='Una renta.<br>Todo incluido.',
    inc_p='Enfócate en tu trabajo: el internet, el café, la limpieza y el correo corren por nuestra cuenta.',
    items=[('wifi', 'Wi-Fi rápido', 'Seguro y sin interrupciones.'), ('clock', 'Acceso 24/7', 'Entra con tu teléfono y tu huella.'),
           ('cal', 'Términos flexibles', 'Un mes por adelantado, sin contratos largos.'), ('table', 'Sala de reuniones', '2 horas al mes incluidas.'),
           ('cup', 'Café, té y snacks', 'Gratis para todos los miembros.'), ('fork', 'Cocina', 'Totalmente equipada, úsala cuando quieras.'),
           ('mail', 'Buzón', 'Te entregamos tu correo directamente.'), ('car', 'Estacionamiento gratis', 'Para miembros e invitados.'),
           ('sofa', 'Áreas comunes', 'Una sala y un jardín.'), ('star', 'Eventos', 'Nos gusta compartir de vez en cuando.')],
    band=[('openoffice', 'Oficina compartida con escritorios'), ('kitchen', 'Barra de cocina con bancos'), ('mail', 'Buzones de los miembros')],
    spaces_h='Elige tu espacio',
    spaces=[
        ('office2', 'Oficina privada', True, 'Tu propia oficina con llave, con todo incluido. Un mes por adelantado.', 'Pregunta por disponibilidad', 'Oficina privada'),
        ('conf', 'Sala de reuniones', False, 'Para 6 personas, con pantalla. Los miembros tienen 2 horas al mes; cualquiera puede reservarla por hora.', 'Pregunta por reservas', 'Sala de reuniones'),
        ('garden', 'Organiza algo en el jardín', False, '¿Tienes una idea para un pop-up, un taller o una reunión pequeña? El jardín está abierto para eso: cuéntanos qué tienes en mente.', 'Propón tu idea', 'Idea para el jardín'),
    ],
    available_n=lambda n: f'{n} disponibles',
    rev_k='Plano 02 — Reseñas', rev_h='Lo que dicen nuestros miembros', rev_badge='en Google · 20 reseñas', rev_src='Reseña de Google',
    faq_h='Buenas<br>preguntas.',
    faqs=[
        ('¿Cómo agendo una visita?', f'Toca “Agenda una visita” en cualquier parte de esta página o escribe a {EMAIL} y coordinamos un horario.'),
        ('¿Cuánto cuesta?', 'Depende de la oficina y del tiempo que la necesites. Envíanos una solicitud y te respondemos con la disponibilidad y las tarifas actuales.'),
        ('¿Hay que firmar un contrato largo?', 'No. Los términos son mes a mes, con un mes de renta por adelantado.'),
        ('¿Puedo venir de noche o los fines de semana?', 'Sí. Los miembros tienen acceso electrónico 24/7 con su teléfono y su huella.'),
        ('¿El estacionamiento está incluido?', 'Sí, es gratis para miembros y sus invitados.'),
        ('¿Puedo usar la sala de reuniones?', 'Cada miembro tiene 2 horas al mes de sala de reuniones.'),
        ('¿Puedo recibir mi correo aquí?', 'Sí. Los miembros tienen un buzón y les entregamos el correo directamente.'),
    ],
    visit_h='Ven a conocer<br>la casa.', visit_p='Escríbenos y coordinamos una visita.',
    visit_btn='Solicita una visita →', visit_small='Cuéntanos qué necesitas y te respondemos con disponibilidad y tarifas.',
    addr='5798 SW 68th Street<br>South Miami, FL 33143', maps='Google Maps', menu='Menú', skip='Saltar al contenido',
    tour_room='Espacio',
),
}

def esc(s): return html.escape(s, quote=True)

def cta(t, topic=None):
    subj = t['mail_subject'] + (f' ({topic})' if topic else '')
    return f'mailto:{EMAIL}?subject={subj.replace(" ", "%20")}&amp;body={t["mail_body"].replace(" ", "%20")}'

def page(t):
    n = AVAILABLE_OFFICES
    a = '../' if t['lang'] == 'es' else ''
    img = lambda k: f'{a}assets/{IMAGES[k]}'
    nav_ids = ['house', 'included', 'spaces', 'faq']
    navlinks = ''.join(f'<a href="#{i}">{l}</a>' for i, l in zip(nav_ids, t['nav']))
    strip = ''.join(f'<div><span>{k}</span>{v(n) if callable(v) else v}</div>' for k, v in t['strip'])
    rooms_js = json.dumps([{'img': img(k), 'name': nm, 'desc': d} for k, nm, d in t['rooms']], ensure_ascii=False)
    r0 = t['rooms'][3]
    room_btns = ''.join(
        f'<button type="button" class="room{" on" if i == 3 else ""}" data-i="{i}" aria-pressed="{"true" if i == 3 else "false"}">'
        f'<img src="{img(k)}" alt="" loading="lazy" width="72" height="56"><span><small>{i+1:02d}</small>{nm}</span></button>'
        for i, (k, nm, d) in enumerate(t['rooms']))
    items = ''.join(
        f'<li><span class="ic"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="{ICONS[ic]}"/></svg></span>'
        f'<div><b>{ti}</b><span>{d}</span></div></li>' for ic, ti, d in t['items'])
    band = ''.join(f'<img src="{img(k)}" alt="{esc(al)}" loading="lazy">' for k, al in t['band'])
    av_tag = f'<span class="mono">{t["available_n"](n)}</span>' if n > 0 else ''
    spaces = ''.join(
        f'<article class="space"><img src="{img(k)}" alt="" loading="lazy"><div class="scrim"></div>'
        f'<div class="space-top"><h3>{ti}</h3>{av_tag if av else ""}</div>'
        f'<div class="space-bot"><p>{d}</p><a class="btn light" data-cta href="{cta(t, topic)}">{c}</a></div></article>'
        for k, ti, av, d, c, topic in t['spaces'])
    reviews = ''.join(f'<figure><blockquote>“{q}”</blockquote><figcaption>{who} · {t["rev_src"]}</figcaption></figure>' for q, who in REVIEWS)
    faqs = ''.join(f'<details{" open" if i == 0 else ""}><summary>{q}<span aria-hidden="true"></span></summary><p>{ans}</p></details>' for i, (q, ans) in enumerate(t['faqs']))
    avail_badge = f'<p class="badge"><i aria-hidden="true"></i>{t["avail"](n)}</p>' if n > 0 else ''
    sticky_avail = f'<span class="sa"><i aria-hidden="true"></i>{t["avail"](n)}</span>' if n > 0 else ''
    ld = {"@context": "https://schema.org", "@type": "LocalBusiness", "name": "The Div Project",
          "description": t['desc'], "url": "https://www.thedivproject.com" + t['path'], "email": EMAIL,
          "image": "https://www.thedivproject.com/assets/hero.jpg",
          "address": {"@type": "PostalAddress", "streetAddress": "5798 SW 68th Street", "addressLocality": "South Miami", "addressRegion": "FL", "postalCode": "33143", "addressCountry": "US"},
          "geo": {"@type": "GeoCoordinates", "latitude": 25.7078767, "longitude": -80.2873787},
          "openingHours": "Mo-Su 00:00-23:59", "sameAs": [IG],
          "aggregateRating": {"@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "20"}}
    return f'''<!doctype html>
<html lang="{t['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t['title']}</title>
<meta name="description" content="{esc(t['desc'])}">
<link rel="canonical" href="https://www.thedivproject.com{t['path']}">
<link rel="alternate" hreflang="en" href="https://www.thedivproject.com/">
<link rel="alternate" hreflang="es" href="https://www.thedivproject.com/es/">
<link rel="alternate" hreflang="x-default" href="https://www.thedivproject.com/">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(t['title'])}">
<meta property="og:description" content="{esc(t['desc'])}">
<meta property="og:image" content="https://www.thedivproject.com/assets/{'og-es.jpg' if t['lang']=='es' else 'og.jpg'}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:site_name" content="The Div Project">
<meta property="og:locale" content="{'es_US' if t['lang']=='es' else 'en_US'}">
<meta name="twitter:card" content="summary_large_image">
<meta property="og:url" content="https://www.thedivproject.com{t['path']}">
<meta name="theme-color" content="#0A4F5C">
<link rel="icon" href="{a}assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,700&amp;family=DM+Mono:wght@400;500&amp;display=swap" rel="stylesheet">
<link rel="stylesheet" href="{a}assets/style.css">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
<a class="skip" href="#main">{t['skip']}</a>
<header class="hero" style="background-image:url({img('hero')})">
<div class="scrim"></div>
<nav class="wrap nav" aria-label="Main">
<a href="{t['home']}" class="logo"><img src="{a}assets/logo.png" alt="the div project" width="219" height="80"></a>
<div class="links">{navlinks}
<a class="lang" href="{t['other']}" hreflang="{'es' if t['lang']=='en' else 'en'}" lang="{'es' if t['lang']=='en' else 'en'}">{t['other_label']}</a>
<a class="btn light sm" data-cta href="{cta(t)}">{t['book']}</a></div>
</nav>
<div class="wrap hero-body">
{avail_badge}
<h1>{t['h1']}</h1>
<div class="hero-row"><p>{t['hero_p']}</p>
<div class="btns"><a class="btn light" data-cta href="{cta(t)}">{t['book']}</a><a class="btn ghost" href="#house">{t['explore']}</a></div></div>
<div class="strip mono">{strip}</div>
</div>
</header>
<main id="main">
<section class="teal"><div class="wrap intro"><h2>{t['intro_h']}</h2><p>{t['intro_p']}</p></div></section>

<section id="house" class="bp"><div class="wrap pad">
<div class="head"><h2 class="big">{t['tour_h']}</h2><p>{t['tour_p']}</p></div>
<div class="tour">
<div class="tour-view"><img id="tourImg" src="{img(r0[0])}" alt="{esc(r0[1])}">
<div class="tour-card"><span class="mono" id="tourCode">04 / 07</span><h3 id="tourName">{r0[1]}</h3><p id="tourDesc">{r0[2]}</p></div></div>
<div class="rooms" role="group" aria-label="{t['tour_room']}">{room_btns}</div>
</div></div></section>

<section id="included" class="teal"><div class="wrap pad inc">
<div class="inc-head"><h2 class="big">{t['inc_h']}</h2><p>{t['inc_p']}</p></div>
<ul class="items">{items}</ul>
<div class="band">{band}</div>
</div></section>

<section id="spaces" class="dark"><div class="wrap pad"><h2 class="big mb">{t['spaces_h']}</h2><div class="spaces">{spaces}</div></div></section>

<section class="bp"><div class="wrap pad">
<div class="head"><h2 class="big">{t['rev_h']}</h2>
<a class="rating" href="{MAPS}"><span aria-hidden="true">★★★★★</span><span><b>5.0</b> {t['rev_badge']} →</span></a></div>
<div class="reviews">{reviews}</div>
</div></section>

<section id="faq" class="sand"><div class="wrap pad faq"><h2 class="big">{t['faq_h']}</h2><div class="qs">{faqs}</div></div></section>

<section id="visit" class="visit" style="background-image:url({img('hall')})"><div class="scrim"></div>
<div class="wrap pad visit-in"><div><h2 class="big">{t['visit_h']}</h2><p>{t['visit_p']}</p></div>
<div class="visit-cta"><a class="btn light xl" data-cta href="{cta(t)}">{t['visit_btn']}</a>
<p>{t['visit_small']} <a href="mailto:{EMAIL}">{EMAIL}</a></p></div></div>
</section>
</main>
<footer><div class="wrap">
<div class="foot">
<div>{t['addr']}</div>
<div><a href="mailto:{EMAIL}">{EMAIL}</a><br><a data-cta href="{cta(t)}">{t['book']}</a></div>
<div><a href="{IG}">Instagram</a><br><a href="{MAPS}">{t['maps']}</a></div>
</div>
<p class="word" aria-hidden="true">the &lt;div&gt; project</p>
</div></footer>
<div class="sticky">{sticky_avail}<a class="btn light sm" data-cta href="{cta(t)}">{t['book']}</a></div>
<script>window.ROOMS={rooms_js};</script>
<script src="{a}assets/site.js" defer></script>
</body>
</html>
'''

CSS = r'''
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:#F4F2ED;color:#10222A;font:18px/1.5 'DM Sans',system-ui,sans-serif;-webkit-font-smoothing:antialiased}
img{max-width:100%;display:block}
a{color:#0A4F5C}a:hover{color:#10222A}
h1,h2,h3{margin:0}
.wrap{max-width:1280px;margin:0 auto;padding-left:32px;padding-right:32px}
.pad{padding-top:110px;padding-bottom:110px}
.mono{font-family:'DM Mono',monospace;font-size:13px;letter-spacing:.06em;text-transform:uppercase}
.k{margin:0 0 12px;color:#0A4F5C}.k2{margin:0;color:#9FD0D6}
.big{font-size:clamp(40px,5vw,56px);line-height:1;font-weight:700;letter-spacing:-.03em}
.mb{margin-bottom:40px}
.skip{position:absolute;left:-999px;top:8px;background:#fff;padding:8px 14px;z-index:20}.skip:focus{left:8px}
.btn{display:inline-block;padding:15px 26px;border-radius:999px;font-weight:700;text-decoration:none;font-size:16px;text-align:center}
.btn.light{background:#fff;color:#10222A}.btn.light:hover{background:#E3ECEC}
.btn.ghost{border:1.5px solid #fff;color:#fff}.btn.ghost:hover{background:rgba(255,255,255,.12);color:#fff}
.btn.sm{padding:11px 20px}.btn.xl{font-size:20px;padding:20px 32px}
.scrim{position:absolute;inset:0;background:rgba(6,40,47,.55)}
/* hero */
.hero{position:relative;min-height:820px;display:flex;flex-direction:column;background:#10222A center/cover no-repeat;color:#fff}
.nav{position:relative;display:flex;flex-wrap:wrap;gap:16px 28px;align-items:center;justify-content:space-between;padding-top:26px;padding-bottom:26px;width:100%}
.logo img{height:64px;width:auto}
.links{display:flex;flex-wrap:wrap;gap:8px 26px;align-items:center;font-size:16px}
.links>a:not(.btn){color:#fff;text-decoration:none}.links>a:not(.btn):hover{text-decoration:underline}
.lang{font-family:'DM Mono',monospace;font-size:13px;border:1px solid rgba(255,255,255,.5);border-radius:999px;padding:6px 12px}
.hero-body{position:relative;flex:1;display:flex;flex-direction:column;justify-content:flex-end;padding-bottom:40px;width:100%}
.badge{margin:0 0 24px;align-self:flex-start;display:inline-flex;align-items:center;gap:10px;padding:8px 16px;border-radius:999px;background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.35);font-size:16px;font-weight:500}
.badge i,.sa i{width:9px;height:9px;border-radius:50%;background:#7EE0B0;display:inline-block}
h1{font-size:clamp(56px,9vw,132px);line-height:.92;font-weight:700;letter-spacing:-.04em}
.hero-row{display:flex;flex-wrap:wrap;gap:24px 48px;align-items:flex-end;justify-content:space-between;margin-top:32px}
.hero-row p{margin:0;font-size:21px;max-width:520px;color:#E3ECEC}
.btns{display:flex;flex-wrap:wrap;gap:12px}
.strip{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));margin-top:48px;border:1px solid rgba(255,255,255,.45);font-size:12px}
.strip div{padding:12px 16px;border-right:1px solid rgba(255,255,255,.45)}.strip div:last-child{border-right:0}
.strip span{display:block;opacity:.7}
/* sections */
.teal{background:#0A4F5C;color:#fff}.dark{background:#10222A;color:#fff}.sand{background:#E6E3DC}
.bp{background-color:#EEF3F3;background-image:linear-gradient(#D4E0E1 1px,transparent 1px),linear-gradient(90deg,#D4E0E1 1px,transparent 1px);background-size:32px 32px}
.intro{padding-top:110px;padding-bottom:110px;display:flex;flex-wrap:wrap;gap:32px 80px}
.intro h2{flex:1 1 560px;font-size:clamp(28px,3.2vw,40px);line-height:1.15;font-weight:500;letter-spacing:-.01em}
.intro p{flex:1 1 320px;margin:0;color:#CFE0E2}
.head{display:flex;flex-wrap:wrap;gap:16px 48px;justify-content:space-between;align-items:flex-end;margin-bottom:40px}
.head p{margin:0;max-width:420px;color:#46575C}
/* tour */
.tour{display:flex;flex-wrap:wrap;gap:16px}
.tour-view{flex:3 1 620px;position:relative;min-height:600px;border-radius:6px;overflow:hidden;background:#10222A}
.tour-view img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:opacity .25s}
.tour-card{position:absolute;left:24px;right:24px;bottom:24px;max-width:440px;background:#fff;border-radius:6px;padding:24px 26px;display:flex;flex-direction:column;gap:8px}
.tour-card span{color:#0A4F5C}.tour-card h3{font-size:30px;line-height:1.1}.tour-card p{margin:0;color:#46575C;font-size:17px}
.rooms{flex:1 1 300px;display:flex;flex-direction:column;gap:8px}
.room{flex:1;min-height:72px;display:flex;align-items:center;gap:14px;text-align:left;padding:8px 14px 8px 8px;font:inherit;font-weight:700;font-size:17px;cursor:pointer;border-radius:6px;border:1.5px solid #C9D6D8;background:#fff;color:#10222A}
.room img{width:72px;height:56px;object-fit:cover;border-radius:4px;flex:none}
.room span{display:flex;flex-direction:column}.room small{font:400 11px 'DM Mono',monospace;letter-spacing:.06em;opacity:.75}
.room:hover{border-color:#0A4F5C}.room.on{background:#0A4F5C;border-color:#0A4F5C;color:#fff}
.room:focus-visible,.btn:focus-visible,summary:focus-visible{outline:3px solid #F4BC50;outline-offset:2px}
/* included */
.inc{display:flex;flex-wrap:wrap;gap:56px 72px}
.inc-head{flex:1 1 420px;display:flex;flex-direction:column;gap:28px}.inc-head p:last-child{margin:0;max-width:420px;color:#CFE0E2}
.items{flex:1.3 1 560px;list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:0 40px;align-content:start}
.items li{display:flex;gap:18px;align-items:flex-start;padding:22px 0;border-top:1px solid rgba(255,255,255,.25)}
.ic{flex:none;width:48px;height:48px;border-radius:50%;background:#fff;color:#0A4F5C;display:flex;align-items:center;justify-content:center}
.items b{font-size:20px;display:block}.items div span{color:#CFE0E2;font-size:16px}
.band{flex:1 1 100%;display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px}
.band img{width:100%;height:260px;object-fit:cover;border-radius:6px}
/* spaces */
.spaces{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px}
.space{position:relative;min-height:440px;border-radius:6px;overflow:hidden;display:flex;flex-direction:column;justify-content:space-between;padding:26px;background:#0A4F5C}
.space>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}.space .scrim{background:rgba(6,30,36,.6)}
.space-top,.space-bot{position:relative}.space-top{display:flex;justify-content:space-between;gap:12px;align-items:flex-start}
.space h3{font-size:30px}.space-bot{display:flex;flex-direction:column;gap:16px}.space-bot p{margin:0;color:#E2E8E4}
/* reviews */
.rating{display:flex;align-items:center;gap:14px;background:#fff;border:1.5px solid #10222A;border-radius:999px;padding:10px 22px 10px 14px;text-decoration:none;color:#10222A}
.rating span:first-child{color:#C98500;font-size:22px;letter-spacing:2px}.rating b{font-size:20px}
.reviews{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:24px}
.reviews figure{margin:0;background:#fff;border:1.5px solid #10222A;border-radius:6px;padding:32px;display:flex;flex-direction:column;justify-content:space-between;gap:24px}
.reviews blockquote{margin:0;font-size:22px;line-height:1.4}.reviews figcaption{color:#46575C}
/* faq */
.faq{display:flex;flex-wrap:wrap;gap:40px 80px}.faq h2{flex:1 1 300px}.qs{flex:2 1 560px}
details{border-top:1px solid #10222A}details:last-child{border-bottom:1px solid #10222A}
summary{list-style:none;display:flex;justify-content:space-between;gap:16px;align-items:center;padding:22px 0;font-size:20px;font-weight:700;cursor:pointer}
summary::-webkit-details-marker{display:none}
summary span::before{content:'+';font-size:26px;font-weight:400}details[open] summary span::before{content:'\2212'}
details p{margin:0 0 24px;color:#46575C;max-width:620px}
/* visit */
.visit{position:relative;background:#10222A center/cover no-repeat;color:#fff}.visit .scrim{background:rgba(6,30,36,.72)}
.visit-in{position:relative;display:flex;flex-wrap:wrap;gap:48px 80px;padding-top:120px;padding-bottom:120px}
.visit-in>div:first-child{flex:1 1 380px}.visit-in>div:first-child p{margin:16px 0 0;color:#D3E1E2}
.visit-cta{flex:1 1 440px;display:flex;flex-direction:column;justify-content:center;gap:18px}
.visit-cta p{margin:0;color:#D3E1E2;font-size:16px;text-align:center}.visit-cta p a{color:#fff}
/* footer */
footer{background:#10222A;color:#B5C8CB;overflow:hidden;padding-top:64px;padding-bottom:96px}
.foot{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:24px;font-size:15px}.foot a{color:#fff}
.word{margin:40px 0 -0.18em;font-size:clamp(40px,10.4vw,152px);line-height:1;font-weight:700;letter-spacing:-.05em;color:#fff;white-space:nowrap}
/* sticky */
.sticky{position:fixed;left:50%;bottom:20px;transform:translateX(-50%);z-index:10;display:flex;align-items:center;gap:16px;background:#10222A;color:#fff;border-radius:999px;padding:8px 8px 8px 22px;box-shadow:0 8px 24px rgba(0,0,0,.25);white-space:nowrap;transition:opacity .25s,transform .25s}
.sticky.hide{opacity:0;pointer-events:none;transform:translate(-50%,20px)}
.sa{font-size:15px;display:flex;align-items:center;gap:8px}
@media (max-width:720px){
 .wrap{padding-left:20px;padding-right:20px}.pad{padding-top:72px;padding-bottom:72px}.intro{padding-top:72px;padding-bottom:72px}
 .hero{min-height:720px}.links>a:not(.btn):not(.lang){display:none}.logo img{height:48px}
 .tour-view{min-height:420px}.tour-card{left:12px;right:12px;bottom:12px;padding:18px}
 .strip div{border-right:0;border-bottom:1px solid rgba(255,255,255,.45)}.strip div:last-child{border-bottom:0}
 .sa{display:none}.sticky{padding:6px}
}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}*{transition:none!important}}
'''

JS = r'''
// To send every "Book a visit" button to HubSpot, paste the form or meetings link here:
var HUBSPOT_URL = '';
(function(){
  if (HUBSPOT_URL) document.querySelectorAll('[data-cta]').forEach(function(a){ a.href = HUBSPOT_URL; a.target = '_blank'; a.rel = 'noopener'; });
  var rooms = window.ROOMS || [], img = document.getElementById('tourImg');
  document.querySelectorAll('.room').forEach(function(b){
    b.addEventListener('click', function(){
      var i = +b.dataset.i, r = rooms[i];
      document.querySelectorAll('.room').forEach(function(x){ x.classList.remove('on'); x.setAttribute('aria-pressed','false'); });
      b.classList.add('on'); b.setAttribute('aria-pressed','true');
      img.style.opacity = 0;
      setTimeout(function(){ img.src = r.img; img.alt = r.name; img.style.opacity = 1; }, 150);
      document.getElementById('tourCode').textContent = String(i+1).padStart(2,'0') + ' / ' + String(rooms.length).padStart(2,'0');
      document.getElementById('tourName').textContent = r.name;
      document.getElementById('tourDesc').textContent = r.desc;
    });
  });
  rooms.forEach(function(r){ var p = new Image(); p.src = r.img; });
  var sticky = document.querySelector('.sticky'), hero = document.querySelector('.hero'), visit = document.getElementById('visit');
  if ('IntersectionObserver' in window && sticky) {
    var seen = {};
    var io = new IntersectionObserver(function(es){
      es.forEach(function(e){ seen[e.target.id || 'hero'] = e.isIntersecting; });
      sticky.classList.toggle('hide', !!(seen.hero || seen.visit));
    });
    io.observe(hero); io.observe(visit);
  }
})();
'''

FAVICON = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#0A4F5C"/><path d="M22 20 10 32l12 12M42 20l12 12-12 12M36 16l-8 32" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>'

def main():
    if os.path.exists(OUT): shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, 'assets')); os.makedirs(os.path.join(OUT, 'es'))
    for f in set(IMAGES.values()): shutil.copy(os.path.join(WEB, f), os.path.join(OUT, 'assets', f))
    shutil.copy(os.path.join(WEB, 'logo-white.png'), os.path.join(OUT, 'assets', 'logo.png'))
    open(os.path.join(OUT, 'assets', 'style.css'), 'w').write(CSS.strip() + '\n')
    open(os.path.join(OUT, 'assets', 'site.js'), 'w').write(JS.strip() + '\n')
    open(os.path.join(OUT, 'assets', 'favicon.svg'), 'w').write(FAVICON)
    open(os.path.join(OUT, 'index.html'), 'w').write(page(T['en']))
    open(os.path.join(OUT, 'es', 'index.html'), 'w').write(page(T['es']))
    open(os.path.join(OUT, 'robots.txt'), 'w').write('User-agent: *\nAllow: /\nSitemap: https://www.thedivproject.com/sitemap.xml\n')
    open(os.path.join(OUT, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://www.thedivproject.com/</loc></url><url><loc>https://www.thedivproject.com/es/</loc></url></urlset>\n')
    # Netlify: send old WordPress URLs home
    open(os.path.join(OUT, '_redirects'), 'w').write('/es/inicio-2/*  /es/  301\n/wp-admin/*  /  301\n/wp-login.php  /  301\n')
    open(os.path.join(OUT, 'CNAME'), 'w').write('www.thedivproject.com\n')
    open(os.path.join(OUT, '.nojekyll'), 'w').write('')
    print('built', OUT)

if __name__ == '__main__':
    main()
