import os
from dotenv import load_dotenv

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-&@+xn9_zb%-=x)x4*!#fl27)+f_g&j!j40m5%42$&_f!5mj9mf'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

DATABASE_URL = 'localhost'

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)