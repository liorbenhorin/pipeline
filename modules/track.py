'''

PIPELINE 

BETA 1.0.0

Project manager for Maya

Ahutor: Lior Ben Horin
All rights reserved (c) 2016 
    
liorbenhorin.ghost.io
liorbenhorin@gmail.com

---------------------------------------------------------------------------------------------

install:

Place the pipeline folder in your maya scripts folder. Run these lines in a python tab in the script editor:
 
from pipeline import pipeline
reload(pipeline)
pipeline.show()

---------------------------------------------------------------------------------------------

You are using PIPELINE on you own risk. 
Things can allways go wrong, and under no circumstances the author
would be responsible for any damages cuesed from the use of this software.
When using this beta program you hearby agree to allow this program to collect 
and send usage data to the author.

---------------------------------------------------------------------------------------------  

The coded instructions, statements, computer programs, and/or related
material (collectively the "Data") in these files are subject to the terms 
and conditions defined by
Creative Commons Attribution-NonCommercial-NoDerivs 4.0 Unported License:
   http://creativecommons.org/licenses/by-nc-nd/4.0/
   http://creativecommons.org/licenses/by-nc-nd/4.0/legalcode
   http://creativecommons.org/licenses/by-nc-nd/4.0/legalcode.txt

---------------------------------------------------------------------------------------------  

'''


import os
import sys
import socket
import threading
import urllib
import urllib2
import json
import logging
logging.basicConfig(level=logging.INFO)

import pipeline.modules.mixpanel as mixpanel
reload(mixpanel)

_users = False
        

def track_event(id = None, event = None, data = None):
    if id and event and data:

        g = geo()
        if geo:
            data['country'] = g['country']
            data['regionName'] = g['regionName']
            data['query'] = g['query'] 
            
        mp = mixpanel.Mixpanel("044cfc882c3fef3212a90aa9bab46ef8")
        mp.track(id, event, data)                  
        #logging.info(event)
        #logging.info(data)
        
        return

        
def event(name = None, **kwargs):    
    if name and kwargs:
        kwargs["operating-system"] = sys.platform
        kwargs["host-name"] = socket.gethostname()
        t = threading.Thread(target = track_event, kwargs = {'id': socket.gethostname(), 'event': name, 'data': kwargs})
        t.start()
        t.join()  
        

def geo():
    try:
        geo = json.load(urllib2.urlopen('http://ip-api.com/json'))
        return geo
    except:
        pass
    
    return None     
    
    
    
 
   