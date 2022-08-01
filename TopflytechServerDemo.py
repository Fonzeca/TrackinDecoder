#version 1.0.0
#Copyright ? 2012-2019 TOPFLYTECH Co., Limitd . All rights reserved.
import datetime
import errno
import http.client
import json
import socket
import threading
import time
from threading import Thread
from xmlrpc.client import DateTime

import requests

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



t880xPlusEncoder = T880xPlusEncoder(MessageEncryptType.NONE,"")
t880xdEncoder = T880xdEncoder(MessageEncryptType.NONE,"")
personalEncoder = PersonalAssetMsgEncoder(MessageEncryptType.NONE,"")

def dealObdDeviceMessage(message,socketClient):
    if isinstance(message,SignInMessage):
        print ("receive signInMessage: " + message.imei)
        # if message.isNeedResp:
        #     reply = t880xdEncoder.getSignInMsgReply(message.imei,True,message.serialNo)
        #     socketClient.send(reply)
        reply = t880xdEncoder.getSignInMsgReply(message.imei,True,message.serialNo)
        socketClient.send(reply)
    elif isinstance(message,HeartbeatMessage):
        print ("receive heartbeatMessage" + message.imei)
        # if message.isNeedResp:
        #     reply = t880xdEncoder.getHeartbeatMsgReply(message.imei,True,message.serialNo)
        #     socketClient.send(reply)
        reply = t880xdEncoder.getHeartbeatMsgReply(message.imei,True,message.serialNo)
        socketClient.send(reply)
    elif isinstance(message,LocationInfoMessage):
        print ("receive locationInfoMessage" + message.imei)
        # if message.isNeedResp:
        #     reply = t880xdEncoder.getLocationMsgReply(message.imei,True,message.serialNo)
        #     socketClient.send(reply)
        reply = t880xdEncoder.getLocationMsgReply(message.imei,True,message.serialNo,message.protocolHeadType)
        socketClient.send(reply)
    elif isinstance(message,LocationAlarmMessage):
        print ("receive locationAlarmMessage" + message.imei + " Alarm is : " + str(message.originalAlarmCode))
        # some new model device,need serial no,reply this message
        # if message.isNeedResp:
        #     reply = t880xdEncoder.getLocationAlarmMsgReply(message.imei,True,message.serialNo,message.originalAlarmCode)
        #     socketClient.send(reply)
        reply = t880xdEncoder.getLocationAlarmMsgReply(message.imei,True,message.serialNo,message.originalAlarmCode,message.protocolHeadType)
        socketClient.send(reply)
    elif isinstance(message,GpsDriverBehaviorMessage):
        print ("receive gpsDriverBehaviorMessage" + message.imei + " behavior is :" + getGpsDriverBehaviorDescription(message.behaviorType))
        # if message.isNeedResp:
        #     reply = t880xdEncoder.getGpsDriverBehaviorMsgReply(message.imei,True,message.serialNo)
        #     socketClient.send(reply)
        reply = t880xdEncoder.getGpsDriverBehaviorMsgReply(message.imei,True,message.serialNo)
        socketClient.send(reply)
    elif isinstance(message,AccelerationDriverBehaviorMessage):
        print ("receive accelerationDriverBehaviorMessage" + message.imei + " behavior is :" + getGpsDriverBehaviorDescription(message.behaviorType))
        # if message.isNeedResp:
        #     reply = t880xdEncoder.getAccelerationDriverBehaviorMsgReply(message.imei,True,message.serialNo)
        #     socketClient.send(reply)
        reply = t880xdEncoder.getAccelerationDriverBehaviorMsgReply(message.imei,True,message.serialNo)
        socketClient.send(reply)
    elif isinstance(message,AccidentAccelerationMessage):
        print ("receive accidentAccelerationMessage" + message.imei)
        # if message.isNeedResp:
        #     reply = t880xdEncoder.getAccelerationAlarmMsgReply(message.imei,True,message.serialNo)
        #     socketClient.send(reply)
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
        # if message.isNeedResp:
        #     reply = t880xdEncoder.getObdMsgReply(message.imei,True,message.serialNo)
        #     socketClient.send(reply)
        reply = t880xdEncoder.getObdMsgReply(message.imei,True,message.serialNo)
        socketClient.send(reply)
    elif isinstance(message,BluetoothPeripheralDataMessage):
        print ("receive blue Message: " + message.imei)
        # if message.isNeedResp:
        #     reply = t880xdEncoder.getBluetoothPeripheralMsgReply(message.imei,True,message.serialNo)
        #     socketClient.send(reply)
        reply = t880xdEncoder.getBluetoothPeripheralMsgReply(message.imei,True,message.serialNo,message.protocolHeadType)
        socketClient.send(reply)
    elif isinstance(message,NetworkInfoMessage):
        print ("receive network info Message: " + message.imei)
        # if message.isNeedResp:
        #     reply = t880xdEncoder.getNetworkMsgReply(message.imei,True,message.serialNo)
        #     socketClient.send(reply)
        reply = t880xdEncoder.getNetworkMsgReply(message.imei,True,message.serialNo)
        socketClient.send(reply)

def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.isoformat()



def dealNoObdDeviceMessage(message,socketClient):
    """
    Device model like :8806 plus, use this method.
    :param message:
    :param socketClient:
    :return:
    """
    reply = None
    if isinstance(message,SignInMessage):
        print ("receive signInMessage: " + message.imei)
        #8806 Plus or some new model device,need serial no,reply this message
        # if message.isNeedResp:
        #     reply = t880xPlusEncoder.getSignInMsgReply(message.imei,True,message.serialNo)
        #     socketClient.send(reply)

        reply = t880xPlusEncoder.getSignInMsgReply(message.imei,True,message.serialNo)
        socketClient.send(reply)
        # time.sleep(2)
        # reply2 = t880xPlusEncoder.getConfigSettingMsg(message.imei, 'CONFIG#')
        # socketClient.send(reply2)
        # print("Config: ")
        # printSendMessage(reply2)
    elif isinstance(message,HeartbeatMessage):
        print ("receive heartbeatMessage: " + message.imei)
        #8806 Plus or some new model device,need serial no,reply this message
        # if message.isNeedResp:
        #     reply = t880xPlusEncoder.getHeartbeatMsgReply(message.imei,True,message.serialNo)
        #     socketClient.send(reply)
        reply = t880xPlusEncoder.getHeartbeatMsgReply(message.imei,True,message.serialNo)
        socketClient.send(reply)
    elif isinstance(message,LocationInfoMessage):
        print ("receive locationInfoMessage: " + message.imei)
        
        #8806 Plus or some new model device, these is the code of 8806 plus.
        # if message.isNeedResp:
        #     reply = t880xPlusEncoder.getLocationMsgReply(message.imei,True,message.serialNo,message.originalAlarmCode,message.protocolHeadType)
        #     socketClient.send(reply)
        reply = t880xPlusEncoder.getLocationMsgReply(message.imei,True,message.serialNo,message.protocolHeadType)
        socketClient.send(reply)
        sendDataToTrackin(message)
    elif isinstance(message,LocationAlarmMessage):
        print ("receive locationAlarmMessage: " + message.imei + "Alarm is : " + str(message.originalAlarmCode))
        #8806 Plus or some new model device,need serial no,reply this message
        # if message.isNeedResp:
        #     reply = t880xPlusEncoder.getLocationAlarmMsgReply(message.imei,True,message.serialNo,message.originalAlarmCode,message.protocolHeadType)
        #     socketClient.send(reply)
        reply = t880xPlusEncoder.getLocationAlarmMsgReply(message.imei,True,message.serialNo,message.originalAlarmCode,message.protocolHeadType)
        socketClient.send(reply)
    elif isinstance(message,GpsDriverBehaviorMessage):
        print ("receive gpsDriverBehaviorMessage: " + message.imei + " behavior is :" + getGpsDriverBehaviorDescription(message.behaviorType))
        # if message.isNeedResp:
        #     reply = t880xPlusEncoder.getGpsDriverBehaviorMsgReply(message.imei,True,message.serialNo)
        #     socketClient.send(reply)
        reply = t880xPlusEncoder.getGpsDriverBehaviorMsgReply(message.imei,True,message.serialNo)
        socketClient.send(reply)
    elif isinstance(message,AccelerationDriverBehaviorMessage):
        print ("receive accelerationDriverBehaviorMessage: " + message.imei + " behavior is :" + getGpsDriverBehaviorDescription(message.behaviorType))
        # if message.isNeedResp:
        #     reply = t880xPlusEncoder.getAccelerationDriverBehaviorMsgReply(message.imei,True,message.serialNo)
        #     socketClient.send(reply)
        reply = t880xPlusEncoder.getAccelerationDriverBehaviorMsgReply(message.imei,True,message.serialNo)
        socketClient.send(reply)
    elif isinstance(message,AccidentAccelerationMessage):
        print ("receive accidentAccelerationMessage: " + message.imei)
        #8806 Plus or some new model device,need serial no,reply this message
        # if message.isNeedResp:
        #     reply = t880xPlusEncoder.getAccelerationAlarmMsgReply(message.imei,True,message.serialNo)
        #     socketClient.send(reply)
        reply = t880xPlusEncoder.getAccelerationAlarmMsgReply(message.imei,True,message.serialNo)
        socketClient.send(reply)
    elif isinstance(message,ConfigMessage):
        print ("receive configMessage: " + message.imei + " : " + message.configContent)
    elif isinstance(message,ForwardMessage):
        print ("receive forwardMessage: " + message.imei + " : " + message.content)
    elif isinstance(message,USSDMessage):
        print ("receive forwardMessage: " + message.imei + " : " + message.content)
    elif isinstance(message,RS232Message):
        print ("receive RS232 Message: " + message.imei)
        # if message.isNeedResp:
        #     reply = t880xPlusEncoder.getRS232MsgReply(message.imei,True,message.serialNo)
        #     socketClient.send(reply)
        reply = t880xPlusEncoder.getRS232MsgReply(message.imei,True,message.serialNo)
        socketClient.send(reply)
    elif isinstance(message,BluetoothPeripheralDataMessage):
        print ("receive blue Message: " + message.imei)
        # if message.isNeedResp:
        #     reply = t880xPlusEncoder.getBluetoothPeripheralMsgReply(message.imei,True,message.serialNo,message.protocolHeadType)
        #     socketClient.send(reply)
        reply = t880xPlusEncoder.getBluetoothPeripheralMsgReply(message.imei,True,message.serialNo,message.protocolHeadType)
        socketClient.send(reply)
    elif isinstance(message,NetworkInfoMessage):
        print ("receive network info Message: " + message.imei)
        # if message.isNeedResp:
        #     reply = t880xPlusEncoder.getNetworkMsgReply(message.imei,True,message.serialNo)
        #     socketClient.send(reply)
        reply = t880xPlusEncoder.getNetworkMsgReply(message.imei,True,message.serialNo)
        socketClient.send(reply)
    
    if reply is not None:
        printSendMessage(reply)

def dealPersonalDeviceMessage(message,socketClient):
    """
    Device model like :8806 plus, use this method.
    :param message:
    :param socketClient:
    :return:
    """
    if isinstance(message,SignInMessage):
        print ("receive signInMessage: " + message.imei)
        # if message.isNeedResp:
        #     reply = personalEncoder.getSignInMsgReply(message.imei,True,message.serialNo)
        #     socketClient.send(reply)
        reply = personalEncoder.getSignInMsgReply(message.imei,True,message.serialNo)
        socketClient.send(reply)
    elif isinstance(message,HeartbeatMessage):
        print ("receive heartbeatMessage" + message.imei)
        # if message.isNeedResp:
        #     reply = personalEncoder.getHeartbeatMsgReply(message.imei,True,message.serialNo)
        #     socketClient.send(reply)
        reply = personalEncoder.getHeartbeatMsgReply(message.imei,True,message.serialNo)
        socketClient.send(reply)
    elif isinstance(message,LocationInfoMessage):
        print ("receive locationInfoMessage" + message.imei)
        # if message.isNeedResp:
        #     reply = personalEncoder.getLocationMsgReply(message.imei,True,message.serialNo,message.originalAlarmCode)
        #     socketClient.send(reply)
        reply = personalEncoder.getLocationMsgReply(message.imei,True,message.serialNo)
        socketClient.send(reply)
        sendDataToTrackin(message)
    elif isinstance(message,LocationAlarmMessage):
        print ("receive locationAlarmMessage" + message.imei + " Alarm is : " + str(message.originalAlarmCode))
        # if message.isNeedResp:
        #     reply = personalEncoder.getLocationAlarmMsgReply(message.imei,True,message.serialNo,message.originalAlarmCode)
        #     socketClient.send(reply)
        reply = personalEncoder.getLocationAlarmMsgReply(message.imei,True,message.serialNo,message.originalAlarmCode)
        socketClient.send(reply)
        Thread(target=sendDataToTrackin, args=(message)).start()
    elif isinstance(message,ConfigMessage):
        print ("receive configMessage: " + message.imei + " : " + message.configContent)
    elif isinstance(message,ForwardMessage):
        print ("receive forwardMessage: " + message.imei + " : " + message.content)
    elif isinstance(message,USSDMessage):
        print ("receive forwardMessage: " + message.imei + " : " + message.content)
    elif isinstance(message,BluetoothPeripheralDataMessage):
        print ("receive blue Message: " + message.imei)
        # if message.isNeedResp:
        #     reply = personalEncoder.getBluetoothPeripheralMsgReply(message.imei,True,message.serialNo)
        #     socketClient.send(reply)
        reply = personalEncoder.getBluetoothPeripheralMsgReply(message.imei,True,message.serialNo)
        socketClient.send(reply)
    elif isinstance(message,WifiMessage):
        print ("receive wifi location Message: " + message.imei)
        reply = personalEncoder.getWifiMsgReply(message.imei,True,message.serialNo)
        socketClient.send(reply)
    elif isinstance(message,LockMessage):
        print ("receive lock Message: " + message.imei)
        reply = personalEncoder.getLockMsgReply(message.imei,True,message.serialNo)
        socketClient.send(reply)
    elif isinstance(message,NetworkInfoMessage):
        print ("receive network info Message: " + message.imei)
        # if message.isNeedResp:
        #     reply = personalEncoder.getNetworkMsgReply(message.imei,True,message.serialNo)
        #     socketClient.send(reply)
        reply = personalEncoder.getNetworkMsgReply(message.imei,True,message.serialNo)
        socketClient.send(reply)

def printReciveMessage(message):
    if isinstance(message, Message):
        print("Recive:", end=" ")
        for x in message.orignBytes:
            print('{:02X}'.format(x), end=" ")
        print("")

def printSendMessage(reply):
    if not (reply is None):
        print("Reponse:", end=" ")
        for x in reply:
            print('{:02X}'.format(x), end=" ")
        print("")

def sendDataToTrackin(message):
    json_str = json.dumps(message.__dict__, default=myconverter)

    headers = {'Content-type': 'application/json'}
    response = requests.post("http://trackin:4762/data", data=json_str, headers=headers)

    print(str(message.imei) + " Respuesta Trackin: " + str(response.status_code))



def on_new_client(clientsocket, addr):
    print("\nConnection received from %s" % str(addr))
    while True:
        try:
            data = clientsocket.recv(2048)
        except socket.error as e:
            if e.errno != errno.ECONNRESET:
                raise
            pass
            
        if not data:
            print("End of file from client. Resetting")
            break

        messageList = decoder.decode(data)

        for message in messageList:
            # printReciveMessage(message)
            dealNoObdDeviceMessage(message,c)
            # dealObdDeviceMessage(message,c)
            # dealPersonalDeviceMessage(message,c)
            # configGood = t880xPlusEncoder.getConfigSettingMsg("867730050816697", "CONFIG#")
            # c.send(configGood)
            # print(configGood)

    clientsocket.close()

if __name__ == "__main__":
    print("  _______                   ______   _                    _____                              _               \n |__   __|                 |  ____| | |                  |  __ \\                            | |              \n    | |      ___    _ __   | |__    | |  _   _   ______  | |  | |   ___    ___    ___     __| |   ___   _ __ \n    | |     / _ \\  | '_ \\  |  __|   | | | | | | |______| | |  | |  / _ \\  / __|  / _ \\   / _` |  / _ \\ | '__|\n    | |    | (_) | | |_) | | |      | | | |_| |          | |__| | |  __/ | (__  | (_) | | (_| | |  __/ | |   \n    |_|     \\___/  | .__/  |_|      |_|  \\__, |          |_____/   \\___|  \\___|  \\___/   \\__,_|  \\___| |_|   \n                   | |                    __/ |                                                              \n                   |_|                   |___/                                                               ")
    HOST, PORT = "0.0.0.0", 1001
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(5)
    s.settimeout(None)
    print("Listening on address %s. Kill server with Ctrl-C" %
      str((HOST, PORT)))
    decoder = Decoder(MessageEncryptType.NONE,"")
    while True:
        print("Waiting...")
        c, addr = s.accept()
        # decoder = ObdDecoder(MessageEncryptType.NONE,"")
        # decoder = PersonalAssetMsgDecoder(MessageEncryptType.NONE,"")
        Thread(target=on_new_client, args=(c, addr)).start()
