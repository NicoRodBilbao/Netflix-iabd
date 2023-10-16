import psycopg2
import logging
from configparser import ConfigParser

# The dbContext class provides database connectivity and various database operations.
class dbContext:
    def __init__(self,table = None):
        self._table = table
        self._conn = None
        self._cursor = None

    # Function to parse the database configuration from a config file.
    def config(self, filename='./database/dbData.ini', section='postgresql'):
        parser = ConfigParser()
        parser.read(filename)
        dbConfig = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                dbConfig[param[0]] = param[1]
            return dbConfig
        else:
            raise Exception(f'Section {section} not found in the {filename} file.')

    # Function to open a connection to the PostgreSQL database.
    def openConnection(self):
        try:
            params = self.config()
            logging.info('Connencting to the database...')
            self._conn = psycopg2.connect(**params)
            self._cursor = self._conn.cursor()
        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(error)
            self.closeConnection()

    # Function to close the database connection.
    def closeConnection(self):
        try:
            if self._conn is not None:
                self._conn.close()
                self._cursor.close()
                logging.info('Database connection closed.')
        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(error)
            
    # Function to select data from the database table based on specified columns (result data), key and value (the condition).
    # If no key is provided, it will return all the rows.
    def select(self, columns, key = None, value = None):
        try:
            self.openConnection()
            if key == None:
                self._cursor.execute(f'SELECT {columns} FROM {self._table}')
                results = self._cursor.fetchall()
            else:
                self._cursor.execute(f'SELECT {columns} FROM {self._table} WHERE {key} LIKE \'%{value}%\'')
                results = self._cursor.fetchall()
            self.closeConnection()
            return results
        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(error)
            self.closeConnection()
            
    # Function to select data from the database table based on specified columns (result data), two keys and two values (the conditions).
    def selectTwoConditions(self, columns, keys, values):
        try:
            self.openConnection()
            self._cursor.execute(f'SELECT {columns} FROM {self._table} WHERE {keys[0]} = {values[0]} AND {keys[1]} = {values[1]}')
            result = self._cursor.fetchone()
            self.closeConnection()
            return result
        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(error)
            self.closeConnection()
    
    # Function to select all columns from the database table based on a specified key and value (the condition).
    # If no key is provided, it will return all the rows.
    def selectAllColumns(self, key = None, value = None):
        try:
            self.openConnection()
            if key == None:
                self._cursor.execute(f'SELECT * FROM {self._table}')
                results = self._cursor.fetchall()
            else:
                self._cursor.execute(f'SELECT * FROM {self._table} WHERE {key} LIKE \'{value}\'')
                results = self._cursor.fetchmany()
            self.closeConnection()
            return results
        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(error)
            self.closeConnection()
            
    # Function to select a specific row from the table by its primary key (ID).
    def selectById(self, value):
        try:
            self.openConnection()
            self._cursor.execute(f'SELECT * FROM {self._table} WHERE {self._table[:-1]}_id = {value}')
            results = self._cursor.fetchone()
            self.closeConnection()
            return results
        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(error)
            self.closeConnection()

    # Function to select rows from the table based on a specified integer key and value (the condition).
    def selectByInt(self, key, value):
        try:
            self.openConnection()
            self._cursor.execute(f'SELECT * FROM {self._table} WHERE {key} = {value}')
            results = self._cursor.fetchall()
            self.closeConnection()
            return results
        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(error)
            self.closeConnection()

    # Function to insert data into the table using a stored procedure.
    def insert(self,values):
        try:
            self.openConnection()
            self._cursor.execute(f'CALL insert_{self._table[:-1]}_procedure({",".join(values)})')
            self._conn.commit()
            self.closeConnection()
        except (Exception,psycopg2.DatabaseError) as error:
            logging.error(error)
            self.closeConnection()
        
    # Function to update data in the table based on a specified column, value and condition.
    def update(self,updateColumn,updateValue,whereColumn,whereValue):
        try:
            self.openConnection()
            self._cursor.execute(f'UPDATE {self._table} SET {updateColumn} = \'{updateValue}\' WHERE {whereColumn} LIKE \'%{whereValue}%\'')
            self._conn.commit()
            self.closeConnection()
        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(error)
            self.closeConnection()
    
    # Function to update multiple columns at once based on specified columns, values and condition.
    def updateMany(self,columns_values,whereColumn,whereValue):
        try:
            self.openConnection()
            self._cursor.execute(f'UPDATE {self._table} SET ({",".join(columns_values.keys())}) = ({",".join(columns_values.values())}) WHERE {whereColumn} LIKE \'%{whereValue}%\'')
            self._conn.commit()
            self.closeConnection()
        except (Exception,psycopg2.DatabaseError) as error:
            logging.error(error)
            self.closeConnection()
    
     # Function to delete rows from the table based on a specified column and value.
    def delete(self,column,value):
        try:
            self.openConnection()
            self._cursor.execute(f'DELETE FROM {self._table} WHERE {column} LIKE \'%{value}%\'')
            self._conn.commit()
            self.closeConnection()
        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(error)
            self.closeConnection()
            
    # Function to select subscription data with a count of related user subscriptions.
    def selectSubsCount(self):
        try:
            self.openConnection()
            self._cursor.execute("SELECT sub.*, COUNT(rel.subscription_id) FROM subscriptions sub, users_subscriptions rel WHERE sub.subscription_id = rel.subscription_id GROUP BY rel.subscription_id, sub.subscription_id")
            self._conn.commit()
            results = self._cursor.fetchall()
            self.closeConnection()
            return results
        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(error)
            self.closeConnection()