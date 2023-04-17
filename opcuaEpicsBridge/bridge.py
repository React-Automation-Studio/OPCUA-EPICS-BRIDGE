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
from dbtoolspy import load_template_file, load_database_file

class SubHandler(object):

    """
    Subscription Handler. To receive events from server for a subscription
    data_change and event methods are called directly from receiving thread.
    Do not do expensive, slow or network operation there. Create another 
    thread if you need to do such a thing
    """

    def datachange_notification(self, node, val, data):
        epicsName=self.clients[self.clientName]["opcuaToEpicsNames"][str(node)]
        if self.debug:
            print("client Name:",self.clientName)
            print("client Url:",self.clientUrl)
            print("client Node:", node)
            print("client val:", val)
            print("epics name",epicsName)
            print(str(self.epicsPvs[epicsName]["epicsType"]))
        if self.epicsPvs[epicsName]["initialized"]:

            if self.epicsPvs[epicsName]["epicsType"] in ["AI","BI"]:
                if self.debug:
                    print("val:", val)
                    print("val type:", type(val))
                    print("val name:", epicsName)
                self.epicsPvs[epicsName]["pv"].set(val)
        else:
            self.epicsPvs[epicsName]["pv"].set(val)
            self.epicsPvs[epicsName]["initialized"]=True

    def event_notification(self, event):
        if self.debug:
            print("Python: New event", event)
    def setClientNameAndUrl(self,name,url):
        self.clientName=name
        self.clientUrl=url
    def setClients(self,clients):
        self.clients=clients
    def setEpicsPvs(self,epicsPvs):
        self.epicsPvs=epicsPvs
    def setDebug(self,debug):
        self.debug=debug
        

if __name__ == "__main__":
    def on_epics_pv_update(val,opcuaClientName,epicsPvName,epicsType,opcuaType,opcuaName,opcuaClients,ZNAM=None,ONAM=None,debug=None,**kwargs):
        if debug:
            print("on_epics_pv_update val:",val)
            print("on_epics_pv_update clientName:",opcuaClientName)
            print("on_epics_pv_update epicsPvName:",epicsPvName)
            print("on_epics_pv_update epicsType:",epicsType)
            
        client=opcuaClients[opcuaClientName]["client"]
        var=client.get_node(opcuaName)
        
        currentValue=var.get_value()
        
        if "BO" in epicsType:
            x=int(val)==1
            # print("val,x",val,x)
            dv = ua.DataValue(ua.Variant(int(val)==1, ua.VariantType.Boolean))
            var.set_value(dv)
       
                        
        else:
            newValue=str(val)  
            if newValue!=str(currentValue):
                if opcuaType=='Float':
                    dv = ua.DataValue(ua.Variant(float(newValue), ua.VariantType.Float))
                    var.set_value(dv)
                elif opcuaType=='Double':
                    dv = ua.DataValue(ua.Variant(float(newValue), ua.VariantType.Double))
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
                elif opcuaType=='Byte':
                    dv = ua.DataValue(ua.Variant(int(float(newValue)), ua.VariantType.Int16))
                    var.set_value(dv)
                else:
                    print("incorrect opcua type")
                
        # cothread.Sleep(1)   
        if debug:
            print(f"on_epics_pv_update pv: {epicsPvName} opcua currentValue: {currentValue}")
        
    clients={}
    epicsPvs={}
    logging.basicConfig(level=logging.WARNING)
   
    

    try:
        debug = os.getenv("debug", False)=="True"
        name = os.getenv("name", None)
        url = os.getenv("url", None)
        try:
            subscriptionRate = int(os.environ["subscriptionRate"])
        except:
            subscriptionRate = 1000
        db=load_database_file("bridge.db")
        
        clients[name]={}
        opcuaClient=clients[name]
        opcuaClient["client"]=Client(url)
        
        # opcuaClient["client"].set_security_string("Basic256Sha256,SignAndEncrypt,../certificates/my_cert.der,../certificates/my_private_key.pem")
        opcuaClient["client"].connect()
        opcuaClient["handler"] = SubHandler()
        opcuaClient["handler"].setClientNameAndUrl(name,url)
        opcuaClient["handler"].setClients(clients)
        opcuaClient["handler"].setEpicsPvs(epicsPvs)
        opcuaClient["handler"].setDebug(debug)

        
        opcuaClient["sub"] = opcuaClient["client"].create_subscription(subscriptionRate, opcuaClient["handler"])
        opcuaClient["opcuaToEpicsNames"]={}
        opcuaClient["epicsToOpcuaNames"]={}
        
        for record in db.values():
            DTYP=str(record.fields["DTYP"]).upper()
            if "OPCUA" in DTYP:
                
                epicsPvName=str(record.name)
            
                epicsType=str(record.rtyp).upper()
                opcuaType=(DTYP.split("_"))[1].capitalize()
                epicsPvs[epicsPvName]={}
                epicsPvs[epicsPvName]["initialized"]=False
                    
                if "AI" in epicsType:
                    opcuaName=str(record.fields["INP"])
                    fields={}
                    for field in record.fields:
                        upper=str(field).upper()
                        if upper in ["DESC","EGU","HOPR","LOPR","PREC"]:
                            fields[upper]=record.fields[field]
                    
                    epicsPvs[epicsPvName]["pv"]=builder.aIn(epicsPvName,**fields)
                    epicsPvs[epicsPvName]["epicsType"]="AI"
                    

                if "AO" in epicsType:
                    opcuaName=str(record.fields["OUT"])
                    fields={}
                    for field in record.fields:
                        upper=str(field).upper()
                        if upper in ["DESC","EGU","HOPR","LOPR","PREC"]:
                            fields[upper]=record.fields[field]
                    epicsPvs[epicsPvName]["pv"]=builder.aOut(epicsPvName,on_update=partial(on_epics_pv_update,opcuaClientName=name,epicsPvName=epicsPvName,epicsType=epicsType,opcuaName=opcuaName,opcuaType=opcuaType,opcuaClients=clients,debug=debug,**fields),**fields)
                    epicsPvs[epicsPvName]["epicsType"]="AO"

                elif "BO" in epicsType:
                    opcuaName=str(record.fields["OUT"])
                    fields={}
                    for field in record.fields:
                        upper=str(field).upper()
                        if upper in ["ZNAM","ONAM","DESC","EGU","HOPR","LOPR","PREC"]:
                            fields[upper]=record.fields[field]
                    epicsPvs[epicsPvName]["pv"]=builder.boolOut(epicsPvName,on_update=partial(on_epics_pv_update,opcuaClientName=name,epicsPvName=epicsPvName,epicsType=epicsType,opcuaName=opcuaName,opcuaType=opcuaType,opcuaClients=clients,**fields),**fields)
                    epicsPvs[epicsPvName]["epicsType"]="BO"
                elif "BI" in epicsType:
                    opcuaName=str(record.fields["INP"])
                    fields={}
                    for field in record.fields:
                        upper=str(field).upper()
                        if upper in ["ZNAM","ONAM","DESC","EGU","HOPR","LOPR","PREC"]:
                            fields[upper]=record.fields[field]
                    epicsPvs[epicsPvName]["pv"]=builder.boolIn(epicsPvName,**fields)
                    epicsPvs[epicsPvName]["epicsType"]="BI"
                opcuaClient["opcuaToEpicsNames"][str(opcuaName)]=str(epicsPvName)
                opcuaClient["epicsToOpcuaNames"][str(epicsPvName)]=str(opcuaName)    
                opcuaClient["sub"].subscribe_data_change(opcuaClient["client"].get_node(opcuaName))
        # except Exception as e:
        #     print("e1",e)
    except Exception as e:
        print("exception",e)
        exit(1)
    
    print(str(opcuaClient["opcuaToEpicsNames"]))
    print(str(opcuaClient["epicsToOpcuaNames"]))
    # softioc.dbLoadDatabase("test.db")
    builder.LoadDatabase()
    softioc.iocInit()
    print("EPICS OPCUA bridge loaded")
    print(F"OPCUA HOST URL: {url}")
    
    print("\nThe following bridge PVs are loaded:\n")

    softioc.dbgrep("*")
    print("\n")
    try:
        
        while True:
            cothread.Sleep(0.1)
    finally:
        for clientName in clients:
            client=clients[clientName]["client"]
            client.disconnect()
