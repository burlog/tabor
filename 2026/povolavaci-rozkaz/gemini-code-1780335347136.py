# Pojďme nejdříve vyzkoušet čistou implementaci šikmého razítka přes CSS transformaci.
# Vytvoříme oba soubory: 'sablona.html' a 'generuj_rozkazy.py'.
# Sablona bude používat standardní Jinja2/Python format placeholdery: {{ jmeno }}, {{ cislo_rozkazu }}, {{ agentura_full }}, {{ agentura_sub }}, {{ agentura_color }}, {{ agentura_logo }}, {{ logo_mise }}, {{ footer }}.

sablona_content = """<!DOCTYPE html>
<html lang="cs">
<head>
<meta charset="UTF-8">
<title>Povolávací rozkaz - Ares III</title>
<style>
    *, *::before, *::after { box-sizing: border-box; }
    @page {
        size: A4;
        margin: 18mm 15mm;
    }
    body {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        color: #111111;
        margin: 0;
        padding: 0;
        font-size: 11pt;
        line-height: 1.5;
        background-color: #ffffff;
        position: relative;
    }
    .page {
        position: relative;
        height: 100%;
        width: 100%;
    }
    
    /* Šikmé razítko přes papír */
    .razitko-tajne {
        position: absolute;
        top: 35%;
        left: 10%;
        width: 80%;
        text-align: center;
        border: 4px dashed #c8102e;
        color: #c8102e;
        font-size: 42pt;
        font-weight: 900;
        letter-spacing: 8px;
        padding: 15px;
        text-transform: uppercase;
        transform: rotate(-25deg);
        opacity: 0.15;
        pointer-events: none;
        user-select: none;
        z-index: 10;
    }

    .header-table {
        display: table;
        width: 100%;
        border-bottom: 2px solid #111111;
        padding-bottom: 15px;
        margin-bottom: 25px;
    }
    .header-row {
        display: table-row;
    }
    .header-cell {
        display: table-cell;
        vertical-align: middle;
    }
    .header-logo {
        width: 90px;
    }
    .header-logo img {
        max-width: 80px;
        max-height: 70px;
        display: block;
    }
    .agency-title {
        font-weight: bold;
        font-size: 14pt;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .agency-sub {
        font-size: 9pt;
        color: #555555;
        margin-top: 2px;
    }
    
    .order-meta-table {
        display: table;
        width: 100%;
        margin-bottom: 30px;
        font-size: 10pt;
    }
    .order-meta-row {
        display: table-row;
    }
    .order-meta-cell {
        display: table-cell;
        padding: 4px 0;
    }
    
    /* Generování čárového kódu pomocí CSS */
    .barcode-container {
        display: inline-block;
        text-align: right;
    }
    .bars {
        display: flex;
        justify-content: flex-end;
        height: 35px;
        margin-bottom: 2px;
    }
    .bar-thin { width: 1px; background: #000; margin-right: 1px; }
    .bar-thick { width: 3px; background: #000; margin-right: 1px; }
    .bar-space { width: 2px; background: transparent; margin-right: 1px; }
    .barcode-text {
        font-family: 'Courier New', monospace;
        font-size: 8pt;
        color: #555555;
        letter-spacing: 2px;
    }

    .title-section {
        text-align: center;
        margin-bottom: 30px;
    }
    .main-title {
        font-size: 20pt;
        font-weight: bold;
        letter-spacing: 1px;
        margin: 0 0 5px 0;
        text-transform: uppercase;
    }
    .sub-title {
        font-size: 12pt;
        font-weight: bold;
        color: #444444;
        margin: 0;
    }
    
    .salutation {
        font-size: 12pt;
        font-weight: bold;
        margin-bottom: 15px;
    }
    .content-paragraph {
        text-align: justify;
        margin-bottom: 15px;
        text-indent: 20px;
    }
    
    /* Box s logem mise a detaily */
    .details-table {
        display: table;
        width: 100%;
        background-color: #f8f9fa;
        border: 1px solid #dddddd;
        margin: 25px 0;
    }
    .details-row {
        display: table-row;
    }
    .details-cell-info {
        display: table-cell;
        width: 70%;
        padding: 15px;
        vertical-align: middle;
    }
    .details-cell-logo {
        display: table-cell;
        width: 30%;
        padding: 15px;
        text-align: center;
        vertical-align: middle;
        border-left: 1px solid #dddddd;
        background-color: #ffffff;
    }
    .details-cell-logo img {
        max-width: 110px;
        max-height: 110px;
    }
    
    .info-line {
        margin: 6px 0;
        font-size: 10.5pt;
    }
    .info-label {
        font-weight: bold;
        display: inline-block;
        width: 130px;
    }
    
    .equipment-section {
        margin-top: 25px;
    }
    .equipment-title {
        font-size: 11pt;
        font-weight: bold;
        text-transform: uppercase;
        border-bottom: 1px solid #333333;
        padding-bottom: 3px;
        margin-bottom: 10px;
    }
    .equipment-list-table {
        display: table;
        width: 100%;
        font-size: 10pt;
    }
    .equipment-list-cell {
        display: table-cell;
        width: 50%;
        vertical-align: top;
    }
    .equipment-list {
        margin: 0;
        padding-left: 20px;
    }
    .equipment-list li {
        margin-bottom: 5px;
    }
    
    .signature-area {
        margin-top: 50px;
        display: table;
        width: 100%;
    }
    .signature-cell {
        display: table-cell;
        width: 50%;
        vertical-align: top;
    }
    .signature-line {
        border-top: 1px solid #666666;
        width: 80%;
        margin-top: 40px;
        padding-top: 5px;
        font-size: 9pt;
        color: #555555;
    }
    
    .footer {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        text-align: center;
        font-size: 8pt;
        color: #777777;
        border-top: 1px solid #eeeeee;
        padding-top: 8px;
    }
</style>
</head>
<body>

<div class="page">
    <div class="razitko-tajne">Přísně tajné</div>

    <div class="header-table">
        <div class="header-row">
            <div class="header-cell header-logo">
                <img src="{{ agentura_logo }}" alt="Logo Agentury">
            </div>
            <div class="header-cell" style="padding-left: 15px;">
                <div class="agency-title" style="color: {{ agentura_color }};">{{ agentura_full }}</div>
                <div class="agency-sub">{{ agentura_sub }}</div>
            </div>
        </div>
    </div>

    <div class="order-meta-table">
        <div class="order-meta-row">
            <div class="order-meta-cell" style="width: 60%;">
                <strong>Číslo rozkazu:</strong> {{ cislo_rozkazu }}<br>
                <strong>Datum vydání:</strong> 1. června 2026<br>
                <strong>Klasifikace:</strong> Úroveň 5 (Mezinárodní vesmírný program)
            </div>
            <div class="order-meta-cell" style="width: 40%; text-align: right; vertical-align: top;">
                <div class="barcode-container">
                    <div class="bars">
                        <div class="bar-thick"></div><div class="bar-thin"></div><div class="bar-space"></div>
                        <div class="bar-thin"></div><div class="bar-thick"></div><div class="bar-thin"></div>
                        <div class="bar-space"></div><div class="bar-thick"></div><div class="bar-thick"></div>
                        <div class="bar-thin"></div><div class="bar-space"></div><div class="bar-thin"></div>
                        <div class="bar-thick"></div><div class="bar-thin"></div><div class="bar-space"></div>
                        <div class="bar-thick"></div><div class="bar-thin"></div><div class="bar-thick"></div>
                    </div>
                    <div class="barcode-text">*{{ podklad_kodu }}*</div>
                </div>
            </div>
        </div>
    </div>

    <div class="title-section">
        <h1 class="main-title" style="color: {{ agentura_color }};">Povolávací rozkaz</h1>
        <p class="sub-title">Mise k Marsu: ARES III (Expedice Amicitia)</p>
    </div>

    <div class="salutation">VÁŽENÝ KADETE / VÁŽENÁ KADETKO,</div>
    
    <p class="content-paragraph">
        Na základě dekretu Mezinárodního výboru pro výzkum hlubokého vesmíru a ve spolupráci s partnerskými kosmickými organizacemi jsi byl(a) vybrán(a) jako klíčový člen posádky nadcházející expedice <strong>Ares III</strong>. Tvoje výjimečné výsledky během simulací, logické myšlení a morální integrita tě plně opravňují k účasti na nejvýznamnějším dobrodružství lidstva: <strong>letu na Mars a následném vědeckém výzkumu přímo na místě</strong>.
    </p>
    
    <p class="content-paragraph">
        Tímto se ti nařizuje povinný nástup k předletové přípravě. Cílem této mise není pouhé přistání, ale rozsáhlý geologický a atmosférický průzkum, který nám pomůže odhalit tajemství, jež <strong>Rudá planeta</strong> skrývá. Společně položíme základy pro budoucí trvalé osídlení.
    </p>

    <div class="details-table">
        <div class="details-row">
            <div class="details-cell-info">
                <div class="info-line"><span class="info-label">Povolávaný kadet:</span> <strong style="font-size: 12pt; color: {{ agentura_color }};">{{ jmeno }}</strong></div>
                <div class="info-line"><span class="info-label">Termín startu:</span> <strong>1. června 2026</strong> (Zahájení výcvikového cyklu)</div>
                <div class="info-line"><span class="info-label">Cíl cesty:</span> <strong>Rudá planeta (Mars)</strong>, biom Acidalia Planitia</div>
                <div class="info-line"><span class="info-label">Základna nástupu:</span> <strong>Základna Sedlo</strong> (Simulační středisko)</div>
                <div class="info-line"><span class="info-label">Statut mise:</span> Kritický / Povinný nástup v plné pohotovosti</div>
            </div>
            <div class="details-cell-logo">
                <img src="{{ logo_mise }}" alt="Logo Mise">
            </div>
        </div>
    </div>

    <div class="equipment-section">
        <div class="equipment-title">Materiální zabezpečení pro přežití a výzkum v marťanských podmínkách:</div>
        <p style="margin: 0 0 10px 0; font-size: 9pt; color: #444444; font-style: italic;">Vybavení musí být sbaleno v civilním zavazadle z důvodu utajení předletové fáze přesunu:</p>
        
        <div class="equipment-list-table">
            <div class="order-meta-row">
                <div class="equipment-list-cell" style="padding-right: 10px;">
                    <ul class="equipment-list">
                        <li><strong>Modul pro spánek:</strong> Spací pytel a izolační karimatka.</li>
                        <li><strong>Dekontaminační set:</strong> Kompletní hygienické potřeby, ručník.</li>
                        <li><strong>Ochranný štít:</strong> Nepromokavá svrchní bunda či pláštěnka.</li>
                    </ul>
                </div>
                <div class="equipment-list-cell" style="padding-left: 10px;">
                    <ul class="equipment-list">
                        <li><strong>Hydratační a stravovací kit:</strong> Ešus, lžíce, hrnek.</li>
                        <li><strong>Exteriérová obuv:</strong> Pevné boty určené pro marťanský regolit.</li>
                        <li><strong>Identifikační doklad:</strong> Kopie kartičky zdravotní pojišťovny.</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>

    <p class="content-paragraph" style="font-size: 9pt; font-style: italic; margin-top: 15px;">
        Upozornění: Nedostavení se k zážehu motorů v přesně stanovený čas bude klasifikováno jako hrubé porušení disciplíny a povede k okamžitému vyřazení z mezinárodního programu Ares.
    </p>

    <div class="signature-area">
        <div class="order-meta-row">
            <div class="signature-cell">
                <div class="signature-line">
                    Otisk schvalovacího razítka a podpis velitele
                </div>
            </div>
            <div class="signature-cell" style="text-align: right;">
                <div class="signature-line" style="display: inline-block; text-align: left;">
                    Letový ředitel mise Ares III<br>
                    Společné mezinárodní velitelství sil hlubokého vesmíru
                </div>
            </div>
        </div>
    </div>

    <div class="footer">
        {{ footer }}
    </div>
</div>

</body>
</html>
"""

# Nyní vytvoříme generující python skript
script_content = """# -*- coding: utf-8 -*-
import os
import random

# 1. Čtyři pole pro jména dětí podle odpovídajících agentur
deti_nasa = ["Tomáš Jedno", "Lucie Hvězdná", "Jakub Vesmírný", "Kateřina Odvážná"]
deti_esa = ["Jan Evropský", "Pierre Dupont", "Anna Schmidt", "Mateo Ricci"]
deti_cnsa = ["Li Wang", "Mei Ling", "Chao Chang", "Zhi Wei"]
deti_isro = ["Arjun Singh", "Priya Sharma", "Rohan Patel", "Deepika Padukone"]

# 2. Definice parametrů pro jednotlivé kosmické agentury
agencies = {
    'NASA': {
        'full': 'National Aeronautics and Space Administration',
        'sub': 'Department of Human Exploration and Operations',
        'color': '#0B3D91',
        'prefix': 'NASA-A3-2026',
        'footer': 'NASA Headquarters • 300 E Street SW, Washington, DC 20546, USA',
        'list': deti_nasa
    },
    'ESA': {
        'full': 'European Space Agency • Agence spatiale européenne',
        'sub': 'Directorate of Human and Robotic Exploration',
        'color': '#0032A0',
        'prefix': 'ESA-ARES3-EU',
        'footer': 'ESA Headquarters • 8-10 rue Mario Nikis, 75738 Paris, France',
        'list': deti_esa
    },
    'CNSA': {
        'full': 'China National Space Administration',
        'sub': 'Lunar and Deep Space Exploration Department',
        'color': '#C8102E',
        'prefix': 'CNSA-MARS-A3',
        'footer': 'CNSA Headquarters • 1A Fucheng Road, Haidian District, Beijing, China',
        'list': deti_cnsa
    },
    'ISRO': {
        'full': 'Indian Space Research Organisation',
        'sub': 'Human Space Flight Centre (HSFC)',
        'color': '#FF9933',
        'prefix': 'ISRO-ARES-III',
        'footer': 'ISRO Headquarters • Antariksh Bhavan, New BEL Road, Bengaluru, India',
        'list': deti_isro
    }
}

LOGO_MISE = "nasivka-logo.png"

def generuj_rozkazy():
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
        for jmeno in data['list']:
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
            html_child = html_child.replace("{{ agentura_logo }}", f"{kod.lower()}-logo.svg")
            html_child = html_child.replace("{{ logo_mise }}", LOGO_MISE)
            html_child = html_child.replace("{{ footer }}", data['footer'])
            
            # Uložení do samostatného souboru
            bez_diakritiky = "".join([c for c in jmeno.lower() if c.isalnum()])
            filename = f"vystup_rozkazy/rozkaz_{kod.lower()}_{bez_diakritiky}.html"
            
            with open(filename, "w", encoding="utf-8") as f_out:
                f_out.write(html_child)
                
            celkovy_pocet += 1
            print(f"Vygenerován rozkaz pro: {jmeno} ({kod}) -> {filename}")

    print(f"\\nÚspěšně dokončeno! Celkem vygenerováno {celkovy_pocet} HTML souborů ve složce 'vystup_rozkazy'.")

if __name__ == "__main__":
    generuj_rozkazy()
"""

with open("sablona.html", "w", encoding="utf-8") as f:
    f.write(sablona_content)

with open("generuj_rozkazy.py", "w", encoding="utf-8") as f:
    f.write(script_content)

print("Both files generated successfully in python tester.")