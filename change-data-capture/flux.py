import os
import time
import redis
from pymysqlreplication import BinLogStreamReader
from pymysqlreplication.row_event import (
    WriteRowsEvent,
    UpdateRowsEvent,
    DeleteRowsEvent,
)

cache_host = os.environ.get("CACHE_HOST", "redis")
cache_port = int(os.environ.get("CACHE_PORT", 6379))

redis_client = redis.Redis(host=cache_host, port=cache_port)


def get_cache_connection():
    return redis_client


def invalidate_cache(cache_key):
    redis_client.delete(cache_key)


MYSQL_SETTINGS = {
    "host": os.environ["DB_HOST"],
    "port": 3306,
    "user": os.environ["DB_USER"],
    "passwd": os.environ["DB_PASSWORD"],
}


def main():

    stream = BinLogStreamReader(
        connection_settings=MYSQL_SETTINGS,
        only_events=[DeleteRowsEvent, WriteRowsEvent, UpdateRowsEvent],
        server_id=100,
        blocking=True,
    )

    for binlogevent in stream:
        for row in binlogevent.rows:
            if isinstance(binlogevent, DeleteRowsEvent):
                vals = row["values"]
            elif isinstance(binlogevent, UpdateRowsEvent):
                vals = row["after_values"]
            elif isinstance(binlogevent, WriteRowsEvent):
                vals = row["values"]
            print(vals, binlogevent)
            cache_key = f"{binlogevent.table}:{vals['id']}"
            redis.invalidate_cache(cache_key)
            print(f"Invalidated {cache_key}")
    stream.close()


if __name__ == "__main__":
    print("Change data capture started")
    main()
