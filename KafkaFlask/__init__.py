"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)
print(__name__)
app.config["kafkaurl"] = "[your ip]:9092"



import KafkaFlask.views
import KafkaFlask.kafkaHub


