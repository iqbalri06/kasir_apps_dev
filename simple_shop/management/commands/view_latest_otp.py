from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime
from simple_shop.email_utils import get_latest_otp

class Command(BaseCommand):
    help = 'View the latest OTP sent for debugging purposes'

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, help='Filter by specific email')

    def handle(self, *args, **options):
        email = options.get('email')
        
        otp_info = get_latest_otp(email)
        
        if not otp_info:
            self.stdout.write(self.style.WARNING('No OTP records found'))
            return
            
        self.stdout.write(self.style.SUCCESS(f"""
=======================================================
LATEST OTP INFO
=======================================================
Email: {otp_info['email']}
OTP Code: {otp_info['otp']}
Timestamp: {otp_info['timestamp']}
=======================================================
        """))
        
        # Check if the OTP is still valid (15 minutes)
        try:
            timestamp = datetime.strptime(otp_info['timestamp'], '%Y-%m-%d %H:%M:%S')
            now = timezone.now().replace(tzinfo=None)
            time_diff = now - timestamp
            
            if time_diff.total_seconds() > 15*60:
                self.stdout.write(self.style.WARNING(f'⚠️ OTP sudah kedaluwarsa ({time_diff.total_seconds()/60:.1f} menit)'))
            else:
                self.stdout.write(self.style.SUCCESS(f'✓ OTP masih berlaku ({15-(time_diff.total_seconds()/60):.1f} menit tersisa)'))
        except:
            pass
