from pathlib import Path
from dotenv import load_dotenv
import os
from datetime import timedelta
import sys

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# ====================================================
# Configurações de Segurança
# ====================================================
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'default-unsafe-key')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1').split(',')

ROOT_URLCONF = 'app.urls'

# ====================================================
# Configurações de Aplicações
# ====================================================
INSTALLED_APPS = [
    # Apps Django padrão
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django_extensions',
    'simple_history',
    
    # Apps de Negócio
    'app',              # App principal
    'tenants',          # Gerencia os tenants
    'subscriptions',    # Gerencia planos de assinatura
    'authentication',   # Gerencia usuários e autenticação
]

# ====================================================
# Configurações dos arquivos estpaticos do projeto
# ====================================================

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# ====================================================
# Configurações de Banco de Dados
# ====================================================

# Verifica se está rodando localmente
if "test" in sys.argv or os.getenv("USE_SQLITE", "False") == "True":
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('POSTGRES_DB_NAME', 'prod_db'),
            'USER': os.getenv('POSTGRES_USER', 'postgres'),
            'PASSWORD': os.getenv('POSTGRES_PASSWORD', ''),
            'HOST': os.getenv('POSTGRES_HOST', 'localhost'),
            'PORT': os.getenv('POSTGRES_PORT', '5432'),
        }
    }


# ====================================================
# Configurações de Middleware
# ====================================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'app.middleware.TenantContextMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'app.middleware.LastListViewMiddleware',
]

# ====================================================
# Configurações de Autenticação
# ====================================================
AUTH_USER_MODEL = 'authentication.CustomUser'

AUTHENTICATION_BACKENDS = [
    'authentication.backends.TenantAwareBackend',  # Para autenticação com tenant
    'django.contrib.auth.backends.ModelBackend',   # Padrão do Django
]

LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = '/index'  # Após login, o usuário será redirecionado para a Home
LOGOUT_REDIRECT_URL = "/login/"  # Após logout, redireciona para a tela de login

# ====================================================
# Configurações de Internacionalização
# ====================================================
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_L10N = True
USE_TZ = True

DATE_INPUT_FORMATS = ['%d/%m/%Y']

LOCALE_PATHS = [
    os.path.join(BASE_DIR, "locale"),
]

# ====================================================
# Configurações Gerais
# ====================================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ====================================================
# Configurações do Django REST Framework
# ====================================================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ('rest_framework_simplejwt.authentication.JWTAuthentication',),
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',),
}

# ====================================================
# Configurações dos Templates Django
# ====================================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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


# ====================================================
# Configurações de JWT
# ====================================================
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

