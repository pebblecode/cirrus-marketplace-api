import os
import codecs
from dmutils.status import enabled_since, get_version_label


class Config:

    VERSION = get_version_label(
        os.path.abspath(os.path.dirname(__file__))
    )
    DM_SEARCH_API_URL = None
    DM_SEARCH_API_AUTH_TOKEN = None
    DM_API_AUTH_TOKENS = None
    ES_ENABLED = True
    ALLOW_EXPLORER = True
    AUTH_REQUIRED = True
    DM_HTTP_PROTO = 'http'
    # Logging
    DM_LOG_LEVEL = 'DEBUG'
    DM_APP_NAME = 'api'
    DM_LOG_PATH = '/var/log/digitalmarketplace/application.log'
    DM_REQUEST_ID_HEADER = 'DM-Request-ID'
    DM_DOWNSTREAM_REQUEST_ID_HEADER = 'X-Amz-Cf-Id'
    ORDER_BUYER_FROM_EMAIL = "donotreply@inoket.com"
    ORDER_BUYER_FROM_NAME = "Inoket Orders Management"
    ORDER_SUPPLIER_FROM_EMAIL = "donotreply@inoket.com"
    ORDER_SUPPLIER_FROM_NAME = "Inoket Orders Management"

    # Feature Flags
    RAISE_ERROR_ON_MISSING_FEATURES = True

    FEATURE_FLAGS_TRANSACTION_ISOLATION = False

    DM_API_SERVICES_PAGE_SIZE = 100
    DM_API_SUPPLIERS_PAGE_SIZE = 100
    DM_API_BRIEFS_PAGE_SIZE = 100
    DM_API_BRIEF_RESPONSES_PAGE_SIZE = 100
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/digitalmarketplace'

    DM_FAILED_LOGIN_LIMIT = 5

    @staticmethod
    def init_app(application):
        with codecs.open('email_templates/inoket-order-buyer.html', 'r', encoding='utf-8') as f:
            buyer_template = f.read()
        application.config['email_templates'] = {}
        application.config['email_templates']['buyer_order_received'] = buyer_template

class Test(Config):
    DM_SEARCH_API_AUTH_TOKEN = 'test'
    DM_SEARCH_API_URL = 'http://localhost'
    DEBUG = True
    ES_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://test:test@localhost/inoket_test'
    DM_API_AUTH_TOKENS = 'myToken'
    DM_API_SERVICES_PAGE_SIZE = 5
    DM_API_SUPPLIERS_PAGE_SIZE = 5
    DM_API_BRIEFS_PAGE_SIZE = 5
    DM_API_BRIEF_RESPONSES_PAGE_SIZE = 5
    FEATURE_FLAGS_TRANSACTION_ISOLATION = enabled_since('2015-08-27')


class Development(Config):
    DEBUG = True

    DM_API_AUTH_TOKENS = 'myToken'
    DM_SEARCH_API_AUTH_TOKEN = 'myToken'
    DM_SEARCH_API_URL = 'http://localhost:5001'


class Live(Config):
    """Base config for deployed environments"""
    DEBUG = False
    ALLOW_EXPLORER = False
    DM_HTTP_PROTO = 'https'


class Preview(Live):
    FEATURE_FLAGS_TRANSACTION_ISOLATION = enabled_since('2015-08-27')


class Staging(Live):
    pass


class Production(Live):
    pass


configs = {
    'development': Development,
    'test': Test,

    'preview': Development,
    'staging': Staging,
    'production': Production,
}
