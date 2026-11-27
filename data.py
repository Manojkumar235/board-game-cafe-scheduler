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
    """Returns available tables large enough for the group."""
    matching = []
    for t in tables_list:
        if t["is_available"] and t["capacity"] >= group_size:
            matching.append(t)
    return matching


def filter_games_by_group_size(games_list, group_size):
    """Returns available games suited to the exact group size."""
    matching = []
    for g in games_list:
        if g["min_players"] <= group_size <= g["max_players"] and g["available_copies"] > 0:
            matching.append(g)
    return matching