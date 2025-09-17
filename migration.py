from database import DatabaseConfig, DatabaseConnection

class MigrationManager:
    def __init__(self, config: DatabaseConfig):
        self.config = config
        self.connection = DatabaseConnection(self.config)

    def create_tables(self):
        conn = self.connection.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            price DECIMAL(10,2) NOT NULL,
            count INTEGER NOT NULL,
            quality VARCHAR(100) NOT NULL
        )
        ''')
        conn.commit()
        cursor.close()
        conn.close()