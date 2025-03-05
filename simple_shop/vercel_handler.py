import os
import sys
from pathlib import Path

# Basic setup
os.environ['VERCEL'] = '1'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simple_shop.settings')

# Optimize Python path
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(current_dir))

def get_application():
    try:
        import django
        django.setup()
        from django.core.wsgi import get_wsgi_application
        return get_wsgi_application()
    except Exception as e:
        from django.http import JsonResponse
        return lambda env, start_response: JsonResponse(
            {"error": str(e)}, status=500
        )(env, start_response)

# Initialize app only once
app = get_application()
