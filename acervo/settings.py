import os

# Configuração do laboratório local. Os dados e a chave são de demonstração.
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "chave-publica-do-laboratorio-acervo")
DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

ROOT_URLCONF = "acervo.urls"
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "reservas",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.environ.get("POSTGRES_HOST", "db"),
        "NAME": os.environ.get("POSTGRES_DB", "acervo"),
        "USER": os.environ.get("POSTGRES_USER", "acervo"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "acervo-local"),
    }
}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "UTC"
USE_TZ = True
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "reservas"
LOGOUT_REDIRECT_URL = "login"
