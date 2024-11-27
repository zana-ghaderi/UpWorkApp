
POSTGRES_CONFIG = {
    "dbname": "work_db",
    "user": "zana",
    "password": "work_password",
    "host": "localhost",
    "port": "5432"
}

CASSANDRA_CONFIG = {
    "contact_points": ["localhost"],
    "port": 9042,
    "keyspace": "mybook"
}

KAFKA_CONFIG = {
    'bootstrap.servers': 'localhost:9092',
    'client.id': 'work-producer'
}

REDIS_CONFIG = {
    'host': 'localhost',
    'port': '6379',
    'db': '0'
}
