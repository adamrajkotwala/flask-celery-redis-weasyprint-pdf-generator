from celery import Celery
from weasyprint import HTML

# Create a Celery instance
celery = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

@celery.task
def generate_pdf(html):
    pdf = HTML(string=html).write_pdf()
    pdf_path = '/home/adamraj/weasyprint-celery/output/generated_file.pdf'
    with open(pdf_path, 'wb') as f:
        f.write(pdf)
    return pdf_path