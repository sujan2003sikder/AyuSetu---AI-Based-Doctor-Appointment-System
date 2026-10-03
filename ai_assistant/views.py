from django.shortcuts import render
from doctors.models import DoctorProfile
from .ml_service import predict_specialization
from .guidance import get_guidance
EMERGENCY_KEYWORDS = [
    "severe chest pain",
    "crushing chest pain",
    "difficulty breathing",
    "severe difficulty breathing",
    "loss of consciousness",
    "unconscious",
    "stroke",
    "face drooping",
    "slurred speech",
    "sudden paralysis",
    "heavy bleeding",
    "blue lips",
    "blue or grey lips",
]
def symptom_checker(request):
    symptoms = ""
    recommended_specialization = None
    recommended_doctors = []
    recommendation_score = 0
    confidence_level = None
    emergency_message = None
    emergency_warning = False
    guidance = None
    low_confidence_warning = False
    if request.method == "POST":
        symptoms = request.POST.get(
            "symptoms",
            ""
        ).strip()
        if symptoms:
            if len(symptoms.split()) < 4:
                return render(
            request,
            "ai_assistant/symptom_checker.html",
            {
                "symptoms": symptoms,
                "input_warning": True,
            }
        )
            symptoms_lower = symptoms.lower()
            emergency_warning = any(
                keyword in symptoms_lower
                for keyword in EMERGENCY_KEYWORDS
            )
            if emergency_warning:
             emergency_message = (
        "Your symptoms may require urgent medical attention. "
        "Please seek immediate medical care or contact your "
        "local emergency service. The AI recommendation below "
        "is not a diagnosis."
    )
            result = predict_specialization(
                symptoms
            )
            predicted_specialization = (
                result["specialization"]
            )
            confidence = result["confidence"]
            recommended_specialization = (
                predicted_specialization
            )
            recommendation_score = round(
                confidence * 100
            )
            if confidence >= 0.60:
                confidence_level = "High"
            elif confidence >= 0.35:
                confidence_level = "Moderate"
            else:
                confidence_level = "Low"
                low_confidence_warning = True
            guidance = get_guidance(
                predicted_specialization
            )
            recommended_doctors = (
                DoctorProfile.objects
                .filter(
                    specialization__name__iexact=(
                        predicted_specialization
                    ),
                    verification_status="approved"
                )
                .select_related(
                    "user",
                    "specialization"
                )[:6]
            )
    return render(
        request,
        "ai_assistant/symptom_checker.html",
        {
    "symptoms": symptoms,
    "recommended_specialization": recommended_specialization,
    "recommended_doctors": recommended_doctors,
    "recommendation_score": recommendation_score,
    "confidence_level": confidence_level,
    "emergency_warning": emergency_warning,
    "emergency_message": emergency_message,
    "low_confidence_warning": low_confidence_warning,
    "guidance": guidance,
}
    )