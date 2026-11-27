# ==============================================================================
# MODULE 4: SESSION CHARGE & BILLING CALCULATOR
# ==============================================================================

from utils import find_game_by_id, find_booking_by_id


def calculate_session_charge(group_size, hours, game_hourly_rate):
    """
    Calculates total booking cost:
    - Table cover: ₹50 per person per hour
    - Game rental: game_hourly_rate per hour
    - Discount: 10% off total for marathon sessions (4 hours or more)
    """
    cover_charge = group_size * 50.0 * hours
    game_charge = game_hourly_rate * hours
    subtotal = cover_charge + game_charge

    if hours >= 4.0:
        subtotal *= 0.90  # 10% long-session discount

    return round(subtotal, 2)


def print_receipt(booking, games_list):
    """Prints a detailed itemized receipt for a single booking."""
    game = find_game_by_id(games_list, booking["game_id"])
    game_title = game["title"] if game else "Unknown Game"
    game_rate = game["hourly_rate"] if game else 0.0

    cover_cost = booking["group_size"] * 50.0 * booking["hours"]
    game_cost = game_rate * booking["hours"]
    raw_subtotal = cover_cost + game_cost
    discount = raw_subtotal - booking["total_charge"] if booking["status"] != "Cancelled" else 0.0

    print("\n==========================================")
    print("         BOARD GAME CAFÉ RECEIPT")
    print("==========================================")
    print(f"Booking ID    : {booking['booking_id']}")
    print(f"Customer      : {booking['customer_name']}")
    print(f"Status        : {booking['status']}")
    print(f"Table / Group : {booking['table_id']} ({booking['group_size']} players)")
    print(f"Game Rented   : {game_title} ({booking['game_id']})")
    print(f"Duration      : {booking['hours']} hrs")
    print("-" * 42)
    print(f"Table Cover (₹50 x {booking['group_size']} x {booking['hours']}h) : ₹{cover_cost:.2f}")
    print(f"Game Rental (₹{game_rate:.0f} x {booking['hours']}h)    : ₹{game_cost:.2f}")
    if discount > 0:
        print(f"4+ Hr Marathon Discount (10%)  : -₹{discount:.2f}")
    print("-" * 42)
    print(f"TOTAL AMOUNT                   : ₹{booking['total_charge']:.2f}")
    print("==========================================")


def view_billing_and_receipts(bookings_list, games_list):
    """Displays all bookings, revenue totals, and lets user print a receipt."""
    if not bookings_list:
        print("\nNo bookings recorded yet.")
        return

    print("\n--- ALL BOOKINGS & REVENUE SUMMARY ---")
    print(f"{'ID':<6} {'Customer':<18} {'Table':<6} {'Game':<6} {'Hrs':<5} {'Charge':<10} {'Status':<10}")
    print("-" * 68)

    completed_revenue = 0.0
    active_revenue = 0.0

    for b in bookings_list:
        print(f"{b['booking_id']:<6} {b['customer_name']:<18} {b['table_id']:<6} {b['game_id']:<6} {b['hours']:<5.1f} ₹{b['total_charge']:<9.2f} {b['status']:<10}")
        if b["status"] == "Completed":
            completed_revenue += b["total_charge"]
        elif b["status"] == "Active":
            active_revenue += b["total_charge"]

    print("-" * 68)
    print(f"Collected Revenue (Completed) : ₹{completed_revenue:.2f}")
    print(f"Pending Revenue (Active)      : ₹{active_revenue:.2f}")

    choice = input("\nEnter a Booking ID to view receipt (or press Enter to go back): ").strip()
    if choice:
        booking = find_booking_by_id(bookings_list, choice)
        if booking:
            print_receipt(booking, games_list)
        else:
            print("Booking ID not found.")