import psycopg2
import logging
from configparser import ConfigParser

class dbContext:
    def __init__(self,table):
        self._table = table
        self._conn = None
        self._cursor = None

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

    def openConnection(self):
        try:
            params = self.config()
            logging.info('Connencting to the database...')
            self._conn = psycopg2.connect(**params)
            self._cursor = self._conn.cursor()
        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(error)
            self.closeConnection()
                
                
    def closeConnection(self):
        if self._conn is not None:
            self._conn.close()
            self._cursor.close()
            logging.info('Database connection closed.')
            
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
    
    def selectAllColumns(self, key = None, value = None):
        try:
            self.openConnection()
            if key == None:
                self._cursor.execute(f'SELECT * FROM {self._table}')
                results = self._cursor.fetchall()
            else:
                self._cursor.execute(f'SELECT * FROM {self._table} WHERE {key} LIKE \'%{value}%\'')
                results = self._cursor.fetchall()
            self.closeConnection()
            return results
        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(error)
            self.closeConnection()
            
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
    
    def insert(self,values):
        try:
            self.openConnection()
            self._cursor.execute(f'CALL insert_{self._table[:-1]}_procedure({",".join(values)})')
            self._conn.commit()
            self.closeConnection()
        except (Exception,psycopg2.DatabaseError) as error:
            logging.error(error)
            self.closeConnection()
        
    def update(self,updateColumn,updateValue,whereColumn,whereValue):
        try:
            self.openConnection()
            self._cursor.execute(f'UPDATE {self._table} SET {updateColumn} = \'{updateValue}\' WHERE {whereColumn} LIKE \'%{whereValue}%\'')
            self._conn.commit()
            self.closeConnection()
        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(error)
            self.closeConnection()
        
    def updateMany(self,columns_values,whereColumn,whereValue):
        try:
            self.openConnection()
            self._cursor.execute(f'UPDATE {self._table} SET ({",".join(columns_values.keys())}) = ({",".join(columns_values.values())}) WHERE {whereColumn} LIKE \'%{whereValue}%\'')
            self._conn.commit()
            self.closeConnection()
        except (Exception,psycopg2.DatabaseError) as error:
            logging.error(error)
            self.closeConnection()
        
    def delete(self,column,value):
        try:
            self.openConnection()
            self._cursor.execute(f'DELETE FROM {self._table} WHERE {column} LIKE \'%{value}%\'')
            self._conn.commit()
            self.closeConnection
        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(error)
            self.closeConnection()