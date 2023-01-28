#version 1.0.0
#Copyright ? 2012-2019 TOPFLYTECH Co., Limitd . All rights reserved.
import errno
import socket
from ctypes import cast
from datetime import datetime
from threading import Thread
from xmlrpc.client import DateTime

from DataSender import *
from RabbitClient import *
from TopflytechCodec import *


def getGpsDriverBehaviorDescription(behaviorType):
    if behaviorType == GpsDriverBehaviorType.HIGH_SPEED_ACCELERATE:
        return "The vehicle accelerates at the high speed."
    elif behaviorType == GpsDriverBehaviorType.HIGH_SPEED_BRAKE:
        return "The vehicle brakes  at the high speed."
    elif behaviorType == GpsDriverBehaviorType.MEDIUM_SPEED_ACCELERATE:
        return "The vehicle accelerates at the high speed."
    elif behaviorType == GpsDriverBehaviorType.MEDIUM_SPEED_ACCELERATE:
        return "The vehicle brakes  at the high speed."
    elif behaviorType == GpsDriverBehaviorType.LOW_SPEED_ACCELERATE:
        return "The vehicle accelerates at the high speed."
    elif behaviorType == GpsDriverBehaviorType.LOW_SPEED_ACCELERATE:
        return "The vehicle brakes  at the high speed."
    else:
        return ""



# t880xPlusEncoder = T880xPlusEncoder(MessageEncryptType.NONE,"")
t880xdEncoder = T880xdEncoder(MessageEncryptType.NONE,"")
# personalEncoder = PersonalAssetMsgEncoder(MessageEncryptType.NONE,"")

def dealObdDeviceMessage(message,socketClient):
    if isinstance(message,SignInMessage):
        print ("receive signInMessage: " + message.imei)
        reply = t880xdEncoder.getSignInMsgReply(message.imei,True,message.serialNo)
        socketClient.send(reply)
    elif isinstance(message,HeartbeatMessage):
        print ("receive heartbeatMessage" + message.imei)
        reply = t880xdEncoder.getHeartbeatMsgReply(message.imei,True,message.serialNo)
        socketClient.send(reply)
        sendDataToTrackin(message)
    elif isinstance(message,LocationInfoMessage):
        print ("receive locationInfoMessage" + message.imei)
        reply = t880xdEncoder.getLocationMsgReply(message.imei,True,message.serialNo,message.protocolHeadType)
        socketClient.send(reply)
        sendDataToTrackin(message)
    elif isinstance(message,LocationAlarmMessage):
        print ("receive locationAlarmMessage" + message.imei + " Alarm is : " + str(message.originalAlarmCode))
        reply = t880xdEncoder.getLocationAlarmMsgReply(message.imei,True,message.serialNo,message.originalAlarmCode,message.protocolHeadType)
        socketClient.send(reply)
        sendDataToTrackin(message)
    elif isinstance(message,GpsDriverBehaviorMessage):
        print ("receive gpsDriverBehaviorMessage" + message.imei + " behavior is :" + getGpsDriverBehaviorDescription(message.behaviorType))
        reply = t880xdEncoder.getGpsDriverBehaviorMsgReply(message.imei,True,message.serialNo)
        socketClient.send(reply)
    elif isinstance(message,AccelerationDriverBehaviorMessage):
        print ("receive accelerationDriverBehaviorMessage" + message.imei + " behavior is :" + getGpsDriverBehaviorDescription(message.behaviorType))
        reply = t880xdEncoder.getAccelerationDriverBehaviorMsgReply(message.imei,True,message.serialNo)
        socketClient.send(reply)
        sendDataToTrackin(message)
    elif isinstance(message,AccidentAccelerationMessage):
        print ("receive accidentAccelerationMessage" + message.imei)
        reply = t880xdEncoder.getAccelerationAlarmMsgReply(message.imei,True,message.serialNo)
        socketClient.send(reply)
    elif isinstance(message,ConfigMessage):
        print ("receive configMessage: " + message.imei + " : " + message.configContent)
    elif isinstance(message,ForwardMessage):
        print ("receive forwardMessage: " + message.imei + " : " + message.content)
    elif isinstance(message,USSDMessage):
        print ("receive forwardMessage: " + message.imei + " : " + message.content)
    elif isinstance(message,ObdMessage):
        print ("receive OBD Message: " + message.imei)
        reply = t880xdEncoder.getObdMsgReply(message.imei,True,message.serialNo)
        socketClient.send(reply)
    elif isinstance(message,BluetoothPeripheralDataMessage):
        print ("receive blue Message: " + message.imei)
        reply = t880xdEncoder.getBluetoothPeripheralMsgReply(message.imei,True,message.serialNo,message.protocolHeadType)
        socketClient.send(reply)
    elif isinstance(message,NetworkInfoMessage):
        print ("receive network info Message: " + message.imei)
        reply = t880xdEncoder.getNetworkMsgReply(message.imei,True,message.serialNo)
        socketClient.send(reply)

    if reply is not None:
        printSendMessage(reply)


def printReciveMessage(data):
    buf = bytearray(data)
    print("Recive obd: \n")
    for i, x in enumerate(buf):
        print('{:02X}'.format(x), end=" ")
        if i % 10 == 0:
            print("\n")
    print("")

def printSendMessage(reply):
    if not (reply is None):
        print("Reponse obd:", end=" ")
        for x in reply:
            print('{:02X}'.format(x), end=" ")
        print("")

def on_new_client(clientsocket, addr, decoder):
    print("\nConnection obd received from %s" % str(addr))
    while True:
        try:
            data = clientsocket.recv(2048)
        except socket.error as e:
            if e.errno != errno.ECONNRESET:
                break
            pass
            
        if not data:
            print("End of file from client. Resetting obd")
            break
        
        printReciveMessage(data)
        messageList = decoder.decode(data)

        for message in messageList:
            dealObdDeviceMessage(message,clientsocket)

        print("\n----------------------------------------------\n")
    clientsocket.close()

def initOBDDecoder(HOST,PORT):
    # Creamos el socket
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(500)
    s.settimeout(None)
    print("Listening obd on address %s." %
      str((HOST, PORT)))
    decoder = ObdDecoder(MessageEncryptType.NONE,"")
    while True:
        print("Waiting obd new connection...")
        c, addr = s.accept()
        # decoder = PersonalAssetMsgDecoder(MessageEncryptType.NONE,"")
        Thread(target=on_new_client, args=(c, addr, decoder)).start()
