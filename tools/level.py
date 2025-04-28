# tools/level.py

def calculate_xp_gain(difficulty: str = "normal") -> int:
    base_xp = 10
    difficulty_multiplier = {
        "easy": 0.8,
        "normal": 1.0,
        "hard": 1.5,
        "extreme": 2.0
    }
    return int(base_xp * difficulty_multiplier.get(difficulty, 1.0))


def should_level_up(current_xp: int, current_level: int) -> bool:
    return current_xp >= current_level * 100


def apply_xp_and_level(user, gained_xp: int):
    user.current_xp += gained_xp
    while should_level_up(user.current_xp, user.level):
        user.current_xp -= user.level * 100
        user.level += 1