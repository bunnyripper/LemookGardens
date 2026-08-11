from flask import render_template,redirect,url_for,flash,request,current_app
from flask_login import login_user,logout_user,login_required,current_user
from werkzeug.security import check_password_hash
from app.admin import bp
from .forms import LoginForm,AnnouncementForm
from app.models import Booking,Setting,Announcement
from app.extensions import db
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from flask import current_app


ALLOWED_EXTENSIONS={"pmg","jpg","gif","jpeg","webp"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".",1)[1].lower() in ALLOWED_EXTENSIONS

class AdminUser:
    def __init__(self,username):
        self.id=username
        self.is_authenticated=True
        self.is_active=True
        self.is_anonymous=False
        
    def get_id(self):
        return self.id

@bp.route("/login",methods=["GET","POST"])
def login():
    if current_user.is_authenticated:
       return redirect(url_for("admin.dashboard"))
    
    form=LoginForm()
    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data
        
        admin_username=current_app.config.get("ADMIN_USERNAME","admin")
        admin_password_hash=current_app.config.get("ADMIN_PASSWORD_HASH","")
        if username == admin_username and check_password_hash(admin_password_hash,password):
            user=AdminUser(username)
            login_user(user,remember=True)
            flash("Logged in successfully","success")
            return redirect(url_for("admin.dashboard"))
        else:
            flash("Invalid username or password","danger")
    return render_template("admin/login.html",form=form)

@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out!","info")
    return redirect(url_for("admin.login"))

@bp.route("/dashboard")
@login_required
def dashboard():
    bookings=Booking.query.filter_by(deleted=False).order_by(Booking.created_at.desc()).all()
    
    pending_count=Booking.query.filter_by(status="pending").count()
    confirmed_count=Booking.query.filter_by(status="confirmed").count()
    cancelled_count=Booking.query.filter_by(status="cancelled").count()
    completed_count=Booking.query.filter_by(status="completed").count()
    
    return render_template("admin/dashboard.html",bookings=bookings,
                           pending_count=pending_count,confirmed_count=confirmed_count,
                           cancelled_count=cancelled_count,completed_count=completed_count)
    
@bp.route("/booking/<int:booking_id>")
@login_required
def booking_detail(booking_id):
    booking=Booking.query.get_or_404(booking_id)
    return render_template("admin/booking_detail.html",booking=booking)

@bp.route("/booking/<int:booking_id>/update",methods=["POST","GET"])
@login_required
def update_booking_status(booking_id):
    booking=Booking.query.get_or_404(booking_id)
    new_status=request.form.get("status")
    
    if new_status in ["pending","confirmed","cancelled","completed"]:
        booking.status=new_status
        db.session.commit()
        flash(f"Booking #{booking.booking_id} status updated to {new_status}","success")
    else:
        flash("Invalid status","danger")
    
    return redirect(url_for("admin.booking_detail",booking_id=booking.booking_id))
@bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        for key, value in request.form.items():
            setting = Setting.query.filter_by(key=key).first()
            if setting:
                setting.value = value
            else:
                setting = Setting(key=key, value=value)
                db.session.add(setting)
        db.session.commit()
        flash('Settings saved!', 'success')
        return redirect(url_for('admin.settings'))
    

    settings = {s.key: s.value for s in Setting.query.all()}
    return render_template('admin/settings.html', settings=settings)

@bp.route("/booking/<int:booking_id>/delete",methods=["POST"])
@login_required
def delete_bookings(booking_id):
    booking=Booking.query.get_or_404(booking_id)
    booking.deleted=True
    booking.deleted_at=datetime.utcnow()
    db.session.commit()
    
    flash(f"Booking #{booking.booking_id} has been deleted.","warning")
    return redirect(url_for("admin.dashboard"))
@bp.route("/announcement")
@login_required
def announcements():
    announcements=Announcement.query.order_by(Announcement.created_at.desc()).all()
    return render_template("admin/announcements.html",announcements=announcements)

@bp.route("/announcements/new",methods=["GET","POST"])
@login_required
def new_announcements():
    form=AnnouncementForm()
    if form.validate_on_submit():
        filename=None
        if form.image.data:
            file=form.image.data
            if allowed_file(file.filename):
                filename=secure_filename(file.filename)
                file_path=os.path.join(current_app.config["UPLOAD_FOLDER"],filename)
                file.save(file_path)
            else:
                flash("Invalid file type.Please upload an image","danger")
                return render_template("admin/announcement_form.html",form=form,title="New Announcement")
        announcement=Announcement(
            title=form.title.data,
            content=form.content.data,
            image_filename=filename,
            is_active=form.is_active.data
        )
        db.session.add(announcement)
        db.session.commit()
        flash("Announcement created succesfully!","Success")
        return redirect(url_for("admin.announcements"))
    return render_template("admin/announcements_form.html",form=form,title="New announcement")

@bp.route("/announcements/<int:id>/edit",methods=["GET","POST"])
@login_required
def edit_announcement(id):
    announcement=Announcement.query.get_or_404(id)
    if announcement.image_filename:
            file_path=os.path.join(current_app.config["UPLOAD_FOLDER"],announcement.image_filename)
            if os.path.exists(file_path):
                os.remove(file_path)
    form=AnnouncementForm(obj=announcement)
    if form.validate_on_submit():
        announcement.title=form.title.data
        announcement.content=form.content.data
        announcement.image=form.image.data
        announcement.is_active=form.is_active.data
        announcement.updated_at=datetime.utcnow()
        db.session.commit()
        flash("Announcement updated successfully!","success")
        return redirect(url_for("admin.announcements"))
    return render_template("admin/announcements_form.html",form=form,title="Edit Announcements")

@bp.route("/announcements/<int:id>/delete",methods=["POST"])
@login_required
def delete_announcement(id):
    announcement=Announcement.query.get_or_404(id)
    if announcement.image_filename:
        file_path=os.path.join(current_app.config["UPLOAD_FOLDER"],announcement.image_filename)
        if os.path.exists(file_path):
            os.remove(file_path)
    db.session.delete(announcement)
    db.session.commit()
    flash("Announcement deleted successfully!","Warning")
    return redirect(url_for("admin.announcements"))

@bp.route("/announcements/<int:id>/toggle",methods=["POST"])
@login_required
def toggle_announcement(id):
    announcement=Announcement.query.get_or_404(id)
    announcement.is_active=not announcement.is_active
    db.session.commit()
    status="activated" if announcement.is_active else "deactivated"
    flash(f"Annoncement {status}!","Success")
    return redirect(url_for("admin.announcements"))