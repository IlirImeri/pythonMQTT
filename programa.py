
#domain.com es el dominio del broker MQTT

import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time
import socket

payloads = ""

def on_connect(mqttc, obj, flags, rc):
	print("rc: " + str(rc))


def on_message(mqttc, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " El mensaje es:" + str(msg.payload))
    payloads = str(msg.payload)
    if payloads == "b'OK'":
	    time.sleep(1)
	    (rc, mid) = mqttc.publish("201804070068", "201804070068,767,677", qos=0)
	    turn_on_led(7)
#    mqttc.loop_start()


def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))


def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))



def on_log(mqttc, obj, level, string):
    print(string)

# Funcion para encender un LED
# @param pin = el pin GPIO del LED que quieres encender
def turn_on_led (pin):
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin, GPIO.HIGH)
	GPIO.output(pin, GPIO.HIGH)
	time.sleep(2)
	GPIO.output(pin, GPIO.LOW)
	GPIO.cleanup()

# Funcion para comprobar la conexion entre
# cliente y servidor
# Funcion recursiva que se invoca a si misma hasta
# el momento de la conexion
# Si hay una conexion, se enciende un LED verde, de
# lo contrario un LED rojo.
def test_connection():
	try:
		socket.create_connection(('domain.com', 80))
		turn_on_led(22)
		return True
	except OSError:
		time.sleep(3)
		print("Connection Failed")
		turn_on_led(12)
		test_connection()


mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe

print("Connection:" + str(test_connection()))


mqttc.connect("domain.com", 1883, 60)
mqttc.subscribe("201804070068/#", 0)

mqttc.loop_forever()
