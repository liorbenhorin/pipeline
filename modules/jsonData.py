import os
import json
import string
import random
import json


class jsonDict(object):
    
    
    def __init__(self, **kwargs): 

        '''
        json file Class
        @input: 
            **keyword args:
                path(string): path to file
        @retun: class object of the file
        '''
        
        
        
        self.path = None
        self.data = None
        for key in kwargs:
            if key == "path":
                self.path = kwargs[key] 
    '''
    @property
    def path(self):
        if self.path:
            return self.path  
    '''
    def create(self, path, data):
        '''
        Create's a json file and stores a dict in it
        @input: 
            *args:
                path(string): path to new file
                data(dict): data to create in file
        @retun: class object of the file
        '''
        
        
        if not os.path.isfile(path):
            self.path = path
            with open(path, "w") as jsonFile:
                json.dump( data, jsonFile,  indent=4, sort_keys=True)                
            return self       
        else:                   
            raise ValueError('cant overwrite files')

    def remove_key(self, *args, **kwargs):
        '''
        Remove's a key from the file
        @input: 
            **keyword args:
                path(string): path to new file
            *args:
                keys (dict keys): keys to remove if exists
                
        @retun: class object of the file
        '''
        path = self.path
        for key in kwargs:
            if key == "path":
                path = kwargs[key]
                
        if os.path.isfile(path):
            with open(path, "r+") as jsonFile:
                if args:
                    data = json.load(jsonFile)
                    for a in args:
                        if a in data:                                                                
                            del data[a]
                                
                    jsonFile.seek(0)                    
                    jsonFile.truncate()    
                    json.dump( data, jsonFile,  indent=4, sort_keys=True)   
            return self            
        else:
            raise ValueError( ' file dose not exists ')
            
            
            
    def edit(self,*args,**kwargs):
        '''
        Edit key's values, if the key is not on the file it wold be added.
        @input: 
            **keyword args:
                path(string): path to new file
            *args:
                dicts(dict): dictioneries to add to file, if a dict exists in the file it would be overwritten
                
        @retun: class object of the file
        '''
        path = self.path
        for key in kwargs:
            if key == "path":
                path = kwargs[key] 

        if os.path.isfile(path):
            self.path = path
            with open(path, "r+") as jsonFile:
                if args:
                    try:
                        data = json.load(jsonFile)
                    except:
                        data = {}
                        
                    for a in args:
                        for key in a:
                            if key in data:                                                                
                                del data[key]
                                data[key] = a[key]
                            else:
                                data[key] = a[key]
                                
                    jsonFile.seek(0)                    
                    jsonFile.truncate()    
                    json.dump( data, jsonFile,  indent=4, sort_keys=True)  
            return self
        else:
            raise ValueError ('file dose not exists')
            
    def read(self, *args, **kwargs):
        '''
        Read all the file, if given keys will return only them
        @input: 
            **keyword args:
                path(string): path to new file
            *args:
                keys(dict keys): keys to read from the file
                
        @retun: data(dict)
        '''
        
        #print "READ CALL: ", self
        
        path = self.path
        for key in kwargs:
            if key == "path":
                path = kwargs[key]        
        #if path:   
        
                 
        if os.path.isfile(path):
            with open(path, "r") as jsonFile:
                if args:
                    data = {}
                    for a in args:
                        try:
                            data[a] = json.load(jsonFile)[a]  
                        except:
                            print "no key in file" 
                else:
                    try:
                        data = json.load(jsonFile)
                    except:
                        print "file is empty"
                
                try:
                    return data
                except:
                    print "no data was read" 
        else:
            raise ValueError( ' file dose not exists ')
        #else:
        #    raise ValueError ( ' path to file is needed ' )


    def clear(self):
        '''
        Clear the file
        @input: None
        @retun: None
        '''
        if self.path:
            if os.path.isfile(self.path):
                with open(path, "w") as file:
                    pass

    def print_nice(self):
        try:
            return json.dumps(self.read(),indent=2)
        except:
            import logging
            logging.info("can't print the data file")
                  

def encoded_strings():
    return ['cHJvamVjdHNfdG9vbHRpcF9sYWJlbA==',
            'cHJvamVjdHNfdG9vbHRpcF93aWRnZXQ=',            
            'c2V0VGV4dA==',
            'c2V0SGlkZGVu',
            'Tm9uIGNvbW1lcmNpYWwgdmVyc2lvbiBvZiBwaXBlbGluZQ==',
            'TkZSIHZlcnNpb24gb2YgUGlwZWxpbmU=',
            'VHJ1ZQ==',
            'RmFsc2U='] 
            
def edit_key(dict = None ,key = None ,value = None):
    
    if key in dict:                                                                
        del dict[key]
        dict[key] = value
        
        return dict
    else:
        return None
        
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


