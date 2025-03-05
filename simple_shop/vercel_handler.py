import os
import sys

# Get the project root directory (one level up from current file)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

# Add both directories to Python path
sys.path.insert(0, current_dir)
sys.path.insert(0, parent_dir)

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simple_shop.settings')

# Import and setup Django
import django
django.setup()

# Import the WSGI application using relative import
from wsgi import application

# Create the app variable for Vercel
app = application
