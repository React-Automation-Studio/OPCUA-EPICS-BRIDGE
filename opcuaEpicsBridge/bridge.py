import sys
sys.path.insert(0, "..")
import logging
import time
import os
import json
from asyncua.sync import Client,ua
from softioc import softioc, builder
import cothread
from functools import partial



def loadConfig():
    try:
        path='config/config.json'
        
        with open(path) as json_file:
            data = json.load(json_file)
            
            return data
    except:
        print("Error: Can't load file config.json")
        return None

 

class SubHandler(object):

    """
    Subscription Handler. To receive events from server for a subscription
    data_change and event methods are called directly from receiving thread.
    Do not do expensive, slow or network operation there. Create another 
    thread if you need to do such a thing
    """

    def datachange_notification(self, node, val, data):
        print("client Name:",self.clientName)
        print("client Url:",self.clientUrl)
        print("client Node:", node)
        print("client val:", val)
        # opcuaClient=self.clients[self.clientUrl]
        epicsName=self.clients[self.clientName]["opcuaToEpicsNames"][str(node)]
        print("epics name",epicsName)
        self.epicsPvs[epicsName].set(val)
    def event_notification(self, event):
        print("Python: New event", event)
    def setClientNameAndUrl(self,name,url):
        self.clientName=name
        self.clientUrl=url
    def setClients(self,clients):
        self.clients=clients
    def setEpicsPvs(self,epicsPvs):
        self.epicsPvs=epicsPvs
        

if __name__ == "__main__":
    def on_epics_pv_update(val,opcuaClientName,epicsPvName,epicsType,opcuaType,opcuaName,opcuaClients,ZNAM=None,ONAM=None):
        print("on_epics_pv_update val:",val)
        print("on_epics_pv_update clientName:",opcuaClientName)
        print("on_epics_pv_update epicsPvName:",epicsPvName)
        print("on_epics_pv_update epicsType:",epicsType)
        
        client=opcuaClients[opcuaClientName]["client"]
        var=client.get_node(opcuaName)
        
        currentValue=var.get_value()
        if "BO" in epicsType:
            if ZNAM:
                if ONAM:
                    if int(val)==1:
                        newValue=str(ONAM)
                    else:
                        newValue=str(ZNAM)
                    if newValue!=str(currentValue):
                        dv = ua.DataValue(ua.Variant(newValue=='True', ua.VariantType.Boolean))
                        var.set_value(dv)
                else:
                    if newValue!=str(currentValue):
                        dv = ua.DataValue(ua.Variant(newValue=='1', ua.VariantType.Boolean))
                        var.set_value(dv)  
            else:
                if newValue!=str(currentValue):
                    dv = ua.DataValue(ua.Variant(newValue=='0', ua.VariantType.Boolean))
                    var.set_value(dv)
        elif "BI" in epicsType:
            if ZNAM:
                if ONAM:
                    if int(val)==1:
                        newValue=str(ONAM)
                    else:
                        newValue=str(ZNAM)
                    if newValue!=str(currentValue):
                        dv = ua.DataValue(ua.Variant(newValue=='True', ua.VariantType.Boolean))
                        var.set_value(dv)
                else:
                    if newValue!=str(currentValue):
                        dv = ua.DataValue(ua.Variant(newValue=='1', ua.VariantType.Boolean))
                        var.set_value(dv)  
            else:
                if newValue!=str(currentValue):
                    dv = ua.DataValue(ua.Variant(newValue=='0', ua.VariantType.Boolean))
                    var.set_value(dv)    
                        
        else:
            newValue=str(val)  
            print(f'xxx newValue: {newValue} current value: {currentValue}')
            if newValue!=str(currentValue):
                if opcuaType=='Float':
                    dv = ua.DataValue(ua.Variant(float(newValue), ua.VariantType.Float))
                    var.set_value(dv)
                elif opcuaType=='Int16':
                    dv = ua.DataValue(ua.Variant(int(float(newValue)), ua.VariantType.Int16))
                    var.set_value(dv)
                elif opcuaType=='Int32':
                    dv = ua.DataValue(ua.Variant(int(float(newValue)), ua.VariantType.Int32))
                    var.set_value(dv)
                elif opcuaType=='Int64':
                    dv = ua.DataValue(ua.Variant(int(float(newValue)), ua.VariantType.Int64))
                    var.set_value(dv)
                else:
                    print("incorrect opcua type")
                
        #     var.set_value(1)


        print("on_epics_pv_update opcua currentValue:",currentValue)
        
    clients={}
    epicsPvs={}
    logging.basicConfig(level=logging.WARNING)
    config=loadConfig()
    print(str(config))
    # builder.SetDeviceName("")
    
    
    for client in config["subscriptions"]:  
        try:
            name=client["name"]
            url=client["url"]

            subscriptionRate=client["subscriptionRate"]
            clients[name]={}
            opcuaClient=clients[name]
            opcuaClient["client"]=Client(url)
            
            # opcuaClient["client"].set_security_string("Basic256Sha256,SignAndEncrypt,../certificates/my_cert.der,../certificates/my_private_key.pem")
            opcuaClient["client"].connect()
            opcuaClient["handler"] = SubHandler()
            opcuaClient["handler"].setClientNameAndUrl(name,url)
            opcuaClient["handler"].setClients(clients)
            opcuaClient["handler"].setEpicsPvs(epicsPvs)
            opcuaClient["sub"] = opcuaClient["client"].create_subscription(subscriptionRate, opcuaClient["handler"])
            opcuaClient["opcuaToEpicsNames"]={}
            opcuaClient["epicsToOpcuaNames"]={}
            for pv in client["pvs"]:
                try:
                    opcuaName=pv["opcuaName"]
                    epicsPvName=pv["epicsName"]
                    
                    opcuaClient["opcuaToEpicsNames"][opcuaName]=epicsPvName
                    opcuaClient["epicsToOpcuaNames"][epicsPvName]=opcuaName
                    epicsType=pv["epicsType"]
                    opcuaType=pv["opcuaType"]
                    if "AI" in epicsType:
                        epicsPvs[epicsPvName]=builder.aOut(epicsPvName)

                    if "AO" in epicsType:
                        epicsPvs[epicsPvName]=builder.aOut(epicsPvName,on_update=partial(on_epics_pv_update,opcuaClientName=name,epicsPvName=epicsPvName,epicsType=epicsType,opcuaName=opcuaName,opcuaType=opcuaType,opcuaClients=clients))

                    elif "BO" in epicsType:
                        ZNAM=pv["epicsZNAM"] if pv["epicsZNAM"] else None
                        ONAM=pv["epicsONAM"] if pv["epicsONAM"] else None
                        epicsPvs[epicsPvName]=builder.boolOut(epicsPvName,ZNAM=ZNAM,ONAM=ONAM,on_update=partial(on_epics_pv_update,opcuaClientName=name,epicsPvName=epicsPvName,epicsType=epicsType,ZNAM=ZNAM,ONAM=ONAM,opcuaName=opcuaName,opcuaType=opcuaType,opcuaClients=clients))
                    elif "BI" in epicsType:
                        ZNAM=pv["epicsZNAM"] if pv["epicsZNAM"] else None
                        ONAM=pv["epicsONAM"] if pv["epicsONAM"] else None
                        epicsPvs[epicsPvName]=builder.boolIn(epicsPvName,ZNAM=ZNAM,ONAM=ONAM)    
                    print("opcuaName",opcuaName)
                    opcuaClient["sub"].subscribe_data_change(opcuaClient["client"].get_node(opcuaName))
                    
                except Exception as e:
                    print("e1",e)
        except Exception as e:
            print("efinal",e)
    
    builder.LoadDatabase()
    softioc.iocInit()
    softioc.dbgrep("*")
    print("here")
    try:
        
        while True:
            cothread.Sleep(0.1)
    finally:
        for clientName in clients:
            client=clients[clientName]["client"]
            client.disconnect()
