from google.transit import gtfs_realtime_pb2
import urllib.request

feed = gtfs_realtime_pb2.FeedMessage()
#response = urllib.request.urlopen('http://www.google.com')
response = urllib.request.urlopen('http://njttraindata_tst.njtransit.com:8090/njttraindata.asmx/getGTFS_RTfeed?username=ngvincentdev&password=a3BkcF7s4H')
feed.ParseFromString(response.read())
for entity in feed.entity:
    print(entity)
