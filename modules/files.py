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

import maya.cmds as cmds
import os
import warnings
import shutil
from send2trash import send2trash
import operator
import sys
import subprocess
import glob
import logging

def dir_rename(dir_fullpath, new_name):
    
    new_dir = os.path.join(os.path.dirname(dir_fullpath),new_name)
    #create_directory(new_dir)
    try:
        shutil.move(dir_fullpath, new_dir)
        return new_dir
    except:
        return False

def dir_move(dir_fullpath, new_dir_fullpath):
    
    try:
        shutil.move(dir_fullpath, new_dir_fullpath)
        return new_dir_fullpath
    except:
        return False
        
            
def file_rename(fullpath, new_name):
    '''
    input: string, fullpath of the file to rename
           string, new_name without the extension
    output True if the rename is successful        
    '''
    dir = os.path.dirname(fullpath)
    
    name = file_name(fullpath)
    file_extension = extension(name)
    new_name_with_extension = new_name + file_extension
    
    new_fullpath = os.path.join(dir,new_name_with_extension)
    
    try:
        os.rename(fullpath, new_fullpath)
        return new_fullpath
    except:
        return False
    

def file_copy(source, dest):
    if os.path.exists(source):
        try:
            return shutil.copy2(source, dest)
        except:
            return None
    else:
        return None


def find_by_name(path, name):
    files = []
    for file in glob.glob(os.path.join(path, "%s.*"%(name))):
        files.append(file)
    
    if len(files)>0:
        return files
    else:
        return None
        
        
def file_name(fullPath):
    return os.path.basename(fullPath)

def file_name_no_extension(file_name):
    return os.path.splitext(file_name)[0]

def extension(file_name):
    return os.path.splitext(file_name)[1]

def extract_asset_comp_name(file_name_, padding = None):
    if os.path.isfile(file_name_):
        fullname = file_name_no_extension(file_name(file_name_))
        try:            
            asset_name = fullname.split("_")[0]
            split_name = fullname.split("_")

            master = split_name[1:][-1]
            number = split_name[1:][-1]
            master_version = split_name[1:][-2]

            if len(number) == padding and number.isdigit():
                #print "version case"
                component_name = ""
                for part in split_name[1:][:-1]:
                    component_name = component_name + part + "_"
                component_name = component_name[:-1]
            
            if len(number) == padding and number.isdigit() and master_version == "MASTER":   
                #print "master_version case"
                component_name = ""
                for part in split_name[1:][:-2]:
                    component_name = component_name + part + "_"
                component_name = component_name[:-1]
                      
            if master == "MASTER":
                #print "master case"
                component_name = ""
                for part in split_name[1:][:-1]:
                    component_name = component_name + part + "_"
                component_name = component_name[:-1]
                                
            return asset_name, component_name                

        except:
            return False
            
        
def list_directory(path,type):
    '''
    This method return all files of given type in a folder
        
    @param path: directory to map
    @type path: string
    
    @param type: type of files to list
    @type type: string
    
    @return: list of strings
    '''    
    if os.path.exists(path):        
        fullNames = []
        for file in os.listdir(path):        
            if os.path.isfile(os.path.join(path, file)):
                if extension(file)[1:] == type:
                    fullNames.append(os.path.join(path, file))

        return fullNames
    else:
        return None


def list_all_directory(path):
    '''
    This method return all files in a folder
        
    @param path: directory to map
    @type path: string
        
    @return: list of strings
    '''    
    if os.path.exists(path):        
        fullNames = []
        for file in os.listdir(path):        
            fullNames.append(os.path.join(path, file))

        return fullNames
    else:
        return None

def list_dir_folders(path):
    return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]


def assure_path_exists(path):
        dir = os.path.dirname(path)
        if not os.path.exists(dir):
                os.makedirs(dir)

def assure_folder_exists(path):
        if not os.path.exists(path):
                os.makedirs(path)

def reletive_path(absolute_path, path):
    return os.path.relpath(path, absolute_path)

def is_subdir(dir,subdir):
    return subdir.startswith(os.path.abspath(dir)+'/')

def create_directory(path):
                     
    if not os.path.exists(path):
        os.makedirs(path)
        return True
    else:
        warnings.warn("Path exists")    
        return False

def create_dummy(path, file_name):
        assure_path_exists(os.path.join(path,file_name))
        file = open(os.path.join(path,file_name),'w')
        file.close()

def delete(path):
    if path:                 
        if os.path.exists(path):
            # shutil.rmtree(path) DELETE FOR GOOD
            send2trash(path) # SEND TO BIN
            return True
        else:
            warnings.warn("Unable to delete")    
            return False

def delete_file(path):
    if path:
        if os.path.isfile(path):
            os.remove(path)
            return True
        else:
            warnings.warn("Unable to delete")    
            return False    

def file_size_mb(filePath):
    if filePath: 
        if os.path.exists(filePath):
            return (os.path.getsize(filePath)) / (1024 * 1024.0)
        else:
            return None
        
def extract_version(file, padding):
    return file[-padding:]

def dict_versions(versions,padding):
    '''
    This method return a dictionery of versions and their file path
        
    @param workshops: workshops as paths ["/folder/file0001.ma","/folder/file0002.ma",...]
    @type workshops: list of strings
    
    @param padding: number padding of version names
    @type padding: int
    
    @return: dict: {version: "path",...}
    '''
  
    versions_dict = {}
    
    for version in versions:
        try:
            name = file_name_no_extension(file_name(version))
            versions_dict[int(name[-padding:len(name)])] = version
        except:
            pass
            #logging.info( "cant find version in %s"%version)
    return versions_dict
        

def sort_version(versions_dict):
    '''
    @return: list of tuples: [(version, "path"),...]
    '''
    sorted_list_of_tupels = sorted(versions_dict.items(), key=operator.itemgetter(1))
    versions = []
    for entry in sorted_list_of_tupels:
        versions.append(entry[0])
    
    return sorted(versions)
    #return sorted(versions_dict.items(), key=operator.itemgetter(1))

def os_qeury():
    return sys.platform 
    
def explore(path):

    if os.path.exists(path):
        path = os.path.dirname(path)
        platform = os_qeury()
        if platform == "darwin":
            subprocess.Popen(['open',path])
        elif platform == "win32":
            os.startfile(path)
        
        
def run(filename):
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener ="open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])            
