import time
import paho.mqtt.client as paho
#import matplotlib.pyplot as plt
import RPi.GPIO as GPIO

brokerAddr="broker.hivemq.com"
eventName = "unibo/marchesini/sonar/events"
TSONAR = 2
DLIMIT = 10
clientPublisher = paho.Client("Publisher")  
TRIG = 18
ECHO = 24
LED  = 25
MINDISTANCE = 6
MAXDISTANCE = 1000

print("Start SonarRobot ")

def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    #pass

def initsonar():
    print ('Waiting a few seconds for the sensor to settle')
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)


    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)

    GPIO.output(TRIG, False)   #TRIG parte LOW
    #print ('Waiting a few seconds for the sensor to settle')
    time.sleep(2)

def getDistance():
    GPIO.output(TRIG, True)    #invia impulsoTRIG
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    pulse_start = 0
    pulse_end = 0
    #attendi che ECHO parta e memorizza tempo
    while GPIO.input(ECHO)==0:
      pulse_start = time.time()

    # register the last timestamp at which the receiver detects the signal.
    while GPIO.input(ECHO)==1:
      pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17165   #distance = vt/2
    #distance = round(distance, 0)
    distance = int(distance)
    #print ('getDistance {distance}'.format(distance=distance))
    #print ( distance ) 
    #time.sleep(0.25)
    return distance

def readConfig():
    global DLIMIT
    global TSONAR
    lines = []
    with open('./config.txt') as f:
        lines = f.readlines()
    count = 0
    for line in lines:
        if count == 0 :
            DLIMIT = int(line)
            print ('DLIMIT {DLIMIT}'.format(DLIMIT=DLIMIT)) 
        else :
            TSONAR = int(line)
            print ('TSONAR {TSONAR}'.format(TSONAR=TSONAR)) 
        count +=1
        


def loop() :
    GPIO.setup(LED,GPIO.OUT)
    clientPublisher.on_publish = on_publish                          #assign function to callback
    clientPublisher.connect(brokerAddr)                             #establish connection
    readConfig()                         
    counter = 0   
    print ('while true') 
    while True :
        #print ('... again ...') 
        distance = getDistance()
        if ( (MINDISTANCE < distance) and (distance < MAXDISTANCE ) ):
            print ('Distance {distance}'.format(distance=distance)) 
            counter += 1 
            ret = clientPublisher.publish(eventName,"msg(sonarrobot,event,sonarrobot,none,sonarrobot(" + str(distance) + ")," + str(counter) + ")")#publish

            if distance < DLIMIT :
                GPIO.output(LED,GPIO.HIGH)
            else :
                GPIO.output(LED,GPIO.LOW)
            time.sleep(TSONAR)    
    loop_forever()



initsonar()
loop() 
