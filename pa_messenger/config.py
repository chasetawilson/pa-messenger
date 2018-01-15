import os


class DefaultConfig(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://mews:mews@localhost/mewsdb')
    TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
    TWILIO_NUMBER = os.environ.get('TWILIO_NUMBER')
    BASIC_AUTH_USERNAME = 'admin'
    BASIC_AUTH_PASSWORD = os.environ.get('BASIC_AUTH_PASSWORD')


class DevelopmentConfig(DefaultConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://mews:mews@localhost/mewsdb')


class TestConfig(DefaultConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://mews:mews@localhost/mewsdb')

    PRESERVE_CONTEXT_ON_EXCEPTION = False
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False


config_env_files = {
    'test': 'pa_messenger.config.TestConfig',
    'development': 'pa_messenger.config.DevelopmentConfig',
}
