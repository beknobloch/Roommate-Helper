

class Ledger:
    def __init__(self, item_list):
        self.item_list = item_list

    def add_item(self, item):
        self.item_list.append(item)
