import pandas as pd

import time
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.feature_selection import SelectFromModel
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score,
    f1_score
)

from lightgbm import LGBMClassifier

print("\ninciando modelo: ")


# data
df = pd.read_excel("csgo_round_snapshots.xlsx")
df = df.drop_duplicates()

x = df.drop(columns=["round_winner"])
y = df["round_winner"]

x_train, x_test, y_train, y_test = train_test_split(
    x, y,
    test_size=0.25,
    random_state=42,
    stratify=y
)


# preprocess
categorical_cols = x.select_dtypes(include=["object", "string"]).columns
numeric_cols = x.select_dtypes(exclude=["object", "string"]).columns

numeric_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median"))
])

categorical_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore"))
])

preprocess = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numeric_cols),
        ("cat", categorical_transformer, categorical_cols)
    ],
    remainder="drop",
    verbose_feature_names_out=False
)


# |
pipeline = Pipeline([
    ("preprocess", preprocess),

    ("feature_selection", SelectFromModel(
        RandomForestClassifier(
            n_estimators=100,
            random_state=1,
            n_jobs=-1
        ),
        threshold="median"
    )),

    ("model", LGBMClassifier(
        n_estimators=400,
        max_depth=8,
        learning_rate=0.08,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        n_jobs=-1,
        verbose=-1,
        force_row_wise=True
    ))
])


# train and prediction
pipeline.fit(x_train, y_train)
y_pred = pipeline.predict(x_test)


print("Acurácia:", round(accuracy_score(y_test, y_pred), 4))
print("F1-Score:", round(f1_score(y_test, y_pred, average="weighted"), 4))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

result = pd.DataFrame({
    "Real": y_test.reset_index(drop=True),
    "Previsto": y_pred
})

print("\nPrimeiras 20 previsões:")
print(result.head(20))


print("Precione Ctrl + C para sair.")
while True:
    time.sleep(3600)
