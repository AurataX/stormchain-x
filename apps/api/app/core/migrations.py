from sqlalchemy import inspect, text


async def migrate_observation_access(connection):
    columns = await connection.run_sync(
        lambda sync: {column["name"] for column in inspect(sync).get_columns("observations")}
    )
    if "access_status" not in columns:
        await connection.execute(
            text(
                "ALTER TABLE observations ADD COLUMN access_status VARCHAR(16) "
                "CONSTRAINT ck_observations_access "
                "CHECK (access_status IN ('OPEN','BLOCKED','UNKNOWN'))"
            )
        )
