SPECIALIZATION_GUIDANCE = {

    "Cardiology": {
        "do": [
            "Rest and avoid strenuous physical activity if symptoms are occurring.",
            "Keep track of when the symptoms occur and what you were doing at the time.",
            "Stay hydrated unless a healthcare professional has advised you to restrict fluids.",
        ],
        "avoid": [
            "Avoid strenuous exercise when experiencing chest discomfort or unusual breathlessness.",
            "Avoid smoking and tobacco products.",
            "Avoid ignoring persistent or worsening chest symptoms.",
        ],
        "seek": "Severe or persistent chest pain, severe breathing difficulty, fainting, or symptoms that may indicate an emergency require immediate medical attention."
    },

    "Dermatology": {
        "do": [
            "Keep the affected skin clean and gently moisturized.",
            "Note any new products, foods, medicines, or environmental exposures that preceded the symptoms.",
            "Use gentle, fragrance-free skincare products.",
        ],
        "avoid": [
            "Avoid scratching irritated skin.",
            "Avoid applying unknown creams or strong chemicals without professional advice.",
            "Avoid sharing personal towels or other items when a contagious skin condition is possible.",
        ],
        "seek": "Seek medical advice if the rash is spreading, painful, infected-looking, persistent, or associated with significant swelling or breathing difficulty."
    },

    "ENT": {
        "do": [
            "Stay hydrated and rest adequately.",
            "Use warm fluids if they are comfortable for you.",
            "Keep track of persistent throat, ear, or nasal symptoms.",
        ],
        "avoid": [
            "Avoid smoking and exposure to smoke.",
            "Avoid unnecessarily irritating the throat.",
            "Avoid self-medicating with antibiotics without professional advice.",
        ],
        "seek": "Seek medical care for severe difficulty breathing, inability to swallow, severe ear pain, or persistent symptoms."
    },

    "Gastroenterology": {
        "do": [
            "Eat smaller meals and observe which foods worsen your symptoms.",
            "Stay adequately hydrated.",
            "Keep a record of recurring stomach symptoms and possible food triggers.",
        ],
        "avoid": [
            "Avoid foods that consistently trigger your symptoms.",
            "Avoid lying down immediately after a large meal.",
            "Avoid excessive alcohol and smoking.",
        ],
        "seek": "Seek medical advice for persistent abdominal pain, repeated vomiting, blood in stool or vomit, unexplained weight loss, or worsening symptoms."
    },

    "General Medicine": {
        "do": [
            "Get adequate rest and maintain hydration.",
            "Monitor your symptoms and temperature when appropriate.",
            "Maintain regular meals and a balanced diet if you are able to eat normally.",
        ],
        "avoid": [
            "Avoid strenuous activity when feeling significantly weak or unwell.",
            "Avoid taking prescription medicines without professional guidance.",
            "Avoid ignoring persistent or worsening symptoms.",
        ],
        "seek": "Seek medical attention if fever or weakness is severe, persistent, worsening, or accompanied by concerning symptoms."
    },

    "Gynecology": {
        "do": [
            "Keep track of your menstrual cycle and symptoms.",
            "Maintain hydration and adequate rest.",
            "Record unusual changes in bleeding, cycle timing, or pelvic symptoms.",
        ],
        "avoid": [
            "Avoid ignoring unusually heavy or persistent bleeding.",
            "Avoid taking medicines for recurring symptoms without professional advice.",
            "Avoid delaying medical evaluation for persistent pelvic pain.",
        ],
        "seek": "Seek medical care for severe pelvic pain, unusually heavy bleeding, fainting, or other concerning symptoms."
    },

    "Neurology": {
        "do": [
            "Rest in a safe environment if dizziness or headache is present.",
            "Stay hydrated and keep track of symptom timing and triggers.",
            "Avoid activities that could cause injury if you are experiencing significant dizziness or balance problems.",
        ],
        "avoid": [
            "Avoid driving or operating machinery during significant dizziness or impaired coordination.",
            "Avoid ignoring new or rapidly worsening neurological symptoms.",
            "Avoid self-diagnosing persistent neurological symptoms.",
        ],
        "seek": "Sudden weakness, facial drooping, speech difficulty, loss of consciousness, severe sudden headache, or other sudden neurological changes require immediate medical attention."
    },

    "Ophthalmology": {
        "do": [
            "Rest your eyes when experiencing eye strain.",
            "Keep your hands clean before touching the area around your eyes.",
            "Keep track of changes in vision or eye discomfort.",
        ],
        "avoid": [
            "Avoid rubbing irritated eyes.",
            "Avoid using someone else's eye drops.",
            "Avoid ignoring sudden changes in vision.",
        ],
        "seek": "Seek urgent medical attention for sudden vision loss, severe eye pain, significant eye injury, or rapidly worsening vision."
    },

    "Orthopedics": {
        "do": [
            "Avoid activities that significantly worsen the pain.",
            "Allow adequate rest after activities that aggravate the symptoms.",
            "Keep track of movements or activities that trigger the pain.",
        ],
        "avoid": [
            "Avoid putting excessive strain on a painful joint.",
            "Avoid repeatedly performing movements that significantly increase pain.",
            "Avoid self-treating a serious injury without professional evaluation.",
        ],
        "seek": "Seek medical care after significant injury, severe swelling, inability to use a limb, or persistent or worsening pain."
    },

    "Pulmonology": {
        "do": [
            "Rest and avoid activities that significantly worsen breathing difficulty.",
            "Stay away from smoke and other respiratory irritants.",
            "Keep track of when coughing or breathing symptoms occur.",
        ],
        "avoid": [
            "Avoid smoking and second-hand smoke.",
            "Avoid known environmental triggers when possible.",
            "Do not ignore worsening breathing difficulty.",
        ],
        "seek": "Severe breathing difficulty, blue or grey lips, loss of consciousness, or rapidly worsening respiratory symptoms require immediate medical attention."
    },

    "Urology": {
        "do": [
            "Maintain adequate hydration unless a healthcare professional has advised fluid restriction.",
            "Keep track of urinary frequency, pain, and other changes.",
            "Seek professional evaluation if symptoms persist or recur.",
        ],
        "avoid": [
            "Avoid ignoring persistent pain or burning during urination.",
            "Avoid taking antibiotics without professional guidance.",
            "Avoid delaying evaluation for blood in urine or severe pain.",
        ],
        "seek": "Seek medical care for severe pain, blood in urine, inability to urinate, high fever, or worsening urinary symptoms."
    },
}


def get_guidance(specialization):
    return SPECIALIZATION_GUIDANCE.get(
        specialization,
        None
    )