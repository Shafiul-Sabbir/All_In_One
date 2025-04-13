from pathlib import Path
import os
# from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

#Load our environmental variables
# load_dotenv()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-df_c!2lc37o5dwg*$nj%3yl$7zsdt@c)q%=b5dmy3do+k44+tw'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = False
# ALLOWED_HOSTS = []
ALLOWED_HOSTS = ['all_in_one.onrender.com']

# ALLOWED_HOSTS = ['allinone-production.up.railway.app', 'https://allinone-production.up.railway.app' ]
# CSRF_TRUSTED_ORIGINS = ['https://allinone-production.up.railway.app']

# the domain as ALLOWED_HOSTS has found from "public networking" under "networking" under "settings" in the main app of railway, not in database section.
# When we will work in local server we have to comment out it, and when we have to push the code in github, we have to uncomment it too.

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'store',
    'cart',
    'payment',
    'whitenoise.runserver_nostatic',
    'paypal.standard.ipn',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'ecom.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processors.cart',
            ],
        },
    },
]

WSGI_APPLICATION = 'ecom.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }


    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql',  # Explicitly define the engine
    #     'NAME': 'railway',
    #     'USER': 'postgres',
    #     'PASSWORD': os.environ['DB_PASSWORD_YO'],
    #     'HOST': 'junction.proxy.rlwy.net',
    #     'PORT': '35649',
    # }
}
# But NAME = PGDATABASE, USER = PGUSER and PASSWORD = PGPASSWORD which are defined in the "variables" section in railway database.
# This HOST and PORT are collected from "public networking" under "Settings" on Railway postgress database. In there it is found as HOST:PORT -> :PGPORT. From there we will collect the HOST and PORT



# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = ['static/']
STATIC_ROOT = BASE_DIR / 'staticfiles'

#white noise satic stuff
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# add paypal settings
# Set sandbox to true
PAYPAL_TEST = True

PAYPAL_RECEIVER_EMAIL = 'business@allinone.com' # Busines sandbox account

