import ledger
import item


class User:
    def __init__(self, username, balance, totals=None):
        self.username = username
        self.balance = balance
        self.totals = totals

    def __repr__(self):
        return self.username

    # this method transfers the amount to the balance of user_being_paid
    def pay_user(self, amount, user_being_paid):
        if self.balance > amount:
            print(f"Noah (Balance: ${self.balance}) is paying ${amount} to Marcos (Balance: ${user_being_paid.balance})")
            self.balance -= amount
            print(f"{self}'s new balance: ${self.balance}")
            user_being_paid.balance += amount
            print(f"{user_being_paid}'s new balance: ${user_being_paid.balance}")
        else:
            print("You do not have enough balance to transfer that amount")
