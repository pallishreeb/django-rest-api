
import os
from pathlib import Path
import boto3
from dotenv import load_dotenv
from secretStore.get_secret import get_secret

# Retrieve secrets from AWS Secrets Manager
# secrets = get_secret("ec2-apis", "ap-south-1")

# Load environment variables from .env file
load_dotenv()
IS_DEV = False
IS_PROD = True

# Function to fetch secrets based on environment
def fetch_secrets():
    if IS_DEV:
        # Local development environment
        return {
            'AWS_ACCESS_KEY_ID': os.getenv('AWS_ACCESS_KEY_ID'),
            'AWS_SECRET_ACCESS_KEY': os.getenv('AWS_SECRET_ACCESS_KEY'),
            'AWS_STORAGE_BUCKET_NAME': os.getenv('AWS_STORAGE_BUCKET_NAME'),
            'AWS_S3_REGION_NAME': os.getenv('AWS_S3_REGION_NAME'),
            # Add other local development secrets as needed
        }
    elif IS_PROD:
        # Production environment - fetch secrets from AWS Secrets Manager
        secrets = get_secret("ec2-apis", "ap-south-1")
        return {
            'AWS_ACCESS_KEY_ID': secrets['AWS_ACCESS_KEY_ID'],
            'AWS_SECRET_ACCESS_KEY': secrets['AWS_SECRET_ACCESS_KEY'],
            'AWS_STORAGE_BUCKET_NAME': secrets['AWS_STORAGE_BUCKET_NAME'],
            'AWS_S3_REGION_NAME': secrets['AWS_S3_REGION_NAME'],
            # Add other production secrets as needed
        }

# Retrieve secrets based on environment
secrets = fetch_secrets()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET_KEY = os.getenv('SECRET_KEY', 'your_default_secret_key')
# DEBUG = os.getenv('DEBUG', 'False').lower() in ['true', '1', 't']

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-3)3mvz4ex@^h$e^@1jbv3*!_e!&f#9k+py)+u58ee_81qd=2ov'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    '15.207.54.50',  # replace this with your EC2 public IP address
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'books',
    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bookstore.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'bookstore.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# AWS settings (for static and media files)
if IS_DEV:
    AWS_ACCESS_KEY_ID = secrets.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = secrets.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = secrets.get('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = secrets.get('AWS_S3_REGION_NAME')
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
    AWS_DEFAULT_ACL = None
    DEFAULT_FILE_STORAGE = 'bookstore.storage_backends.MediaStorage'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
else:  # IS_PROD
    AWS_ACCESS_KEY_ID = secrets['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = secrets['AWS_SECRET_ACCESS_KEY']
    AWS_STORAGE_BUCKET_NAME = secrets['AWS_STORAGE_BUCKET_NAME']
    AWS_S3_REGION_NAME = secrets['AWS_S3_REGION_NAME']
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
    AWS_DEFAULT_ACL = None
    DEFAULT_FILE_STORAGE = 'bookstore.storage_backends.MediaStorage'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'


# AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
# AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
# AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME')
# AWS_S3_CUSTOM_DOMAIN = f'book-store-api.s3.amazonaws.com'
# AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
# AWS_DEFAULT_ACL = None

# DEFAULT_FILE_STORAGE = 'bookstore.storage_backends.MediaStorage'

# MEDIA_URL = f'https://book-store-api.s3.amazonaws.com/media/'


# AWS_ACCESS_KEY_ID = secrets['AWS_ACCESS_KEY_ID']
# AWS_SECRET_ACCESS_KEY = secrets['AWS_SECRET_ACCESS_KEY']
# AWS_STORAGE_BUCKET_NAME = secrets['AWS_STORAGE_BUCKET_NAME']
# AWS_S3_REGION_NAME = secrets['AWS_S3_REGION_NAME']
# AWS S3 Settings
# AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
# AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
# AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME')  # e.g., us-west-2

# AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
# AWS_LOCATION = 'media'

# MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'