from flask import current_app
from datetime import datetime
from .models import Setting

def send_whatsapp_booking_alert(booking):
    from flask import current_app
from twilio.rest import Client

def send_whatsapp_booking_alert(booking):
    """
    Send WhatsApp alert to staff when a new booking is made.
    Returns True if sent successfully, False otherwise.
    """
    twilio_enabled = Setting.query.filter_by(key='twilio_enabled').first()
    if not twilio_enabled or twilio_enabled.value != 'true':
        return False
    account_sid = current_app.config.get('TWILIO_ACCOUNT_SID')
    auth_token = current_app.config.get('TWILIO_AUTH_TOKEN')
    from_number = current_app.config.get('TWILIO_WHATSAPP_FROM')
    to_number = current_app.config.get('STAFF_PHONE')
    
    
    if not all([account_sid, auth_token, from_number, to_number]):
        print(f"[TWILIO DISABLED] Booking #{booking.id} saved. No notification sent.")
        return False
    
    try:
        client = Client(account_sid, auth_token)
        
       
        if booking.booking_type == 'accommodation':
            details = f"""Room: {booking.room_type.replace('_', ' ').title()}
Check-in: {booking.check_in.strftime('%d %b %Y')}
Check-out: {booking.check_out.strftime('%d %b %Y')}
Adults: {booking.adults}"""
            if booking.children:
                details += f"\nChildren: {booking.children}"
        else:
            details = f"""Event: {booking.event_type.title()}
Event Date: {booking.check_in.strftime('%d %b %Y')}
Guests: {booking.guest_count}"""
        
        message_body = f""" NEW BOOKING - Lemook Gardens

Guest: {booking.guest_name}
Email: {booking.guest_email}
Phone: {booking.guest_phone}
Type: {booking.booking_type.title()}

{details}

Special Requests: {booking.special_requests or 'None'}

View in admin: {current_app.config.get('BASE_URL', 'http://localhost:5000')}/admin/dashboard
"""
        
        message = client.messages.create(
            from_=from_number,
            to=to_number,
            body=message_body
        )
        
        print(f"[TWILIO] Booking #{booking.id} notification sent. SID: {message.sid}")
        return True
        
    except Exception as e:
        print(f"[TWILIO ERROR] {e}")
        return False
        