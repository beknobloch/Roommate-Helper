class Item:

    def __init__(self, name, price, user_who_paid, paid=False):
        self.price = price
        self.name = name
        self.users_who_use = {}
        self.user_who_paid = user_who_paid

    def __repr__(self):
        return self.name

    # this function adds a list of users to the item, with their boolean value in the dictionary corresponding to whether they have resolved the amount owed
    def add_users(self, users):
        for user in users:
            self.users_who_use[user] = False