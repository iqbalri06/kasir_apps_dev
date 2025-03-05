import sys
import os
from pathlib import Path

# Get the project root directory
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

# Add project root to Python path
sys.path.append(project_root)

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simple_shop.settings')

# Import and setup Django
import django
django.setup()

# Now import the WSGI application
from simple_shop.wsgi import application

# Create the app variable for Vercel
app = application
