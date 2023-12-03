from value import Value

class Ledger:
    def __init__(self, item_list):
        self.item_list = item_list

    def add_item(self, item):
        self.item_list.append(item)

    # this function takes in two users, a payer and a receiver, and calculates the total that payer owes the receiver. A negative result means the receiver actually owes the payer.
    def calculate_amount_owed(self, payer, receiver):
        amount = Value(0)

        for item in self.item_list:
            item_share = item.price / len(item.users_who_use)
            if item.user_who_paid == receiver and payer in item.users_who_use and not item.users_who_use[payer]:
                amount += item_share
            elif item.user_who_paid == payer and receiver in item.users_who_use and not item.users_who_use[receiver]:
                amount -= item_share

        return amount