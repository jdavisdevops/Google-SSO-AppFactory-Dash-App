# import os
# from pathlib import Path

# basedir = Path(__file__).parent


# os.environ['DATABASE_URL'] = 'postgresql://postgres:postgres@localhost:5432/users'
# class Config:
#     DEBUG = False
#     DEVELOPMENT = False
#     TESTING = False
#     CSRF_ENABLED = True
#     SECRET_KEY = os.urandom(24)
#     SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

# class ProductionConfig(Config):
#     DEBUG = False

# class StagingConfig(Config):
#     DEVELOPEMNT = True
#     DEBUG = True

# class DevelopmentConfig(Config):
#     DEBUG = True
#     DEVELOPMENT = True
#     SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']