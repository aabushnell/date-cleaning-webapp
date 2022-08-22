import os

# Statement for enabling the development environment
DEBUG = True

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Do not sorty when jsonifying
JSON_SORT_KEYS = False

# Define the database - we are working with
SQLALCHEMY_DATABASE_URI = "sqlite:///user/users.sqlite3"
SQLALCHEMY_TRACK_MODIFICATIONS = False
DATABASE_CONNECT_OPTIONS = {}

# Application threads
THREADS_PER_PAGE = 4

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for signing the data
CSRF_SESSION_KEY = "LRGproject"

# Secret key for signing cookies
SECRET_KEY = "LRGproject"
