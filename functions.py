
from database import Database
import pandas as pd
from sqlalchemy import Column, Integer, String, Date, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DataProcessor:
    def __init__(self):
        self.db= Database() 
    
    def get_column_type(self, value):
        # Determines column type based on the value
        if isinstance(value, int):
            return Integer
        elif isinstance(value, float):
            return Float
        elif isinstance(value, pd.Timestamp):
            return Date
        else:
            return String
        
    def create_dynamic_table(self, df, table_name):
        # Set table name dynamically
        columns = {}

        for column in df.columns:
            first_value = df[column].dropna().iloc[0]
            column_type = self.get_column_type(first_value)
            columns[column] = Column(column_type)


        DynamicModel = type(table_name, (Base,), columns)

        DynamicModel.__tablename__ = table_name
        self.db.connect_with_sqlalchemy()
        DynamicModel.metadata.create_all(self.db.engine)
        print(f"Table {table_name} created.")

        return DynamicModel

    def insert_data(self, df, table_name, ):
        self.db.connect_with_sqlalchemy()
        session = self.db.Session()


        self.create_dynamic_table(df, table_name)
        DynamicModel = self.create_dynamic_table(df, table_name)

        for _, row in df.iterrows():
            row_data = DynamicModel(**row.to_dict())
            session.add(row_data)

        session.commit()
        self.db.close()
 