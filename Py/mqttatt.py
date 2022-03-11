import mysql.connector
import paho.mqtt.client as mqtt
from datetime import datetime

now = datetime.now()
tanggal = now.strftime('%Y-%m-%d')
jam = now.strftime('%H:%M:%S')

#db
db = mysql.connector.connect(
    host = "192.168.158.179",
    user = "python",
    password = "python",
    database = "python"
)
cur = db.cursor()

sql_card = """select username, cardUid, cardStatus from cards where cardUid = %(cardId)s"""
sql_reader = """select deviceName, deviceID, deviceMode from devices where deviceID = %(deviceId)s"""
sql_read_logs = """select * from logs where cardUid = %(cardId)s and checkInDate = %(CID)s"""
sql_ins_logs = """insert into logs (username, deviceId, cardUid, checkInDate, timeIn) values (%(username)s, %(deviceId)s, %(cardId)s, %(CID)s, %(TI)s)"""

##mqtt
broker = '192.168.158.169'
port = 1883
topic = "test/+/attend"

def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))

def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))

def on_message(mqttc, obj, msg):
    data = msg.topic.rsplit("/",1)   
    data2 = msg.payload.decode()
    data2 = data2.split("/")
    cur.execute(sql_reader, {'deviceId': data2[0]})
    result = cur.fetchall()
    cur.execute(sql_card, {'cardId': data2[1]})
    result2 = cur.fetchall()
    cur.execute(sql_read_logs, {'cardId': data2[1], 'CID': str(tanggal)})
    result3 = cur.fetchone()
    for (deviceName, deviceid, deviceMode) in result:
        if deviceMode == "enable":
            for (username, deviceId, cardStatus) in result2:
                if cardStatus == "enable":
                    if result3 == None: 
                        cur.execute(sql_ins_logs, {'username': username,'deviceId': data2[0], 'cardId': data2[1], 'CID': tanggal, 'TI': jam})                          
                        db.commit()
                        db.close()
                        db.connect()
                    else:
                        print("2")
                        db.close()
                        db.connect()
                else:
                    print("1")
                    db.close()
                    db.connect()
        else:
            print("0")
            db.close()
            db.connect()

mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_publish = on_publish
mqttc.on_message = on_message
mqttc.connect(broker, port, 60)
mqttc.subscribe("test/+/attend", 2)
mqttc.loop_forever() 
