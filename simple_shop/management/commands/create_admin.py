from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from simple_shop.models import Role
import uuid
import os

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates a new admin user for IQMart with specified email or default credentials'

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, help='Email for the admin user')
        parser.add_argument('--username', type=str, help='Username for the admin user')
        parser.add_argument('--password', type=str, help='Password for the admin user')
        parser.add_argument('--force', action='store_true', help='Force create even if user exists')

    def handle(self, *args, **options):
        email = options.get('email') or 'rosealc02@gmail.com'
        username = options.get('username') or 'iqbalir'
        password = options.get('password') or 'iqbal'
        force = options.get('force', False)
        
        # Get admin role (handle the multiple roles issue)
        try:
            admin_role = Role.objects.filter(name='Admin').first()
            if not admin_role:
                admin_role = Role.objects.create(name='Admin')
                self.stdout.write(self.style.SUCCESS('Admin role created successfully'))
            else:
                self.stdout.write(self.style.SUCCESS('Using existing Admin role'))
                
            # Report duplicate roles if they exist
            admin_roles_count = Role.objects.filter(name='Admin').count()
            if admin_roles_count > 1:
                self.stdout.write(self.style.WARNING(
                    f'Warning: There are {admin_roles_count} Admin roles in the system. '
                    f'Consider cleaning up the database.'
                ))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error getting/creating Admin role: {str(e)}'))
            return
        
        # Check for existing user
        existing_email = User.objects.filter(email=email).exists()
        existing_username = User.objects.filter(username=username).exists()
        
        if existing_email and not force:
            self.stdout.write(self.style.WARNING(f'User with email {email} already exists. Use --force to override.'))
            return
        
        if existing_username and not force:
            self.stdout.write(self.style.WARNING(f'User with username {username} already exists. Use --force to override.'))
            return
            
        # If forcing creation with existing user, update instead of create
        if (existing_email or existing_username) and force:
            user = None
            if existing_email:
                user = User.objects.get(email=email)
            elif existing_username:
                user = User.objects.get(username=username)
                
            user.username = username
            user.email = email
            user.set_password(password)
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            user.role = admin_role
            user.save()
            
            self.stdout.write(self.style.SUCCESS(f'Existing user updated with admin privileges'))
            
        else:
            # Create new admin user
            try:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    is_staff=True,
                    is_superuser=True,
                    is_active=True
                )
                
                # Set role to Admin
                user.role = admin_role
                user.save()
                
                self.stdout.write(self.style.SUCCESS('New admin user created successfully'))
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating user: {str(e)}'))
                return
        
        self.stdout.write(self.style.SUCCESS(f'''
        =======================================================
        Admin user ready!
        =======================================================
        Username: {username}
        Email: {email}
        Password: {password}
        =======================================================
        You can now log in with these credentials.
        '''))
