import sys
import os
from pathlib import Path

# Add the project directory to the sys.path
path_parent = Path(__file__).parent.parent
sys.path.append(str(path_parent))

# Import settings here
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simple_shop.settings')

# Import Django and configure it
import django
django.setup()

# Import the WSGI application
from simple_shop.wsgi import application
app = application
