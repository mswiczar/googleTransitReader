from google.transit import gtfs_realtime_pb2
import urllib.request
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
from mysql.connector.cursor import MySQLCursorPrepared

try:
    connection = mysql.connector.connect(host='localhost',
                                         database='gtfs',
                                         user='root',
                                         password='',use_pure=True)
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL database... MySQL Server version on ",db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print ("Your connected to - ", record)

        sql_Delete_query = """Delete from stop_times """
        cursor.execute(sql_Delete_query)
        connection.commit()
        print ("\n Deleted all stop_times Table successfully ")

        feed = gtfs_realtime_pb2.FeedMessage()
        response = urllib.request.urlopen('http://njttraindata_tst.njtransit.com:8090/njttraindata.asmx/getGTFS_RTfeed?username=ngvincentdev&password=a3BkcF7s4H')
        feed.ParseFromString(response.read())

        #print(feed);
        cursor2 = connection.cursor(cursor_class=MySQLCursorPrepared)
        #cursor = connection.cursor(prepared=True)
        sql_insert_query = """ INSERT INTO `stop_times` (`trip_id`, `arrival_time`, `departure_time`, `stop_id`, `stop_sequence`) VALUES ( %s, %s, %s, %s, %s)"""

        for entity in feed.entity:
            if entity.HasField('trip_update'):
                #print(entity.trip_update)
                #insert into db
                try:
                    print(entity.trip_update.trip.trip_id);
                    #print(entity.trip_update.stop_time_update);
                    for stop_time_update in entity.trip_update.stop_time_update:
                        input_tuple = (entity.trip_update.trip.trip_id , stop_time_update.arrival.time   , stop_time_update.departure.time ,stop_time_update.stop_id,stop_time_update.stop_sequence)
                        #print(input_tuple);
                        result  = cursor2.execute(sql_insert_query,input_tuple)
                        connection.commit()
                        print ("Record inserted successfully into stop_times table")
                except mysql.connector.Error as error :
                    connection.rollback() #rollback if any exception occured
                    print("Failed inserting record into stop_times table {}".format(error))

except Error as e :
    print ("Error while connecting to MySQL", e)
finally:
    #closing database connection.
    if(connection.is_connected()):
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
