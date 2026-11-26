from data import tables, games, bookings


def _is_table_occupied(table):
    if "occupied" in table:
        return bool(table["occupied"])
    if "available" in table:
        return not bool(table["available"])
    if "status" in table:
        return str(table["status"]).lower() in ["occupied", "booked", "reserved"]
    return False


def _get_game(choice):
    if isinstance(games, dict):
        if choice in games:
            game = games[choice]
            return game.get("name", str(choice)), game
        game_items = list(games.items())
        if isinstance(choice, int) and 1 <= choice <= len(game_items):
            key, game = game_items[choice - 1]
            return game.get("name", str(key)), game
        for key, game in game_items:
            if (
                str(key).lower() == str(choice).lower()
                or str(game.get("name", "")).lower() == str(choice).lower()
            ):
                return game.get("name", str(key)), game
    elif isinstance(games, list):
        if isinstance(choice, int) and 1 <= choice <= len(games):
            game = games[choice - 1]
            return game.get("name", f"Game {choice}"), game
        for game in games:
            if str(game.get("name", "")).lower() == str(choice).lower():
                return game.get("name"), game
    return None, None


def is_weekend(day):
    day = day.lower()
    if day == "saturday" or day == "sunday":
        return True
    else:
        return False


def show_menu(day):
    table_list = list(tables.values()) if isinstance(tables, dict) else tables
    total_seats = sum(t.get("seats", t.get("capacity", 0)) for t in table_list)
    occupied = sum(
        t.get("seats", t.get("capacity", 0))
        for t in table_list
        if _is_table_occupied(t)
    )
    free = total_seats - occupied

    print()
    print("Day:", day.capitalize())
    print("Seats:", occupied, "/", total_seats, "| Free:", free)
    print("Active Bookings:", len(bookings))

    game_items = (
        list(games.items())
        if isinstance(games, dict)
        else list(enumerate(games, start=1))
    )
    for i, (key, game) in enumerate(game_items, start=1):
        name = game.get("name", str(key))
        min_p = game.get("min_players", 2)
        max_p = game.get("max_players", 8)
        left = game.get("copies", game.get("available", 0))
        fee = game.get("fee", game.get("price", 0))
        player_range = f"{min_p}" if min_p == max_p else f"{min_p}-{max_p}"
        print(f"{i}. {name} ({player_range} players) | Left: {left} | Fee: Rs. {fee}")

    if is_weekend(day):
        print("Offer: 20% Weekend Offer (3 or more hours)")
    else:
        print("Offer: No Offer (Weekends 3+ hours only)")


def check_game(choice, players):
    name, game = _get_game(choice)
    if game is None:
        print("Wrong game choice.")
        return False

    stock_key = "copies" if "copies" in game else "available"
    if game.get(stock_key, 0) <= 0:
        print(name, "is not available.")
        return False

    min_p = game.get("min_players", 2)
    max_p = game.get("max_players", 8)
    if players < min_p or players > max_p:
        if min_p == max_p:
            print(f"{name} is only for {min_p} players.")
        else:
            print(f"{name} is for {min_p} to {max_p} players.")
        return False

    return True


def calculate_bill(players, hours, choice, day):
    name, game = _get_game(choice)
    if game is None:
        print("Wrong game choice.")
        return 0, 0, 0, 0

    seat_cost = 0
    for i in range(hours):
        seat_cost = seat_cost + (players * 100)

    game_fee = game.get("fee", game.get("price", 0))
    total = seat_cost + game_fee

    if is_weekend(day) and hours >= 3:
        discount = total * 0.20
    else:
        discount = 0

    final_amount = total - discount
    return seat_cost, game_fee, discount, final_amount


def create_booking(table_id, choice, players, hours, day):
    if not check_game(choice, players):
        return None

    name, game = _get_game(choice)
    seat_cost, game_fee, discount, final_amount = calculate_bill(
        players, hours, choice, day
    )

    stock_key = "copies" if "copies" in game else "available"
    if stock_key in game:
        game[stock_key] -= 1

    table = None
    if isinstance(tables, dict) and table_id in tables:
        table = tables[table_id]
    elif isinstance(tables, list):
        for t in tables:
            if t.get("id") == table_id or t.get("table_id") == table_id:
                table = t
                break

    if table is not None:
        if "occupied" in table:
            table["occupied"] = True
        elif "available" in table:
            table["available"] = False
        elif "status" in table:
            table["status"] = "occupied"

    booking = {
        "booking_id": len(bookings) + 1,
        "table_id": table_id,
        "game": name,
        "players": players,
        "hours": hours,
        "day": day.capitalize(),
        "seat_cost": round(seat_cost, 2),
        "game_fee": round(game_fee, 2),
        "discount": round(discount, 2),
        "final_amount": round(final_amount, 2),
    }

    if isinstance(bookings, list):
        bookings.append(booking)
    elif isinstance(bookings, dict):
        bookings[booking["booking_id"]] = booking

    return booking
