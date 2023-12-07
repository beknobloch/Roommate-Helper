import json
from flask import Flask, render_template, request, jsonify, url_for, redirect
from user import User
from item import Item
from ledger import Ledger
from group import Group

app = Flask(__name__)

# fake data start
marcos = User(username="mmorale",balance =0)
ben = User(username ="bknob",balance =0)
noah = User(username ="nspina",balance =0)

items = []
for i in range(1,10):
    items.append(Item(name=f"me{i}",price=i, user_who_paid=marcos))
ledge = Ledger(item_list=items)
print(marcos)

sample_dict = {
    "name": "John Doe",
    "age": 30,
    "city": "Example City",
    "email": "john.doe@example.com",
    "is_student": False,
    "grades": [85, 92, 78, 90]
}
# fake data end

# use case 1 start
noah = User(username ="noah",balance =0)
ben = User(username ="ben",balance =0)
userList = [noah, ben]

items = [
    Item(name=f"Cookies",price=4, user_who_paid=noah),
    Item(name=f"Chicken",price=8, user_who_paid=noah),
    Item(name=f"Peppers",price=3, user_who_paid=noah),
    Item(name=f"Garlic",price=1, user_who_paid=noah),
    Item(name=f"Pasta",price=2, user_who_paid=noah)
]
items[0].add_users([ben])
items[1].add_users([noah, ben])

ledger = Ledger(item_list=items)
group = Group(userList)

@app.route('/get_item_list', methods=['POST'])
def get_item_list():
    return json.dumps([item.get_name() for item in ledger.get_item_list()])

@app.route('/add_new_item', methods=['POST'])
def add_new_item():
    data = request.get_json()
    response = data['data']
    # prints data received
    print(f"Received data: {response}")
    
    #checks if user
    response[2] = ben
    ledger.add_item(Item(name=response[0],price=response[1],user_who_paid=response[2]))

    # returns message (not needed)
    return jsonify({'message': 'Success'})
# use case 1 end

# use case 2 start

@app.route('/get_username_list', methods=['POST'])
def get_username_list():
    return json.dumps([str(username.username) for username in userList])

@app.route('/calculate_amount_owed', methods=['POST'])
def calculate_amount_owed():
    data = request.get_json()['users']
    username1 = str(data[0])
    username2 = str(data[1])
    
    for u in group.user_list:
        if u.username == username1:
            user1 = u
        elif u.username == username2:
            user2 = u

    return str(ledger.calculate_amount_owed(user1, user2))

# use case 2 end

# renders home page
@app.route('/')
def index():  # put application's code here
    return render_template('index.html')

# renders use case 1 page
@app.route('/use_case_1', methods=['GET', 'POST'])
def use_case_1():
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('use_case_1.html')

# renders use case 2 page
@app.route('/use_case_2', methods=['GET', 'POST'])
def use_case_2():
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('use_case_2.html')

@app.route('/pass_data', methods=['POST'])
def pass_data():
    result = ""

    for i in ledge.get_item_list():
        result += f"{i}, "
    return result

@app.route('/pass_list', methods=['POST'])
def pass_list():
    return json.dumps([str(obj) for obj in items])

@app.route('/pass_dict', methods=['POST'])
def pass_dict():
    return json.dumps([[key, value] for key, value in sample_dict.items()])

@app.route('/retrieveData', methods=['POST']) 
def retrieveData(): 
    data = request.get_json()
    response = data['data']
    # prints data received
    print(f"Received data: {response}")
    updateItemList(response)
    
    # returns message (not needed)
    return jsonify({'message': 'Success'})

# takes js user input and uses it to create a new item and appends it to the item list
def updateItemList(newItem):
    items.append(Item(name=newItem[0],price=newItem[1], user_who_paid=marcos))
    pass_list()

# main
if __name__ == '__main__':
    app.run()
