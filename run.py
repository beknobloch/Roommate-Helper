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

@app.after_request
def set_csp(response):
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; script-src 'self'; style-src 'self';"
    )
    return response

@app.after_request
def set_x_frame_options(response):
    response.headers['X-Frame-Options'] = 'DENY'
    return response
