import os
import sys
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Import User model
from django.contrib.auth import get_user_model
User = get_user_model()

print("\n=== USER MODEL INSPECTION ===\n")
print(f"User model class: {User.__name__}")
print(f"User model module: {User.__module__}")

# Print available fields
print("\nAvailable User model fields:")
for field in User._meta.get_fields():
    print(f" - {field.name} ({field.__class__.__name__})")

# Print field details
print("\nField details:")
for field in User._meta.fields:
    print(f" - {field.name}: {field.get_internal_type()}")

# Try to see if the User model has role relationship
print("\nChecking for role field:")
has_role = False
try:
    role_field = User._meta.get_field('role')
    has_role = True
    print(f" - Found role field: {role_field.__class__.__name__}")
    if hasattr(role_field, 'related_model'):
        print(f" - Related model: {role_field.related_model.__name__}")
except Exception as e:
    print(f" - No role field found: {str(e)}")

# Let's try to create a minimal working form with just username
print("\nAttempting to create UserForm with only username:")
try:
    from django import forms
    
    class MinimalUserForm(forms.ModelForm):
        class Meta:
            model = User
            fields = ['username']
            
    print(" - Success! MinimalUserForm created with only username field")
except Exception as e:
    print(f" - Failed: {str(e)}")

print("\n=== INSPECTION COMPLETE ===\n")
