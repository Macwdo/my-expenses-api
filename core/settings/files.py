from . import AWS_STORAGE_BUCKET_NAME, BASE_DIR, DEBUG

# Static files
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"
STATICFILES_DIRS = [
    BASE_DIR / "staticfiles"
]

# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# MEDIA_STORAGE = "django.core.files.storage.FileSystemStorage"
# STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

# Storages
if not DEBUG:
    S3_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    STORAGES = {
        "default": {
            "BACKEND": S3_FILE_STORAGE,
            "OPTIONS": {
                "bucket_name": AWS_STORAGE_BUCKET_NAME,
                "location": "media",
            },
        },
        "staticfiles": {
            "BACKEND": S3_FILE_STORAGE,
            "OPTIONS": {
                "location": "static",
            },
        },
    }
