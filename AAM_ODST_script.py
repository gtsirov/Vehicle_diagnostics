#GTSIROV
#v2019-nov-21

import win32com.client
import datetime
import os
import time
import codecs
from datetime import datetime

testServer = win32com.client.Dispatch("CorvusTestServer.CorvusTestRoot")
root = testServer.GetTestInstanceEx()
vehicle = root.Vehicles.AddNew()
channel_gwm = vehicle.Channels.AddNew()
channel_aam = vehicle.Channels.AddNew()

#------------------------------------------------------------------
def Main():
    try:
        file = open('ODST_log.txt', 'a')
        now = (datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        file.write('Test start: ' + now + '\n')
        file.close()
        #------------------------------------------------------------------
        # User Network selection
        networks = root.NetworkTypes.ListAll()
        numberofnetworks = networks.Count
        i = 0
        networknames = []
        for x in range(numberofnetworks):
            networknames.append(networks[i].Name)
            i = i + 1

        print( "Available network types:" )

        for a, b in enumerate(networknames, 0):
            print( '{}: {}'.format(a, b) )

        #snetwork = input("Select network type by number: ")
        snetwork = 5
        channel_gwm.Properties.NetworkType = networks[snetwork]
        channel_aam.Properties.NetworkType = networks[snetwork]
        print( "Selected Network is: " + networks[snetwork].Name )
        #------------------------------------------------------------------

        #------------------------------------------------------------------
        # User interface selection
        interfaces = root.GetDeviceInterface(networks[snetwork]).ListAll()
        numberofinterfaces = interfaces.Count
        i = 0
        interfacenames = []
        for x in range(numberofinterfaces):
            interfacenames.append(interfaces[i].Name)
            i = i + 1

        print( "\nAvailable interface types:" )

        for a, b in enumerate(interfacenames, 0):
            print( '{}: {}'.format(a, b) )

        #sinterface = input("Select interface type by number: ")
        sinterface = 0
        channel_gwm.Properties.DeviceInterface = interfaces[sinterface]
        channel_aam.Properties.DeviceInterface = interfaces[sinterface]
        print( "Selected Interface is: " + interfaces[sinterface].Name )
        #------------------------------------------------------------------

        #------------------------------------------------------------------
        # User device selection
        devicechannels = interfaces[sinterface].DeviceChannels.ListAll()
        numberofdevicechannels = devicechannels.Count
        i = 0
        devicechannelnames = []
        for x in range(numberofdevicechannels):
            devicechannelnames.append(devicechannels[i].Name)
            i = i + 1

        print( "\nAvailable device types:" )

        for a, b in enumerate(devicechannelnames, 0):
            print( '{}: {}'.format(a, b) )

        #sdevicechannel = input("Select device type by number: ")
        sdevicechannel = 0
        channel_gwm.Properties.DeviceChannel = devicechannels[sdevicechannel]
        channel_aam.Properties.DeviceChannel = devicechannels[sdevicechannel]
        print( "Selected Interface is: " + devicechannels[sdevicechannel].Name )
        #------------------------------------------------------------------
        print( '----------' )
        
        #------------------------------------------------------------------
        # Create ECU GWM
        ecu_gwm = channel_gwm.ECUs.AddNew()
        ecu_gwm.Properties.Name = "GWM"
        ecu_gwm.Properties.RequestId = 0x1716
        ecu_gwm.Properties.ResponseId = 0x0E80
        print( 'channel_gwm Id:', channel_gwm.Id )
        #------------------------------------------------------------------

        #------------------------------------------------------------------
        # Create ECU AAM
        ecu_aam = channel_aam.ECUs.AddNew()
        ecu_aam.Properties.Name = "AAM"
        ecu_aam.Properties.RequestId = 0x17A4
        ecu_aam.Properties.ResponseId = 0x0E80
        #print(bytes.fromhex('0E80'))
        print( 'channel_aam Id:', channel_aam.Id )
        #------------------------------------------------------------------

        #------------------------------------------------------------------
        # Connect to GWM
        channel_gwm.NetworkConfiguration.Properties.GetItemByName('ECUID').Value = "1716"

        if channel_gwm.IsConnected == True:
            print( "channel_gwm already connected" )
        else:
            connect(channel_gwm)
        #------------------------------------------------------------------
        
        #------------------------------------------------------------------
        # Connect to AAM
        channel_aam.NetworkConfiguration.Properties.GetItemByName('ECUID').Value = "17A4"
        
        if channel_aam.IsConnected == True:
            print( "channel_aam already connected" )
        else:
            connect(channel_aam)

        #------------------------------------------------------------------
        #AAM_ODST sequence
        start_time = time.time()
        i = 0
        while i < 10000:
            file = open('ODST_log.txt', 'a')
            '''force_message(ecu_aam, '1001')
            time.sleep(0.5)
            force_message(ecu_aam, '3E00')
            time.sleep(0.5)
            force_message(ecu_aam, '3E00')
            time.sleep(0.5)
            force_message(ecu_aam, '22F186')
            time.sleep(0.5)        
            force_message(ecu_aam, '1003')
            time.sleep(0.5)
            force_message(ecu_aam, '3E00')
            time.sleep(0.5)
            force_message(ecu_aam, '3E00')
            time.sleep(0.5)
            force_message(ecu_aam, '22F186')
            time.sleep(0.5)'''
            time.sleep(5)
            force_message(ecu_aam, '1003')
            time.sleep(0.5)
            force_message(ecu_aam, '3E00')
            force_message(ecu_gwm, '3E00')
            time.sleep(0.5)
            force_message(ecu_aam, '3E00')
            force_message(ecu_gwm, '3E00')
            time.sleep(0.5)
            force_message(ecu_aam, '31010202')
            while True:
                time.sleep(0.5)
                #force_message(ecu_aam, '1003')
                status = ecu_aam.ExecuteMessage('31 03 02 02')                
                result = ecu_aam.Receive()
                print( 'Received: ' + result.DataString )
                if result == None:
                    print('GWM disconnected')
                elif result.DataString[0:14] == '71 03 02 02 7A':
                    if i == 0:
                        first_result = result.DataString
                    elif first_result == result.DataString:
                        file.write(result.DataString + 'PASS' + '\n')
                        file.close()
                    else:
                        file.write(result.DataString + 'FAIL' + '\n')
                        file.close()
                    break
                elif result.DataString[0:14] == '71 03 02 02 79':
                    print('Busy')
                else:
                    print('Unexpected response')
                    break
            i += 1
            print('Test_counter =',i)
        #------------------------------------------------------------------
        # Disconnect channels

        file.write("Test time: %s seconds" % (time.time() - start_time))
        time.sleep(2)
        file.close()
        channel_gwm.Disconnect()
        print( "channel_gwm disconnected" )
        channel_aam.Disconnect()
        print( "channel_aam disconnected" )
        
        print( "--- END ---" )
        time.sleep(2)
        #------------------------------------------------------------------
    except:
        print( "--- ERROR ---" )
        file.close()
        channel_gwm.Disconnect()
        print( "channel_gwm disconnected" )
        channel_aam.Disconnect()
        print( "channel_aam disconnected" )
        print( "--- END ---" )
    finally:
        testServer = None

#------------------------------------------------------------------
# Connect to channel
def connect(channel):
    i = 1
    while channel.IsConnected == False and i < 10:
        channel.Connect()
        if channel.IsConnected == False:
            print( 'Connection attempt ' + str(i) + ' Failed', channel.Id )
            i = i + 1
        else:
            print( 'Channel connected:', channel.Id )
    if i == 11:
        exit()
#------------------------------------------------------------------

#------------------------------------------------------------------
# Message to ECU
def message(ecu, message):
    print( "Sending to " +ecu.Properties.Name + ": " + message )
    status = ecu.ExecuteMessage(message)
    result = ecu.Receive()
    print( 'Received: ' + result.DataString )
#------------------------------------------------------------------

#------------------------------------------------------------------
# Message to ECU
def force_message(ecu, message):
    i = 0
    result = None
    while result == None and i < 5:
        print( "Sending to " +ecu.Properties.Name + ": " + message )
        status = ecu.ExecuteMessage(message)
        result = ecu.Receive()
    print( 'Received: ' + result.DataString )
    #print(i)
    i += 1
#------------------------------------------------------------------

#------------------------------------------------------------------
# Message to ECU
def force_message_decoded(ecu, message):
    i = 0
    result = None
    while result == None and i < 5:
        print( "Sending to " +ecu.Properties.Name + ": " + message )
        status = ecu.ExecuteMessage(message)
        result = ecu.Receive()
        
    decode_hex = codecs.getdecoder("hex_codec")
    msg_in_hex = result.DataString.replace(' ', '')
    #msg_in_hex = msg_in_hex.replace("62F188","")

    decodedhex = decode_hex(msg_in_hex)[0]
    #decodedhex = decodedhex.replace("\\x00", "")
    #decodedhex = decodedhex.decode("utf-8").strip()
    decodedhex = decodedhex.decode("ascii").strip()

    print( decodedhex )

    return decodedhex
    """
    print( result.DataString.replace(' ', '').decode('Hex') )
    data = result.DataString.replace(' ', '').decode('Hex')
    return data
    """
#------------------------------------------------------------------


# Run Main() function  
Main()
