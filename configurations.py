import psycopg2
from sqlalchemy import create_engine
import os



# this is a postgre sql db connection in order to your sql db connection you need to write these parameters again
# THis is my local connection where my abtestdb is located.

connection_clientsdb = psycopg2.connect(user=os.environ['db_user'],
                                         password=os.environ['db_password'],
                                         host=os.environ['connection_host'],
                                         port=os.environ['port'],
                                         database=os.environ['db_name_clientsdb'])

connection_abtestdb = psycopg2.connect(user=os.environ['db_user'],
                                        password=os.environ['db_password'],
                                        host=os.environ['connection_host'],
                                        port=os.environ['port'],
                                        database=os.environ['db_name_abtestdb'])

#connection_abtestdb = create_engine('postgresql://mac:1234@127.0.0.1:5434/abtestdb')
#connection_clientsdb = create_engine('postgresql://mac:1234@127.0.0.1:5434/clientsdb')

connection_parameters = {'connection_clientsdb': connection_clientsdb,
                         'connection_abtestdb': connection_abtestdb
                         }

