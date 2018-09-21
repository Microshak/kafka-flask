
from flask import Blueprint, json

from datetime import datetime
from flask import render_template
from KafkaFlask import app

from flask import Response
from flask import request
import json
import time
from flask import Response, Flask
db = Blueprint('db', __name__)
uri =app.config["kafkaurl"]

from kafka import KafkaConsumer
import ast

@db.route('/realtime/')
def realtime():

    def createGenerator():



       consumer = KafkaConsumer('test',
                         group_id='my-group',
                         bootstrap_servers='[your ip]:9092',auto_offset_reset='earliest')
       for message in consumer:
           # yield "%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
           #                                 message.offset, message.key,
           # 
            yield  message.value
            time.sleep(1)

    return Response(createGenerator(), mimetype= 'text/event-stream')



@db.route('/poll/<string:topic>', methods=['GET'])
def consume(topic):
    limit=10
    group = 'my-group'
    consumer = KafkaConsumer(topic,
                         group_id='my-group',
                         bootstrap_servers='[your ip]:9092')
  
  
    res = {"group": group.decode("utf-8"), "messages": []}

    for n, message in enumerate(consumer):
        dic = message.value.decode("utf-8")
        dic = dic.replace('\\\"', '"')
        dic = dic.replace('\"', '"')
       
        res["messages"].append(json.loads(message.value))
        if n >= limit - 1:
            break
    consumer.commit()
    consumer.close()
    #consumer.stop()
    go =json.dumps(res["messages"])
    go = go.replace('\"', '"')
    resp = Response(response=go,
                    status=200,
                    mimetype="application/json")
    return resp


