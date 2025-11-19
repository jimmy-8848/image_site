import os

DB_USERNAME = os.environ.get("DB_USERNAME", "test")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "test")
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "3306")
DB_NAME = os.environ.get("DB_NAME", "imageshare")

SQLALCHEMY_DATABASE_URI = (
    f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
