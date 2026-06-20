# -*- coding: utf-8 -*-
import os
import sys
import random
import argparse
import smtplib
import subprocess
import io
from email.message import EmailMessage
try:
    from PIL import Image as _PILImage
    _PILLOW_OK = True
except ImportError:
    _PILLOW_OK = False

LOGO_EMAIL_MAX_WIDTH = 200  # px, šířka loga v emailu

# ============================================================
# Autorizační údaje pro SMTP server
# ============================================================
SMTP_HOST = "smtp.seznam.cz"
SMTP_PORT = 465
SMTP_USER = "burlog@seznam.cz"
SMTP_PASS = os.environ.get("SMTP_PASSWORD", "")
if not SMTP_PASS:
    raise EnvironmentError("Proměnná prostředí SMTP_PASSWORD není nastavena!")
EMAIL_FROM = "burlog@seznam.cz"
EMAIL_SUBJECT = "Povolávací rozkaz: {{ jmeno }}"
EMAIL_BODY_TXT = """\
Ahoj,

posílám povolávací rozkaz na misi ARES III pro {{ jmeno }}. Tento
dokument vytiskni, dej ho do obálky a předej svému dítěti, jakoby přišel
poštou.

Děkujeme,
Velitelství mise ARES III
"""
EMAIL_BODY_HTML = """\
<!DOCTYPE html>
<html lang="cs">
<head>
  <meta charset="UTF-8">
  <style>
    body {{ font-family: Arial, sans-serif; background: #f4f4f4; margin: 0; padding: 0; }}
    .wrapper {{ max-width: 580px; margin: 40px auto; background: #ffffff;
                border-radius: 8px; overflow: hidden;
                box-shadow: 0 2px 8px rgba(0,0,0,.12); }}
    .footer img {{ width: 64px; height: auto; }}
    .body {{ padding: 36px 40px; color: #222222; line-height: 1.7; }}
    .body h2 {{ margin-top: 0; color: #0B3D91; }}
    .footer {{ background: #f0f0f0; padding: 16px 40px;
               font-size: 12px; color: #888; text-align: center; }}
  </style>
</head>
<body>
  <div class="wrapper">
    <div class="body">
      <p>Ahoj,</p>
      <p>posílám povolávací rozkaz na misi <strong>ARES III</strong>
         pro <strong>{{ jmeno }}</strong>. Tento dokument vytiskni,
         dej ho do obálky a předej svému dítěti, jakoby přišel poštou.</p>
      <p>Děkujeme,<br>
         <strong>Velitelství mise ARES III</strong></p>
    </div>
    <div class="footer">
      <img src="cid:logo_mise" alt="Logo mise ARES III">
    </div>
  </div>
</body>
</html>
"""
# ============================================================

# 1. Pole pro jména dětí podle odpovídajících agentur
#    Každá položka je tuple: (jmeno, email)
deti_nasa = [
    ("Týna Kubová",          "jana.kubova@seznam.cz"),
    ("Jakub Mikiska",        ""),
    ("Dominik Vávra",        "andrejkavavrova@gmail.com"),
    ("Šárka Zavadilová",     "hela.zavadilova@gmail.com"),
    ("Matěj Boreš",          "boresova.lucie@gmail.com"),
    ("Tereza Hamzová",       "hamzova.hana@gmail.com"),
]

deti_esa = [
    ("Berenika Topinková",   "anita.topinkova@seznam.cz"),
    ("Jakub Zavadil",        "hela.zavadilova@gmail.com"),
    ("Josef Caudr",          "lcaudrova@gmail.com"),
    ("Jáchym Bukovský",      "kaja.bukovska@seznam.cz"),
    ("Eliška Adámková",      "Radim.Adamek@seznam.cz"),
    ("Anežka Hamzová",       "hamzova.hana@gmail.com"),
]

deti_cnsa = [
    ("Radomír Jedlička",     "jedlikar@email.cz"),
    ("Rozálie Hamzová",      "hamzova.hana@gmail.com"),
    ("Matěj Mikiska",        ""),
    ("Antonín Michek",       "lukas.michek@email.cz"),
    ("Martin Vondra",        "lubos.vondra@email.cz"),
    ("Ella Bukovská",        "kaja.bukovska@seznam.cz"),
]

deti_isro = [
    ("Bohumil Boreš ml.",    "boresova.lucie@gmail.com"),
    ("Jan Vávra",            "andrejkavavrova@gmail.com"),
    ("Štěpán Topinka",       "anita.topinkova@seznam.cz"),
    ("Alžběta Caudrová",     "lcaudrova@gmail.com"),
    ("Dominik Adámek",       "Radim.Adamek@seznam.cz"),
    ("Stela Bruštíková",     "brustikova.katerina@seznam.cz"),
    ("Vojtěch Bukovský",     "kaja.bukovska@seznam.cz"),
]

deti_jaxa = [
    ("Anežka Borešová",      "boresova.lucie@gmail.com"),
    ("Viktorie Vávrová",     "andrejkavavrova@gmail.com"),
    ("Jindřich Bruštík",     "brustikova.katerina@seznam.cz"),
    ("Filip Vondra",         "lubos.vondra@email.cz"),
    ("Eliška Hamzová",       "hamzova.hana@gmail.com"),
    ("Bronislava Blümelová", "kaja.bukovska@seznam.cz"),
]

# 2. Definice parametrů pro jednotlivé kosmické agentury
agencies = {
    'NASA': {
        'full': 'National Aeronautics and Space Administration',
        'sub': 'Department of Human Exploration and Operations',
        'color': '#0B3D91',
        'prefix': 'NASA-A3-2026',
        'footer': 'NASA Headquarters • 300 E Street SW, Washington, DC 20546, USA',
        'list': deti_nasa,
        'velitel_mise': 'Michal Bukovský',
        'font_velitel_mise': "'Caveat'",
        'reditel_agentury': 'Bill Nelson',
        'font_reditel_agentury': "'Homemade Apple'",
        'titul_reditel_agentury': 'Administrátor NASA'
    },
    'ESA': {
        'full': 'European Space Agency • Agence spatiale européenne',
        'sub': 'Directorate of Human and Robotic Exploration',
        'color': '#003210',
        'prefix': 'ESA-ARES3-EU',
        'footer': 'ESA Headquarters • 8-10 rue Mario Nikis, 75738 Paris, France',
        'list': deti_esa,
        'velitel_mise': 'Michal Bukovský',
        'font_velitel_mise': "'Caveat'",
        'reditel_agentury': 'Josef Aschbacher',
        'font_reditel_agentury': "'Yellowtail'",
        'titul_reditel_agentury': 'Generální ředitel ESA'
    },
    'CNSA': {
        'full': 'China National Space Administration',
        'sub': 'Lunar and Deep Space Exploration Department',
        'color': '#C8102E',
        'prefix': 'CNSA-MARS-A3',
        'footer': 'CNSA Headquarters • 1A Fucheng Road, Haidian District, Beijing, China',
        'list': deti_cnsa,
        'velitel_mise': 'Michal Bukovský',
        'font_velitel_mise': "'Caveat'",
        'reditel_agentury': '张克俭',
        'font_reditel_agentury': "'Zhi Mang Xing'",
        'titul_reditel_agentury': 'Administrátor CNSA'
    },
    'ISRO': {
        'full': 'Indian Space Research Organisation',
        'sub': 'Human Space Flight Centre (HSFC)',
        'color': '#FF9933',
        'prefix': 'ISRO-ARES-III',
        'footer': 'ISRO Headquarters • Antariksh Bhavan, New BEL Road, Bengaluru, India',
        'list': deti_isro,
        'velitel_mise': 'Michal Bukovský',
        'font_velitel_mise': "'Caveat'",
        'reditel_agentury': 'S. Somanath',
        'font_reditel_agentury': "'Dawning of a New Day'",
        'titul_reditel_agentury': 'Předseda ISRO'
    },
    'JAXA': {
        'full': 'Japan Aerospace Exploration Agency',
        'sub': 'Human Spaceflight Technology Directorate',
        'color': '#1B365D',
        'prefix': 'JAXA-ARES3-JP',
        'footer': 'JAXA Headquarters • 2-1-1 Sengen, Tsukuba, Ibaraki 305-8505, Japan',
        'list': deti_jaxa,
        'velitel_mise': 'Michal Bukovský',
        'font_velitel_mise': "'Caveat'",
        'reditel_agentury': '山川 宏',
        'font_reditel_agentury': "'Yuji Syuku'",
        'titul_reditel_agentury': 'Prezident JAXA'
    }
}

LOGO_MISE = "logo-mise.png"


def html_na_pdf(html_soubor, pdf_soubor):
    """Převede HTML soubor na PDF pomocí wkhtmltopdf nebo chromium."""
    # Zkusíme nejprve chromium/google-chrome
    for cmd in ["chromium", "chromium-browser", "google-chrome", "google-chrome-stable"]:
        if subprocess.call(["which", cmd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
            subprocess.run([
                cmd, "--headless", "--disable-gpu", "--no-sandbox",
                f"--print-to-pdf={pdf_soubor}", html_soubor
            ], check=True)
            return
    # Fallback na wkhtmltopdf
    if subprocess.call(["which", "wkhtmltopdf"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
        subprocess.run(["wkhtmltopdf", html_soubor, pdf_soubor], check=True)
        return
    raise RuntimeError(
        "Nepodařilo se najít nástroj pro konverzi HTML→PDF. "
        "Nainstalujte 'wkhtmltopdf' nebo 'chromium'."
    )


def odeslat_email(jmeno, email, pdf_soubor):
    """Odešle PDF rozkaz na zadaný email s HTML tělem a inline logem mise."""
    msg = EmailMessage()
    msg["From"] = f"Michal Bukovský <{EMAIL_FROM}>"
    # msg["To"] = email
    msg["To"] = "burlog@seznam.cz"
    msg["Subject"] = EMAIL_SUBJECT.replace("{{ jmeno }}", jmeno)

    # Prostý text jako fallback
    msg.set_content(EMAIL_BODY_TXT.replace("{{ jmeno }}", jmeno))

    # HTML alternativa
    html_content = EMAIL_BODY_HTML.replace("{{ jmeno }}", jmeno)
    msg.add_alternative(html_content, subtype="html")

    # Inline logo mise (připojeno k HTML části pomocí Content-ID)
    logo_path = os.path.join(os.path.dirname(__file__), "logo-mise.png")
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as img_f:
            logo_data = img_f.read()

        # Zmenšení loga v paměti — originální soubor zůstane nedotčen
        if _PILLOW_OK:
            img = _PILImage.open(io.BytesIO(logo_data))
            if img.width > LOGO_EMAIL_MAX_WIDTH:
                ratio = LOGO_EMAIL_MAX_WIDTH / img.width
                new_size = (LOGO_EMAIL_MAX_WIDTH, int(img.height * ratio))
                img = img.resize(new_size, _PILImage.LANCZOS)
            buf = io.BytesIO()
            img.save(buf, format="PNG", optimize=True)
            logo_data = buf.getvalue()
        else:
            print("  ℹ Pillow není nainstalován, logo se přikládá v původní velikosti.")
            print("    Pro zmenšení spusť: pip install pillow")

        # Najdeme HTML payload a přiložíme k němu obrázek
        html_part = next(
            p for p in msg.walk()
            if p.get_content_type() == "text/html"
        )
        html_part.get_payload(decode=False)  # ujistíme se, že je načten
        msg.get_payload(1).add_related(
            logo_data,
            maintype="image",
            subtype="png",
            cid="<logo_mise>",
            filename="logo-mise.png",
        )
    else:
        print(f"  ⚠ Logo mise nenalezeno ({logo_path}), odesílám bez obrázku.")

    with open(pdf_soubor, "rb") as f:
        pdf_data = f.read()

    msg.add_attachment(
        pdf_data,
        maintype="application",
        subtype="pdf",
        filename=os.path.basename(pdf_soubor),
    )

    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as smtp:
        smtp.login(SMTP_USER, SMTP_PASS)
        smtp.send_message(msg)

    print(f"  → Email odeslán na {email} ({jmeno})")


def generuj_rozkazy(odeslat=False):
    # Načtení univerzální šablony
    if not os.path.exists("sablona.html"):
        print("Chyba: Soubor 'sablona.html' nebyl nalezen!")
        return

    with open("sablona.html", "r", encoding="utf-8") as f:
        template = f.read()

    os.makedirs("vystup_rozkazy", exist_ok=True)
    celkovy_pocet = 0

    # Projdeme všechny agentury a vygenerujeme rozkaz pro každé dítě v poli
    for kod, data in agencies.items():
        for jmeno, email in data['list']:
            # Náhodné vygenerování unikátního čísla rozkazu a podkladu kódu
            nahodne_id = random.randint(1000, 9999)
            cislo_rozkazu = f"{data['prefix']}-X2026-{nahodne_id}"
            podklad_kodu = f"{kod}*{nahodne_id}*2026"

            # Nahrazení placeholderů v šabloně
            html_child = template
            html_child = html_child.replace("{{ jmeno }}", jmeno)
            html_child = html_child.replace("{{ cislo_rozkazu }}", cislo_rozkazu)
            html_child = html_child.replace("{{ podklad_kodu }}", podklad_kodu)
            html_child = html_child.replace("{{ agentura_full }}", data['full'])
            html_child = html_child.replace("{{ agentura_sub }}", data['sub'])
            html_child = html_child.replace("{{ agentura_color }}", data['color'])
            html_child = html_child.replace("{{ agentura_logo }}", f"../{kod.lower()}-logo.svg")
            html_child = html_child.replace("{{ logo_mise }}", LOGO_MISE)
            html_child = html_child.replace("{{ footer }}", data['footer'])
            html_child = html_child.replace("{{ velitel_mise }}", data['velitel_mise'])
            html_child = html_child.replace("{{ font_velitel_mise }}", data['font_velitel_mise'])
            html_child = html_child.replace("{{ reditel_agentury }}", data['reditel_agentury'])
            html_child = html_child.replace("{{ font_reditel_agentury }}", data['font_reditel_agentury'])
            html_child = html_child.replace("{{ titul_reditel_agentury }}", data['titul_reditel_agentury'])

            # Uložení do samostatného HTML souboru
            bez_diakritiky = "".join([c for c in jmeno.lower() if c.isalnum()])
            html_filename = f"vystup_rozkazy/rozkaz_{kod.lower()}_{bez_diakritiky}.html"

            with open(html_filename, "w", encoding="utf-8") as f_out:
                f_out.write(html_child)

            celkovy_pocet += 1
            print(f"Vygenerován rozkaz pro: {jmeno} ({kod}) -> {html_filename}")

            # Odesílání emailem (pokud je vyžádáno)
            if odeslat:
                pdf_filename = html_filename.replace(".html", ".pdf")
                try:
                    html_na_pdf(os.path.abspath(html_filename), os.path.abspath(pdf_filename))
                    odeslat_email(jmeno, email, pdf_filename)
                except Exception as e:
                    print(f"  ✗ Chyba při odesílání pro {jmeno}: {e}")

            sys.exit(0)  # Pro testování generování pouze jednoho rozkazu, odkomentujte pro produkční běh

    print(f"\nÚspěšně dokončeno! Celkem vygenerováno {celkovy_pocet} HTML souborů ve složce 'vystup_rozkazy'.")
    if odeslat:
        print("Rozkazy byly odeslány emailem.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generátor povolávacích rozkazů mise ARES III"
    )
    parser.add_argument(
        "--odeslat",
        action="store_true",
        help="Kromě generování HTML také převede rozkazy na PDF a odešle je emailem.",
    )
    args = parser.parse_args()

    generuj_rozkazy(odeslat=args.odeslat)
