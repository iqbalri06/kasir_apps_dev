# Add WeasyPrint logging
import logging
logging.getLogger('weasyprint').addHandler(logging.StreamHandler())
