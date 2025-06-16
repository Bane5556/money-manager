from db import init_db, connect_db
from models import Transaction
from utils import export_to_csv
from utils import show_category_pie_chart
from models import add_transaction




def view_transactions():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transactions ORDER BY date DESC")
        for row in cursor.fetchall():
            print(row)

def run_cli():
    init_db()
    print("💰 Money Manager CLI (macOS)")

    while True:
        print("\n1. Add  2. View  3. Exit  4. Export CSV  5. Show Pie Chart")
        choice = input("Choose: ")

        if choice == '1':
            date = input("Date (YYYY-MM-DD): ")
            t_type = input("Type (Spend, Borrow, Lend): ")
            category = input("Category (e.g. Food, Travel): ")
            amount = float(input("Amount: "))
            person = input("Person (optional): ")
            notes = input("Notes (optional): ")

            tx = Transaction(date, t_type, category, amount, person, notes)
            add_transaction(tx)
            print("✅ Transaction added.")
        elif choice == '2':
            view_transactions()
        elif choice == '3':
            print("👋 Exiting.")
        elif choice == '4':
            export_to_csv()
        elif choice == '5':
             show_category_pie_chart()
        else:
            print("❌ Invalid option.")

if __name__ == "__main__":
    run_cli()
