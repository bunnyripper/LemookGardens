from flask_wtf import FlaskForm
from wtforms import StringField,EmailField,TelField,DateField,IntegerField,TextAreaField,SelectField,RadioField
from wtforms.validators import DataRequired,Email,Length,Optional,ValidationError
from datetime import date

from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, TelField, DateField, IntegerField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Length, Optional, ValidationError

class AccommodationForm(FlaskForm):
    guest_name = StringField('Full Name', validators=[DataRequired(), Length(max=100)])
    guest_email = EmailField('Email Address', validators=[DataRequired(), Email(), Length(max=120)])
    guest_phone = TelField('Phone Number', validators=[DataRequired(), Length(max=20)])
    
    room_type = SelectField(
        'Room Type',
        choices=[
            ('', 'Select a room...'),
            ('bamboo_hut', 'Bamboo Hut'),
            ('garden_cottage', 'Garden Cottage'),
            ('family_suite', 'Family Suite')
        ],
        validators=[DataRequired()]
    )
    check_in = DateField('Check-in Date', validators=[DataRequired()], format='%Y-%m-%d')
    check_out = DateField('Check-out Date', validators=[DataRequired()], format='%Y-%m-%d')
    adults = IntegerField('Adults', validators=[DataRequired()], default=1)
    children = IntegerField('Children', validators=[Optional()], default=0)
    special_requests = TextAreaField('Special Requests', validators=[Optional()])
    
    def validate_check_out(self, field):
        if self.check_in.data and field.data:
            if field.data <= self.check_in.data:
                raise ValidationError('Check-out must be after check-in.')

class EventForm(FlaskForm):
    guest_name = StringField('Full Name', validators=[DataRequired(), Length(max=100)])
    guest_email = EmailField('Email Address', validators=[DataRequired(), Email(), Length(max=120)])
    guest_phone = TelField('Phone Number', validators=[DataRequired(), Length(max=20)])
    
    event_type = SelectField(
        'Event Type',
        choices=[
            ('', 'Select an event...'),
            ('wedding', 'Wedding'),
            ('engagement', 'Engagement'),
            ('party', 'Party'),
            ('corporate', 'Corporate Event'),
            ('other', 'Other')
        ],
        validators=[DataRequired()]
    )
    event_date = DateField('Event Date', validators=[DataRequired()], format='%Y-%m-%d')
    guest_count = IntegerField('Number of Guests', validators=[DataRequired()])
    special_requests = TextAreaField('Special Requests', validators=[Optional()])
    
    def validate_event_date(self, field):
        if field.data and field.data < date.today():
            raise ValidationError('Event date cannot be in the past.')
    
    def validate_check_out(self,field):
        """Ensure check-out is after check-in"""
        if self.check_in.data and field.data:
            if field.data <= self.check_in.data:
                raise ValidationError("check-out date must be after check in date")
            
    def vaidate_event_date(self,field):
        """Ensure event date is not in the past"""
        if field.data and field.data < date.today():
            raise ValidationError("Event date cannot be in the past.")