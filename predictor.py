import random

def get_expected_run_rate(wickets, overs_played, current_rr):
    wickets_left = 10 - wickets

    # Partnerships
    if wickets <= 2:
        stability = 1.1   # strong start
    elif wickets <= 5:
        stability = 1.0   # normal
    else:
        stability = 0.85  # collapse risk

    # ⚔️ Aggression based on wickets LEFT
    if wickets_left >= 8:
        aggression = 1.4
    elif wickets_left >= 6:
        aggression = 1.25
    elif wickets_left >= 4:
        aggression = 1.1
    elif wickets_left >= 2:
        aggression = 0.9
    else:
        aggression = 0.7

    # ⏱️ Match Phase (IPL T20)
    if overs_played <= 6:
        phase = "powerplay"
        phase_boost = 1.25
    elif overs_played <= 15:
        phase = "middle"
        phase_boost = 1.0
    else:
        phase = "death"
        phase_boost = 1.5

    # 💥 Special Situations
    
    # Death over explosion (if wickets in hand)
    if phase == "death" and wickets_left >= 6:
        explosion = 1.2
    else:
        explosion = 1.0

    # Collapse risk (too many wickets lost early)
    if wickets >= 7 and overs_played < 15:
        collapse_penalty = 0.75
    else:
        collapse_penalty = 1.0

    # 🔢 Final Expected Run Rate
    expected_rr = (
        current_rr
        * stability
        * aggression
        * phase_boost
        * explosion
        * collapse_penalty
    )

    return expected_rr


def predict_score(current_score, overs_played, wickets, current_rr):
    overs_left = 20 - overs_played

    expected_rr = get_expected_run_rate(
        wickets,
        overs_played,
        current_rr
    )

    predicted = current_score + (expected_rr * overs_left)

    # 🎲 Smart Randomness (context-aware)
    if wickets >= 7:
        noise = random.uniform(0.85, 1.0)   # collapse risk
    elif overs_played >= 16:
        noise = random.uniform(1.0, 1.15)   # death over boost
    elif wickets <= 2:
        noise = random.uniform(1.0, 1.08)   # strong start
    else:
        noise = random.uniform(0.95, 1.05)  # normal

    predicted *= noise

    return int(predicted)