class Item:

    def __init__(self, name, price, user_who_paid):
        self.name = name
        self.price = price
        self.users_who_use = {}
        self.user_who_paid = user_who_paid
        self.paid = False

    def __repr__(self) -> str:
        return self.name

    def get_price(self):
        return self.price
    # this function adds a list of users to the item, with their boolean value in the dictionary corresponding to whether they have resolved the amount owed
    def add_users(self, users):
        for user in users:
            self.users_who_use[user] = False

    # toString
    def __str__(self) -> str:
        return f"Name: {self.name} Price: {self.price} User who paid: {self.user_who_paid.get_name()} Paid?: {self.paid}"