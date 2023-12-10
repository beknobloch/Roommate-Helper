from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config["SECRET_KEY"] = "abc"
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(int(user_id))


# ------------------ DATABASE STUFF START ------------------ #
class Items(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    itemName = db.Column(db.String(200), nullable=False)
    itemPrice = db.Column(db.Float, nullable=False)
    payerID = db.Column(db.Integer, db.ForeignKey('users.id'))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Item %r>' % self.id


class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    balance = db.Column(db.Float, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship declaration placed after both models are defined
    items = db.relationship('Items', secondary='user_items', backref='users')

    def __repr__(self):
        return '<User %r>' % self.id


user_items = db.Table('user_items',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('item_id', db.Integer, db.ForeignKey('items.id'), primary_key=True))
# ------------------ DATABASE STUFF END ------------------ #


# ------------------ HOMEPAGE STUFF START ------------------ #
@app.route('/', methods=['POST', 'GET'])
def index():
    users = Users.query.order_by(Users.date_created).all()
    items = Items.query.order_by(Items.date_created).all()
    return render_template('index.html', items=items, users=users)


# ------------------ HOMEPAGE STUFF END ------------------ #


# ------------------ LEDGER/ITEM STUFF START ------------------ #
@app.route('/ledger', methods=['POST', 'GET'])
def ledger():
    users = Users.query.order_by(Users.date_created).all()
    items = Items.query.order_by(Items.date_created).all()
    return render_template('ledger.html', users=users, items=items)


@app.route('/addItem', methods=['POST', 'GET'])
def add_item():
    if request.method == 'POST':
        new_item = Items(itemName=request.form.get('itemName'),
                        itemPrice=request.form.get('itemPrice'),
                        payerID=request.form.get('payerID'))
        selected_users_ids = request.form.getlist('itemUsers')
        selected_users = Users.query.filter(Users.id.in_(selected_users_ids)).all()
        for user in selected_users:
            new_item.users.append(user)
        try:
            db.session.add(new_item)
            db.session.commit()
        except:
            return 'There was an issue adding your item'
        users = Users.query.order_by(Users.date_created).all()
        items = Items.query.order_by(Items.date_created).all()
        return render_template('ledger.html', users=users, items=items)
    return render_template("index.html")


@app.route('/deleteItem/<int:id>')
def delete_item(id):
    item_to_delete = Items.query.get_or_404(id)
    try:
        db.session.delete(item_to_delete)
        db.session.commit()
        return redirect('/ledger')
    except:
        return 'There was an issue deleting that item'
# ------------------ LEDGER/ITEM STUFF END ------------------ #


# ------------------ ACCOUNT STUFF START ------------------ #
@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(user_id)


@app.route('/account', methods=['POST', 'GET'])
def account():
    users = Users.query.order_by(Users.date_created).all()
    return render_template('account.html', users=users)


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


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        try:
            user = Users.query.filter_by(username=request.form.get("username_login")).first()
            # Check if the password entered is the same as the user's password
            if user.password == request.form.get("password_login"):
                # Use the login_user method to log in the user
                login_user(user)
                users = Users.query.order_by(Users.date_created).all()
                items = Items.query.order_by(Items.date_created).all()
                return render_template('index.html', users=users, items=items)
        except:
            return 'There was an issue logging into your account'
    return render_template('login.html')


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    if current_user.is_authenticated and current_user == user_to_delete:
        try:
            logout_user()
            db.session.delete(user_to_delete)
            db.session.commit()
            return redirect('/login')
        except:
            return 'There was an issue deleting that user'
    else:
        return "You have to log in to delete a user"
    
@app.route('/pay/<int:id>')
def pay(id):
    owed_balance = 0.00

    user_to_pay = Users.query.get_or_404(id)
    if current_user.is_authenticated and current_user != user_to_pay:
        try:
            oweList = Items.query.filter_by(payerID=user_to_pay.id)
            owedList = Items.query.filter_by(payerID=current_user.id)
            oweList_pass = []
            owedList_pass = []
            for item in oweList:
                if current_user in item.users:
                    owed_balance += item.itemPrice
                    oweList_pass.append(item)
            for item in owedList:
                if user_to_pay in item.users:
                    owed_balance -= item.itemPrice
                    owedList_pass.append(item)
            
            return render_template('payment.html', balance=owed_balance, user_to_pay=user_to_pay, owe_list=oweList_pass, owed_list=owedList_pass)
        except:
            return 'There was an issue loading the pay page for that user'
    else:
        return "You have to log in to pay another user."
# ------------------ ACCOUNT STUFF END ------------------ #


# main
if __name__ == '__main__':
    app.run()
