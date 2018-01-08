import os


class DefaultConfig(object):
    SECRET_KEY = 'youshouldreallychangethis'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://mews:mews@localhost/mewsdb')
    TWILIO_ACCOUNT_SID = ''
    TWILIO_AUTH_TOKEN = ''
    TWILIO_NUMBER = ''
    BASIC_AUTH_USERNAME = 'admin'
    BASIC_AUTH_PASSWORD = 'SoSecret'


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
