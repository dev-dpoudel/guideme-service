# Declare Application Level Settings
from functools import lru_cache
from pydantic import BaseSettings


# SESSION ACTIVE TIME
SESSION_TIME = 15
# JWT ALGORITHM
ALGORITHM = "HS256"
# To Generate New use  openssl rand -hex 32
SECRET_KEY = "1f2d98baf9dbd390b97a9750689297b12ea71fb6859219a797e1da111714b947"


# Declare class for Database Settings
class SessionSettings(BaseSettings):
    session_time: int = SESSION_TIME
    secret_key: str = SECRET_KEY
    algorithm: str = ALGORITHM


# Declare class for Database Settings
class DatabaseSettings(BaseSettings):
    db_name: str = "guides"
    db_host: str = 'localhost'
    db_port: int = 21707
    db_username: str = "guide"
    db_password: str = "GuideAdmin"
    db_auth_source: str = 'admin'


# Declare a global setting
class AppSettings(DatabaseSettings, SessionSettings):
    app_name: str = "GuideMe"
    default_page_size: int = 25
    in_development: bool = True
    debug_mode = True
    log_dir: str = ""
    admin_email: str = "ryon_a@hotmail.com"
    test_email: str = "dinesh.poudel_nepal@outlook.com"

    # Get Environmental Variables from environment files
    class Config:
        env_file = ".sysenv"


# Decalre Dependency for App Settings
@lru_cache(maxsize=128)
def get_settings():
    return AppSettings()
