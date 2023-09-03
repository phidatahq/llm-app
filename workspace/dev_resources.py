from os import getenv

from phi.docker.app.fastapi import FastApi
from phi.docker.app.postgres import PgVectorDb
from phi.docker.app.streamlit import Streamlit
from phi.docker.resource.image import DockerImage
from phi.docker.resource.group import DockerResourceGroup

from workspace.settings import ws_settings

#
# -*- Resources for the Development Environment
#

# -*- Dev application image
dev_image = DockerImage(
    name=f"{ws_settings.image_repo}/{ws_settings.ws_name}",
    tag=ws_settings.dev_env,
    enabled=ws_settings.build_images,
    path=str(ws_settings.ws_root),
    pull=ws_settings.force_pull_images,
    # Uncomment to push the dev image
    # push_image=ws_settings.push_images,
    skip_docker_cache=ws_settings.skip_image_cache,
)

# -*- Dev database running on port 5432:5432
dev_db = PgVectorDb(
    name=f"{ws_settings.dev_key}-db",
    enabled=ws_settings.dev_db_enabled,
    db_user="llm",
    db_password="llm",
    db_schema="llm",
)

# -*- Build container environment
container_env = {
    # Get the OpenAI API key from the local environment
    "OPENAI_API_KEY": getenv("OPENAI_API_KEY"),
    # Database configuration
    "DB_HOST": dev_db.get_db_host(),
    "DB_PORT": dev_db.get_db_port(),
    "DB_USER": dev_db.get_db_user(),
    "DB_PASS": dev_db.get_db_password(),
    "DB_SCHEMA": dev_db.get_db_schema(),
    # Wait for database to be available before starting the application
    "WAIT_FOR_DB": ws_settings.dev_db_enabled,
}

# -*- FastApi running on port 9090
dev_fastapi = FastApi(
    name=f"{ws_settings.dev_key}-api",
    enabled=ws_settings.dev_api_enabled,
    image=dev_image,
    command="uvicorn api.main:app --reload",
    debug_mode=True,
    mount_workspace=True,
    env_vars=container_env,
    use_cache=ws_settings.use_cache,
    # Read secrets from secrets/dev_app_secrets.yml
    secrets_file=ws_settings.ws_root.joinpath("workspace/secrets/dev_app_secrets.yml"),
    depends_on=[dev_db],
)

# -*- Streamlit running on port 9095
dev_streamlit = Streamlit(
    name=f"{ws_settings.dev_key}-app",
    enabled=ws_settings.dev_app_enabled,
    image=dev_image,
    command="streamlit run app/Home.py",
    debug_mode=True,
    mount_workspace=True,
    streamlit_server_headless=True,
    env_vars=container_env,
    use_cache=ws_settings.use_cache,
    # Read secrets from secrets/dev_app_secrets.yml
    secrets_file=ws_settings.ws_root.joinpath("workspace/secrets/dev_app_secrets.yml"),
    depends_on=[dev_db],
)

# -*- DockerResourceGroup defining the dev docker resources
dev_docker_resources = DockerResourceGroup(
    env=ws_settings.dev_env,
    network=ws_settings.ws_name,
    apps=[dev_db, dev_fastapi, dev_streamlit],
)
