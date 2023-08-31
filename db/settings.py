from typing import Optional

from pydantic_settings import BaseSettings

from workspace.dev_resources import dev_db
from utils.log import logger


class DbSettings(BaseSettings):
    """Database settings that can be set using environment variables.

    Reference: https://docs.pydantic.dev/latest/usage/pydantic_settings/
    """

    # Database configuration
    db_host: Optional[str] = None
    db_port: Optional[int] = None
    db_user: Optional[str] = None
    db_pass: Optional[str] = None
    db_schema: Optional[str] = None
    db_driver: str = "postgresql+psycopg"
    # Create/Upgrade database on startup using alembic
    upgrade_db: bool = False

    def get_db_url(self) -> str:
        url = "{}://{}{}@{}:{}/{}".format(
            self.db_driver,
            self.db_user,
            f":{self.db_pass}" if self.db_pass else "",
            self.db_host,
            self.db_port,
            self.db_schema,
        )
        # Use local database if db_host is None
        if "None" in url:
            logger.debug("Using local database")
            return dev_db.get_db_connection_local()
        return url


# Create DbSettings object
db_settings = DbSettings()
