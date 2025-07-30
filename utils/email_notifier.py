import smtplib
from email.mime.text import MIMEText

def send_notification_email(to_email, subject, body):
    # Placeholder for email sending logic
    # In a real application, you would configure your SMTP server details
    # and handle authentication securely.

    # Example (for demonstration purposes only - DO NOT use in production without proper security):
    # smtp_server = 'your_smtp.example.com'
    # smtp_port = 587  # or 465 for SSL
    # sender_email = 'your_email@example.com'
    # sender_password = 'your_email_password'

    # msg = MIMEText(body)
    # msg['Subject'] = subject
    # msg['From'] = sender_email
    # msg['To'] = to_email

    # try:
    #     with smtplib.SMTP(smtp_server, smtp_port) as server:
    #         server.starttls()  # Use TLS
    #         server.login(sender_email, sender_password)
    #         server.send_message(msg)
    #     print(f"Email sent to {to_email} with subject: {subject}")
    # except Exception as e:
    #     print(f"Failed to send email: {e}")

    print(f"[MOCK] Sending email to {to_email} with subject: {subject}")
    print(f"Body:\n{body}")

if __name__ == '__main__':
    send_notification_email("test@example.com", "Test Subject", "This is a test email body.")
