from app import create_app

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        from app.models import db
        db.create_all()

        from app.routes.ledger import initialize_item_user_status_dict
        initialize_item_user_status_dict()

    app.run(host="0.0.0.0", port=8000)
