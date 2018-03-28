class Config(object):
    """
    Common configurations
    """

    # Put any configurations here that are common across all environments
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """
    Development configurations
    """

    DEBUG = True
    DEBUG_TB_ENABLED = True
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}