def classify_text_label(text: str, categories: dict, default_label: str = "unknown") -> dict:
    if not text or not categories:
        return {"label": default_label, "confidence": 0.0, "scores": {}}

    text_lower = text.lower()
    scores = {}

    for label, keywords in categories.items():
        score = 0
        for kw in keywords:
            if kw.lower() in text_lower:
                score += 1
        scores[label] = float(score)

    max_score = max(scores.values()) if scores else 0
    if max_score == 0:
        return {"label": default_label, "confidence": 0.0, "scores": scores}

    best_label = max(scores, key=scores.get)
    total_matches = sum(scores.values())
    confidence = round(best_label_score := scores[best_label] / (total_matches if total_matches > 0 else 1), 2)

    return {
        "label": best_label,
        "confidence": confidence,
        "scores": scores
    }
