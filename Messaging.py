# Author: Manas Bhatt
# Contact: manas.bh4tt@gmail.com
# Date : Aug 2022

#python functions to send message to mobile devices

import requests
import json

url='https://wirepusher.com/send'
msg='Hi Alex'
id='aDjjmpss7'
title='Test Message'

def sendWPMessage(deviceId, wpUrl, title, message):
    params = { 'id' : deviceId,
               'title' :  title,
               'message' : message,
               'type': 'GreekCalculator'
  #             'type' : 'monitoring'
               }

    req = requests.Request('GET', wpUrl, params = params).prepare()
    #print(req.url)

    response = requests.session().send(req)
    json_response = response.json()

    print(json_response)
    #if json_response['status'] == False:
    #    return print(f"Error sending Message : {json_response['error']}")
    
    print(json_response["results"][1])
    
               
