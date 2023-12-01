class Item:

    def __init__(self, name, price, user_who_paid):
        self.price = price
        self.name = name
        self.users_who_use = []
        self.user_who_paid = user_who_paid

    def __repr__(self):
        return self.name
