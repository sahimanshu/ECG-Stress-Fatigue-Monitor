def get_stress_level(stress_score):



    if stress_score < 0:
        raise ValueError("Stress score cannot be negative")


    if stress_score <= 30:
        return "Low"


    elif stress_score <= 70:
        return "Moderate"


    elif stress_score <= 100:
        return "High"


    else:
        return "High"