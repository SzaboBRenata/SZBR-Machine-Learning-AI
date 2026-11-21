import pandas as pd
import matplotlib.pyplot as plt
import joblib

from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    recall_score,
    precision_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
    RocCurveDisplay
)

# 1. Fájlok elérési útja
projekt_mappa = Path(__file__).parent
excel_fajl = projekt_mappa / "data" / "ugyek_adatok.xlsx"
eredmeny_mappa = projekt_mappa / "eredmenyek"
eredmeny_mappa.mkdir(exist_ok=True)

# 2. Adatok beolvasása
df = pd.read_excel(excel_fajl, sheet_name="Ugyek")

# 3. Bemeneti változók és célváltozó
X = df.drop(columns=[
    "Ugy_azonosito",
    "Hatarido_tullepes",
    "Hataridoig_hatralevo_napok"
])

y = df["Hatarido_tullepes"].map({
    "Nem": 0,
    "Igen": 1
})

# 4. Numerikus és kategóriaváltozók
numerikus_oszlopok = [
    "Hianypotlasok_szama",
    "Ugyintezesi_napok",
    "Ugyfelmegkeresesek_szama"
]

kategorikus_oszlopok = [
    "Ugytipus",
    "Beerkezes_modja",
    "Dokumentum_hianyos",
    "Korabbi_hasonlo_ugy_kesett"
]

# 5. Adatok előkészítése
elo_feldolgozo = ColumnTransformer(
    transformers=[
        ("numerikus", StandardScaler(), numerikus_oszlopok),
        ("kategorikus",
         OneHotEncoder(handle_unknown="ignore"),
         kategorikus_oszlopok)
    ]
)

# 6. Tanító- és tesztadatok szétválasztása
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("Tanítóadatok:", len(X_train))
print("Tesztadatok:", len(X_test))

# 7. Gépi tanulási modell létrehozása
modell = Pipeline([
    ("elokeszites", elo_feldolgozo),
    ("tanitas", LogisticRegression(
        class_weight="balanced",
        max_iter=1000,
        random_state=42
    ))
])

# 8. Modell tanítása
modell.fit(X_train, y_train)

print("\nA modell tanítása befejeződött!")

# 9. Előrejelzés
y_pred = modell.predict(X_test)
y_prob = modell.predict_proba(X_test)[:, 1]

# 10. Modellértékelés
print("\nMODELLÉRTÉKELÉS")
print("-" * 40)

print("Pontosság:",
      round(accuracy_score(y_test, y_pred), 3))

print("Recall:",
      round(recall_score(y_test, y_pred), 3))

print("Precision:",
      round(precision_score(y_test, y_pred), 3))

print("F1-score:",
      round(f1_score(y_test, y_pred), 3))

print("ROC-AUC:",
      round(roc_auc_score(y_test, y_prob), 3))

print("\nOsztályozási jelentés:")
print(classification_report(
    y_test,
    y_pred,
    target_names=["Nem késedelmes", "Késedelmes"],
    zero_division=0
))

# 11. Konfúziós mátrix
print("Konfúziós mátrix:")
print(confusion_matrix(y_test, y_pred))

# 12. ROC-görbe
RocCurveDisplay.from_predictions(y_test, y_prob)
plt.title("ROC-görbe - Késedelmi kockázat")
plt.tight_layout()
plt.savefig(eredmeny_mappa / "roc_gorbe.png")
plt.close()

# 13. Tesztadatok előrejelzéseinek mentése
eredmenyek = X_test.copy()
eredmenyek["Tenyleges_ertek"] = y_test
eredmenyek["Elorejelzes"] = y_pred
eredmenyek["Keses_valoszinusege"] = y_prob.round(4)

eredmenyek.to_excel(
    eredmeny_mappa / "modell_eredmenyek.xlsx",
    index=False
)

# 14. Modell mentése
joblib.dump(
    modell,
    projekt_mappa / "ugy_kockazati_modell.pkl"
)

print("\nA modell és az eredmények mentése kész!")
print("Elmentett modell: ugy_kockazati_modell.pkl")
print("Elmentett ROC-görbe: roc_gorbe.png")
print("Elmentett eredmények: modell_eredmenyek.xlsx")
