from __init__ import create_app

app, celery = create_app()  # Unpack the tuple

if __name__ == "__main__":
    app.run(debug=True)