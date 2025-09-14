"""
Django settings for LibraryProject project.

1. Purpose

The Django application has been configured to enforce secure HTTPS connections and implement key security measures to protect against common web vulnerabilities such as XSS, CSRF, clickjacking, and cookie interception.

2. HTTPS Enforcement

SECURE_SSL_REDIRECT = True: Redirects all HTTP requests to HTTPS to ensure encrypted communication.

HSTS (HTTP Strict Transport Security):

SECURE_HSTS_SECONDS = 31536000 → Browsers will only access the site via HTTPS for 1 year.

SECURE_HSTS_INCLUDE_SUBDOMAINS = True → Applies HSTS to all subdomains.

SECURE_HSTS_PRELOAD = True → Allows inclusion in browser preload lists.

Note: For local development on http://127.0.0.1:8000, HTTPS redirects can be disabled to avoid certificate issues.

3. Secure Cookies

SESSION_COOKIE_SECURE = True → Ensures session cookies are only transmitted over HTTPS.

CSRF_COOKIE_SECURE = True → Ensures CSRF cookies are only transmitted over HTTPS.

SESSION_COOKIE_HTTPONLY & CSRF_COOKIE_HTTPONLY → Prevent JavaScript access to cookies, mitigating XSS risks.

4. Secure Headers

X_FRAME_OPTIONS = 'DENY' → Prevents clickjacking by disallowing framing.

SECURE_CONTENT_TYPE_NOSNIFF = True → Prevents browsers from MIME-type sniffing responses.

SECURE_BROWSER_XSS_FILTER = True → Enables browser XSS filters to mitigate reflected XSS attacks.

5. Content Security Policy (CSP)

Configured via django-csp middleware with restrictive defaults:

Only scripts, styles, and resources from 'self' are allowed.

Frames and objects are disallowed.

Images can load from 'self' and data: URIs.

6. Review Notes

Local Development:

SECURE_SSL_REDIRECT and secure cookies can be temporarily disabled.

Self-signed certificates or runserver_plus can be used to test HTTPS locally.

Production:

Ensure ALLOWED_HOSTS includes your domain.

Web server (Nginx/Apache) should have valid SSL/TLS certificates installed.

Verify that HSTS, secure cookies, headers, and CSP are active via browser dev tools.

Testing:

Check that all forms have {% csrf_token %}.

Attempt HTTP access to confirm redirection to HTTPS.

Inspect cookies and headers to ensure flags (Secure, HttpOnly) are set.

Test CSP using the browser console to ensure no unsafe sources are loaded.
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-u)1_pdn_7s#y14o3rtn4(p6*lqq0rsc4f207nce5utw^zsu5wn'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bookshelf',
    'relationship_app',
    'csp',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'csp.middleware.CSPMiddleware',
]

ROOT_URLCONF = 'LibraryProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'LibraryProject.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model
AUTH_USER_MODEL = 'bookshelf.CustomUser'

# ------------------------------
# HTTPS and Security Settings
# ------------------------------

# Redirect all HTTP requests to HTTPS
SECURE_SSL_REDIRECT = True

# HSTS (1 year) to force HTTPS in browsers
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# ------------------------------
# Secure Cookies
# ------------------------------

SESSION_COOKIE_SECURE = True          # Session cookie only over HTTPS
CSRF_COOKIE_SECURE = True             # CSRF cookie only over HTTPS
SESSION_COOKIE_HTTPONLY = True        # Prevent JavaScript access
CSRF_COOKIE_HTTPONLY = True           # Prevent JavaScript access

# ------------------------------
# Secure HTTP Headers
# ------------------------------

X_FRAME_OPTIONS = 'DENY'              # Prevent clickjacking
SECURE_CONTENT_TYPE_NOSNIFF = True    # Prevent MIME-type sniffing
SECURE_BROWSER_XSS_FILTER = True      # Enable browser XSS filter

# ------------------------------
# Content Security Policy (CSP)
# ------------------------------

CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'",)
CSP_STYLE_SRC = ("'self'",)
CSP_IMG_SRC = ("'self'", "data:")
CSP_FONT_SRC = ("'self'",)
CSP_CONNECT_SRC = ("'self'",)
CSP_FRAME_SRC = ("'none'",)
CSP_OBJECT_SRC = ("'none'",)