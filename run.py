from app import create_app, db, login_manager
from app.routes.ledger import initialize_item_user_status_dict

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        initialize_item_user_status_dict()

    app.run(host="0.0.0.0", port=8000)
