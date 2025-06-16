from db import connect_db
class Transaction:
    def __init__(self, date, t_type, category, amount, person='', notes=''):
        self.date = date
        self.type = t_type
        self.category = category
        self.amount = amount
        self.person = person
        self.notes = notes
def add_transaction(tx):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO transactions (date, type, category, amount, person, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (tx.date, tx.type, tx.category, tx.amount, tx.person, tx.notes))
        conn.commit()