import pandas as pd
import joblib
from pathlib import Path

# Mappák és fájlok
projekt_mappa = Path(__file__).parent
adatfajl = projekt_mappa / "data" / "uj_ugyek.xlsx"
modell_fajl = projekt_mappa / "ugy_kockazati_modell.pkl"
eredmeny_mappa = projekt_mappa / "eredmenyek"

# Modell betöltése
modell = joblib.load(modell_fajl)

# Új ügyek beolvasása
adatok = pd.read_excel(adatfajl)

# Azonosítók megőrzése, ha vannak
azonositok = (
    adatok["Ugy_azonosito"]
    if "Ugy_azonosito" in adatok.columns
    else pd.Series(
        [f"UJ{i:03d}" for i in range(1, len(adatok) + 1)]
    )
)

# Modell bemeneti adatai
X = adatok.drop(
    columns=["Ugy_azonosito"],
    errors="ignore"
)

# Késési valószínűség
valoszinusegek = modell.predict_proba(X)[:, 1]

# Kockázati besorolás
eredmenyek = []

for p in valoszinusegek:
    if p >= 0.70:
        eredmenyek.append("MAGAS")
    elif p >= 0.40:
        eredmenyek.append("KÖZEPES")
    else:
        eredmenyek.append("ALACSONY")

# Eredménytábla
eredmeny = adatok.copy()
eredmeny["Ugy_azonosito"] = azonositok
eredmeny["Keses_valoszinusege_%"] = (
    valoszinusegek * 100
).round(2)
eredmeny["Kockazati_besorolas"] = eredmenyek

# Mentés
eredmeny_mappa.mkdir(exist_ok=True)

kimeneti_fajl = (
    eredmeny_mappa / "uj_ugyek_kockazati_eredmenye.xlsx"
)

eredmeny.to_excel(kimeneti_fajl, index=False)

print("Elemzés befejeződött!")
print(f"Elemzett ügyek száma: {len(eredmeny)}")
print(f"Eredményfájl: {kimeneti_fajl}")
print(eredmeny[
    ["Ugy_azonosito", "Keses_valoszinusege_%",
     "Kockazati_besorolas"]
])
