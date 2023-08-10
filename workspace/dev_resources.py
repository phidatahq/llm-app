from os import getenv

from phi.docker.app.fastapi import FastApi
from phi.docker.app.jupyter import Jupyter
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

# -*- Dev jupyter image
jupyter_image = DockerImage(
    name=f"{ws_settings.image_repo}/{ws_settings.ws_name}-jupyter",
    tag=ws_settings.dev_env,
    enabled=(ws_settings.build_images and ws_settings.dev_jupyter_enabled),
    path=str(ws_settings.ws_root),
    dockerfile="workspace/jupyter.Dockerfile",
    pull=ws_settings.force_pull_images,
    # Uncomment to push the dev image
    # push_image=ws_settings.push_images,
    skip_docker_cache=ws_settings.skip_image_cache,
)

# -*- Dev database running on port 9315:5432
dev_db = PgVectorDb(
    name=f"{ws_settings.dev_key}-db",
    enabled=ws_settings.dev_db_enabled,
    db_user="llm",
    db_password="llm",
    db_schema="llm",
    # Connect to this db locally on port 9315
    host_port=9315,
)

# -*- Build container environment
container_env = {
    # Get the OpenAI API key from the local environment
    "OPENAI_API_KEY": getenv("OPENAI_API_KEY", None),
}
if ws_settings.dev_db_enabled:
    container_env.update(
        {
            # Database configuration
            "DB_HOST": dev_db.get_db_host(),
            "DB_PORT": dev_db.get_db_port(),
            "DB_USER": dev_db.get_db_user(),
            "DB_PASS": dev_db.get_db_password(),
            "DB_SCHEMA": dev_db.get_db_schema(),
            # Wait for database to be available before starting the application
            "WAIT_FOR_DB": ws_settings.dev_db_enabled,
        }
    )

# -*- FastApi running on port 9090
dev_fastapi = FastApi(
    name=f"{ws_settings.dev_key}-api",
    enabled=ws_settings.dev_api_enabled,
    image=dev_image,
    command="unicorn api:main:app",
    debug_mode=True,
    mount_workspace=True,
    env_vars={
        **container_env,
        "UVICORN_HOST": "0.0.0.0",
        "UVICORN_RELOAD": True,
    },
    use_cache=ws_settings.use_cache,
    # Read secrets from secrets/dev_app_secrets.yml
    secrets_file=ws_settings.ws_root.joinpath("workspace/secrets/dev_app_secrets.yml"),
)

# -*- Streamlit running on port 9095
dev_streamlit = Streamlit(
    name=f"{ws_settings.dev_key}-app",
    enabled=ws_settings.dev_app_enabled,
    image=dev_image,
    command="streamlit run app/Home.py",
    debug_mode=True,
    mount_workspace=True,
    env_vars={
        **container_env,
        "STREAMLIT_SERVER_HEADLESS": True,
    },
    use_cache=ws_settings.use_cache,
    # Read secrets from secrets/dev_app_secrets.yml
    secrets_file=ws_settings.ws_root.joinpath("workspace/secrets/dev_app_secrets.yml"),
)

# -*- Jupyter running on port 8888
dev_jupyter = Jupyter(
    name=f"{ws_settings.ws_name}-jupyter",
    enabled=ws_settings.dev_jupyter_enabled,
    image=jupyter_image,
    debug_mode=True,
    mount_workspace=True,
    env_vars=container_env,
    use_cache=ws_settings.use_cache,
    # Read secrets from secrets/dev_jupyter_secrets.yml
    secrets_file=ws_settings.ws_root.joinpath(
        "workspace/secrets/dev_jupyter_secrets.yml"
    ),
)

# -*- DockerResourceGroup defining the dev resources
dev_docker_resources = DockerResourceGroup(
    env=ws_settings.dev_env,
    network=ws_settings.ws_name,
    apps=[dev_db, dev_fastapi, dev_streamlit, dev_jupyter],
)
