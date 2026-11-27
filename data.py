# ==============================================================================
# MODULE 1: SHARED DATA STRUCTURES, INVENTORY & FILTERING
# ==============================================================================

tables = [
    {"table_id": "T1", "capacity": 2, "is_available": True},
    {"table_id": "T2", "capacity": 2, "is_available": False},  # Occupied by B101
    {"table_id": "T3", "capacity": 4, "is_available": True},
    {"table_id": "T4", "capacity": 4, "is_available": True},
    {"table_id": "T5", "capacity": 6, "is_available": True},
    {"table_id": "T6", "capacity": 8, "is_available": True},
]

games = [
    {"game_id": "G1", "title": "Catan", "min_players": 3, "max_players": 4, "total_copies": 3, "available_copies": 3, "hourly_rate": 150.0},
    {"game_id": "G2", "title": "Ticket to Ride", "min_players": 2, "max_players": 5, "total_copies": 2, "available_copies": 2, "hourly_rate": 120.0},
    {"game_id": "G3", "title": "Codenames", "min_players": 4, "max_players": 8, "total_copies": 4, "available_copies": 4, "hourly_rate": 100.0},
    {"game_id": "G4", "title": "Azul", "min_players": 2, "max_players": 4, "total_copies": 2, "available_copies": 2, "hourly_rate": 120.0},
    {"game_id": "G5", "title": "Chess", "min_players": 2, "max_players": 2, "total_copies": 3, "available_copies": 2, "hourly_rate": 80.0},  # 1 copy in use by B101
    {"game_id": "G6", "title": "Dune: Imperium", "min_players": 1, "max_players": 4, "total_copies": 1, "available_copies": 1, "hourly_rate": 200.0},
]

bookings = [
    {
        "booking_id": "B101",
        "customer_name": "Rohan Sharma",
        "group_size": 2,
        "table_id": "T2",
        "game_id": "G5",
        "hours": 2.0,
        "total_charge": 360.0,
        "status": "Active"  # Valid statuses: "Active", "Completed", "Cancelled"
    }
]


def view_all_tables(tables_list):
    print("\n--- CAFÉ TABLES ---")
    print(f"{'ID':<6} {'Capacity':<10} {'Status':<12}")
    print("-" * 30)
    for t in tables_list:
        status = "Available" if t["is_available"] else "Occupied"
        print(f"{t['table_id']:<6} {t['capacity']:<10} {status:<12}")


def view_all_games(games_list):
    print("\n--- BOARD GAME LIBRARY ---")
    print(f"{'ID':<6} {'Title':<20} {'Players':<10} {'Available':<12} {'Rate/Hr':<10}")
    print("-" * 62)
    for g in games_list:
        players = f"{g['min_players']}-{g['max_players']}"
        avail = f"{g['available_copies']}/{g['total_copies']}"
        print(f"{g['game_id']:<6} {g['title']:<20} {players:<10} {avail:<12} ₹{g['hourly_rate']:<9.2f}")


def filter_tables_by_group_size(tables_list, group_size):
    if group_size <= 0:
        return []
    matching = []
    for t in tables_list:
        if t["is_available"] and t["capacity"] >= group_size:
            matching.append(t)
    return matching


def filter_games_by_group_size(games_list, group_size):
    if group_size <= 0:
        return []
    matching = []
    for g in games_list:
        if g["min_players"] <= group_size <= g["max_players"] and g["available_copies"] > 0:
            matching.append(g)
    return matching


def find_table_by_id(tables_list, table_id):
    target = table_id.strip().upper()
    for t in tables_list:
        if t["table_id"].upper() == target:
            return t
    return None


def find_game_by_id(games_list, game_id):
    target = game_id.strip().upper()
    for g in games_list:
        if g["game_id"].upper() == target:
            return g
    return None


def find_booking_by_id(bookings_list, booking_id):
    target = booking_id.strip().upper()
    for b in bookings_list:
        if b["booking_id"].upper() == target:
            return b
    return None


if __name__ == "__main__":
    view_all_tables(tables)
    view_all_games(games)
    assert filter_tables_by_group_size(tables, 0) == []
    assert filter_tables_by_group_size(tables, -2) == []
    assert filter_tables_by_group_size(tables, 12) == []
    assert filter_games_by_group_size(games, 0) == []
    assert filter_games_by_group_size(games, 10) == []
    assert find_table_by_id(tables, "t1")["capacity"] == 2
    assert find_game_by_id(games, "g1")["title"] == "Catan"
    assert find_booking_by_id(bookings, "b101")["customer_name"] == "Rohan Sharma"
    print("\nAll data.py edge-case checks passed.")
