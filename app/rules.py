def calculate_risk(age: int, smoker: str, annual_income: float, coverage_amount: float):
    score = 0
    flags = []

    if age > 50:
        score += 20
        flags.append("Age over 50")

    if smoker.lower() == "yes":
        score += 30
        flags.append("Smoker")

    if coverage_amount > 500000:
        score += 25
        flags.append("High coverage amount")

    if annual_income < 30000:
        score += 15
        flags.append("Low income")

    if score >= 60:
        decision = "Declined"
    elif score >= 30:
        decision = "Manual Review"
    else:
        decision = "Approved"

    return score, decision, flags
