import json
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from user import User
from item import Item
from ledger import Ledger
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User %r>' % self.id

# fake data start
me = User(username="mmorale", balance=0)
ben = User(username="bknob", balance=0)
noah = User(username="nspina", balance=0)

items = []
for i in range(1, 10):
    items.append(Item(name=f"me{i}", price=i, user_who_paid=me))
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


@app.route('/', methods=['POST', 'GET'])
def index():  # put application's code here
    return render_template('index.html')


@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = Users.query.get_or_404(id)

    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem deleting that user"


@app.route('/user', methods=['POST', 'GET'])
def add_user():
    if request.method == 'POST':
        username_content = request.form['content']
        new_user = Users(content=username_content)

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your user'
    else:
        users = Users.query.order_by(Users.date_created).all()
        return render_template('user.html', users=users)


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
    items.append(Item(name=newItem[0], price=newItem[1], user_who_paid=me))
    pass_list()


# main
if __name__ == '__main__':
    app.run()
