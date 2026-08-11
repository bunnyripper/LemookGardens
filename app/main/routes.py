from flask import Blueprint,render_template,redirect,url_for,flash,request,current_app
from datetime import datetime
from .forms import AccommodationForm, EventForm
from app.models import Booking
from app.extensions import db , limiter
from app.utils import send_whatsapp_booking_alert
from app.main import bp

@bp.route("/")
def index():
    return render_template("main/index.html")
@bp.route("/dining")
def dining():
    return render_template("main/dining.html")
@bp.route('/booking')
def booking():
    return render_template('main/booking.html')
@bp.route("/rooms")
def rooms():
    return render_template("main/rooms.html")
@bp.route("/gallery")
def gallery():
    return render_template("main/gallery.html")
@bp.route('/book/accommodation', methods=['GET', 'POST'])
@limiter.limit("5 per second")
def book_accommodation():
    form = AccommodationForm()
    if form.validate_on_submit():
        booking = Booking(
            booking_type='accommodation',
            room_type=form.room_type.data,
            guest_name=form.guest_name.data,
            guest_email=form.guest_email.data,
            guest_phone=form.guest_phone.data,
            check_in=form.check_in.data,
            check_out=form.check_out.data,
            adults=form.adults.data,
            children=form.children.data or 0,
            special_requests=form.special_requests.data
        )
        db.session.add(booking)
        db.session.commit()
        flash('Booking submitted successfully!', 'success')
        return redirect(url_for('main.booking_success', booking_id=booking.booking_id))
    return render_template('main/book_accommodation.html', form=form)
@bp.route("/event")
def event():
    return render_template("main/event.html")
@bp.route('/book/event', methods=['GET', 'POST'])
@limiter.limit("5 per second")
def book_event():
    form = EventForm()
    if form.validate_on_submit():
        booking = Booking(
            booking_type='event',
            event_type=form.event_type.data,
            guest_name=form.guest_name.data,
            guest_email=form.guest_email.data,
            guest_phone=form.guest_phone.data,
            check_in=form.event_date.data,  
            guest_count=form.guest_count.data,
            special_requests=form.special_requests.data
        )
        db.session.add(booking)
        db.session.commit()
        flash('Event booking submitted successfully!', 'success')
        return redirect(url_for('main.booking_success', booking_id=booking.booking_id))
    return render_template('main/book_event.html', form=form)
    
@bp.route("/booking-success/<int:booking_id>")
def booking_success(booking_id):
    booking=Booking.query.get_or_404(booking_id)
    return render_template("main/booking_success.html",booking=booking)
            

