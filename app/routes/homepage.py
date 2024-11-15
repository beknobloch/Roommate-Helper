from flask import Blueprint, render_template
from ..models import Users, Items

homepage_bp = Blueprint('homepage', __name__, template_folder='../../templates')

@homepage_bp.route('/')
def index():
    users = Users.query.order_by(Users.date_created).all()
    items = Items.query.order_by(Items.date_created).all()
    return render_template('index.html', items=items, users=users)
