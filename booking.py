# ==============================================================================
# MODULE 2: CORE OPERATION 1 — CREATE RESERVATION
# ==============================================================================

from datetime import datetime
from data import filter_tables_by_group_size, filter_games_by_group_size
from billing import calculate_session_charge, print_receipt
from utils import (
    get_valid_customer_name,
    get_valid_int,
    get_valid_duration,
    get_non_empty_string,
    generate_next_booking_id,
)


def create_booking(tables_list: list, games_list: list, bookings_list: list) -> dict | None:
    # 1. Validate container integrity before collecting input
    if not all(isinstance(lst, list) for lst in (tables_list, games_list, bookings_list)):
        raise TypeError("tables_list, games_list, and bookings_list must all be lists.")

    print("\n--- CREATE NEW RESERVATION ---")
    customer_name = get_valid_customer_name("Customer Name: ")
    group_size = get_valid_int("Group Size (1-8 players): ", 1, 8)
    hours = get_valid_duration("Session Duration in hours (0.5 - 12.0): ", 0.5, 12.0)

    # 2. Filter suitable & genuinely available resources
    suitable_tables = [
        t for t in filter_tables_by_group_size(tables_list, group_size)
        if t.get("is_available", True) and t.get("capacity", 0) >= group_size
    ]
    if not suitable_tables:
        print(f"\nSorry, no available tables can accommodate a group of {group_size}.")
        return None

    suitable_games = [
        g for g in filter_games_by_group_size(games_list, group_size)
        if g.get("available_copies", 0) > 0
        and g.get("min_players", 1) <= group_size <= g.get("max_players", 8)
    ]
    if not suitable_games:
        print(f"\nSorry, no available board games are suited for {group_size} players.")
        return None

    # 3. Table selection with normalized lookup
    table_lookup = {str(t["table_id"]).strip().upper(): t for t in suitable_tables}
    print("\nAvailable Tables for your group:")
    for t in suitable_tables:
        print(f"  - {t['table_id']} (Seats up to {t['capacity']})")

    selected_table = None
    while selected_table is None:
        tid = get_non_empty_string("Enter Table ID to reserve: ").strip().upper()
        selected_table = table_lookup.get(tid)
        if selected_table is None:
            print("Invalid selection. Choose one of the listed Table IDs.")

    # 4. Game selection with normalized lookup
    game_lookup = {str(g["game_id"]).strip().upper(): g for g in suitable_games}
    print("\nAvailable Games suited for your group:")
    for g in suitable_games:
        print(
            f"  - {g['game_id']}: {g['title']} "
            f"({g['min_players']}-{g['max_players']} players | "
            f"₹{g['hourly_rate']:.0f}/hr | {g['available_copies']} left)"
        )

    selected_game = None
    while selected_game is None:
        gid = get_non_empty_string("Enter Game ID to reserve: ").strip().upper()
        selected_game = game_lookup.get(gid)
        if selected_game is None:
            print("Invalid selection. Choose one of the listed Game IDs.")

    # 5. Re-verify resource availability & commit atomically
    if not selected_table.get("is_available", True) or selected_game.get("available_copies", 0) < 1:
        print("\nResource availability changed before confirmation. Booking aborted.")
        return None

    total_charge = calculate_session_charge(group_size, hours, selected_game["hourly_rate"])
    booking_id = generate_next_booking_id(bookings_list)

    booking_record = {
        "booking_id": booking_id,
        "customer_name": customer_name,
        "group_size": group_size,
        "table_id": selected_table["table_id"],
        "game_id": selected_game["game_id"],
        "hours": hours,
        "total_charge": total_charge,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "status": "Active",
    }

    # Mutate state together so partial updates cannot occur
    selected_table["is_available"] = False
    selected_game["available_copies"] -= 1
    bookings_list.append(booking_record)

    print(f"\nReservation Confirmed! Booking ID: {booking_id} | Total: ₹{total_charge:.2f}")
    print_receipt(booking_record, games_list)
    return booking_record
