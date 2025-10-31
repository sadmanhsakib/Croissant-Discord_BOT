import asyncpg
import config

class Database():
    def __init__(self):
        self.pool = None

    async def connect(self):
        try:
            # since we have no Authentication, we can just use the URL
            self.pool = await asyncpg.create_pool(config.DATABASE_URL, ssl=True, min_size=1, max_size=15)

            # gets the database connection from pool
            async with self.pool.acquire() as conn:
                # setting the correct schema
                await conn.execute("CREATE SCHEMA IF NOT EXISTS public")
                await conn.execute("SET search_path TO public")

            print("✅Connected to the database.")

            await self.create_tables()
        except Exception as error:
            print(f"❌Failed to connect to the database: {error}")

    async def create_tables(self):
        try:
            # gets the database connection from pool
            async with self.pool.acquire() as conn:
                # creating a SQL table for dynamic variables
                await conn.execute(
                    """
                    -- creating a table called 'SERVER_DATA' if not exists
                    CREATE TABLE IF NOT EXISTS SERVER_DATA (
                        variable_name VARCHAR(100),
                        variable_value TEXT,
                        created_at TIMESTAMP DEFAULT (NOW() AT TIME ZONE 'Asia/Dhaka'),
                        updated_at TIMESTAMP DEFAULT (NOW() AT TIME ZONE 'Asia/Dhaka'),
                        -- ensures that each combination of server_id and variable_name is unique
                        PRIMARY KEY (variable_name)
                    );
                """
                )
                print("✅ Variables table ready!")
        except Exception as error:
            print(f"❌ Error creating tables: {error}")

    async def set_variable(self,variable_name: str, variable_value: str):
        try:
            # gets the database connection from pool
            async with self.pool.acquire() as conn:
                # inserting/updating the variable
                await conn.execute(
                    """
                    -- inserts a new variable in the table
                    INSERT INTO SERVER_DATA (variable_name, variable_value)
                    -- $1 $2 are asyncpg placeholders
                    VALUES ($1, $2)
                    -- conflict occurs when the variable_name already exists
                    -- if the variable_name already exists, it updates the variable_value
                    ON CONFLICT (variable_name) DO UPDATE
                    SET variable_value = $2,
                    updated_at = TIMEZONE('Asia/Dhaka', NOW())
                    """,
                    variable_name,
                    variable_value,
                )
                print(f"✅ {variable_name} set to {variable_value} successfully!")
        except Exception as error:
            print(f"❌ Error setting variables: {error}")

    async def get_variable(self, variable_name: str):
        try:
            # gets the database connection from pool
            async with self.pool.acquire() as conn:
                result = await conn.fetchrow(
                    """
                    -- gets the variable value from the table
                    SELECT variable_value
                    FROM SERVER_DATA
                    WHERE variable_name = $1
                    """,
                    variable_name
                )
                # returning the variable value
                return result["variable_value"] if result else None
        except Exception as error:
            print(f"Error at fetching variable value: {error}")
            return None


db = Database()
