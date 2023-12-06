import ledger
import item
from value import Value

class User:
    # constructor
    def __init__(self, username, balance, totals=None):
        self.username = username
        self.balance = balance
        self.totals = totals

    def get_name(self):
        return self.username

    # this method transfers the amount to the balance of user_being_paid
    def pay_user(self, amount, user_being_paid):
        if self.balance > amount:
            print(f"{self} (Balance: {self.balance}) is paying {amount} to {user_being_paid} (Balance: {user_being_paid.balance})")
            self.balance -= amount
            print(f"{self}'s new balance: {self.balance}")
            user_being_paid.balance += amount
            print(f"{user_being_paid}'s new balance: {user_being_paid.balance}")
        else:
            print("You do not have enough balance to transfer that amount")

    # this function takes in a ledger and calculates what everybody owes this user
    def calculate_totals(self, ldger):
        # set the dictionary to empty if none (None is its default declaration in the class)
        if self.totals is None:
            self.totals = {}

        # iterate through the items in the ledger's item list
        for itm in ldger.item_list:
            # if the user didn't pay for that item, continue
            if self != itm.user_who_paid:
                continue
            # calculate the length of users who use the item.
            length = len(itm.users_who_use)
            # if the user paid for that item, iterate through the people who use that item
            for person in itm.users_who_use:
                # if we're at the person who paid, continue, since they've already paid their share
                if person == self:
                    continue
                if person.username in self.totals:
                    self.totals[person.username] += itm.price / length
                else:
                    self.totals[person.username] = itm.price / length
        return_string = f"{self}'s owed by: " + str(self.totals)
        return return_string
    
    def pay_all_owed(self, user_being_paid, ldger):
        payment = ldger.calculate_amount_owed(self, user_being_paid)
        if payment > Value(0):
            # make the payment
            self.pay_user(payment, user_being_paid)

            # mark the individual amounts owed as having being paid
            for item in ldger.item_list:
                if item.user_who_paid == user_being_paid and self in item.users_who_use:
                    item.users_who_use[self] = True
            
            return payment
        return -1
    
    def __str__(self):
        return f"Username: {self.username} Balance: {self.balance} Totals: {self.totals}"