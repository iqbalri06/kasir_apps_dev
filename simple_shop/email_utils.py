import os
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.utils import timezone
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def send_otp_email(email, otp, debug=False):
    """
    Send OTP email with HTML template
    
    Args:
        email: Recipient email
        otp: The OTP code
        debug: Whether to print debug information
    
    Returns:
        bool: True if successful, False otherwise
    """
    subject = "Kode Verifikasi OTP untuk Reset Password IQMart"
    
    # Prepare context for email template
    context = {
        'otp': otp,
        'email': email,
        'current_year': datetime.now().year,
        'valid_minutes': 15
    }
    
    # Render HTML message from template
    html_message = render_to_string('email/otp_email.html', context)
    plain_message = strip_tags(html_message)  # Create plain text version for clients that don't support HTML
    
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    
    try:
        # Use EmailMultiAlternatives to send both HTML and plain text
        email_message = EmailMultiAlternatives(
            subject=subject,
            body=plain_message,
            from_email=from_email,
            to=recipient_list
        )
        email_message.attach_alternative(html_message, "text/html")
        
        # Send email
        sent = email_message.send()
        
        if sent:
            logger.info(f"OTP email successfully sent to {email}")
        else:
            logger.error(f"Failed to send OTP email to {email}")
            
        return sent > 0
        
    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")
        return False
