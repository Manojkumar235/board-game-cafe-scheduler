# ==============================================================================
# MODULE 5: INPUT VALIDATION & LOOKUP HELPERS
# ==============================================================================

import re


def get_valid_int(prompt, min_val=1, max_val=100):
    """Safely prompts the user for an integer within a range."""
    while True:
        raw = input(prompt).strip()
        if raw.isdigit():
            val = int(raw)
            if min_val <= val <= max_val:
                return val
        print(f"Invalid input. Enter a whole number between {min_val} and {max_val}.")


def get_valid_float(prompt, min_val=0.5, max_val=12.0):
    """Safely prompts the user for a positive float (e.g., hours)."""
    while True:
        raw = input(prompt).strip()
        try:
            val = float(raw)
            if min_val <= val <= max_val:
                return val
        except ValueError:
            pass
        print(f"Invalid input. Enter a number between {min_val} and {max_val}.")


def get_valid_duration(prompt: str, min_hrs: float = 0.5, max_hrs: float = 12.0) -> float:
    """Enforce half-hour increments to prevent floating-point billing anomalies."""
    while True:
        val = round(get_valid_float(prompt, min_hrs, max_hrs), 2)
        if (val * 2) % 1 == 0:
            return val
        print("Duration must be in 0.5-hour increments (e.g., 1.0, 1.5, 2.0).")


def get_non_empty_string(prompt):
    """Safely prompts the user for a non-empty string."""
    while True:
        val = input(prompt).strip()
        if len(val) > 0:
            return val
        print("Input cannot be empty. Please try again.")


def is_valid_customer_name(name: str) -> bool:
    """Ensure name is 2-60 chars, contains letters, and uses valid name characters."""
    cleaned = name.strip()
    if not (2 <= len(cleaned) <= 60):
        return False
    return bool(re.match(r"^(?=.*[A-Za-z])[A-Za-z\s\-'.]+$", cleaned))


def get_valid_customer_name(prompt: str) -> str:
    while True:
        raw = get_non_empty_string(prompt).strip()
        if is_valid_customer_name(raw):
            return re.sub(r"\s+", " ", raw)
        print("Invalid name. Use 2-60 letters (spaces, hyphens, and apostrophes allowed).")


def confirm_action(prompt: str) -> bool:
    """Require explicit y/n confirmation for irreversible state changes."""
    while True:
        ans = get_non_empty_string(f"{prompt} (y/n): ").strip().lower()
        if ans in ("y", "yes"):
            return True
        if ans in ("n", "no"):
            return False
        print("Please enter 'y' or 'n'.")


def generate_next_booking_id(bookings_list):
    """Generates sequential IDs like B102, B103..."""
    next_num = 101 + len(bookings_list)
    return f"B{next_num}"


def find_table_by_id(tables_list, table_id):
    if not table_id:
        return None
    for t in tables_list:
        if t["table_id"].upper() == table_id.upper():
            return t
    return None


def find_game_by_id(games_list, game_id):
    if not game_id:
        return None
    for g in games_list:
        if g["game_id"].upper() == game_id.upper():
            return g
    return None


def find_booking_by_id(bookings_list, booking_id):
    if not booking_id:
        return None
    for b in bookings_list:
        if b["booking_id"].upper() == booking_id.upper():
            return b
    return None