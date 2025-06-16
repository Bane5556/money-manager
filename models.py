class Transaction:
    def __init__(self, date, t_type, category, amount, person='', notes=''):
        self.date = date
        self.type = t_type
        self.category = category
        self.amount = amount
        self.person = person
        self.notes = notes
