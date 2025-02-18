import pyodbc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

# Load ENVs from .env file
load_dotenv()

Base = declarative_base()

class Database:
    def __init__(self):
        self.server = os.getenv('DB_SERVER')
        self.database = os.getenv('DB_DATABASE')
        self.driver = os.getenv('DB_DRIVER')

        self.connection_string = (
            f'Driver={{{self.driver}}};'
            f'Server={self.server};'
            f'Database={self.database};'
            f'Trusted|_Connection=yes;'
        )

        self.conn = None
        self.cursor = None

    # Function to use pyodbc for raw queries
    def connect_with_pyodbc(self):
        try:
            conn = pyodbc.connect(self.connection_string)
            print("Connected to database with pyodbc successfully.")
            return conn
        except Exception as e:
            print(f"Error connecting with pyodbc: {e}")
            return None
        
    def connect_with_sqlalchemy(self):
        try:
            self.engine = create_engine(f"mssql+pyodbc:///?odbc_connect={self.connection_string}")
            self.Session = sessionmaker(bind=self.engine)
            print("Connected to database with SQLAlchemy successfully.")
            return self.engine
        except Exception as e:
            print(f"Error connecting to SQLAlchemy: {e}")
            return None

    # Closses the connection
    def close(self):
        if self.engine:
            self.engine.dispose()
            print("SQLAlchemy connection closed.")

    # Function for Raw Queries
    def execute_raw_query(self, query, params=None):
        # Executes the query
        try:
            conn = self.connect_with_pyodbc()
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            conn.commit()
            cursor.close()
            conn.close()
            print("Query executed successfullu")
        except Exception as e:
            print(f"Error executing raw query: {e}")

    def create_tables(self, base):
        try:
            base.metadata.create_all(self.engine)
            print("Tables created successfully.")
        except Exception as e:
            print(f"Error creating tables: {e}")

