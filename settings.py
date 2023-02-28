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

