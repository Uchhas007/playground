# from website import create_app
# import sys
# import os
# sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# from pw import app  # import your Flask app
# # Create the Flask app
# app = create_app()

# # Vercel needs a variable named `app`
# # Don't run app.run() here
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from website import create_app

app = create_app()