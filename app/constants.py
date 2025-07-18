from modules.helpers import getenv
from typing import Literal
from typing import cast

EnvironmentMode = Literal["DEV", "PRD"]

env_value = getenv("ENVIRONMENT_MODE", "DEV")  # default to 'dev' if not set

if env_value not in ("DEV", "PRD"):
    raise ValueError(f"Invalid ENVIRONMENT_MODE: {env_value}")

ENVIRONMENT_MODE: EnvironmentMode = cast(EnvironmentMode, env_value)

TELEGRAM_BOT_API_KEY = (getenv("TELEGRAM_BOT_API_KEY_DEV")
    if ENVIRONMENT_MODE == "DEV"
    else getenv("TELEGRAM_BOT_API_KEY_PRD" )
)

OWNER_USER_ID = getenv("OWNER_ID")
