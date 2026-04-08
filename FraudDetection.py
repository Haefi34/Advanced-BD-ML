import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.metrics import confusion_matrix
import kagglehub
import os

import joblib

path = kagglehub.dataset_download("mlg-ulb/creditcardfraud")
csv_path = os.path.join(path, "creditcard.csv")

df = pd.read_csv(csv_path)
df = df.sort_values("Time").reset_index(drop=True)


#Analyse Daten
counts = df["Class"].value_counts()
print(counts)

X = df.drop("Class", axis=1)   # alle Spalten außer "Class"
y = df["Class"]                # Ziel: 0 = normal, 1 = Betrug

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,       # 20% Testdaten
    random_state=42,
    stratify=y           # für die unbalancierten Daten
)

model = LogisticRegression(
    max_iter=2000,
    solver="liblinear",# mehr Iterationen für Konvergenz
)

model.fit(X_train, y_train)

y_proba = model.predict_proba(X_test)[:, 1]

threshold = 0.9
y_pred = (y_proba >= threshold).astype(int)

print("Classification Report:")
print(classification_report(y_test, y_pred))

print(confusion_matrix(y_test, y_pred))


joblib.dump(model, "models/logistic_regression.joblib")