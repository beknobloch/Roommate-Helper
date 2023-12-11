# import user
# import ledger
# import item
# from value import Value
#
# # ----------------------------- EXAMPLE -----------------------------
#
#
# # make a Noah user with username and balance
# Noah = user.User("Noah76", Value(50))
#
# # make a Marcos user with username and balance
# Marcos = user.User("Marcos50", Value(20))
#
# # make a Ben user with username and balance
# Ben = user.User("Ben10", Value(100))
#
# # use the pay_user function to pay marcos $10. Will not allow me to pay marcos more than my balance
# Noah.pay_user(Value(10), Marcos)
#
# # create a milk item that has a price and a list of users that use that item
# milk = item.Item("Milk", Value(5.00), Noah)
# milk.add_users([Marcos, Ben, Noah])
#
# # create an apple item that has a price and a list of users that use that item
# apple = item.Item("Apple", Value(3.00), Marcos)
# apple.add_users([Noah, Ben])
#
# # instantiate a ledger with item_list filled by items
# main_ledger = ledger.Ledger([milk, apple])
#
# # calculate who owes the user
# print(Noah.calculate_totals(main_ledger))
# print(Marcos.calculate_totals(main_ledger))
#
# # test Ben paying his total amount owed to Noah
# print("\n\n")
# print(Ben.pay_all_owed(Noah, main_ledger))
master_paid_dict = {}
items = [i for i in range(10)]
users = [i for i in range(10, 20)]
for item in items:
    user_dict = {}
    for user in users:
        user_dict[user] = False
        master_paid_dict[item] = user_dict

print(master_paid_dict)
