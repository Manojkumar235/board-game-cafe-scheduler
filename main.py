# ==============================================================================
# MAIN ENTRY POINT — BOARD GAME CAFÉ SCHEDULER
# ==============================================================================

from data import tables, games, bookings, view_all_tables, view_all_games
from booking import create_booking
from manage import manage_booking
from billing import view_billing_and_receipts
from utils import get_valid_int


def main_menu():
    while True:
        print("\n==========================================")
        print("      BOARD GAME CAFÉ SCHEDULER")
        print("==========================================")
        print("1. View Tables & Available Board Games")
        print("2. Create New Reservation")
        print("3. Modify / Swap Game / Checkout / Cancel")
        print("4. View Receipts & Revenue Summary")
        print("5. Exit")
        print("==========================================")

        choice = get_valid_int("Select an option (1-5): ", 1, 5)

        if choice == 1:
            view_all_tables(tables)
            view_all_games(games)
        elif choice == 2:
            create_booking(tables, games, bookings)
        elif choice == 3:
            manage_booking(tables, games, bookings)
        elif choice == 4:
            view_billing_and_receipts(bookings, games)
        elif choice == 5:
            print("Closing Board Game Café Scheduler. Goodbye!")
            break


if __name__ == "__main__":
    main_menu()