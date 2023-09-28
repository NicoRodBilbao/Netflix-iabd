import psycopg2
import logging
from configparser import ConfigParser

conn = None

def config(filename='dbData.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)
    
    dbConfig = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            dbConfig[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in the {filename} file.')
    
    return dbConfig

def openConnection():
    try:
        params = config()
        logging.info('Connencting to the database...')
        conn = psycopg2.connect(**params)
        return conn.cursor()
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
    finally:
        closeConnection()
            
            
def closeConnection():
    if conn is not None:
        conn.close()
        logging.info('Database connection closed.')