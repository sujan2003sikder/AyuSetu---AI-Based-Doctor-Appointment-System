import pandas as pd
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report

DATASET_PATH = Path(
    "ml_model/dataset/ayusetu_symptom_specialization_v5_combined.csv"
)
MODEL_PATH = Path(
    "ml_model/saved_model/ayusetu_symptom_specialization_model_v5.pkl"
)
print("Loading AyuSetu V5 dataset...")

df = pd.read_csv(DATASET_PATH)
df = df.dropna(
    subset=["symptoms", "specialization"]
)
df["symptoms"] = (
    df["symptoms"]
    .astype(str)
    .str.strip()
)
df["specialization"] = (
    df["specialization"]
    .astype(str)
    .str.strip()
)
X = df["symptoms"]
y = df["specialization"]
print(f"Total samples: {len(df)}")
print(f"Total specializations: {y.nunique()}")
print("\nClass distribution:")
print(y.value_counts().sort_index())
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)
print("\nTraining AyuSetu V5 ML model...")
model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2),
            sublinear_tf=True,
            min_df=1
        )
    ),
    (
        "classifier",
        LogisticRegression(
            max_iter=3000,
            class_weight="balanced"
        )
    )
])


model.fit(
    X_train,
    y_train
)


print("Training completed.")


y_pred = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    y_pred
)


print(f"\nV5 Model accuracy: {accuracy * 100:.2f}%")


print("\nClassification report:")

print(
    classification_report(
        y_test,
        y_pred,
        zero_division=0
    )
)


MODEL_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)


joblib.dump(
    model,
    MODEL_PATH
)

print("\nV5 model saved successfully:")
print(MODEL_PATH)