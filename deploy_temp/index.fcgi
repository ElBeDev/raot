#!/usr/bin/env python3
import os
import sys
import logging

# Set up logging
logging.basicConfig(
    filename='django_error.log',
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] - %(message)s',
)

try:
    logging.info("Starting FastCGI script")
    
    # Add the current directory to Python path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    logging.info(f"Current directory: {current_dir}")
    
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    # Set Django settings
    os.environ['DJANGO_SETTINGS_MODULE'] = 'raotproject.production_settings'
    logging.info(f"Settings module: {os.environ['DJANGO_SETTINGS_MODULE']}")
    
    # Try to import Django
    logging.info("Importing Django WSGI application")
    from django.core.wsgi import get_wsgi_application
    
    # Import flup for FastCGI
    logging.info("Importing flup WSGI server")
    from flup.server.fcgi import WSGIServer
    
    # Run the WSGI application with flup
    logging.info("Starting WSGI server")
    WSGIServer(get_wsgi_application()).run()
    
except Exception as e:
    logging.error(f"Error in FastCGI script: {str(e)}")
    logging.error(f"Python version: {sys.version}")
    logging.error(f"Python path: {sys.path}")
    
    import traceback
    logging.error(traceback.format_exc())