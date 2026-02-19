import asyncpg

async def create_if_not_exist(_user, _database, _password, _port, _host):
    try:
        conn = await asyncpg.connect(
            host=_host,
            port=_port,
            password=_password,
            database=_database,
            user=_user,
        )
    except asyncpg.InvalidCatalogNameError:
        # if database does not exist, create it
        sys_conn = await asyncpg.connect(
            host=_host,
            port=_port,
            password=_password,
            user=_user,
        )
        await sys_conn.execute(
            f'CREATE DATABASE "{_database}" OWNER "{_user}"'
        )
        await sys_conn.close()

        # Connect to the newly created database.
        conn = await asyncpg.connect(
            host=_host,
            port=_port,
            password=_password,
            database=_database,
            user=_user,
        )

    return conn