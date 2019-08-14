import psycopg2


# this is a postgre sql db connection in order to your sql db connection you need to write these parameters again
# THis is my local connection where my abtestdb is located.
connection_parameters = {'connection_clientsdb' : psycopg2.connect(user = "mac",
                                                                   password = "1234",
                                                                   host = "127.0.0.1",
                                                                   port = "5434",
                                                                   database = "clientsdb"),

                         'connection_abtestdb' : psycopg2.connect(user = "mac",
                                                                     password = "1234",
                                                                     host = "127.0.0.1",
                                                                     port = "5434",
                                                                     database = "abtestdb")
}

