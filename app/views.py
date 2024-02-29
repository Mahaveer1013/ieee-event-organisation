#views.py
from flask import Blueprint, render_template, request, jsonify,redirect,url_for
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
import os
from werkzeug.utils import secure_filename
from flask import current_app as app
import uuid
from .models import Event,Event_basic,IEEEEvent
from sqlalchemy.exc import SQLAlchemyError


views = Blueprint('views', __name__)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@views.route('/')
def home():
    mainevent=Event_basic.query.get_or_404(1)
    all_events = Event.query.all()
    return render_template('index.html',events=all_events,mainevent=mainevent)

@views.route('/event-view/<int:event_id>',methods=['GET','POST'])
def event_view(event_id):
    event=Event.query.get_or_404(event_id)
    return render_template('event-view.html', event=event)

@views.route('/admin')
@login_required
def admin():
    events = IEEEEvent.query.all()
    return render_template('admin.html',events=events)

from datetime import datetime, time

from datetime import datetime, time

@views.route('/create_event', methods=['POST', 'GET'])
@login_required
def create_event():
    if request.method == 'POST':
        images1_filename = None
        coordinator_name = request.form['coordinator_name']
        event_name = request.form['event_name']
        description = request.form['description']
        date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        place = request.form['place']
        judge = request.form['judge']
        number = request.form['number']
        start_time_str = request.form['start_time']
        end_time_str = request.form['end_time']

        # Convert string time to datetime.time objects
        start_time = datetime.strptime(start_time_str, '%H:%M').time() if start_time_str else None
        end_time = datetime.strptime(end_time_str, '%H:%M').time() if end_time_str else None

        if 'images1' in request.files:
            images1 = request.files['images1']
            if images1 and allowed_file(images1.filename):
                images1_filename = secure_filename(str(uuid.uuid4()) + "_" + images1.filename)
                images1.save(os.path.join(app.config['UPLOAD_FOLDER'], images1_filename))

        if 'images2' in request.files:
            images2 = request.files['images2']
            if images2 and allowed_file(images2.filename):
                images2_filename = secure_filename(str(uuid.uuid4()) + "_" + images2.filename)
                images2.save(os.path.join(app.config['UPLOAD_FOLDER'], images2_filename))


        # Create and add event to the database
        create = Event(coordinator_name=coordinator_name, event_name=event_name, description=description,
                       date=date, place=place, judge=judge, number=number,
                       start_time=start_time, end_time=end_time,
                       images1=images1_filename, images2=images2_filename)
        db.session.add(create)
        db.session.commit()

        return redirect('/list_event')  # Redirect after successful creation

    return render_template('event_form.html')


@views.route('/list_event')
@login_required
def list_event():
	all_events = Event.query.all()
	return render_template('list_event.html',events=all_events)

@views.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    # Retrieve the event from the database
    event = Event.query.get_or_404(event_id)

    if request.method == 'POST':
        event.coordinator_name = request.form['coordinator_name']
        event.event_name = request.form['event_name']
        event.description = request.form['description']
        event.date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        event.place = request.form['place']
        event.judge = request.form['judge']
        event.number = request.form['number']

        # Convert string time to datetime.time objects
        start_time = datetime.strptime(request.form['start_time'], '%H:%M:%S').time() if request.form['start_time'] else None
        end_time = datetime.strptime(request.form['end_time'], '%H:%M:%S').time() if request.form['end_time'] else None
        event.start_time_str = start_time
        event.end_time_str = end_time

        # Handle file uploads
        if 'images1' in request.files:
            images1 = request.files['images1']
            if images1 and allowed_file(images1.filename):
                filename = secure_filename(str(uuid.uuid4()) + "_" + images1.filename)
                images1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                event.images1 = filename

        if 'images2' in request.files:
            images2 = request.files['images2']
            if images2 and allowed_file(images2.filename):
                filename = secure_filename(str(uuid.uuid4()) + "_" + images2.filename)
                images2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                event.images2 = filename

        db.session.commit()

        return redirect(url_for('views.list_event'))

    # Handle GET request (displaying the form)
    return render_template('edit_event.html', event=event)


@views.route('/delete_event/<int:event_id>', methods=['GET', 'POST'])
@login_required
def delete_event(event_id):
    try:
        event = Event.query.get_or_404(event_id)
        db.session.delete(event)
        db.session.commit()
    except SQLAlchemyError as e:
        return e

    return redirect(url_for('views.list_event'))

@views.route('/create_event_basic', methods=['POST','GET'])
@login_required
def create_event_basic():
    if request.method == 'POST':
        try:
            event_name = request.form['event_name']
            clg_name = request.form['clg_name']
            dept_name = request.form['dept_name']
            club = request.form['club']
            coordinator_name = request.form['coordinator_name']
            # Parse the date from the form and convert it to a datetime object
            date_str = request.form['date']
            date = datetime.strptime(date_str, '%Y-%m-%d')

            # Handle file upload for event logo
            if 'event_logo' in request.files:
                event_logo = request.files['event_logo']
                if event_logo.filename != '':
                    filename = str(uuid.uuid4()) + "_" + secure_filename(event_logo.filename)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    event_logo.save(file_path)
                else:
                    filename = None
            else:
                filename = None

            # Create a new Event_basic instance and add it to the database
            new_event = Event_basic(event_name=event_name, clg_name=clg_name, dept_name=dept_name,
                                    club=club, event_logo=filename, coordinator_name=coordinator_name,
                                    date=date)
            db.session.add(new_event)
            db.session.commit()

            return redirect('/')
        except SQLAlchemyError as e:
            print(str(e))
            db.session.rollback()
            return "Error occurred while creating the event."
        finally:
            db.session.close()

    return render_template('event_details.html')