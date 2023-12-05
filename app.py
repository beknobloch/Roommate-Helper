import json
from flask import Flask, render_template
from user import User
from item import Item
from ledger import Ledger

app = Flask(__name__)

# fake data start
me = User(username="mmorale",balance =0)
ben = User(username ="bknob",balance =0)
noah = User(username ="nspina",balance =0)

items = []
for i in range(1,10):
    items.append(Item(name=f"me{i}",price=i, user_who_paid=me))
ledge = Ledger(item_list=items)
print(me)

sample_dict = {
    "name": "John Doe",
    "age": 30,
    "city": "Example City",
    "email": "john.doe@example.com",
    "is_student": False,
    "grades": [85, 92, 78, 90]
}
# fake data end

@app.route('/')
def index():  # put application's code here
    return render_template('index.html')

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

if __name__ == '__main__':
    app.run()
