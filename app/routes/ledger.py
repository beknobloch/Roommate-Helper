from flask import Blueprint, render_template, request, redirect
from ..models import Users, Items, db

ledger_bp = Blueprint('ledger', __name__, template_folder='../../templates')

item_user_status_dict = {}
def initialize_item_user_status_dict():
    global item_user_status_dict
    item_user_status_dict = {}
    items = Items.query.order_by(Items.date_created).all()
    for item in items:
        user_dict = {user.id: False for user in item.users}
        item_user_status_dict[item.id] = user_dict

@ledger_bp.route('/ledger', methods=['GET'])
def ledger():
    users = Users.query.order_by(Users.date_created).all()
    items = Items.query.order_by(Items.date_created).all()
    return render_template('ledger.html', users=users, items=items)

@ledger_bp.route('/addItem', methods=['POST'])
def add_item():
    if request.method == 'POST':
        new_item = Items(itemName=request.form.get('itemName'),
                         itemPrice=request.form.get('itemPrice'),
                         payerID=request.form.get('payerID'))
        selected_users = request.form.getlist('itemUsers')
        selected_users_ids = Users.query.filter(Users.id.in_(selected_users)).all()
        for user in selected_users_ids:
            new_item.users.append(user)
        try:
            db.session.add(new_item)
            db.session.commit()
        except:
            return 'There was an issue adding your item'
        users = Users.query.order_by(Users.date_created).all()
        items = Items.query.order_by(Items.date_created).all()

        user_dict = {}
        for user in selected_users_ids:
            user_dict[user.id] = False
        item_user_status_dict[items[-1].id] = user_dict

        return render_template('ledger.html', users=users, items=items)
    return render_template("index.html")

@ledger_bp.route('/deleteItem/<int:id>')
def delete_item(id):
    item_to_delete = Items.query.get_or_404(id)
    item_user_status_dict.pop(item_to_delete.id)
    try:
        db.session.delete(item_to_delete)
        db.session.commit()
        return redirect('/ledger')
    except:
        return 'There was an issue deleting that item'
