import user
import ledger
import item
from value import Value

# ----------------------------- EXAMPLE -----------------------------


# this function takes in a ledger and a user and calculates what everybody owes that user
def calculate_totals(ldger, usr):
    # set the dictionary to empty if none (None is its default declaration in the class)
    if usr.totals is None:
        usr.totals = {}

    # iterate through the items in the ledger's item list
    for itm in ldger.item_list:
        # if the user didn't pay for that item, continue
        if usr != itm.user_who_paid:
            continue
        # calculate the length of users who use the item.
        # find the number of users the item
        length = len(itm.users_who_use)
        # if the user paid for that item, iterate through the people who use that item
        for person in itm.users_who_use:
            # if we're at the person who paid, continue, since they've already paid their share
            if person == usr:
                continue
            if person.username in usr.totals:
                usr.totals[person.username] += itm.price / length
            else:
                usr.totals[person.username] = itm.price / length
    return_string = f"{usr}'s owed by: " + str(usr.totals)
    return return_string


# make a Noah user with username and balance
Noah = user.User("Noah76", Value(50))

# make a Marcos user with username and balance
Marcos = user.User("Marcos50", Value(20))

# make a Ben user with username and balance
Ben = user.User("Ben10", Value(100))

# use the pay_user function to pay marcos $10. Will not allow me to pay marcos more than my balance
Noah.pay_user(Value(10), Marcos)

# create a milk item that has a price and a list of users that use that item
milk = item.Item("Milk", Value(5.00), Noah)
milk.users_who_use = [Marcos, Ben, Noah]

# create an apple item that has a price and a list of users that use that item
apple = item.Item("Apple", Value(3.00), Marcos)
apple.users_who_use = [Noah, Ben]

# instantiate a ledger with item_list filled by items
main_ledger = ledger.Ledger([milk, apple])

# calculate who owes the user
print(calculate_totals(main_ledger, Noah))
print(calculate_totals(main_ledger, Marcos))
