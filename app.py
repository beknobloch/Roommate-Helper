import json
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from user import User
from item import Item
from ledger import Ledger
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config["SECRET_KEY"] = "abc"
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(int(user_id))


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    balance = db.Column(db.Float, nullable=False)
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


@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(user_id)


@app.route('/register', methods=["GET", "POST"])
def register():
    # If the user made a POST request, create a new user
    if request.method == "POST":
        new_user = Users(balance=float(request.form.get("balance")),
                         username=request.form.get("username"),
                         password=request.form.get("password"))

        try:
            db.session.add(new_user)
            db.session.commit()
        except:
            return 'There was an issue adding your user'
        # Once user account created, redirect them
        # to login route (created later on)
        return render_template('login.html')
        # return redirect(url_for('login'))
    # Renders sign_up template if user made a GET request
    return render_template("register.html")


@app.route('/', methods=['POST', 'GET'])
def index():  # put application's code here
    return render_template('index.html')


@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = Users.query.get_or_404(id)

    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        return redirect(url_for('account'))
    except:
        return "There was a problem deleting that user"


@app.route('/account', methods=['POST', 'GET'])
def account():
    users = Users.query.order_by(Users.date_created).all()
    return render_template('account.html', users=users)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = Users.query.filter_by(username=request.form.get("username_login")).first()
        # Check if the password entered is the same as the user's password
        if user.password == request.form.get("password_login"):
            # Use the login_user method to log in the user
            login_user(user)
            return render_template('index.html')
    return render_template('login.html')


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
