import random
import pandas as pd

# Parametrii pentru distribuția CNP-urilor
num_records = 1_000_000
female_ratio = 0.511  # 51.1%
male_ratio = 1 - female_ratio  # 48.9%

# Distribuția pe grupe de vârstă (în procente)
age_groups = {
    '0-14': 0.15,     # 15%
    '15-59': 0.60,    # 60%
    '60+': 0.25       # 25%
}

# Codurile județelor (presupunem că sunt disponibile ca procentaje)
judete = {
    1: 1.76,      # Alba
    2: 1.48,      # Arad
    3: 3.34,      # Argeș
    4: 3.34,      # Bacău
    5: 3.12,      # Bihor
    6: 1.79,      # Bistrița-Năsăud
    7: 2.08,      # Botoșani
    8: 3.35,      # Brașov
    9: 1.74,      # Brăila
    10: 1.54,     # Buzău
    11: 3.97,     # Caraș-Severin
    12: 3.08,     # Cluj
    13: 3.71,     # Constanța
    14: 1.45,     # Covasna
    15: 1.64,     # Dâmbovița
    16: 2.72,     # Dolj
    17: 3.35,     # Galați
    18: 2.59,     # Giurgiu
    19: 1.80,     # Gorj
    20: 2.06,     # Harghita
    21: 1.95,     # Hunedoara
    22: 2.13,     # Ialomița
    23: 4.19,     # Iași
    24: 2.59,     # Ilfov
    25: 1.76,     # Maramureș
    26: 1.48,     # Mehedinți
    27: 2.88,     # Mureș
    28: 2.25,     # Neamț
    29: 4.13,     # Olt
    30: 2.15,     # Prahova
    31: 1.34,     # Satu Mare
    32: 2.30,     # Sălaj
    33: 3.37,     # Sibiu
    34: 1.15,     # Suceava
    35: 1.14,     # Teleorman
    36: 1.13,     # Timiș
    37: 2.72,     # Tulcea
    38: 3.08,     # Vaslui
    39: 2.15,     # Vâlcea
    40: 9.97,     # Vrancea
    41: 2.91,     # București Sector 1
    42: 2.91,     # București Sector 2
    51: 2.91,     # București Sector 3
    52: 2.91      # București Sector 4
}


# Transformăm procentele județelor într-o listă de coduri repetate pentru sampling ușor
judete_expanded = [j for j, pct in judete.items() for _ in range(int(pct * 10))]

# Codificare sex și secol pentru generarea CNP-urilor
sex_code = {
    "F": {"0-14": "6", "15-59": "2", "60+": "4"},
    "M": {"0-14": "5", "15-59": "1", "60+": "3"}
}

# Generare CNP în funcție de anul nașterii și datele demografice
def genereaza_cnp(sex, age_group, judet_code):
    secol_cod = sex_code[sex][age_group]
    
    if age_group == '0-14':
        an = random.randint(2010, 2023)
    elif age_group == '15-59':
        an = random.randint(1964, 2009)
    elif age_group == '60+':
        an = random.randint(1924, 1963)

    # Formatăm anul, luna și ziua
    aa = str(an % 100).zfill(2)  # Ultimele două cifre ale anului
    ll = str(random.randint(1, 12)).zfill(2)
    zz = str(random.randint(1, 28)).zfill(2)  # Zile între 1-28 pentru simplitate
    
    # Cod județ, asigurându-ne că este numeric
    jj = str(int(judet_code)).zfill(2)
    
    # Număr unic de identificare (aleator între 001 și 999)
    nnn = str(random.randint(1, 999)).zfill(3)

    # Formăm CNP-ul fără cifra de control
    cnp_fara_control = f"{secol_cod}{aa}{ll}{zz}{jj}{nnn}"
    
    # Calculăm cifra de control pentru validitate
    control_weights = [2, 7, 9, 1, 4, 6, 3, 5, 8, 2, 7, 9]
    suma = sum(int(cnp_fara_control[i]) * control_weights[i] for i in range(12))
    cifra_control = suma % 11
    cifra_control = 1 if cifra_control == 10 else cifra_control
    
    return cnp_fara_control + str(cifra_control)

# Generăm CNP-urile conform distribuției pe sexe și grupe de vârstă
records = []
for _ in range(num_records):
    sex = "F" if random.random() < female_ratio else "M"
    age_group = random.choices(list(age_groups.keys()), weights=list(age_groups.values()), k=1)[0]
    judet_code = int(random.choice(judete_expanded))
    cnp = genereaza_cnp(sex, age_group, judet_code)
    records.append((sex, age_group, judet_code, cnp))

# Salvăm datele în CSV
df = pd.DataFrame(records, columns=["Sex", "Age_Group", "Judet_Code", "CNP"])
df.to_csv("cnp_generat.csv", index=False)
print("Fișierul CSV cu CNP-uri a fost generat!")
