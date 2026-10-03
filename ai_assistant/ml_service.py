import joblib
from pathlib import Path
MODEL_PATH = (
    Path(__file__).resolve().parent.parent
    / "ml_model"
    / "saved_model"
    / "ayusetu_symptom_specialization_model_v5.pkl"
)
_model = None
def load_model():
    global _model
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    return _model
def predict_specialization(symptoms):
    model = load_model()
    probabilities = model.predict_proba([symptoms])[0]
    prediction_index = probabilities.argmax()
    specialization = model.classes_[prediction_index]
    confidence = float(
        probabilities[prediction_index]
    )
    return {
        "specialization": specialization,
        "confidence": confidence,
    }