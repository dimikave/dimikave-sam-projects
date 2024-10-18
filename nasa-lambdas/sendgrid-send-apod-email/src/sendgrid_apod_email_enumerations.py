from enum import Enum


class APODResponseKeys(Enum):
    """
    Enumeration containing APOD Response related keys
    """

    TITLE = "title"
    URL = "url"
    EXPLANATION = "explanation"
    DATE = "date"
    COPYRIGHT = "copyright"
    MEDIA_TYPE = "media_type"
    SERVICE_VERSION = "service_version"
    HD_URL = "hdurl"  # Optional key if HD version exists


class GPTKeys(Enum):
    """
    Enumeration containing GPT related keys
    """

    MODEL = "model"
    MESSAGES = "messages"
    MESSAGE = "message"
    ROLE = "role"
    USER = "user"
    CONTENT = "content"
    MAX_TOKENS = "max_tokens"
    CHOICES = "choices"


class S3Keys(Enum):
    """
    Enumeration containing S3 related keys
    """

    RECIPIENTS_KEY = "recipients"
    BODY = "Body"
    UTF_8 = "utf-8"
