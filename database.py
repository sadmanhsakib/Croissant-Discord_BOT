import os, logging
import psycopg2, dotenv
from psycopg2.extras import RealDictCursor

dotenv.load_dotenv(".env")

# setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        self.connection_string = os.getenv("DATABASE_URL")

    # connects with the database
    def get_connection(self):
        try:
            conn = psycopg2.connect(
                self.connection_string, cursor_factory=RealDictCursor)

            # set the timezone to GMT+6
            cursor = conn.cursor()
            cursor.execute("SET TIME ZONE 'GMT+6';")
            cursor.close()
            
            logger.info("Connected to the database.")
            return conn
        except Exception as e:
            logger.error(f"Error connecting to the database: {e}")
            return None

    # sets up the database by creating a table if it does not exist.
    def setup_database(self):
        conn = self.get_connection()

        if not conn:
            return False

        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS server_variables (
                    -- VARCHAR(value) is the amount of characters that can be stored
                    server_id VARCHAR(20) NOT NULL,
                    var_name VARCHAR(255) NOT NULL,
                    var_value VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    -- avoids adding duplicate variable entries
                    PRIMARY KEY (server_id, var_name)
                );
            """
            )

            conn.commit()
            return True
        except Exception as e:
            logger.error(f"Database setup failed: {e}")
            return False
        finally:
            # closing for better resource management
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def set_variable(self, server_id, var_name, value):
        conn = self.get_connection()

        if not conn:
            return False

        try:
            # creating a cursor
            cursor = conn.cursor()

            # inserts the data into the table
            cursor.execute(
                """INSERT INTO server_variables (server_id, var_name, var_value) 
                VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
                ON CONFLICT (server_id, var_name) 
                DO UPDATE SET
                    var_value = %s,
                    updated_at = CURRENT_TIMESTAMP""",
                (server_id, var_name, value, value),
            )

            conn.commit()
            logger.info(
                f"Variable '{var_name}' set to '{value}' for server {server_id}"
            )
            return True            
        except Exception as e:
            logger.error(f"Error setting up the database: {e}")
            return False

        finally:
            # closing for better resource management
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def test_connection(self):
        conn = self.get_connection()

        if not conn:
            return False

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            logger.info(f"Connected to PostgreSQL version: {version}")
            return True
        except Exception as e:
            logger.error(f"Error connecting to the database: {e}")
            return False
        finally:
            # closing for better resource management
            if cursor:
                cursor.close()
            if conn:
                conn.close()


database = DatabaseManager()

database.test_connection()
