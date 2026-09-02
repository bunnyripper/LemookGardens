from datetime import datetime
from .extensions import db
#yooh the id for booking is booking_id not id. so anywhere in the code where it`s booking.booking_id is correct
class Booking(db.Model):
    booking_id=db.Column(db.Integer,primary_key=True)
    booking_type=db.Column(db.String(50),nullable=False)
    
    room_type=db.Column(db.String(50),nullable=True)
    
    event_type=db.Column(db.String(50),nullable=True)
    
    guest_name=db.Column(db.String(100),nullable=False)
    guest_email=db.Column(db.String(120),nullable=False)
    guest_phone=db.Column(db.String(20),nullable=False)
    check_in=db.Column(db.Date,nullable=False)
    check_out=db.Column(db.Date,nullable=True)
    adults=db.Column(db.Integer,nullable=False,default=1)
    children=db.Column(db.Integer,nullable=False,default=0)
    guest_count=db.Column(db.Integer,nullable=True)
    special_requests=db.Column(db.Text,nullable=True)
    status=db.Column(db.String(20),nullable=False,default="pending")
    created_at=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    deleted=db.Column(db.Boolean,default=False)
    deleted_at=db.Column(db.DateTime,nullable=True)
    
    @property
    def is_deleted(self):
        return self.deleted_at is not None
    
    def __repr__(self):
        return f"<Booking {self.id} - {self.guest_name}"
    
class Setting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False)
    value = db.Column(db.String(200), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_filename = db.Column(db.String(200), nullable=True)  
    is_active = db.Column(db.Boolean, default=True)
    is_popup = db.Column(db.Boolean, default=False)  
    starts_at = db.Column(db.DateTime, nullable=True)  
    ends_at = db.Column(db.DateTime, nullable=True)    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @property
    def is_visible(self):
        """Check if announcement is currently visible."""
        if not self.is_active:
            return False
        now = datetime.utcnow()
        if self.starts_at and self.starts_at > now:
            return False
        if self.ends_at and self.ends_at < now:
            return False
        return True
    
    
class Events(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100),nullable=False)
    description=db.Column(db.Text,nullable=False)
    event_type=db.Column(db.String(50),nullable=False)
    image=db.Column(db.String(200),nullable=False)
    is_active=db.Column(db.Boolean,default=True)
    created_at=db.Column(db.DateTime,default=datetime.utcnow)
    updated_at=db.Column(db.DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)
    