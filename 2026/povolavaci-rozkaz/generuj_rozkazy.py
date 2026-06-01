# -*- coding: utf-8 -*-
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
        'color': '#003210',
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

LOGO_MISE = "../../logo-mise.png"

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
            html_child = html_child.replace("{{ agentura_logo }}", f"../{kod.lower()}-logo.svg")
            html_child = html_child.replace("{{ logo_mise }}", LOGO_MISE)
            html_child = html_child.replace("{{ footer }}", data['footer'])

            # Uložení do samostatného souboru
            bez_diakritiky = "".join([c for c in jmeno.lower() if c.isalnum()])
            filename = f"vystup_rozkazy/rozkaz_{kod.lower()}_{bez_diakritiky}.html"

            with open(filename, "w", encoding="utf-8") as f_out:
                f_out.write(html_child)

            celkovy_pocet += 1
            print(f"Vygenerován rozkaz pro: {jmeno} ({kod}) -> {filename}")

    print(f"\nÚspěšně dokončeno! Celkem vygenerováno {celkovy_pocet} HTML souborů ve složce 'vystup_rozkazy'.")

if __name__ == "__main__":
    generuj_rozkazy()
