from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user
from ..models import Users, db, Items
from app.routes.ledger import item_user_status_dict
import bcrypt

account_bp = Blueprint('account', __name__, template_folder='../../templates')

@account_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            user = Users.query.filter_by(username=request.form.get("username_login")).first()
            # Check if the password entered is the same as the user's password
            entered_password_bytes = request.form.get("password_login").encode('utf-8')
            passwords_match = bcrypt.checkpw(entered_password_bytes, user.password) 

            if passwords_match:
                # Use the login_user method to log in the user
                login_user(user)
                users = Users.query.order_by(Users.date_created).all()
                items = Items.query.order_by(Items.date_created).all()
                return render_template('index.html', users=users, items=items)
        except:
            return 'There was an issue logging into your account'
    return render_template('login.html')

@account_bp.route('/account_logout')
def account_logout():
    logout_user()
    return redirect(url_for('account.login'))

@account_bp.route('/register', methods=['GET', 'POST'])
def register():
    # If the user made a POST request, create a new user
    if request.method == "POST":
        password_bytes = request.form.get("password").encode('utf-8') 
        password_hash = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

        new_user = Users(balance=float(request.form.get("balance")),
                         username=request.form.get("username"),
                         password=password_hash)

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

@account_bp.route('/account', methods=['POST', 'GET'])
def account():
    users = Users.query.order_by(Users.date_created).all()
    return render_template('account.html', users=users)

@account_bp.route('/delete/<int:id>')
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

@account_bp.route('/pay/<int:id>')
def pay(id):
    owed_balance = 0.00

    user_to_pay = Users.query.get_or_404(id)
    if current_user.is_authenticated and current_user != user_to_pay:
        try:
            oweList = Items.query.filter_by(payerID=user_to_pay.id)
            oweList_pass = []
            oweAmount_pass = []
            oweListDate_pass = []
            itemBuyerList_pass = []

            for item in oweList:
                if current_user in item.users:
                    owed_balance += item.itemPrice / len(item.users)
                    oweAmount_pass.append(item.itemPrice / len(item.users))
                    oweList_pass.append(item)
                    oweListDate_pass.append(item.date_created.date())
                    itemBuyerList_pass.append(user_to_pay)

            owedList = Items.query.filter_by(payerID=current_user.id)
            owedList_pass = []
            owedAmount_pass = []
            owedListDate_pass = []
            for item in owedList:
                if user_to_pay in item.users:
                    owed_balance -= item.itemPrice / len(item.users)
                    owedAmount_pass.append(item.itemPrice / len(item.users))
                    owedList_pass.append(item)
                    owedListDate_pass.append(item.date_created.date())
            combined_owe_list = zip(oweList_pass, oweAmount_pass, oweListDate_pass, itemBuyerList_pass)
            combined_owed_list = zip(owedList_pass, owedAmount_pass, owedListDate_pass)
            return render_template('payment.html', balance=owed_balance, user_to_pay=user_to_pay, combined_owe_list=combined_owe_list, combined_owed_list=combined_owed_list, item_user_status_dict=item_user_status_dict)
        except:
            return 'There was an issue loading the pay page for that user'
    else:
        return "You have to log in to pay another user."
