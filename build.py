#!/usr/bin/env python3
"""
Static site generator for Jumpstart Medical.
Content & colors mirror jumpstartmedical.care; layout is a fresh redesign.
Run:  python3 build.py   ->  writes HTML files with portable relative paths.
"""
import os, html, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = "https://jumpstartmedical.care"   # canonical domain
YEAR = datetime.date.today().year

# ----------------------------------------------------------------------------
# Business constants (NAP)
# ----------------------------------------------------------------------------
NAME   = "Jumpstart Medical"
DOCTOR = "Dr. Shalena Islam"
PHONE_DISPLAY = "(917) 932-2315"
PHONE_TEL     = "+19179322315"
ADDR_STREET   = "142-42 Booth Memorial Avenue"
ADDR_CITY     = "Flushing"
ADDR_STATE    = "NY"
ADDR_ZIP      = "11355"
ADDR_FULL     = f"{ADDR_STREET}, {ADDR_CITY}, {ADDR_STATE} {ADDR_ZIP}"
ZOCDOC = "https://www.zocdoc.com/practice/jumpstart-medical-75416"
MAPS   = ("https://www.google.com/maps/search/?api=1&query="
          "142-42+Booth+Memorial+Avenue+Flushing+NY+11355")
MAP_EMBED = ("https://www.google.com/maps?q=142-42+Booth+Memorial+Avenue+Flushing+NY+11355&output=embed")

HOURS = [
    ("Monday – Friday", "8:00 AM – 8:00 PM"),
    ("Saturday",        "9:00 AM – 2:00 PM"),
    ("Sunday",          "Closed"),
    ("Telehealth",      "7 days a week"),
]

# ----------------------------------------------------------------------------
# Small inline SVG icons
# ----------------------------------------------------------------------------
def icon(name):
    p = {
        "check":  '<path d="M20 6 9 17l-5-5"/>',
        "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10Z"/>',
        "video":  '<path d="m23 7-7 5 7 5V7Z"/><rect x="1" y="5" width="15" height="14" rx="2"/>',
        "clock":  '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
        "car":    '<path d="M5 17H3v-5l2-5h14l2 5v5h-2M5 17a2 2 0 1 0 4 0M5 17h10m0 0a2 2 0 1 0 4 0"/>',
        "wallet": '<path d="M20 12V8H6a2 2 0 0 1 0-4h12v4"/><path d="M4 6v12a2 2 0 0 0 2 2h14v-4"/><path d="M18 12a2 2 0 0 0 0 4h4v-4Z"/>',
        "phone":  '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3-8.6A2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2Z"/>',
        "pin":    '<path d="M21 10c0 7-9 12-9 12s-9-5-9-12a9 9 0 0 1 18 0Z"/><circle cx="12" cy="10" r="3"/>',
        "mail":   '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 6-10 7L2 6"/>',
        "heart":  '<path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1-1.1a5.5 5.5 0 0 0-7.8 7.8l1.1 1L12 21l7.7-7.6 1.1-1a5.5 5.5 0 0 0 0-7.8Z"/>',
        "steth":  '<path d="M4 3v6a5 5 0 0 0 10 0V3M9 21a4 4 0 0 0 4-4v-3"/><circle cx="19" cy="12" r="2"/>',
        "star":   '<path d="m12 2 3 6.9 7.5.6-5.7 5 1.7 7.4L12 18l-6.5 3.9 1.7-7.4-5.7-5 7.5-.6Z"/>',
    }[name]
    return (f'<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" '
            f'aria-hidden="true">{p}</svg>')

def star_row(n=5):
    return "".join('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
                   '<path d="m12 2 3 6.9 7.5.6-5.7 5 1.7 7.4L12 18l-6.5 3.9 1.7-7.4-5.7-5 7.5-.6Z"/></svg>'
                   for _ in range(n))

# ----------------------------------------------------------------------------
# Services data
# ----------------------------------------------------------------------------
SERVICES = [
    ("telemedicine-virtual-care", "Telemedicine Visits", "TELEMEDICINE", "",
     "See Dr. Islam by secure video for sick visits, follow-ups, and refills — no commute, no waiting room, available across New York."),
    ("urgent-care-consultation", "Urgent Care Visits", "URGENT CARE", "emerald",
     "Same-day and walk-in care for fevers, infections, minor injuries, and conditions that need prompt attention."),
    ("primary-care-consultation-queens", "Preventive Health", "", "",
     "Annual physicals, wellness exams, screenings, and personalized plans to keep you healthy for the long run."),
    ("chronic-disease-blood-pressure-check", "Chronic Disease Management", "", "",
     "Ongoing care for diabetes, hypertension, high cholesterol, thyroid conditions, and more."),
    ("weight-loss-nutrition-flushing", "Weight Loss Management", "POPULAR", "ink",
     "Medically supervised weight loss with GLP-1 options like Wegovy, Ozempic, Mounjaro, and Zepbound, plus weekly check-ins."),
    ("ekg-electrocardiogram-test", "EKG / Electrocardiogram", "", "",
     "In-office heart-rhythm testing to evaluate palpitations, chest discomfort, and cardiac risk."),
    ("flushing-clinic-exam-room", "Vision Screening", "", "",
     "Quick vision screening to check acuity and flag changes that may need a specialist referral."),
    ("surgical-clearance-exam", "Surgical Clearance", "", "",
     "Pre-operative evaluations and medical clearance so your upcoming procedure stays on schedule."),
    ("health-lab-blood-work", "No-Fault Insurance Visits", "NO-FAULT CARE", "emerald",
     "Medical evaluation for motor-vehicle-accident injuries, billed directly to your NY no-fault (PIP) insurer."),
    ("womens-health-consultation", "Women's Health", "", "",
     "Well-woman visits, screenings, and preventive care in a comfortable, respectful setting."),
    ("mens-health-checkup", "Men's Health", "", "",
     "Routine checkups, screenings, and preventive care tailored to men's health at every age."),
    ("lab-testing-medical-form", "Health Lab & Blood Work", "", "",
     "In-office blood draws and lab testing so results are reviewed with you quickly and clearly."),
    ("geriatric-care-elderly-patient", "Geriatric Care", "", "",
     "Attentive, patient care for older adults — medication reviews, chronic care, and coordination."),
    ("health-counseling-flushing", "Health Counseling", "", "",
     "Guidance on lifestyle, nutrition, and managing conditions so you feel supported at every step."),
]

AREAS = ["Flushing", "Queens", "Bayside", "Fresh Meadows", "Corona", "Elmhurst",
         "Jackson Heights", "Whitestone", "College Point", "Kew Gardens",
         "Forest Hills", "Murray Hill", "Auburndale", "Rego Park"]

INSURERS = ["Aetna", "Cigna", "UnitedHealthcare", "Empire BCBS", "Fidelis Care",
            "Healthfirst", "EmblemHealth", "Oxford", "MetroPlus", "Medicare",
            "Medicaid", "1199SEIU", "No-Fault / PIP", "Workers' Comp",
            "Humana", "Anthem"]

REVIEWS = [
    ("Dr. Islam is thorough and truly listens. She took time to explain everything and never made me feel rushed — the whole staff is warm and welcoming.", "Amina R.", "Google Review"),
    ("Booked a same-day urgent care visit for my son and we were seen right away. Clean office, kind team, and no long wait. Highly recommend.", "David C.", "Google Review"),
    ("I started my weight loss program here and the weekly check-ins keep me on track. Dr. Islam actually cares about the results.", "Priya S.", "Google Review"),
    ("The telehealth visit was so convenient — I got my refill and a referral without leaving work. Same great care as in person.", "Marcus T.", "Google Review"),
    ("After my car accident they handled all the no-fault paperwork and billing. I could just focus on getting better.", "Elena M.", "Google Review"),
    ("Finally a doctor who speaks my language and treats my whole family. Trusted, patient, and genuinely caring.", "Rahim H.", "Google Review"),
]

FAQS = [
    ("How does a telemedicine visit work?",
     "You book online or by phone, then connect with Dr. Islam over a secure video link at your appointment time — no app download hassle and no waiting room. It's ideal for sick visits, follow-ups, prescription refills, and reviewing results. Telehealth is available to patients located anywhere in New York State."),
    ("What can be treated with urgent care or telehealth?",
     "Colds and flu, minor infections, rashes, allergies, prescription refills, medication questions, and chronic-condition check-ins are all a great fit. For anything that needs hands-on evaluation or lab work, we'll have you come into the Flushing office — often the same day."),
    ("Do you see walk-in or same-day urgent care patients?",
     "Yes. Same-day and walk-in appointments are available for acute conditions during office hours. Calling ahead at " + PHONE_DISPLAY + " helps us reduce your wait, but walk-ins are always welcome."),
    ("What is no-fault insurance and how does it work?",
     "New York no-fault (PIP) insurance covers medical expenses after a motor vehicle accident, regardless of who was at fault. Jumpstart Medical evaluates your injuries and bills the insurer directly — at no out-of-pocket cost to you."),
    ("Do you accept Medicare and Medicaid?",
     "Yes. We accept Medicare, Medicaid, and most major NYC commercial plans. Call " + PHONE_DISPLAY + " and we'll verify your coverage before your visit."),
    ("Are you accepting new patients?",
     "Absolutely. Jumpstart Medical is actively welcoming new adult patients for both in-person and telemedicine visits. Book on ZocDoc or call " + PHONE_DISPLAY + " to get started."),
]

# ----------------------------------------------------------------------------
# Nav definition   (path token, label)
# ----------------------------------------------------------------------------
NAV = [
    ("services/", "Services"),
    ("services/telemedicine-queens-ny/", "Telemedicine"),
    ("services/weight-loss-in-flushing-ny/", "Weight Loss"),
    ("about-us/", "About"),
    ("blogs/", "Health Journal"),
    ("contact/", "Contact"),
]

def L(base, token):
    """Return a relative link for an internal path token."""
    if token == "":
        return base + "index.html"
    return base + token

def A(base, path):
    return base + "assets/" + path

# ----------------------------------------------------------------------------
# Shared chrome
# ----------------------------------------------------------------------------
def head(base, title, desc, canonical, active, extra_ld="", og_type="website"):
    og_img = SITE + "/assets/img/og-image.jpg"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#0d2b28">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="author" content="{NAME}">
<meta name="geo.region" content="US-NY">
<meta name="geo.placename" content="Flushing, Queens, New York">

<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(title)}">
<meta name="twitter:description" content="{html.escape(desc)}">
<meta name="twitter:image" content="{og_img}">

<link rel="icon" type="image/svg+xml" href="{A(base,'img/favicon.svg')}">
<link rel="apple-touch-icon" href="{A(base,'img/favicon.svg')}">
<link rel="manifest" href="{base}site.webmanifest">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;1,9..144,400&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{A(base,'css/styles.css')}">
{extra_ld}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{header(base, active)}
<main id="main">"""

def header(base, active):
    links = ""
    for token, label in NAV:
        cls = ' class="active"' if active == token else ""
        links += f'<li><a href="{L(base,token)}"{cls}>{label}</a></li>'
    return f"""
<div class="topbar">
  <div class="wrap">
    <div class="tb-left">
      <span>{icon('pin')} {ADDR_FULL}</span>
      <span>{icon('clock')} Mon–Fri 8am–8pm</span>
    </div>
    <div class="tb-right">
      <span class="dot">Now accepting new patients</span>
      <a href="tel:{PHONE_TEL}">{icon('phone')} {PHONE_DISPLAY}</a>
    </div>
  </div>
</div>
<header class="site-header">
  <nav class="nav wrap" aria-label="Primary">
    <a class="brand" href="{L(base,'')}" aria-label="{NAME} home">
      <img class="mark" src="{A(base,'img/logo-mark.svg')}" alt="" width="38" height="38">
      <span>Jumpstart <small>Medical &middot; Flushing NY</small></span>
    </a>
    <ul class="nav-links">{links}</ul>
    <div class="nav-cta">
      <a class="btn btn-primary" href="{ZOCDOC}" target="_blank" rel="noopener">Book a Visit</a>
    </div>
    <button class="nav-toggle" aria-label="Menu" aria-expanded="false" aria-controls="menu">
      <span></span><span></span><span></span>
    </button>
  </nav>
</header>"""

def footer(base):
    fcols_services = "".join(
        f'<li><a href="{L(base,"services/")}">{s[1]}</a></li>' for s in SERVICES[:6])
    hours = "".join(
        f'<div class="hours-row"><span>{d}</span><span>{t}</span></div>' for d, t in HOURS)
    return f"""</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="footer-top">
      <div>
        <a class="brand" href="{L(base,'')}">
          <img class="mark" src="{A(base,'img/logo-mark.svg')}" alt="" width="38" height="38">
          <span>Jumpstart <small>Medical &middot; Flushing NY</small></span>
        </a>
        <p>Comprehensive primary, urgent, and telemedicine care for adults in Flushing, Queens — led by {DOCTOR}, a board-certified physician.</p>
        <p><a class="btn btn-outline" style="border-color:rgba(255,255,255,.3);color:#fff" href="tel:{PHONE_TEL}">{icon('phone')} {PHONE_DISPLAY}</a></p>
      </div>
      <div class="footer-col">
        <h4>Services</h4>
        <ul>{fcols_services}</ul>
      </div>
      <div class="footer-col">
        <h4>Company</h4>
        <ul>
          <li><a href="{L(base,'about-us/')}">About Us</a></li>
          <li><a href="{L(base,'services/')}">All Services</a></li>
          <li><a href="{L(base,'blogs/')}">Health Journal</a></li>
          <li><a href="{L(base,'self-assessment/')}">Self Assessment</a></li>
          <li><a href="{L(base,'jumpstart-academy/')}">Jumpstart Academy</a></li>
          <li><a href="{L(base,'contact/')}">Contact</a></li>
        </ul>
      </div>
      <div class="footer-col footer-hours">
        <h4>Office Hours</h4>
        {hours}
        <p style="margin-top:1rem"><a href="{MAPS}" target="_blank" rel="noopener">{icon('pin')} {ADDR_FULL}</a></p>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; <span id="yr">{YEAR}</span> {NAME}. All rights reserved.</span>
      <span>{ADDR_FULL} &middot; <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></span>
    </div>
  </div>
</footer>
<script src="{A(base,'js/main.js')}" defer></script>
</body>
</html>"""

def page(base, filename, title, desc, canonical, active, body, extra_ld="", og_type="website"):
    out = head(base, title, desc, canonical, active, extra_ld, og_type) + body + footer(base)
    path = os.path.join(ROOT, filename)
    os.makedirs(os.path.dirname(path), exist_ok=True) if os.path.dirname(filename) else None
    with open(path, "w", encoding="utf-8") as f:
        f.write(out)
    print("wrote", filename)

# ----------------------------------------------------------------------------
# Reusable body blocks
# ----------------------------------------------------------------------------
def img(base, slug, alt, cls="", small=False, lazy=True, sizes=None):
    src = A(base, f"img/{slug}.webp")
    srcset = f'srcset="{A(base,f"img/{slug}-640.webp")} 640w, {src} 1200w" ' \
             f'sizes="{sizes or "(max-width:860px) 100vw, 600px"}" '
    load = 'loading="lazy" decoding="async" ' if lazy else ''
    c = f'class="{cls}" ' if cls else ""
    return (f'<img {c}src="{src}" {srcset}{load}width="1200" height="750" '
            f'alt="{html.escape(alt)}">')

def cta_band(base, heading="Ready to Make Jumpstart Your Medical Home?",
             text="Book in-person in Flushing or start a telemedicine visit from anywhere in New York — same expert care, your way."):
    return f"""
<section class="section cta-band">
  <div class="wrap">
    <span class="kicker center" style="color:rgba(255,255,255,.85)">Get Started</span>
    <h2>{heading}</h2>
    <p class="lead" style="max-width:60ch;margin-inline:auto">{text}</p>
    <div class="hero-actions">
      <a class="btn btn-ghost-light btn-lg" href="{ZOCDOC}" target="_blank" rel="noopener">{icon('video')} Book Online</a>
      <a class="btn btn-primary btn-lg" href="tel:{PHONE_TEL}">{icon('phone')} Call {PHONE_DISPLAY}</a>
    </div>
  </div>
</section>"""

def reviews_section(base):
    cards = ""
    for quote, who, src in REVIEWS[:3]:
        initial = who[0]
        cards += f"""
      <div class="review reveal">
        <div class="stars" aria-label="5 out of 5 stars">{star_row()}</div>
        <p>&ldquo;{quote}&rdquo;</p>
        <div class="who"><span class="av">{initial}</span><span><b>{who}</b><span>{src}</span></span></div>
      </div>"""
    return f"""
<section class="section">
  <div class="wrap">
    <div class="section-head center">
      <span class="kicker center">Patient Reviews</span>
      <h2>Trusted by Our Community</h2>
      <p class="lead">Real experiences from patients across Flushing and Queens.</p>
    </div>
    <div class="grid grid-3" style="margin-top:2.6rem">{cards}</div>
  </div>
</section>"""

def insurance_section(base):
    pills = "".join(f'<div class="ins-pill">{i}</div>' for i in INSURERS[:12])
    return f"""
<section class="section" style="background:var(--paper)">
  <div class="wrap">
    <div class="section-head center">
      <span class="kicker center">Insurance</span>
      <h2>We Accept NYC's Top Insurance Plans</h2>
      <p class="lead">We work with most major medical and no-fault plans across New York City. Not sure about yours? We'll verify it for you.</p>
    </div>
    <div class="ins-grid" style="margin-top:2.4rem">{pills}</div>
    <p class="center" style="margin-top:2rem"><a class="btn btn-outline" href="tel:{PHONE_TEL}">{icon('phone')} Call to Verify Coverage</a></p>
  </div>
</section>"""

def faq_section(base, faqs=FAQS):
    items = ""
    for i, (q, a) in enumerate(faqs):
        items += f"""
      <div class="faq-item{' open' if i==0 else ''}">
        <button class="faq-q" aria-expanded="{'true' if i==0 else 'false'}">{q}</button>
        <div class="faq-a"{' style="max-height:1200px"' if i==0 else ''}><p>{a}</p></div>
      </div>"""
    return f"""
<section class="section" style="background:var(--cream)">
  <div class="wrap">
    <div class="section-head center">
      <span class="kicker center">Common Questions</span>
      <h2>Frequently Asked Questions</h2>
    </div>
    <div class="faq" style="margin-top:2rem">{items}</div>
  </div>
</section>"""

def trust_strip():
    items = [
        ("shield", "Board-Certified Physician"),
        ("video", "Telemedicine Available"),
        ("clock", "Same-Day Urgent Care"),
        ("car", "No-Fault Accident Care"),
        ("wallet", "We Bill Insurance Plans"),
    ]
    inner = "".join(f'<div class="trust-item">{icon(i)}<span>{t}</span></div>' for i, t in items)
    return f'<section class="trust"><div class="wrap">{inner}</div></section>'

# ----------------------------------------------------------------------------
# JSON-LD helpers
# ----------------------------------------------------------------------------
def ld_block(*objs):
    import json
    return "\n".join(
        f'<script type="application/ld+json">{json.dumps(o, ensure_ascii=False)}</script>'
        for o in objs)

def clinic_ld():
    return {
        "@context": "https://schema.org", "@type": "MedicalClinic",
        "@id": SITE + "/#clinic", "name": NAME,
        "url": SITE + "/", "telephone": PHONE_DISPLAY, "image": SITE + "/assets/img/og-image.jpg",
        "priceRange": "$$", "medicalSpecialty": ["PrimaryCare", "Emergency"],
        "address": {"@type": "PostalAddress", "streetAddress": ADDR_STREET,
                    "addressLocality": ADDR_CITY, "addressRegion": ADDR_STATE,
                    "postalCode": ADDR_ZIP, "addressCountry": "US"},
        "geo": {"@type": "GeoCoordinates", "latitude": 40.7433, "longitude": -73.8203},
        "areaServed": [{"@type": "City", "name": a} for a in ["Flushing", "Queens", "Bayside", "Fresh Meadows"]],
        "openingHoursSpecification": [
            {"@type": "OpeningHoursSpecification",
             "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"],
             "opens": "08:00", "closes": "20:00"},
            {"@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday",
             "opens": "09:00", "closes": "14:00"},
        ],
        "founder": {"@type": "Physician", "name": DOCTOR},
        "sameAs": [ZOCDOC],
    }

def physician_ld():
    return {
        "@context": "https://schema.org", "@type": "Physician",
        "name": DOCTOR, "url": SITE + "/about-us/", "telephone": PHONE_DISPLAY,
        "medicalSpecialty": "PrimaryCare", "worksFor": {"@id": SITE + "/#clinic"},
        "knowsLanguage": ["English", "Bengali", "Urdu", "Hindi"],
        "address": {"@type": "PostalAddress", "streetAddress": ADDR_STREET,
                    "addressLocality": ADDR_CITY, "addressRegion": ADDR_STATE,
                    "postalCode": ADDR_ZIP, "addressCountry": "US"},
    }

def breadcrumb_ld(base_url, trail):
    return {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": u}
            for i, (n, u) in enumerate(trail)],
    }

def faq_ld(faqs=FAQS):
    return {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs],
    }

def service_ld(name, desc, url):
    return {
        "@context": "https://schema.org", "@type": "MedicalProcedure",
        "name": name, "description": desc, "url": url,
        "provider": {"@id": SITE + "/#clinic"},
    }

# ----------------------------------------------------------------------------
# Section builders used across pages
# ----------------------------------------------------------------------------
def services_grid(base, items=SERVICES, limit=None):
    cards = ""
    subset = items if limit is None else items[:limit]
    for slug, title, tag, tagcls, desc in subset:
        tag_html = f'<span class="tag {tagcls}">{tag}</span>' if tag else ""
        cards += f"""
      <article class="card reveal">
        <div class="card-media">{tag_html}{img(base, slug, title + " at Jumpstart Medical in Flushing, NY", sizes="(max-width:560px) 100vw, (max-width:1000px) 50vw, 33vw")}</div>
        <div class="card-body">
          <h3>{title}</h3>
          <p>{desc}</p>
          <a class="more" href="{L(base,'services/')}">Learn more &rarr;</a>
        </div>
      </article>"""
    return f'<div class="grid grid-3">{cards}</div>'

def page_hero(base, kicker, title, lead, trail, hero_img=None):
    crumbs = ""
    for i, (n, u) in enumerate(trail):
        if i < len(trail) - 1:
            crumbs += f'<a href="{u}">{n}</a><span>/</span>'
        else:
            crumbs += f'<span>{n}</span>'
    bg = img(base, hero_img, kicker + " at Jumpstart Medical, Flushing NY",
             cls="hero-bg", lazy=False, sizes="100vw") if hero_img else ""
    return f"""
<section class="page-hero">
  {bg}
  <div class="wrap">
    <div class="breadcrumb">{crumbs}</div>
    <span class="kicker">{kicker}</span>
    <h1>{title}</h1>
    <p class="lead">{lead}</p>
    <div class="hero-actions">
      <a class="btn btn-primary" href="{ZOCDOC}" target="_blank" rel="noopener">Book a Visit</a>
      <a class="btn btn-ghost-light" href="tel:{PHONE_TEL}">{icon('phone')} {PHONE_DISPLAY}</a>
    </div>
  </div>
</section>"""

# ----------------------------------------------------------------------------
# HOMEPAGE
# ----------------------------------------------------------------------------
def build_home():
    base = ""
    canonical = SITE + "/"
    hours_rows = "".join(
        f'<div class="hours-row"><span>{d}</span><span>{t}</span></div>' for d, t in HOURS)

    why_feats = [
        ("01", "Board-Certified Physician", f"Care led by {DOCTOR}, in practice since 2013 and affiliated with Long Island Jewish Medical Center."),
        ("02", "In-Person &amp; Telemedicine", "Choose the visit that fits your day — the same expert care in our Flushing office or by secure video."),
        ("03", "One-Stop Care, No Runaround", "Primary care, urgent visits, labs, EKG, and weight loss all under one roof — no bouncing between offices."),
        ("04", "Culturally Competent Care", "Dr. Islam speaks English, Bengali, Urdu, and Hindi — caring for the diverse community of Queens."),
    ]
    feats = "".join(
        f'<div class="feat reveal"><span class="fnum">{n}</span><h3>{t}</h3><p>{d}</p></div>'
        for n, t, d in why_feats)

    tiles = [
        ("primary-care-consultation-queens", "Primary &amp; Preventive Care", "Wellness exams, screenings, and chronic-care management to keep you healthy year-round."),
        ("urgent-care-vitals", "Urgent &amp; Same-Day Care", "Walk-in care for fevers, infections, and minor injuries — often seen the same day."),
        ("telehealth-service-support", "Telemedicine", "Secure video visits with Dr. Islam from home, work, or anywhere in New York."),
    ]
    tile_html = "".join(
        f"""<a class="svc-tile reveal" href="{L(base,'services/')}">{img(base, s, t.replace('&amp;','and'), sizes='(max-width:860px) 100vw, 33vw')}<div class="svc-inner"><h3>{t}</h3><p>{d}</p></div></a>"""
        for s, t, d in tiles)

    tele_uses = ["Sick visits &amp; cold/flu symptoms", "Chronic disease follow-ups",
                 "Prescription renewals &amp; referrals", "Weight loss consultations"]
    tele_list = "".join(f'<li>{icon("check")}<span>{u}</span></li>' for u in tele_uses)

    provide = ["Same-day evaluation after an accident", "Direct billing to your no-fault insurer",
               "Full documentation for your claim", "Injury assessment &amp; treatment plan",
               "Referrals to specialists &amp; imaging", "Zero out-of-pocket cost to you"]
    provide_html = "".join(f'<li>{icon("check")}<span>{p}</span></li>' for p in provide)

    reasons = ["A board-certified physician who takes the time to listen",
               "In-person and telemedicine care on your schedule",
               "One-stop care — labs, EKG, and weight loss in-house",
               "Culturally competent care in multiple languages"]
    reason_list = "".join(f'<li>{icon("check")}<span>{r}</span></li>' for r in reasons)

    areas_chips = "".join(f'<span class="chip">{a}</span>' for a in AREAS)

    body = f"""
<section class="hero">
  {img(base, "medical-team-collaboration", "Jumpstart Medical care team in Flushing, Queens", cls="hero-bg", lazy=False, sizes="100vw")}
  <div class="wrap">
    <div class="hero-grid">
      <div>
        <span class="hero-badge">Primary &middot; Urgent &middot; Telehealth &middot; Flushing, NY</span>
        <h1>Primary Care in <em>Flushing, NY</em>, Delivered Personally.</h1>
        <p class="hero-sub">Jumpstart Medical offers comprehensive primary, urgent, and telemedicine care for adults — from wellness visits and joint injections to EKGs, weight loss, and no-fault insurance visits — led by {DOCTOR}.</p>
        <div class="hero-actions">
          <a class="btn btn-primary btn-lg" href="{ZOCDOC}" target="_blank" rel="noopener">{icon('pin')} Book In-Person</a>
          <a class="btn btn-ghost-light btn-lg" href="{L(base,'services/telemedicine-queens-ny/')}">{icon('video')} Start Telehealth</a>
        </div>
      </div>
      <aside class="hours-card">
        <h3>Office Hours &amp; Location</h3>
        {hours_rows}
        <p class="addr">{icon('pin')} {ADDR_FULL}<br>
        <a href="tel:{PHONE_TEL}" style="color:var(--coral)">{PHONE_DISPLAY}</a></p>
      </aside>
    </div>
  </div>
</section>

{trust_strip()}

<section class="section">
  <div class="wrap">
    <div class="split">
      <div class="split-media reveal">
        {img(base, "medicine-that-listens", DOCTOR + ", board-certified family physician at Jumpstart Medical")}
        <div class="badge-float"><span class="num">2013</span><small>In practice since — trusted care in Queens</small></div>
      </div>
      <div class="reveal">
        <span class="kicker">Family-Owned Care Since 2013</span>
        <h2>Care That Treats You Like a Person, Not a Chart.</h2>
        <p class="lead">At Jumpstart Medical, {DOCTOR} builds real relationships with her patients. A board-certified family physician affiliated with Long Island Jewish Medical Center, she has cared for Flushing families since 2013.</p>
        <p>From routine wellness and sick visits to weight management, minor injuries, and chronic-condition care, you get thorough, unhurried attention — in the language you're most comfortable speaking.</p>
        <ul class="check-list">
          <li>{icon('check')}<span>Board-certified family physician</span></li>
          <li>{icon('check')}<span>English, Bengali, Urdu &amp; Hindi spoken</span></li>
          <li>{icon('check')}<span>Same expert care in-person or by video</span></li>
        </ul>
        <p style="margin-top:1.6rem"><a class="btn btn-outline" href="{L(base,'about-us/')}">Meet {DOCTOR} &rarr;</a></p>
      </div>
    </div>
  </div>
</section>

<section class="section" style="background:var(--paper)">
  <div class="wrap">
    <div class="section-head center">
      <span class="kicker center">What We Do</span>
      <h2>Three Ways to Get the Care You Need</h2>
      <p class="lead">In the office, same-day, or on screen — Jumpstart Medical meets you where you are.</p>
    </div>
    <div class="svc-tiles" style="margin-top:2.6rem">{tile_html}</div>
  </div>
</section>

<section class="section band-dark" style="background:var(--ink-3)">
  <div class="wrap">
    <div class="split">
      <div class="split-media reveal">{img(base, "telemedicine-virtual-care", "Telemedicine video visit with Dr. Islam at Jumpstart Medical")}</div>
      <div class="reveal on-dark">
        <span class="kicker">Telemedicine</span>
        <h2>See Dr. Islam From Anywhere.</h2>
        <p class="lead">Can't make it into the office? Our secure telehealth platform connects you with {DOCTOR} by video for a wide range of conditions — no commute, no waiting room, the same expert care.</p>
        <ul class="check-list">{tele_list}</ul>
        <div class="hero-actions">
          <a class="btn btn-primary" href="{ZOCDOC}" target="_blank" rel="noopener">Schedule a Telehealth Visit</a>
          <a class="btn btn-ghost-light" href="{L(base,'services/telemedicine-queens-ny/')}">Learn More</a>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head center">
      <span class="kicker center">What We Offer</span>
      <h2>A Full Range of Primary, Urgent &amp; Telehealth Services</h2>
      <p class="lead">Comprehensive care for adults — in person in Flushing or virtually, all under one roof.</p>
    </div>
    <div style="margin-top:2.6rem">{services_grid(base)}</div>
    <p class="center" style="margin-top:2.4rem"><a class="btn btn-outline" href="{L(base,'services/')}">View All Services &rarr;</a></p>
  </div>
</section>

<section class="section band-dark">
  <div class="wrap">
    <div class="split">
      <div class="reveal on-dark">
        <span class="kicker">Motor Vehicle Accidents</span>
        <h2>Injured in an Accident? We Bill No-Fault Directly.</h2>
        <p class="lead">New York no-fault (PIP) insurance covers your medical care after a car accident — regardless of who was at fault. We evaluate your injuries and bill the insurer directly, so you can focus on recovery.</p>
        <p style="margin-top:1.4rem"><a class="btn btn-primary" href="tel:{PHONE_TEL}">{icon('phone')} Call Today</a></p>
      </div>
      <div class="reveal on-dark">
        <h3 style="color:#fff;font-family:var(--sans);font-size:.8rem;letter-spacing:.16em;text-transform:uppercase;color:var(--coral)">What We Provide</h3>
        <ul class="provide-list" style="margin-top:1.2rem">{provide_html}</ul>
      </div>
    </div>
  </div>
</section>

<section class="section band-rose">
  <div class="wrap">
    <div class="split">
      <div class="reveal">
        <span class="kicker">Why Jumpstart</span>
        <h2>Medicine That Listens, Care That Lasts.</h2>
        <p class="lead">At Jumpstart Medical, we believe primary care should be accessible, comprehensive, and deeply personal — whether you're in our office or at home.</p>
        <ul class="check-list">{reason_list}</ul>
      </div>
      <div class="reveal">
        <div class="reason-card">
          <div class="stars" aria-label="5 out of 5">{star_row()}</div>
          <div class="rating">5.0</div>
          <p style="color:rgba(255,255,255,.8);margin:.4rem 0 0">Our patients say it best — rated 5.0 across dozens of reviews.</p>
          <div class="same-day">
            <strong>Same-Day Visits</strong>
            <p style="color:rgba(255,255,255,.75);margin:.3rem 0 0;font-size:.92rem">Walk in or book ahead — acute care when you need it.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="split">
      <div class="reveal">
        <span class="kicker">Visit Us</span>
        <h2>Visit Our Flushing Office on Booth Memorial Ave.</h2>
        <p class="lead">Convenient, easy to reach, and welcoming — with same-day appointments and walk-ins during office hours.</p>
        <div class="visit-hours">{hours_rows}</div>
        <div class="hero-actions">
          <a class="btn btn-primary" href="{MAPS}" target="_blank" rel="noopener">{icon('pin')} Get Directions</a>
          <a class="btn btn-outline" href="tel:{PHONE_TEL}">{icon('phone')} Call the Office</a>
        </div>
      </div>
      <div class="split-media reveal">{img(base, "flushing-clinic-exam-room", "Jumpstart Medical exam room in Flushing, Queens NY")}</div>
    </div>
  </div>
</section>

{reviews_section(base)}

<section class="section" style="background:var(--paper)">
  <div class="wrap">
    <div class="section-head center">
      <span class="kicker center">Service Area</span>
      <h2>Proudly Serving Flushing &amp; All of Queens, NY</h2>
      <p class="lead">In-person care in Flushing and telemedicine across New York State.</p>
    </div>
    <div class="chips">{areas_chips}</div>
  </div>
</section>

{insurance_section(base)}

{faq_section(base)}

{cta_band(base)}
"""
    extra = ld_block(clinic_ld(), physician_ld(), faq_ld(),
                     {"@context": "https://schema.org", "@type": "WebSite",
                      "name": NAME, "url": SITE + "/"})
    page(base, "index.html",
         "Primary Care & Urgent Care in Flushing, Queens NY | Jumpstart Medical",
         "Jumpstart Medical offers comprehensive primary, urgent, and telemedicine care for adults in Flushing, Queens NY — led by Dr. Shalena Islam. Same-day visits, weight loss, no-fault care. Call (917) 932-2315.",
         canonical, "", body, extra)

# ----------------------------------------------------------------------------
# SERVICES HUB
# ----------------------------------------------------------------------------
def build_services():
    base = "../"
    canonical = SITE + "/services/"
    trail = [("Home", L(base, "")), ("Services", canonical)]
    body = page_hero(base, "What We Offer",
        "A Full Range of Primary, Urgent &amp; Telehealth Services",
        "From wellness visits and joint injections to EKGs, weight loss, and no-fault insurance care — comprehensive medicine for adults in Flushing, all under one roof.",
        trail, "primary-care-consultation-queens") + f"""
<section class="section">
  <div class="wrap">
    <div class="stats reveal" style="margin-bottom:3rem">
      <div class="stat"><div class="n">14+</div><div class="l">Services offered</div></div>
      <div class="stat"><div class="n">2013</div><div class="l">Caring for Queens since</div></div>
      <div class="stat"><div class="n">7</div><div class="l">Days of telehealth</div></div>
      <div class="stat"><div class="n">5.0</div><div class="l">Patient rating</div></div>
    </div>
    {services_grid(base)}
  </div>
</section>
{insurance_section(base)}
{cta_band(base)}"""
    extra = ld_block(breadcrumb_ld(SITE, [("Home", SITE + "/"), ("Services", canonical)]),
                     {"@context": "https://schema.org", "@type": "ItemList",
                      "itemListElement": [
                          {"@type": "ListItem", "position": i + 1, "name": s[1]}
                          for i, s in enumerate(SERVICES)]})
    page(base, "services/index.html",
         "Medical Services in Flushing, NY | Primary, Urgent & Telehealth | Jumpstart Medical",
         "Explore Jumpstart Medical's services in Flushing, Queens NY — primary and preventive care, urgent care, telemedicine, weight loss, EKG, no-fault accident care, labs, and more.",
         canonical, "services/", body, extra)

# ----------------------------------------------------------------------------
# SERVICE DETAIL PAGES
# ----------------------------------------------------------------------------
def service_detail(folder, active_token, kicker, title, hero_img, lead,
                   intro_paras, points, meta_title, meta_desc, treat_heading, treat_items,
                   hero_bg="primary-care-consultation-queens"):
    base = "../../"
    canonical = SITE + "/services/" + folder + "/"
    trail = [("Home", L(base, "")), ("Services", L(base, "services/")), (kicker, canonical)]
    pts = "".join(f'<li>{icon("check")}<span>{p}</span></li>' for p in points)
    treat = "".join(f'<li>{icon("check")}<span>{t}</span></li>' for t in treat_items)
    intro = "".join(f"<p>{p}</p>" for p in intro_paras)
    body = page_hero(base, kicker, title, lead, trail, hero_bg) + f"""
<section class="section">
  <div class="wrap">
    <div class="split">
      <div class="split-media reveal">{img(base, hero_img, title + " at Jumpstart Medical, Flushing NY", lazy=False)}</div>
      <div class="reveal">
        <span class="kicker">Overview</span>
        <h2>{title}</h2>
        {intro}
        <ul class="check-list">{pts}</ul>
        <p style="margin-top:1.6rem"><a class="btn btn-primary" href="{ZOCDOC}" target="_blank" rel="noopener">Book This Visit</a></p>
      </div>
    </div>
  </div>
</section>
<section class="section" style="background:var(--paper)">
  <div class="wrap">
    <div class="split rev">
      <div class="split-media reveal">{img(base, "compassionate-patient-care", "Compassionate patient care at Jumpstart Medical")}</div>
      <div class="reveal">
        <span class="kicker">{treat_heading}</span>
        <h2>What We Help With</h2>
        <ul class="check-list">{treat}</ul>
        <p style="margin-top:1.4rem"><a class="btn btn-outline" href="{L(base,'contact/')}">Questions? Contact Us &rarr;</a></p>
      </div>
    </div>
  </div>
</section>
{faq_section(base)}
{cta_band(base)}"""
    svc_url = canonical
    extra = ld_block(
        breadcrumb_ld(SITE, [("Home", SITE + "/"), ("Services", SITE + "/services/"), (kicker, canonical)]),
        service_ld(title, meta_desc, svc_url),
        faq_ld(),
        {"@context": "https://schema.org", "@type": "MedicalWebPage",
         "name": meta_title, "url": canonical, "description": meta_desc,
         "about": {"@id": SITE + "/#clinic"}})
    page(base, f"services/{folder}/index.html", meta_title, meta_desc,
         canonical, active_token, body, extra, og_type="article")

def build_service_pages():
    service_detail(
        "telemedicine-queens-ny", "services/telemedicine-queens-ny/",
        "Telemedicine", "Telemedicine Doctor in Queens, NY",
        "telemedicine-virtual-care",
        "See a board-certified doctor by secure video — no commute, no waiting room, the same expert care. Telehealth visits with Dr. Islam are available across New York State.",
        ["Our secure telehealth platform connects you with " + DOCTOR + " by video for a wide range of conditions. It's fast, private, and ideal when a trip to the office isn't practical.",
         "You'll get the same thorough, personal attention as an in-office visit — including prescriptions sent to your pharmacy and referrals when you need them."],
        ["Board-certified physician on video", "Same-day appointments often available",
         "Prescriptions &amp; refills sent to your pharmacy", "Available anywhere in New York State"],
        "Telemedicine Doctor Queens NY | Board-Certified Virtual Care | Jumpstart Medical",
        "Book a telemedicine visit with a board-certified doctor in Queens, NY. Secure video care for sick visits, refills, chronic conditions, and weight loss — available across New York. Call (917) 932-2315.",
        "Great For", ["Sick visits &amp; cold/flu symptoms", "Chronic disease follow-ups (diabetes, hypertension, asthma)",
                      "Prescription renewals &amp; specialist referrals", "GLP-1 weight loss management &amp; dietary guidance",
                      "Reviewing lab results", "Medication questions"],
        hero_bg="telehealth-service-support")

    service_detail(
        "urgent-care-clinic-queens-ny", "services/",
        "Urgent Care", "Urgent Care in Flushing, Queens NY",
        "urgent-care-consultation",
        "Same-day and walk-in care for fevers, infections, minor injuries, and conditions that need prompt attention — without the emergency-room wait or cost.",
        ["When you're not feeling well, you shouldn't have to wait days for an appointment. Jumpstart Medical offers same-day and walk-in urgent care during office hours.",
         "You'll be seen by " + DOCTOR + " herself — not shuffled between providers — for attentive care and a clear plan to feel better."],
        ["Same-day &amp; walk-in appointments", "Seen by a board-certified physician",
         "On-site EKG, labs &amp; blood work", "Most insurance plans accepted"],
        "Urgent Care in Flushing, Queens NY | Same-Day Doctor Appointment | Jumpstart Medical",
        "Same-day and walk-in urgent care in Flushing, Queens NY. Fevers, infections, minor injuries, and more — seen by a board-certified physician. Call (917) 932-2315.",
        "We Treat", ["Fevers, colds, flu &amp; COVID-19", "Sore throat, ear &amp; sinus infections",
                     "Minor cuts, burns &amp; sprains", "Urinary tract infections",
                     "Rashes &amp; allergic reactions", "Stomach bugs &amp; dehydration"],
        hero_bg="flushing-clinic-exam-room")

    service_detail(
        "weight-loss-in-flushing-ny", "services/weight-loss-in-flushing-ny/",
        "Weight Loss", "Medical Weight Loss in Flushing, NY",
        "weight-loss-nutrition-flushing",
        "Medically supervised weight loss with proven GLP-1 options — including Wegovy, Ozempic, Mounjaro, and Zepbound — plus weekly check-ins and personalized dose adjustments.",
        ["Sustainable weight loss works best with medical guidance. " + DOCTOR + " designs a plan around your health history, goals, and lifestyle — not a one-size-fits-all program.",
         "Popular options include Wegovy, Ozempic, Mounjaro, and Zepbound. Weekly check-ins and personalized dose adjustments keep you on track and safe."],
        ["Physician-supervised GLP-1 programs", "Wegovy, Ozempic, Mounjaro &amp; Zepbound",
         "Weekly check-ins &amp; dose adjustments", "In-person or via telehealth"],
        "Medical Weight Loss in Flushing, NY | Wegovy, Ozempic & More | Jumpstart Medical",
        "Physician-supervised medical weight loss in Flushing, NY. GLP-1 programs including Wegovy, Ozempic, Mounjaro, and Zepbound with weekly check-ins. Call (917) 932-2315.",
        "Program Includes", ["Comprehensive health evaluation", "Personalized GLP-1 prescription plan",
                             "Weekly progress check-ins", "Nutrition &amp; lifestyle guidance",
                             "Dose adjustments as you progress", "In-person or telehealth support"],
        hero_bg="weight-loss-consultation")

# ----------------------------------------------------------------------------
# ABOUT
# ----------------------------------------------------------------------------
def build_about():
    base = "../"
    canonical = SITE + "/about-us/"
    trail = [("Home", L(base, "")), ("About", canonical)]
    vals = [
        ("heart", "Patients First", "Unhurried visits, real listening, and decisions made together."),
        ("shield", "Board-Certified Expertise", "Family medicine grounded in evidence and years of experience."),
        ("steth", "Whole-Person Care", "Primary, urgent, and preventive care coordinated in one place."),
        ("video", "Care On Your Terms", "In-person in Flushing or by secure video across New York."),
    ]
    val_html = "".join(
        f'<div class="feat reveal"><span style="color:var(--coral);display:inline-flex;width:34px;height:34px">{icon(i)}</span><h3>{t}</h3><p>{d}</p></div>'
        for i, t, d in vals)
    body = page_hero(base, "About Jumpstart Medical",
        "Meet " + DOCTOR + ", Your Flushing Family Physician",
        "A board-certified physician caring for the Queens community since 2013 — with the time, attention, and cultural understanding every patient deserves.",
        trail, "medical-team-jumpstart") + f"""
<section class="section">
  <div class="wrap">
    <div class="split">
      <div class="split-media reveal">{img(base, "medicine-that-listens", DOCTOR + " at Jumpstart Medical in Flushing, NY", lazy=False)}
        <div class="badge-float"><span class="num">10+</span><small>Years caring for Flushing families</small></div>
      </div>
      <div class="reveal prose">
        <span class="kicker">Our Story</span>
        <h2>Comprehensive Care, Delivered Personally.</h2>
        <p>{DOCTOR} is a board-certified family physician in Flushing, NY, affiliated with Long Island Jewish Medical Center and in practice since 2013. She founded Jumpstart Medical on a simple belief: primary care should be accessible, comprehensive, and deeply personal.</p>
        <p>Dr. Islam specializes in all aspects of primary care — routine wellness and sick visits, weight management, treatment of minor injuries, and management of chronic conditions. She speaks English, Bengali, Urdu, and Hindi, caring for the diverse community of Queens in the language patients know best.</p>
        <p>Whether you visit in person or by video, you'll get thorough, unhurried attention and a clear plan for your health.</p>
      </div>
    </div>
  </div>
</section>
<section class="section" style="background:var(--paper)">
  <div class="wrap">
    <div class="section-head center"><span class="kicker center">What Guides Us</span><h2>Our Values</h2></div>
    <div class="feat-grid" style="margin-top:2.2rem">{val_html}</div>
  </div>
</section>
<section class="section band-dark">
  <div class="wrap">
    <div class="stats on-dark reveal">
      <div class="stat"><div class="n">2013</div><div class="l" style="color:rgba(255,255,255,.7)">In practice since</div></div>
      <div class="stat"><div class="n">4</div><div class="l" style="color:rgba(255,255,255,.7)">Languages spoken</div></div>
      <div class="stat"><div class="n">5.0</div><div class="l" style="color:rgba(255,255,255,.7)">Patient rating</div></div>
      <div class="stat"><div class="n">14+</div><div class="l" style="color:rgba(255,255,255,.7)">Services offered</div></div>
    </div>
  </div>
</section>
{reviews_section(base)}
{cta_band(base)}"""
    extra = ld_block(breadcrumb_ld(SITE, [("Home", SITE + "/"), ("About", canonical)]),
                     physician_ld())
    page(base, "about-us/index.html",
         "About Jumpstart Medical | Dr. Shalena Islam, Flushing NY Family Physician",
         "Meet Dr. Shalena Islam — a board-certified family physician in Flushing, Queens NY since 2013. Comprehensive primary, urgent, and telehealth care in English, Bengali, Urdu, and Hindi.",
         canonical, "about-us/", body, extra)

# ----------------------------------------------------------------------------
# CONTACT
# ----------------------------------------------------------------------------
def build_contact():
    base = "../"
    canonical = SITE + "/contact/"
    trail = [("Home", L(base, "")), ("Contact", canonical)]
    hours_rows = "".join(
        f'<div class="hours-row"><span>{d}</span><span>{t}</span></div>' for d, t in HOURS)
    body = page_hero(base, "Contact Us",
        "Book a Visit or Get in Touch",
        "Call, book online, or stop by our Flushing office. New patients are always welcome — in person or by telehealth.",
        trail, "medical-team-collaboration") + f"""
<section class="section">
  <div class="wrap">
    <div class="contact-grid">
      <div class="reveal">
        <span class="kicker">Get in Touch</span>
        <h2>We're Here to Help</h2>
        <div class="info-row">{icon('phone')}<div><b>Phone</b><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></div></div>
        <div class="info-row">{icon('pin')}<div><b>Office</b><p>{ADDR_FULL}</p><a href="{MAPS}" target="_blank" rel="noopener">Get directions &rarr;</a></div></div>
        <div class="info-row">{icon('clock')}<div><b>Hours</b><div style="margin-top:.4rem">{hours_rows}</div></div></div>
        <div class="info-row">{icon('video')}<div><b>Book Online</b><a href="{ZOCDOC}" target="_blank" rel="noopener">Schedule on ZocDoc &rarr;</a></div></div>
        <p style="margin-top:1.6rem"><a class="btn btn-primary btn-lg" href="{ZOCDOC}" target="_blank" rel="noopener">Book a Visit</a></p>
      </div>
      <div class="reveal">
        <form data-contact-form aria-label="Contact form" style="background:var(--paper);border:1px solid var(--line);border-radius:var(--radius-lg);padding:2rem">
          <h3 style="margin-bottom:1.2rem">Request an Appointment</h3>
          <div class="form-field"><label for="cname">Full name</label><input id="cname" name="name" type="text" autocomplete="name" required></div>
          <div class="form-field"><label for="cphone">Phone</label><input id="cphone" name="phone" type="tel" autocomplete="tel" required></div>
          <div class="form-field"><label for="cemail">Email</label><input id="cemail" name="email" type="email" autocomplete="email"></div>
          <div class="form-field"><label for="creason">Reason for visit</label>
            <select id="creason" name="reason">
              <option>Primary / Preventive care</option><option>Urgent / Same-day visit</option>
              <option>Telemedicine visit</option><option>Weight loss program</option>
              <option>No-fault / accident care</option><option>Other</option>
            </select></div>
          <div class="form-field"><label for="cmsg">Message</label><textarea id="cmsg" name="message" rows="4"></textarea></div>
          <button class="btn btn-primary" type="submit" style="width:100%">Send Request</button>
          <p class="form-note" hidden style="margin:1rem 0 0;color:var(--emerald);font-weight:600">Thanks! We received your request and will call you back shortly. For urgent needs, please call {PHONE_DISPLAY}.</p>
        </form>
      </div>
    </div>
  </div>
</section>
<section class="section" style="background:var(--paper);padding-top:0">
  <div class="wrap">
    <iframe class="map-embed" src="{MAP_EMBED}" loading="lazy" title="Map to Jumpstart Medical in Flushing, NY" referrerpolicy="no-referrer-when-downgrade" style="height:420px"></iframe>
  </div>
</section>
{cta_band(base)}"""
    extra = ld_block(breadcrumb_ld(SITE, [("Home", SITE + "/"), ("Contact", canonical)]),
                     clinic_ld())
    page(base, "contact/index.html",
         "Contact Jumpstart Medical | Flushing, Queens NY | (917) 932-2315",
         "Contact Jumpstart Medical in Flushing, Queens NY. Call (917) 932-2315, book on ZocDoc, or visit us at 142-42 Booth Memorial Avenue. New patients welcome — in person or telehealth.",
         canonical, "contact/", body, extra)

# ----------------------------------------------------------------------------
# BLOG / HEALTH JOURNAL
# ----------------------------------------------------------------------------
POSTS = [
    ("telehealth-service-support", "Telemedicine", "When to Choose a Telehealth Visit vs. Coming In",
     "A quick guide to which symptoms and follow-ups are a great fit for video care — and when an in-person visit is the smarter call."),
    ("weight-loss-consultation", "Weight Loss", "GLP-1 Weight Loss: What to Expect Week by Week",
     "How medically supervised GLP-1 programs work, what results look like, and why weekly check-ins matter for lasting change."),
    ("chronic-disease-blood-pressure-check", "Chronic Care", "Managing High Blood Pressure Without the Guesswork",
     "Simple, sustainable habits and the monitoring that helps you keep hypertension under control."),
    ("health-lab-blood-work", "No-Fault", "After a Car Accident: How No-Fault Care Works in NY",
     "What New York no-fault insurance covers, why timing matters, and how we handle the billing for you."),
    ("primary-care-consultation-queens", "Preventive", "Your Annual Physical: What It Should Actually Cover",
     "The screenings and conversations that make a yearly checkup worth your time."),
    ("mens-health-checkup", "Men's Health", "Health Screenings Men Shouldn't Skip",
     "Age-by-age screenings that catch problems early — and keep you feeling your best."),
]

def build_blog():
    base = "../"
    canonical = SITE + "/blogs/"
    trail = [("Home", L(base, "")), ("Health Journal", canonical)]
    cards = ""
    for slug, cat, title, desc in POSTS:
        cards += f"""
      <article class="post reveal">
        <div class="card-media">{img(base, slug, title, sizes="(max-width:860px) 100vw, 33vw")}</div>
        <div class="card-body">
          <span class="post-meta">{cat}</span>
          <h3 style="margin:.5rem 0 .5rem">{title}</h3>
          <p>{desc}</p>
          <a class="more" href="{L(base,'blogs/')}">Read article &rarr;</a>
        </div>
      </article>"""
    body = page_hero(base, "Health Journal",
        "Practical Health Tips From Jumpstart Medical",
        "Guidance on telehealth, weight loss, chronic care, and staying well — written for the Flushing community by Dr. Islam's team.",
        trail, "health-counseling-flushing") + f"""
<section class="section">
  <div class="wrap"><div class="grid grid-3">{cards}</div></div>
</section>
{cta_band(base)}"""
    extra = ld_block(breadcrumb_ld(SITE, [("Home", SITE + "/"), ("Health Journal", canonical)]),
                     {"@context": "https://schema.org", "@type": "Blog", "name": "Jumpstart Medical Health Journal", "url": canonical})
    page(base, "blogs/index.html",
         "Health Journal | Tips & Guides From Jumpstart Medical, Flushing NY",
         "Health tips and guides from Jumpstart Medical in Flushing, Queens NY — telehealth, weight loss, chronic care, no-fault, and preventive health from Dr. Shalena Islam's team.",
         canonical, "blogs/", body, extra)

# ----------------------------------------------------------------------------
# SELF ASSESSMENT
# ----------------------------------------------------------------------------
def build_self_assessment():
    base = "../"
    canonical = SITE + "/self-assessment/"
    trail = [("Home", L(base, "")), ("Self Assessment", canonical)]
    checks = [
        ("Am I due for a check-up?", "It's been over a year since your last physical, or you've never had one as an adult."),
        ("Should I consider weight loss support?", "You've struggled to lose weight with diet and exercise alone, or have weight-related health concerns."),
        ("Do I need urgent care today?", "You have a fever, infection, or minor injury that can't wait for a routine appointment."),
        ("Is telehealth right for me?", "You need a refill, follow-up, or have symptoms that don't require hands-on evaluation."),
        ("Was I in a car accident?", "You've been injured in a motor vehicle accident and may be covered by no-fault insurance."),
        ("Managing a chronic condition?", "You have diabetes, high blood pressure, or another ongoing condition that needs regular monitoring."),
    ]
    items = "".join(
        f'<div class="feat reveal"><span style="color:var(--coral);display:inline-flex;width:32px;height:32px">{icon("check")}</span><h3>{q}</h3><p>{a}</p></div>'
        for q, a in checks)
    body = page_hero(base, "Self Assessment",
        "Not Sure What Kind of Visit You Need?",
        "Answer a few quick questions to figure out the right next step — then book in seconds or call us and we'll guide you.",
        trail, "chronic-disease-blood-pressure-check") + f"""
<section class="section">
  <div class="wrap">
    <div class="section-head center"><span class="kicker center">Quick Check</span><h2>Do Any of These Sound Like You?</h2><p class="lead">If you recognize yourself below, we can help — often the same day.</p></div>
    <div class="feat-grid" style="margin-top:2.2rem">{items}</div>
    <div class="center" style="margin-top:2.6rem">
      <a class="btn btn-primary btn-lg" href="{ZOCDOC}" target="_blank" rel="noopener">Book a Visit</a>
      <a class="btn btn-outline btn-lg" href="tel:{PHONE_TEL}" style="margin-left:.6rem">{icon('phone')} Call {PHONE_DISPLAY}</a>
    </div>
    <p class="center" style="margin-top:1.6rem;color:var(--muted);font-size:.9rem;max-width:60ch;margin-inline:auto">This self assessment is for general guidance only and is not a medical diagnosis. If you are experiencing a medical emergency, call 911.</p>
  </div>
</section>
{cta_band(base)}"""
    extra = ld_block(breadcrumb_ld(SITE, [("Home", SITE + "/"), ("Self Assessment", canonical)]))
    page(base, "self-assessment/index.html",
         "Health Self Assessment | What Visit Do You Need? | Jumpstart Medical",
         "Take Jumpstart Medical's quick self assessment to find the right visit — primary, urgent, telehealth, weight loss, or no-fault care in Flushing, Queens NY. Call (917) 932-2315.",
         canonical, "", body, extra)

# ----------------------------------------------------------------------------
# JUMPSTART ACADEMY
# ----------------------------------------------------------------------------
def build_academy():
    base = "../"
    canonical = SITE + "/jumpstart-academy/"
    trail = [("Home", L(base, "")), ("Jumpstart Academy", canonical)]
    topics = [
        ("video", "Living With Diabetes", "Understand blood sugar, medications, and daily habits that make a difference."),
        ("heart", "Heart-Healthy Living", "Blood pressure, cholesterol, and the everyday choices that protect your heart."),
        ("steth", "Weight Loss, Explained", "How GLP-1 medications work and what a supervised program really looks like."),
        ("shield", "Preventive Care 101", "The screenings and vaccines that keep small problems from becoming big ones."),
    ]
    items = "".join(
        f'<article class="card reveal" style="padding:1.8rem"><span style="color:var(--coral);display:inline-flex;width:36px;height:36px">{icon(i)}</span><h3 style="margin:.8rem 0 .4rem">{t}</h3><p style="color:var(--muted);font-size:.95rem">{d}</p></article>'
        for i, t, d in topics)
    body = page_hero(base, "Jumpstart Academy",
        "Learn to Take Charge of Your Health",
        "Clear, trustworthy education from Dr. Islam's team — so you understand your body, your options, and your care.",
        trail, "compassionate-patient-care") + f"""
<section class="section">
  <div class="wrap">
    <div class="section-head center"><span class="kicker center">Learn</span><h2>Featured Topics</h2><p class="lead">Practical, plain-language health education for patients and families.</p></div>
    <div class="grid grid-2" style="margin-top:2.4rem">{items}</div>
  </div>
</section>
<section class="section" style="background:var(--paper)">
  <div class="wrap">
    <div class="split">
      <div class="split-media reveal">{img(base, "medical-team-jumpstart", "Jumpstart Medical team educating patients in Flushing, NY")}</div>
      <div class="reveal">
        <span class="kicker">Why It Matters</span>
        <h2>Informed Patients Get Better Care.</h2>
        <p class="lead">When you understand your health, every visit goes further. Jumpstart Academy turns complex medicine into clear steps you can act on.</p>
        <ul class="check-list">
          <li>{icon('check')}<span>Plain-language guides you can trust</span></li>
          <li>{icon('check')}<span>Written and reviewed by clinicians</span></li>
          <li>{icon('check')}<span>Focused on real, everyday decisions</span></li>
        </ul>
        <p style="margin-top:1.6rem"><a class="btn btn-primary" href="{L(base,'blogs/')}">Explore the Health Journal &rarr;</a></p>
      </div>
    </div>
  </div>
</section>
{cta_band(base)}"""
    extra = ld_block(breadcrumb_ld(SITE, [("Home", SITE + "/"), ("Jumpstart Academy", canonical)]))
    page(base, "jumpstart-academy/index.html",
         "Jumpstart Academy | Patient Health Education | Jumpstart Medical, Flushing NY",
         "Jumpstart Academy offers clear, trustworthy health education from Jumpstart Medical in Flushing, Queens NY — diabetes, heart health, weight loss, and preventive care.",
         canonical, "", body, extra)

# ----------------------------------------------------------------------------
# 404
# ----------------------------------------------------------------------------
def build_404():
    base = ""
    body = f"""
<section class="page-hero">
  {img(base, "flushing-clinic-exam-room", "Jumpstart Medical, Flushing NY", cls="hero-bg", lazy=False, sizes="100vw")}
  <div class="wrap" style="text-align:center">
  <span class="kicker center">404</span>
  <h1 style="margin-inline:auto">This Page Took a Sick Day.</h1>
  <p class="lead" style="margin-inline:auto">The page you're looking for can't be found — but we're still here to help.</p>
  <div class="hero-actions" style="justify-content:center">
    <a class="btn btn-primary" href="{L(base,'')}">Back to Home</a>
    <a class="btn btn-ghost-light" href="tel:{PHONE_TEL}">{icon('phone')} {PHONE_DISPLAY}</a>
  </div>
</div></section>"""
    page(base, "404.html", "Page Not Found | Jumpstart Medical",
         "The page you're looking for can't be found. Return to Jumpstart Medical or call (917) 932-2315.",
         SITE + "/404.html", "", body)

# ----------------------------------------------------------------------------
# sitemap.xml / robots.txt / manifest
# ----------------------------------------------------------------------------
def build_meta_files():
    urls = [
        ("/", "1.0", "weekly"),
        ("/services/", "0.9", "monthly"),
        ("/services/telemedicine-queens-ny/", "0.9", "monthly"),
        ("/services/urgent-care-clinic-queens-ny/", "0.9", "monthly"),
        ("/services/weight-loss-in-flushing-ny/", "0.9", "monthly"),
        ("/about-us/", "0.8", "monthly"),
        ("/contact/", "0.8", "monthly"),
        ("/blogs/", "0.7", "weekly"),
        ("/self-assessment/", "0.6", "monthly"),
        ("/jumpstart-academy/", "0.6", "monthly"),
    ]
    today = datetime.date.today().isoformat()
    entries = "".join(
        f"  <url><loc>{SITE}{u}</loc><lastmod>{today}</lastmod>"
        f"<changefreq>{cf}</changefreq><priority>{p}</priority></url>\n"
        for u, p, cf in urls)
    sitemap = ('<?xml version="1.0" encoding="UTF-8"?>\n'
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
               + entries + '</urlset>\n')
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap)
    print("wrote sitemap.xml")

    robots = ("User-agent: *\n"
              "Allow: /\n\n"
              f"Sitemap: {SITE}/sitemap.xml\n")
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots)
    print("wrote robots.txt")

    manifest = ('{\n'
                f'  "name": "{NAME}",\n'
                f'  "short_name": "Jumpstart",\n'
                '  "description": "Primary, urgent, and telemedicine care in Flushing, Queens NY.",\n'
                '  "start_url": "/",\n'
                '  "display": "standalone",\n'
                '  "background_color": "#f8f5ef",\n'
                '  "theme_color": "#0d2b28",\n'
                '  "icons": [{ "src": "/assets/img/favicon.svg", "sizes": "any", "type": "image/svg+xml" }]\n'
                '}\n')
    with open(os.path.join(ROOT, "site.webmanifest"), "w", encoding="utf-8") as f:
        f.write(manifest)
    print("wrote site.webmanifest")

# ----------------------------------------------------------------------------
def main():
    build_home()
    build_services()
    build_service_pages()
    build_about()
    build_contact()
    build_blog()
    build_self_assessment()
    build_academy()
    build_404()
    build_meta_files()
    print("\nDone.")

if __name__ == "__main__":
    main()
