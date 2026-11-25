import copy
import data
import billing
import booking
import manage
import utils


def run_data_edge_tests():
    assert data.filter_tables_by_group_size(data.tables, 0) == []
    assert data.filter_tables_by_group_size(data.tables, -1) == []
    assert data.filter_tables_by_group_size(data.tables, 20) == []
    assert len(data.filter_tables_by_group_size(data.tables, 4)) == 3
    assert data.filter_games_by_group_size(data.games, 0) == []
    assert data.filter_games_by_group_size(data.games, 15) == []
    assert len(data.filter_games_by_group_size(data.games, 4)) == 7


def run_billing_tests():
    catan = data.find_game_by_id(data.games, "G1")
    standard_total = billing.calculate_session_charge(4, 3.0, catan["hourly_rate"])
    assert standard_total == 1050.0
    marathon_total = billing.calculate_session_charge(4, 4.0, catan["hourly_rate"])
    assert marathon_total == 1260.0


def run_lifecycle_tests():
    test_tables = copy.deepcopy(data.tables)
    test_games = copy.deepcopy(data.games)
    test_bookings = copy.deepcopy(data.bookings)

    t3 = data.find_table_by_id(test_tables, "T3")
    g2 = data.find_game_by_id(test_games, "G2")
    assert t3["is_available"] is True
    assert g2["available_copies"] == 2

    t3["is_available"] = False
    g2["available_copies"] -= 1
    new_booking = {
        "booking_id": "B104",
        "customer_name": "Test Guest",
        "group_size": 4,
        "table_id": "T3",
        "game_id": "G2",
        "hours": 4.0,
        "total_charge": billing.calculate_session_charge(4, 4.0, g2["hourly_rate"]),
        "status": "Active"
    }
    test_bookings.append(new_booking)

    assert new_booking["total_charge"] == 1152.0
    assert t3["is_available"] is False
    assert g2["available_copies"] == 1

    t3["is_available"] = True
    g2["available_copies"] += 1
    new_booking["status"] = "Completed"

    assert t3["is_available"] is True
    assert g2["available_copies"] == 2


if __name__ == "__main__":
    run_data_edge_tests()
    run_billing_tests()
    run_lifecycle_tests()
    print("All procedural integration checks passed cleanly.")