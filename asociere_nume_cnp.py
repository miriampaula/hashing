import pandas as pd

# Încărcăm fișierele
df_nume = pd.read_csv("nume_unice.csv")     # Fișierul cu numele
df_cnp = pd.read_csv("cnp_generat.csv")      # Fișierul cu CNP-urile generate

# Filtrăm CNP-urile pe sexe
cnp_femei = df_cnp[df_cnp["Sex"] == "F"]
cnp_barbati = df_cnp[df_cnp["Sex"] == "M"]

# Separăm numele în funcție de sex
nume_femei = df_nume[df_nume["Sex"] == "F"]
nume_barbati = df_nume[df_nume["Sex"] == "M"]

# Resetăm indecșii pentru a ne asigura că sunt aliniați
nume_femei = nume_femei.reset_index(drop=True)
nume_barbati = nume_barbati.reset_index(drop=True)
cnp_femei = cnp_femei.reset_index(drop=True)
cnp_barbati = cnp_barbati.reset_index(drop=True)

# Convertim CNP-urile la text pentru a evita .0
cnp_femei["CNP"] = cnp_femei["CNP"].astype(str)
cnp_barbati["CNP"] = cnp_barbati["CNP"].astype(str)

# Asociem CNP-urile cu numele
nume_femei["CNP"] = cnp_femei["CNP"]
nume_barbati["CNP"] = cnp_barbati["CNP"]

# Concatenăm datele într-un singur DataFrame
df_final = pd.concat([nume_femei, nume_barbati], ignore_index=True)

# Salvăm fișierul final
df_final.to_csv("nume_cu_cnp.csv", index=False)
print("Fișierul final cu nume și CNP-uri a fost generat!")
