from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-*1lf3u*@)e^0=*28+tsw0f*%%h$801mf^rf486%0_!g@2y&ekq"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]


try:
    from .local import *
except ImportError:
    pass
