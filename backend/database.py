import os
from pathlib import Path
from psycopg_pool import ConnectionPool
from psycopg.rows import dict_row

DB_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:password@localhost:5432/fantasy_marketplace")

pool = ConnectionPool(
    conninfo=DB_URL,
    min_size=2,
    max_size=10,
    open=False, # Open pool upon lifespan start in app.py (catches errors during startup)
    kwargs={"row_factory": dict_row} # Automatically convert rows to dictionaries
)

def get_connection():
    """
    Get a connection from the connection pool.
    Returns:
        A connection object from the connection pool.
    """
    with pool.connection() as conn:
        yield conn
        
def init_db():
    """
    Initialize the database by creating necessary tables if they do not exist.
    This function should be called at the start of the application to ensure that
    the database schema is set up correctly.
    """
    schema_path = Path(__file__).parent / "schema.sql"
    with open(schema_path, "rb") as f:
        schema_sql = f.read()
        
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(schema_sql)
        conn.commit()
    print("Database initialized successfully.")
    
def reset_db():
    """
    Reset the database by dropping all tables and re-initializing the schema.
    """
    pool_closed = pool.closed
    if pool_closed:
        pool.open()
    
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DROP SCHEMA public CASCADE; CREATE SCHEMA public;")
        conn.commit()
        
    with pool:
        init_db()
    print("Database reset successfully.")