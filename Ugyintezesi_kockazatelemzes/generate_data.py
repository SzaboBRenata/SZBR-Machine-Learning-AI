import pandas as pd
import random
from pathlib import Path

random.seed(42)

N = 1000
Kesedelmes_UGYEK = 80

adatok = []

for i in range(N):
    kesett = 1 if i < Kesedelmes_UGYEK else 0
    
    if kesett:
        hianypotlas = random.randint(4, 14)
        ugyintezesi_nap = random.randint(35, 60)
        hatralevo_nap = 0
        megkereses = random.randint(2, 8)
        hianyos = "Igen"
        korabbi_keses = "Igen"
    else:
        hianypotlas = random.randint(0, 5)
        ugyintezesi_nap = random.randint(1, 45)
        hatralevo_nap = random.randint(1, 30)
        megkereses = random.randint(0, 3)
        hianyos = random.choice(["Igen", "Nem"])
        korabbi_keses = random.choice(["Igen", "Nem"])

    adatok.append({
        "Ugy_azonosito": f"UGY{i+1:04d}",
        "Ugytipus": random.choice(
            ["Sajtó", "Reklám", "Nyomvonal", "Frekvencia", "Piacfelügyelet"]
        ),
        "Beerkezes_modja": random.choice(
            ["Elektronikus", "Papir"]
        ),
        "Hianypotlasok_szama": hianypotlas,
        "Ugyintezesi_napok": ugyintezesi_nap,
        "Hataridoig_hatralevo_napok": hatralevo_nap,
        "Ugyfelmegkeresesek_szama": megkereses,
        "Dokumentum_hianyos": hianyos,
        "Korabbi_hasonlo_ugy_kesett": korabbi_keses,
        "Hatarido_tullepes": "Igen" if kesett else "Nem"
    })

df = pd.DataFrame(adatok)

mappa = Path("data")
mappa.mkdir(exist_ok=True)

df.to_excel(mappa / "ugyek_adatok.xlsx",
            sheet_name="Ugyek", index=False)

print("Adatgenerálás kész!")
print("Ügyek száma:", len(df))
print("Késedelmes ügyek:",
      (df["Hatarido_tullepes"] == "Igen").sum())
print("Excel mentve:", mappa / "ugyek_adatok.xlsx")
