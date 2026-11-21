import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 1. Fájlok elérési útja
projekt_mappa = Path(__file__).parent
excel_fajl = projekt_mappa / "data" / "ugyek_adatok.xlsx"

# 2. Excel beolvasása
df = pd.read_excel(excel_fajl, sheet_name="Ugyek")

print("=" * 50)
print("ÜGYINTÉZÉSI ESETEK ELEMZÉSE")
print("=" * 50)

# 3. Alapadatok ellenőrzése
print("\n1. ADATÁLLOMÁNY")

print("Ügyek száma:", len(df))
print("Oszlopok száma:", len(df.columns))
print("Hiányzó adatok:", df.isnull().sum().sum())

print("\nOszlopnevek:")
print(df.columns.tolist())

# 4. Késedelmes és nem késedelmes ügyek
print("\n2. HATÁRIDŐ TÚLLÉPÉSEK")

keses_megoszlas = df["Hatarido_tullepes"].value_counts()

print(keses_megoszlas)

print("\nKésedelmes ügyek aránya:")
print(
    round(
        (df["Hatarido_tullepes"] == "Igen").mean() * 100,
        2
    ),
    "%"
)

# 5. Ügytípusok megoszlása
print("\n3. ÜGYTÍPUSOK")

ugytipusok = df["Ugytipus"].value_counts()

print(ugytipusok)

# 6. Ügytípusonkénti késedelmek
print("\n4. KÉSEDELEM ÜGYTÍPUSONKÉNT")

ugytipus_keses = pd.crosstab(
    df["Ugytipus"],
    df["Hatarido_tullepes"]
)

print(ugytipus_keses)

# 7. Statisztikai elemzés
print("\n5. LEÍRÓ STATISZTIKA")

print(
    df[
        [
            "Hianypotlasok_szama",
            "Ugyintezesi_napok",
            "Hataridoig_hatralevo_napok",
            "Ugyfelmegkeresesek_szama"
        ]
    ].describe().round(2)
)

# 8. Diagramok mentése
eredmeny_mappa = projekt_mappa / "eredmenyek"
eredmeny_mappa.mkdir(exist_ok=True)

# 1. diagram: ügytípusok
ugytipusok.plot(kind="bar", title="Ügyek megoszlása ügytípus szerint")
plt.xlabel("Ügytípus")
plt.ylabel("Ügyek száma")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(eredmeny_mappa / "ugytipusok.png")
plt.close()

# 2. diagram: késedelmes ügyek
keses_megoszlas.plot(
    kind="bar",
    title="Határidő túllépések megoszlása"
)
plt.xlabel("Határidő túllépés")
plt.ylabel("Ügyek száma")
plt.tight_layout()
plt.savefig(eredmeny_mappa / "kesedelmek.png")
plt.close()

# 3. diagram: hiánypótlások és késedelmek
df.boxplot(
    column="Hianypotlasok_szama",
    by="Hatarido_tullepes"
)
plt.title("Hiánypótlások száma késedelmi kategóriánként")
plt.suptitle("")
plt.xlabel("Határidő túllépés")
plt.ylabel("Hiánypótlások száma")
plt.tight_layout()
plt.savefig(eredmeny_mappa / "hianypotlasok.png")
plt.close()

print("\nElemzés befejeződött!")
print("A diagramok az eredmenyek mappába kerültek.")
