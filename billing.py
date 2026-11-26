from data import tables, games, bookings


def _records(items):
    return list(items.values()) if isinstance(items, dict) else items


def _is_table_occupied(table):
    if "is_available" in table:
        return not bool(table["is_available"])
    if "occupied" in table:
        return bool(table["occupied"])
    if "available" in table:
        return not bool(table["available"])
    if "status" in table:
        return str(table["status"]).lower() in ["occupied", "booked", "reserved"]
    return False


def _get_game(choice):
    game_items = _records(games)
    if isinstance(choice, int) and 1 <= choice <= len(game_items):
        game = game_items[choice - 1]
        return game.get("title", game.get("name", f"Game {choice}")), game

    choice_text = str(choice).strip().lower()
    for index, game in enumerate(game_items, start=1):
        game_id = game.get("game_id", index)
        name = game.get("title", game.get("name", str(game_id)))
        if (
            str(game_id).strip().lower() == choice_text
            or str(name).strip().lower() == choice_text
        ):
            return name, game
    return None, None


def is_weekend(day):
    return str(day).strip().lower() in ["saturday", "sunday"]


def show_menu(day):
    table_items = _records(tables)
    total_seats = sum(t.get("capacity", t.get("seats", 0)) for t in table_items)
    occupied = sum(
        t.get("capacity", t.get("seats", 0))
        for t in table_items
        if _is_table_occupied(t)
    )
    active_bookings = sum(
        1
        for booking in _records(bookings)
        if str(booking.get("status", "Active")).lower() == "active"
    )

    print()
    print("Day:", str(day).capitalize())
    print("Seats:", occupied, "/", total_seats, "| Free:", total_seats - occupied)
    print("Active Bookings:", active_bookings)

    for index, game in enumerate(_records(games), start=1):
        game_id = game.get("game_id", index)
        name = game.get("title", game.get("name", str(game_id)))
        min_players = game.get("min_players", 2)
        max_players = game.get("max_players", 8)
        available = game.get(
            "available_copies", game.get("copies", game.get("available", 0))
        )
        total = game.get("total_copies", available)
        rate = game.get("hourly_rate", game.get("fee", game.get("price", 0)))
        player_range = (
            f"{min_players}"
            if min_players == max_players
            else f"{min_players}-{max_players}"
        )
        print(
            f"{index}. {name} ({player_range} players) | "
            f"Available: {available}/{total} | Rate: Rs. {rate}/hour"
        )

    if is_weekend(day):
        print("Offer: 20% Weekend Offer (3 or more hours)")
    else:
        print("Offer: No Offer (Weekends 3+ hours only)")


def check_game(choice, players):
    name, game = _get_game(choice)
    if game is None:
        print("Wrong game choice.")
        return False

    available = game.get(
        "available_copies", game.get("copies", game.get("available", 0))
    )
    if available <= 0:
        print(name, "is not available.")
        return False

    min_players = game.get("min_players", 2)
    max_players = game.get("max_players", 8)
    if players < min_players or players > max_players:
        if min_players == max_players:
            print(f"{name} is only for {min_players} players.")
        else:
            print(f"{name} is for {min_players} to {max_players} players.")
        return False

    return True


def calculate_bill(players, hours, choice, day):
    name, game = _get_game(choice)
    if game is None:
        print("Wrong game choice.")
        return 0, 0, 0, 0

    seat_cost = players * 100 * hours
    if "hourly_rate" in game:
        game_fee = game["hourly_rate"] * hours
    else:
        game_fee = game.get("fee", game.get("price", 0))

    total = seat_cost + game_fee
    discount = total * 0.20 if is_weekend(day) and hours >= 3 else 0
    return seat_cost, game_fee, discount, total - discount


def _find_table(table_id):
    if isinstance(tables, dict) and table_id in tables:
        return tables[table_id]
    for table in _records(tables):
        if (
            str(table.get("table_id", table.get("id", ""))).strip().lower()
            == str(table_id).strip().lower()
        ):
            return table
    return None


def _next_booking_id():
    highest = 0
    for booking in _records(bookings):
        booking_id = str(booking.get("booking_id", ""))
        if booking_id.startswith("B") and booking_id[1:].isdigit():
            highest = max(highest, int(booking_id[1:]))
    return f"B{highest + 1}"


def create_booking(table_id, choice, players, hours, day, customer_name="Walk-in"):
    if not check_game(choice, players):
        return None

    table = _find_table(table_id)
    if table is None:
        print("Wrong table choice.")
        return None
    if _is_table_occupied(table):
        print("Table", table_id, "is not available.")
        return None
    if table.get("capacity", table.get("seats", 0)) < players:
        print("Table", table_id, "does not have enough seats.")
        return None

    name, game = _get_game(choice)
    seat_cost, game_fee, discount, final_amount = calculate_bill(
        players, hours, choice, day
    )

    stock_key = (
        "available_copies"
        if "available_copies" in game
        else "copies"
        if "copies" in game
        else "available"
    )
    game[stock_key] -= 1
    if "is_available" in table:
        table["is_available"] = False
    elif "occupied" in table:
        table["occupied"] = True
    elif "available" in table:
        table["available"] = False
    elif "status" in table:
        table["status"] = "occupied"

    booking = {
        "booking_id": _next_booking_id(),
        "customer_name": customer_name,
        "group_size": players,
        "table_id": table.get("table_id", table_id),
        "game_id": game.get("game_id", name),
        "hours": hours,
        "total_charge": round(final_amount, 2),
        "status": "Active",
    }

    if isinstance(bookings, list):
        bookings.append(booking)
    else:
        bookings[booking["booking_id"]] = booking
    return booking
