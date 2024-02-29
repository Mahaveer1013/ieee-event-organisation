import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_mail(email, subject, body):
    sender_email = "ieee.events.pec.it@gmail.com"
    receiver_email = email
    password = 'neaq qucv zqia mhcq'  # Use an App Password or enable Less Secure Apps

    # Create the email message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    # Attach the HTML body to the message
    message.attach(MIMEText(body, 'html'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print('Email sent successfully!')
    except Exception as e:
        print(f'An error occurred: {str(e)}')


send_mail('vsabarinathan1611@gmail.com','TEST','html')







        
        