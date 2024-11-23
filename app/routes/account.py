from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user
from ..models import Users, db, Items, UserItem
from app.forms import LoginForm, RegisterForm
import bcrypt

account_bp = Blueprint('account', __name__, template_folder='../../templates')

@account_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Uses FlaskForm instead of html forms for CSRF protection
    form = LoginForm()
    if form.validate_on_submit():
        try:
            # Get the username and password from the form
            # Data retrieval from FlaskForms is different from getting data from html forms
            username = form.username.data
            password = form.password.data

            # Query the user from the database
            user = Users.query.filter_by(username=username).first()

            if user:
                # Check the password
                passwords_match = bcrypt.checkpw(password.encode('utf-8'), user.password)

                if passwords_match:
                    # Log in the user
                    login_user(user)
                    users = Users.query.order_by(Users.date_created).all()
                    items = Items.query.order_by(Items.date_created).all()
                    return render_template('index.html', users=users, items=items)

        except Exception as e:
            return f'There was an issue logging into your account: {str(e)}'
    return render_template('login.html', form=form)

@account_bp.route('/account_logout')
def account_logout():
    logout_user()
    return redirect(url_for('account.login'))

@account_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data.strip()
        password = form.password.data.strip()
        balance = form.balance.data

        if username == password: #username is not the same as password
            return render_template("register.html", form=form, error="Username and password cannot be the same.")

        if Users.query.filter_by(username=username).first(): #no duplicate usernames
            return render_template("register.html", form=form, error="Username already exists.")

        # password validation
        if len(password) < 8:
            return render_template("register.html", form=form, error="Password must be at least 8 characters long.")
        if not any(char.isdigit() for char in password):
            return render_template("register.html", form=form, error="Password must contain at least one number.")
        if not any(char.isalpha() for char in password):
            return render_template("register.html", form=form, error="Password must contain at least one letter.")
        if not any(char.isupper() for char in password):
            return render_template("register.html", form=form, error="Password must contain at least one uppercase letter.")
        if not any(char.islower() for char in password):
            return render_template("register.html", form=form, error="Password must contain at least one lowercase letter.")
        if not any(char in "!@#$%^&*()-_=+<>?/" for char in password):
            return render_template("register.html", form=form, error="Password must contain at least one special character (example: !@#$%^&*)")

        password_bytes = password.encode('utf-8') #hash password
        password_hash = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

        try:
            new_user = Users( #create new user and save hashed password
                username=username,
                password=password_hash,
                balance=float(balance) if balance else 0.0
            )
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('account.login'))
        except Exception as e:
            db.session.rollback()
            return render_template("register.html", form=form, error=f"There was an issue creating your account: {str(e)}")

    return render_template("register.html", form=form)

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

            # If the item is paid for, don't add it to the total balance owed
            if user_item.paid is False:
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
