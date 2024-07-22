from flask import Flask, render_template, request, jsonify
from celery import Celery
from tasks import generate_pdf  # Import the task directly

def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['CELERY_RESULT_BACKEND']
    )
    celery.conf.update(app.config)
    return celery

def create_app():
    app = Flask(__name__)
    
    app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
    app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
    
    celery = make_celery(app)

    @app.route('/', methods=['GET', 'POST'])
    def generate_pdf_view():
        if request.method == 'POST':
            html = request.json.get('html')
            if not html:
                return jsonify({"error": "No HTML content provided"}), 400

            task = generate_pdf.delay(html)
            return jsonify({"task_id": task.id}), 202
        else:
            return render_template('index.html')
    
    return app, celery