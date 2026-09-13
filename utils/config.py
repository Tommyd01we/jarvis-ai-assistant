class Config:
    """Configuration settings for Jarvis AI"""
    
    MODEL_LEARNING_RATE = 0.1
    MODEL_ITERATIONS = 100
    MODEL_BATCH_SIZE = 32
    
    MAX_INTERACTION_HISTORY = 10000
    MAX_CONTEXT_SIZE = 100
    MAX_KNOWLEDGE_BASE_SIZE = 50000
    
    RESPONSE_TIMEOUT = 30
    MAX_RETRY_ATTEMPTS = 3
    
    LOG_LEVEL = 'INFO'
    LOG_FILE = 'logs/jarvis.log'
    LOG_MAX_BYTES = 10485760
    LOG_BACKUP_COUNT = 5
    
    ENABLE_LEARNING = True
    ENABLE_AUTO_SAVE = True
    ENABLE_FEEDBACK_PROCESSING = True
    AUTO_SAVE_INTERVAL = 300
    
    USE_CACHE = True
    CACHE_TTL = 3600
    ENABLE_ASYNC = False
    
    DATA_DIR = 'data'
    MODEL_DIR = 'models'
    LOG_DIR = 'logs'
    
    @classmethod
    def get_config(cls, key: str, default=None):
        return getattr(cls, key, default)
    
    @classmethod
    def update_config(cls, key: str, value):
        setattr(cls, key, value)
