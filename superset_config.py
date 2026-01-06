# The internal database for Superset's metadata
SQLALCHEMY_DATABASE_URI = "postgresql://cafe_user:cafe_pass@postgres:5432/cafe"
SECRET_KEY = "super_secret_cafe_key_123"
TALISMAN_ENABLED = False # Helpful for local on-prem setups
WTF_CSRF_ENABLED = False # Simplifies local testing