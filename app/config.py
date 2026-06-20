import os
from dotenv import load_dotenv

load_dotenv()


def get_required_env(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise RuntimeError(
            f"Required environment variable '{name}' is missing."
        )

    return value


# ==========================================
# Required Configuration
# ==========================================

QDRANT_URL: str = get_required_env(
    "QDRANT_URL"
)

QDRANT_API_KEY: str = get_required_env(
    "QDRANT_API_KEY"
)

GOOGLE_API_KEY: str = get_required_env(
    "GOOGLE_API_KEY"
)


# ==========================================
# Optional Configuration
# ==========================================

CORS_ORIGINS: list[str] = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:3000"
).split(",")