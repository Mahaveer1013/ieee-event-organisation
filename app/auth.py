from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import Admin,Ticket,IEEEEvent
from flask import current_app as app
from collections import defaultdict

auth = Blueprint('auth', __name__)
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

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if the admin exists in the database
        admin = Admin.query.filter_by(id=1).first()
        if admin:
            # Verify password
            if check_password_hash(admin.password, password):
                login_user(admin)
                return redirect(url_for('views.admin'))  # Redirect to homepage after login
            else:
                return 'Incorrect password'
        else:
            # If admin doesn't exist, create one and add to the database
            hashed_password = generate_password_hash(password)
            new_admin = Admin(username=username,  password=hashed_password)
            db.session.add(new_admin)
            db.session.commit()
            login_user(new_admin)
            return redirect(url_for('views.admin'))

    return render_template('login.html')
@auth.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        # Fetching form data
        tl_name = request.form.get('tl_name')
        tm_name = request.form.get('tm_name')
        tl_roll = request.form.get('tl_roll')
        tm_roll = request.form.get('tm_roll')
        tl_section = request.form.get('tl_section')
        tm_section = request.form.get('tm_section')
        tl_email = request.form.get('tl_email')
        tm_email = request.form.get('tm_email')

        # Retrieving the selected radio button value
        event = None
        if 'first' in request.form:
            event = request.form.get('first')
        elif 'second' in request.form:
            event = request.form.get('second')
        elif 'third' in request.form:
            event = request.form.get('third')
        elif 'fourth' in request.form:
            event = request.form.get('fourth')

        # Debug print all form values
        print("Team Leader Name:", tl_name)
        print("Team Member Name:", tm_name)
        print("Team Leader Roll:", tl_roll)
        print("Team Member Roll:", tm_roll)
        print("Team Leader Section:", tl_section)
        print("Team Member Section:", tm_section)
        print("Team Leader Email:", tl_email)
        print("Team Member Email:", tm_email)
        print("Selected Event:", event)

        # Check if team leader has already registered for the event
        team_leader_event = IEEEEvent.query.filter_by(team_leader_roll=tl_roll, event_type=event).first()
        if team_leader_event:
            return "Team leader has already registered for this event."

        # Check if team member has already registered for the event
        team_member_event = IEEEEvent.query.filter_by(team_member_roll=tm_roll, event_type=event).first()
        if team_member_event:
            return "Team member has already registered for this event."

        # Check if team leader has already registered for two events
        team_leader_events = IEEEEvent.query.filter(IEEEEvent.team_leader_roll == tl_roll).count()
        if team_leader_events >= 2:
            return "Team leader has already registered for two events."

        # Check if team member has already registered for two events
        team_member_events = IEEEEvent.query.filter(IEEEEvent.team_member_roll == tm_roll).count()
        if team_member_events >= 2:
            return "Team member has already registered for two events."

        # Creating a new Event object and adding it to the database session
        new_event = IEEEEvent(
            team_leader_name=tl_name,
            team_member_name=tm_name,
            team_leader_roll=tl_roll,
            team_member_roll=tm_roll,
            team_leader_section=tl_section,
            team_member_section=tm_section,
            team_leader_email=tl_email,
            team_member_email=tm_email,
            event_type=event
        )
        db.session.add(new_event)
        db.session.commit()
        html = f"""
 <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Email Verification</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    max-width: 600px;
                    margin: 20px auto;
                    background-color: #ffffff;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }}
                h1 {{
                    text-align: center;
                    color: #333333;
                }}
                p {{
                    color: #666666;
                }}
                .btn {{
                    display: inline-block;
                    background-color: #007bff;
                    color: #ffffff;
                    text-decoration: none;
                    padding: 10px 20px;
                    border-radius: 5px;
                    transition: background-color 0.3s;
                }}
                .btn:hover {{
                    background-color: #0056b3;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Thank You for Registering!</h1>
                <p>
                Dear {tl_roll},<br>

We hope this message finds you well!

We wanted to take a moment to express our sincere gratitude for registering for our upcoming event, {event}. Your interest and commitment mean a great deal to us, and we are thrilled to have you join us.

Your participation will undoubtedly enrich our event, and we're looking forward to sharing valuable insights and experiences together.

Should you have any questions or need further information before the event, please don't hesitate to reach out to us. We're here to assist you in any way we can.

Once again, thank you for your registration, and we eagerly anticipate seeing you at {event}!

Best regards,</p>
            </div>
        </body>
        </html>
        """
        subject="Thank You for Registering!"
        to=tl_email
        send_mail(email=to,subject=subject,body=html)


        return redirect(url_for('views.home'))


    return render_template('register.html')

@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('views.home'))