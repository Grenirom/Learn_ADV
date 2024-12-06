from apps.account.send_email import send_activation_email, send_password_reset_email

from config.celery import app


@app.task
def send_activation_email_task(email, code):
    send_activation_email(email, code)


@app.task
def send_password_reset_email_task(email, reset_code):
    send_password_reset_email(email, reset_code)
