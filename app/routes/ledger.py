from flask import Blueprint, render_template, request, redirect
from ..models import Users, Items, db, UserItem

ledger_bp = Blueprint('ledger', __name__, template_folder='../../templates')

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

        try:
            db.session.add(new_item)
            db.session.commit()

            selected_users = request.form.getlist('itemUsers')
            # For each selected user, create an association in UserItem
            for user_id in selected_users:
                user_item = UserItem(
                    user_id=int(user_id),
                    item_id=new_item.id,
                    paid=False  # Default unpaid
                )
                db.session.add(user_item)

                db.session.commit()

        except Exception as e:
            db.session.rollback()
            return f'There was an issue adding your item: {str(e)}'
        users = Users.query.order_by(Users.date_created).all()
        items = Items.query.order_by(Items.date_created).all()

        return render_template('ledger.html', users=users, items=items)
    return render_template("index.html")

@ledger_bp.route('/deleteItem/<int:id>')
def delete_item(id):
    item_to_delete = Items.query.get_or_404(id)

    try:
        # Delete all associated UserItem records
        UserItem.query.filter_by(item_id=item_to_delete.id).delete()

        # Delete the item itself
        db.session.delete(item_to_delete)
        db.session.commit()
        return redirect('/ledger')
    except Exception as e:
        db.session.rollback()  # Rollback in case of an error
        return f'There was an issue deleting the item: {str(e)}'
