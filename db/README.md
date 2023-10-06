## Add tables to the database

Steps to create/update the database using alembic:

1. Add/update your tables in the `db/tables` directory.
2. Import the table in the `db/tables/__init__.py` file.
3. Create a database revision using: `alembic -c db/alembic.ini revision --autogenerate -m "Revision Name"`
4. Upgrade database using: `alembic -c db/alembic.ini upgrade head`

> Note: Set Env Var `MIGRATE_DB = True` to run the database migration in the entrypoint script at container startup.

## Creat a database revision using alembic

SSH into the dev container to run the alembic command to create a database migration.

```bash
docker exec -it llm-dev-api zsh

alembic -c db/alembic.ini revision --autogenerate -m "Initialize DB"
```

## Upgrade development database

SSH into the dev container to run the alembic command to upgrade the database.

```bash
docker exec -it llm-dev-api zsh

alembic -c db/alembic.ini upgrade head
```

## Upgrade production database

1. Recommended: Set Env Var `MIGRATE_DB = True` which runs `alembic -c db/alembic.ini upgrade head` from the entrypoint script at container startup.
2. **OR** you can SSH into the production container to run the migration manually

```bash
ECS_CLUSTER=llm-prd-cluster
TASK_ARN=$(aws ecs list-tasks --cluster phi-api-prd --query "taskArns[0]" --output text)
CONTAINER_NAME=llm-prd

aws ecs execute-command --cluster $ECS_CLUSTER \
    --task $TASK_ARN \
    --container $CONTAINER_NAME \
    --interactive \
    --command "zsh"
```

```bash
alembic -c db/alembic.ini upgrade head
```

---

## How to create the migrations directory

> This has already been run and is described here for completeness

```bash
docker exec -it llm-dev-api zsh

cd db
alembic init migrations
```

- After running the above commands, the `db/migrations` directory should be created.
- Update `alembic.ini`
  - set `script_location = db/migrations`
  - uncomment `black` hook in `[post_write_hooks]`
- Update `migrations/env.py` file following [this link](https://alembic.sqlalchemy.org/en/latest/autogenerate.html)
