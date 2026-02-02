def calculate_score(data):
    score = 0

    # Education
    if data["education"]["found"]:
        score += 20

    # Skills
    tech_count = len(data["skills"]["technical"])
    score += min(tech_count * 5, 30)

    # Experience
    if data["experience"]["found"]:
        score += 20

    # Projects
    if data["projects"]["found"]:
        score += 15

    # Certifications
    score += min(data["certifications"]["count"] * 5, 15)

    return min(score, 100)
