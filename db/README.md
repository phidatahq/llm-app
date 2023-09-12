## Add tables to the database

Steps to create/update the database using alembic:

1. Add/update your tables in the `db/tables` directory.
2. Import the table in the `db/tables/__init__.py` file.
3. Create a database revision using: `alembic -c db/alembic.ini revision --autogenerate -m "Revision Name"`
4. Upgrade database using: `alembic -c db/alembic.ini upgrade head`

> Note: Set Env Var `MIGRATE_DB = True` to run the database migration in the entrypoint script at container startup.

## Example: Creating your first table

### Step 1: Create table definition

Create a file `db/tables/users.py` with the following content:

```python
from datetime import datetime
from typing import Optional

from sqlalchemy.sql.expression import text
from sqlalchemy.types import DateTime
from sqlalchemy.orm import Mapped, mapped_column

from db.tables.base import Base


class UsersTable(Base):
    id: Mapped[int] = mapped_column(primary_key=True,     created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=text("now()"))
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=text("now()"))
```

### Step 2: Import the table

Import the table in the `db/tables/__init__.py` file:

```python
from db.tables.base import Base
from db.tables.users import UsersTable
```

### Step 3: Creat a database revision using alembic

```bash
docker exec -it llm-dev-api zsh

alembic -c db/alembic.ini revision --autogenerate -m "Initialize DB"
```

## Step 4: Upgrade local database

```bash
docker exec -it llm-dev-api zsh

alembic -c db/alembic.ini upgrade head
```

## Upgrading the production database

1. Recommended: Set Env Var `MIGRATE_DB = True` which runs `alembic -c db/alembic.ini upgrade head` from the entrypoint script at container startup.
2. **OR** you can ssh into the production container to run the migration manually

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
