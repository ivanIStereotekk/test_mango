from dotenv import dotenv_values
import pathlib

# ROOT DIRECTORY OF THE PROJECT
root_dir = pathlib.Path(__file__).parent.resolve()

# DOTENV FILE
config = dotenv_values(f"{root_dir}/.env")

# PARAMS FOR THE DATABASE
PG_USER = config["POSTGRES_USER"]
PG_PASS = config["POSTGRES_PASSWORD"]
PG_HOST = config["POSTGRES_HOST"]
PG_PORT = config["POSTGRES_PORT"]
PG_DB_NAME = config["POSTGRES_DB_NAME"]
# Authentication secret key
AUTH_SECRET_KEY = config["AUTH_SECRET_KEY"]

# Hidden mail address
MAIL_ADDRESS = config["MAIL_ADDRESS"]

# Telemetry and logging
SENTRY_DSN = config["SENTRY_DSN"]
SENTRY_TRACES_SAMPLE_RATE = config["SENTRY_TRACES_SAMPLE_RATE"]
OPEN_AI_API_KEY = config["OPEN_AI_API_KEY"]
OPEN_AI_ENGINE = config["OPEN_AI_ENGINE"]

# Redis TTL
REDIS_CACHING_DAY = config["REDIS_CACHING_DAY"]
REDIS_CACHING_HOUR = config["REDIS_CACHING_HOUR"]
REDIS_CACHING_MIN = config["REDIS_CACHING_MIN"]

