import logging
import os
import random
import time
from datetime import datetime, timedelta, timezone
from decimal import Decimal

import psycopg


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "postgres"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "dbname": os.getenv("DB_NAME", "retail"),
    "user": os.getenv("DB_USER", "retail_user"),
    "password": os.getenv("DB_PASSWORD", "retail_password"),
}
INTERVAL_SECONDS = int(os.getenv("ETL_INTERVAL_SECONDS", "10"))
BATCH_SIZE = int(os.getenv("ETL_BATCH_SIZE", "8"))

CATALOG = {
    "Electronics": [
        ("Wireless Headphones", Decimal("89.90")),
        ("Mechanical Keyboard", Decimal("119.00")),
        ("USB-C Hub", Decimal("49.90")),
    ],
    "Home": [
        ("Coffee Maker", Decimal("79.00")),
        ("Desk Lamp", Decimal("39.50")),
        ("Air Purifier", Decimal("159.00")),
    ],
    "Office": [
        ("Notebook Pack", Decimal("14.90")),
        ("Ergonomic Chair", Decimal("249.00")),
        ("Monitor Stand", Decimal("64.90")),
    ],
}
REGIONS = ["Central", "East", "North", "South", "West"]


def make_order(created_at=None):
    category = random.choice(list(CATALOG))
    product, unit_price = random.choice(CATALOG[category])
    return (
        created_at or datetime.now(timezone.utc),
        random.choice(REGIONS),
        category,
        product,
        random.randint(1, 5),
        unit_price,
    )


def seed_history(connection):
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM orders")
        if cursor.fetchone()[0] > 0:
            return

        now = datetime.now(timezone.utc)
        historical_orders = [
            make_order(now - timedelta(minutes=random.randint(0, 1440)))
            for _ in range(350)
        ]
        cursor.executemany(
            """
            INSERT INTO orders
                (created_at, region, category, product, quantity, unit_price)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            historical_orders,
        )
        connection.commit()
        logging.info("Seeded %s historical orders", len(historical_orders))


def run():
    while True:
        try:
            with psycopg.connect(**DB_CONFIG) as connection:
                seed_history(connection)
                while True:
                    orders = [make_order() for _ in range(BATCH_SIZE)]
                    with connection.cursor() as cursor:
                        cursor.executemany(
                            """
                            INSERT INTO orders
                                (created_at, region, category, product, quantity, unit_price)
                            VALUES (%s, %s, %s, %s, %s, %s)
                            """,
                            orders,
                        )
                    connection.commit()
                    logging.info("Loaded %s new orders", len(orders))
                    time.sleep(INTERVAL_SECONDS)
        except psycopg.Error:
            logging.exception("Database connection failed; retrying")
            time.sleep(5)


if __name__ == "__main__":
    run()
