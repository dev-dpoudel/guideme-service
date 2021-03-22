# Declare Application Level Settings
from pydantic import BaseSettings


# Declare class for Database Settings
class Database(BaseSettings):
    db_name: str = "guides"
    db_host: str = 'localhost'
    db_port: int = 21707
    db_username: str = "guide"
    db_password: str = "GuideAdmin"
    db_auth_source: str = 'admin'


# Declare a global setting
class AppSettings(Database):
    app_name: str = "GuideMe"
    default_page_size: int = 25
    in_development: bool = True
    debug_mode = True
    log_dir: str = ""
    admin_email: str = "ryon_a@hotmail.com"
    test_email: str = "dinesh.poudel_nepal@outlook.com"
    token_active_time: int = 15
    secret_key: str = ""
    algotithm: str = ""

    # Get Environmental Variables from environment files
    class Config:
        env_file = ".sysenv"
