import pandas as pd

df_nume = pd.read_csv("nume_unice.csv")    
df_cnp = pd.read_csv("cnp_generat.csv")     

cnp_femei = df_cnp[df_cnp["Sex"] == "F"]
cnp_barbati = df_cnp[df_cnp["Sex"] == "M"]

nume_femei = df_nume[df_nume["Sex"] == "F"]
nume_barbati = df_nume[df_nume["Sex"] == "M"]

nume_femei = nume_femei.reset_index(drop=True)
nume_barbati = nume_barbati.reset_index(drop=True)
cnp_femei = cnp_femei.reset_index(drop=True)
cnp_barbati = cnp_barbati.reset_index(drop=True)

cnp_femei["CNP"] = cnp_femei["CNP"].astype(str)
cnp_barbati["CNP"] = cnp_barbati["CNP"].astype(str)

nume_femei["CNP"] = cnp_femei["CNP"]
nume_barbati["CNP"] = cnp_barbati["CNP"]

df_final = pd.concat([nume_femei, nume_barbati], ignore_index=True)

df_final.to_csv("nume_cu_cnp.csv", index=False)
print("Fișierul final cu nume și CNP-uri a fost generat!")
