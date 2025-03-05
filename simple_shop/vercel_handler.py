import os
import sys
from pathlib import Path

def init_django():
    try:
        # Set up paths
        current_dir = Path(__file__).resolve().parent
        project_root = current_dir.parent
        sys.path.insert(0, str(project_root))
        
        # Configure Django
        os.environ['VERCEL'] = '1'
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simple_shop.settings')
        
        import django
        django.setup()
        
        return True
    except Exception as e:
        print(f"Django initialization error: {e}")
        return False

def create_app():
    if not init_django():
        from http.server import BaseHTTPRequestHandler, HTTPServer
        def error_app(environ, start_response):
            start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
            return [b'Internal Server Error: Django initialization failed']
        return error_app
    
    try:
        from django.core.wsgi import get_wsgi_application
        return get_wsgi_application()
    except Exception as e:
        print(f"WSGI application error: {e}")
        def error_app(environ, start_response):
            start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
            return [b'Internal Server Error: WSGI application failed']
        return error_app

app = create_app()
