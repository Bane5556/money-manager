import csv
from db import connect_db
import matplotlib.pyplot as plt

def show_category_pie_chart():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT category, SUM(amount) FROM transactions GROUP BY category")
        data = cursor.fetchall()

    if not data:
        print("No data to display.")
        return

    labels = [row[0] for row in data]
    values = [row[1] for row in data]

    plt.figure(figsize=(6, 6))
    plt.pie(values, labels=labels, autopct='%1.1f%%')
    plt.title("Spending by Category")
    plt.show()


def export_to_csv(filename="transactions_export.csv"):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transactions")
        rows = cursor.fetchall()
        headers = [desc[0] for desc in cursor.description]

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(rows)

    print(f"✅ Exported to {filename}")
