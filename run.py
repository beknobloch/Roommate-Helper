from app import create_app

app = create_app()

@app.context_processor
def inject_logout_form():
    from app.forms import LogoutForm
    return {'logout_form': LogoutForm()}

if __name__ == "__main__":
    with app.app_context():
        from app.models import db
        db.create_all()

    app.run(host="0.0.0.0", port=8080)
