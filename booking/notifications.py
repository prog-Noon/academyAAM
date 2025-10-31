from django.core.mail import send_mail

def send_notification_to_admin(user):
    # You can customize the subject and message based on your requirements
    subject = 'New Student Registration'
    message = f'A new student has registered: {user.username} ({user.email})'

    # Send the email to the admin
    send_mail(subject, message, 'from@example.com', ['admin@example.com'])
