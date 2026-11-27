# ==============================================================================
# MODULE 3: CORE OPERATION 2 — MODIFY / CHECKOUT / CANCEL BOOKING
# ==============================================================================

from datetime import datetime
from data import filter_games_by_group_size
from billing import calculate_session_charge, print_receipt
from utils import (
    get_valid_int,
    get_valid_duration,
    get_non_empty_string,
    confirm_action,
    find_table_by_id,
    find_game_by_id,
    find_booking_by_id,
)


def release_booking_resources(booking: dict, tables_list: list, games_list: list) -> None:
    """Idempotently frees the table and returns the board game copy to stock."""
    if not isinstance(booking, dict):
        raise TypeError("booking must be a dictionary.")

    # Guard against double-releasing resources for the same booking
    if booking.get("resources_released", False):
        return

    table = find_table_by_id(tables_list, booking.get("table_id"))
    game = find_game_by_id(games_list, booking.get("game_id"))

    if table:
        table["is_available"] = True

    if game:
        max_copies = game.get("total_copies", game.get("available_copies", 0) + 1)
        if game.get("available_copies", 0) < max_copies:
            game["available_copies"] += 1

    booking["resources_released"] = True


def manage_booking(tables_list: list, games_list: list, bookings_list: list) -> None:
    if not all(isinstance(lst, list) for lst in (tables_list, games_list, bookings_list)):
        raise TypeError("tables_list, games_list, and bookings_list must all be lists.")

    print("\n--- MANAGE ACTIVE BOOKING ---")
    active_bookings = [
        b for b in bookings_list
        if isinstance(b, dict) and str(b.get("status", "")).strip().lower() == "active"
    ]

    if not active_bookings:
        print("There are currently no Active bookings.")
        return

    print("Active Bookings:")
    for b in active_bookings:
        print(
            f"  - {b['booking_id']} | {b['customer_name']} | "
            f"Table {b['table_id']} | Game {b['game_id']} | "
            f"{b['hours']} hrs | ₹{b['total_charge']:.2f}"
        )

    bid = get_non_empty_string("\nEnter Booking ID to manage: ").strip().upper()
    booking = find_booking_by_id(bookings_list, bid)

    if not booking:
        print("Booking ID not found.")
        return

    if str(booking.get("status", "")).strip().lower() != "active":
        print(f"Booking {booking['booking_id']} is already '{booking.get('status')}' and cannot be modified.")
        return

    print(f"\nManaging {booking['booking_id']} ({booking['customer_name']}):")
    print("1. Extend / Update Session Hours")
    print("2. Swap Board Game")
    print("3. Complete Session & Checkout (Release Table & Game)")
    print("4. Cancel Booking (Release Table & Game)")
    print("5. Back to Main Menu")

    action = get_valid_int("Choose an action (1-5): ", 1, 5)

    if action == 5:
        return

    elif action == 1:
        current_hours = float(booking["hours"])
        new_hours = get_valid_duration(
            f"Enter new total session hours (current: {current_hours} hrs, range 0.5 - 12.0): ",
            0.5,
            12.0,
        )
        if new_hours == current_hours:
            print("New duration is identical to current duration. No changes made.")
            return

        game = find_game_by_id(games_list, booking["game_id"])
        if not game:
            print("Error: Associated game record not found; cannot recalculate rate safely.")
            return

        booking["hours"] = new_hours
        booking["total_charge"] = round(
            calculate_session_charge(booking["group_size"], new_hours, game["hourly_rate"]),
            2,
        )
        booking["updated_at"] = datetime.now().isoformat(timespec="seconds")
        print(f"Updated {booking['booking_id']} to {new_hours} hrs. New Total: ₹{booking['total_charge']:.2f}")

    elif action == 2:
        current_gid = str(booking["game_id"]).strip().upper()
        suitable_games = [
            g for g in filter_games_by_group_size(games_list, booking["group_size"])
            if g.get("available_copies", 0) > 0
            and str(g.get("game_id", "")).strip().upper() != current_gid
        ]
        if not suitable_games:
            print("No other available games match this group size.")
            return

        game_lookup = {str(g["game_id"]).strip().upper(): g for g in suitable_games}
        print("\nAvailable Replacement Games:")
        for g in suitable_games:
            print(f"  - {g['game_id']}: {g['title']} (₹{g['hourly_rate']:.0f}/hr | {g['available_copies']} left)")

        new_gid = get_non_empty_string("Enter new Game ID: ").strip().upper()
        new_game = game_lookup.get(new_gid)

        if not new_game or new_game.get("available_copies", 0) < 1:
            print("Invalid or unavailable Game ID selected. Swap cancelled.")
            return

        old_game = find_game_by_id(games_list, booking["game_id"])

        # Atomic inventory & booking update
        if old_game:
            max_copies = old_game.get("total_copies", old_game.get("available_copies", 0) + 1)
            if old_game.get("available_copies", 0) < max_copies:
                old_game["available_copies"] += 1

        new_game["available_copies"] -= 1
        booking["game_id"] = new_game["game_id"]
        booking["total_charge"] = round(
            calculate_session_charge(booking["group_size"], booking["hours"], new_game["hourly_rate"]),
            2,
        )
        booking["updated_at"] = datetime.now().isoformat(timespec="seconds")
        print(f"Swapped game to {new_game['title']}. Updated Total: ₹{booking['total_charge']:.2f}")

    elif action == 3:
        if not confirm_action(f"Confirm checkout for {booking['booking_id']} (Total: ₹{booking['total_charge']:.2f})?"):
            print("Checkout aborted.")
            return

        booking["status"] = "Completed"
        booking["closed_at"] = datetime.now().isoformat(timespec="seconds")
        release_booking_resources(booking, tables_list, games_list)
        print(f"\nBooking {booking['booking_id']} checked out! Table {booking['table_id']} and Game {booking['game_id']} are now available.")
        print_receipt(booking, games_list)

    elif action == 4:
        if not confirm_action(f"Are you sure you want to cancel booking {booking['booking_id']}?"):
            print("Cancellation aborted.")
            return

        booking["status"] = "Cancelled"
        booking["total_charge"] = 0.0
        booking["closed_at"] = datetime.now().isoformat(timespec="seconds")
        release_booking_resources(booking, tables_list, games_list)
        print(f"\nBooking {booking['booking_id']} has been cancelled. Table {booking['table_id']} and Game {booking['game_id']} are now available.")