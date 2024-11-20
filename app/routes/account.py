from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user
from ..models import Users, db, Items, UserItem
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
        except Exception as e:
            return f'There was an issue logging into your account: {str(e)}'
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
            # Log out the user
            logout_user()

            # Delete all associated UserItem entries
            UserItem.query.filter_by(user_id=user_to_delete.id).delete()

            # Delete the user record
            db.session.delete(user_to_delete)
            db.session.commit()

            return redirect('/login')
        except Exception as e:
            db.session.rollback()  # Rollback in case of an error
            return f'There was an issue deleting the user: {str(e)}'
    else:
        return "You must be logged in and own this account to delete it."

@account_bp.route('/pay/<int:id>')
def pay(id):
    if not current_user.is_authenticated:
        return "You must be logged in to pay another user."

    user_to_pay = Users.query.get_or_404(id)
    if current_user == user_to_pay:
        return "You cannot pay yourself."

    try:
        # Calculate amounts owed by current_user to user_to_pay
        owe_items = (
            db.session.query(UserItem, Items)
            .join(Items, UserItem.item_id == Items.id)
            .filter(UserItem.user_id == current_user.id, Items.payerID == user_to_pay.id, UserItem.paid == False)
            .all()
        )

        owe_list = []
        owed_balance = 0.0
        for user_item, item in owe_items:
            share = item.itemPrice / len(item.user_items)  # Split price among all users
            owed_balance += share
            owe_list.append({
                "item": item,
                "amount": share,
                "date": item.date_created.date(),
                "buyer": user_to_pay.username,
            })

        # Calculate amounts owed by user_to_pay to current_user
        owed_items = (
            db.session.query(UserItem, Items)
            .join(Items, UserItem.item_id == Items.id)
            .filter(UserItem.user_id == user_to_pay.id, Items.payerID == current_user.id, UserItem.paid == False)
            .all()
        )

        owed_list = []
        for user_item, item in owed_items:
            share = item.itemPrice / len(item.user_items)  # Split price among all users
            owed_balance -= share
            owed_list.append({
                "item": item,
                "amount": share,
                "date": item.date_created.date(),
            })

        return render_template(
            'payment.html',
            balance=owed_balance,
            user_to_pay=user_to_pay,
            owe_list=owe_list,
            owed_list=owed_list,
        )
    except Exception as e:
        return f'There was an issue loading the payment page: {str(e)}'

@account_bp.route('/payment/<int:item_id>/<int:user_to_pay_id>', methods=['POST', 'GET'])
def process_payment(item_id, user_to_pay_id):
    if not current_user.is_authenticated:
        return redirect('/login')

    item = Items.query.get_or_404(item_id)
    user_item = UserItem.query.filter_by(user_id=current_user.id, item_id=item_id).first()
    user_to_pay = Users.query.get_or_404(user_to_pay_id)
    if not user_item or user_item.paid:
        return "Payment already made or not allowed.", 403

    try:
        # Calculate the amount to pay based on the number of users sharing the item
        amount_to_pay = item.itemPrice / len(item.users)
        if current_user.balance >= amount_to_pay and user_item and not user_item.paid:
            # Process the payment
            user_to_pay.balance += amount_to_pay
            current_user.balance -= amount_to_pay
            user_item.paid = True

            # Commit the changes to the database
            db.session.commit()

        return redirect('/ledger')  # Redirect to the ledger or another appropriate page
    except Exception as e:
        db.session.rollback()
        return f"Error processing payment: {str(e)}", 500
