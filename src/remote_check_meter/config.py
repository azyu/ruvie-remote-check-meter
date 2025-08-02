"""Configuration management."""

import os
from typing import Any, Dict

from dotenv import load_dotenv


class ConfigurationError(Exception):
    """Configuration error exception."""


def load_config() -> Dict[str, Any]:
    """Load configuration from environment variables."""
    load_dotenv()

    # 필수 설정 확인
    base_url = os.getenv("RUVIE_BASE_URL")
    if not base_url:
        raise ConfigurationError("RUVIE_BASE_URL 환경변수가 설정되지 않았습니다.")

    meter_base_url = os.getenv("METER_BASE_URL")
    if not meter_base_url:
        raise ConfigurationError("METER_BASE_URL 환경변수가 설정되지 않았습니다.")

    return {
        "username": os.getenv("RUVIE_USERNAME"),
        "password": os.getenv("RUVIE_PASSWORD"),
        "base_url": base_url,
        "meter_base_url": meter_base_url,
        "debug": os.getenv("DEBUG", "false").lower() in ("true", "1", "yes"),
        "timeout": int(os.getenv("REQUEST_TIMEOUT", "30")),
        "retries": int(os.getenv("REQUEST_RETRIES", "3")),
    }
