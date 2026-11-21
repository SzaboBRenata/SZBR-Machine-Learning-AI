import pandas as pd
import joblib
from pathlib import Path

# 1. Modell betöltése
projekt_mappa = Path(__file__).parent
modell = joblib.load(projekt_mappa / "ugy_kockazati_modell.pkl")

# 2. Új ügy adatainak megadása
uj_ugy = pd.DataFrame([{
    "Ugytipus": "Nyomvonal",
    "Beerkezes_modja": "Elektronikus",
    "Hianypotlasok_szama": 5,
    "Ugyintezesi_napok": 30,
    "Ugyfelmegkeresesek_szama": 3,
    "Dokumentum_hianyos": "Igen",
    "Korabbi_hasonlo_ugy_kesett": "Igen"
}])

# 3. Késési valószínűség kiszámítása
keses_valoszinuseg = modell.predict_proba(uj_ugy)[0][1]

# 4. Kockázati besorolás
if keses_valoszinuseg >= 0.70:
    kockazat = "MAGAS"
elif keses_valoszinuseg >= 0.40:
    kockazat = "KÖZEPES"
else:
    kockazat = "ALACSONY"

# 5. Eredmény megjelenítése
print("ÚJ ÜGY KOCKÁZATELEMZÉSE")
print("-------------------------")
print("Ügytípus:", uj_ugy.loc[0, "Ugytipus"])
print("Késés becsült valószínűsége:",
      round(keses_valoszinuseg * 100, 2), "%")
print("Kockázati besorolás:", kockazat)

