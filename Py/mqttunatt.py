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
sql_upd_logs = """update logs set timeOut = %(TO)s where cardUid = %(cardId)s and checkInDate = %(CID)s"""

##mqtt
broker = '192.168.158.169'
port = 1883
topic = "test/+/unattend"

def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))

def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))

def on_message(mqttc, obj, msg):
    #print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    #print(msg.topic)
    data = msg.topic.rsplit("/",1)
    #print(data)
    #print(data[0])
    
    data2 = msg.payload.decode()
    data2 = data2.split("/")
    #cardId= data2[0]
    #print(data2[1])

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
                        print("2") 
                        db.close()
                        db.connect()
                    else:
                        cur.execute(sql_upd_logs, {'TO': jam, 'cardId': data2[1], 'CID': tanggal})                          
                        db.commit()
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
mqttc.subscribe("test/+/unattend", 2)
mqttc.loop_forever() 
