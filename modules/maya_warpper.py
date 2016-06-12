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
import pymel.core as pm
import os
import maya.mel as mel
import string
import random
import logging

import pipeline.dialogue as dlg
reload(dlg)

import pipeline.modules.files as files
reload(files)

def new_scene():
    checkState()
    return cmds.file(new=True, f=True)

def rewind():
    cmds.currentTime(1)    
    cmds.playbackOptions(minTime=1)

        
def save_scene_as(path = None, file_name = None):
    if os.path.exists(path):
        if file_name:
            fullpath = os.path.join(path,file_name)
            cmds.file(rename = fullpath)
            return cmds.file(s=True, type="mayaAscii")    
            
            
def open_scene(path = None):
    if os.path.exists(path):
        checkState()
        return cmds.file(path, o = True, f = True, esn = False)

def current_open_file():
    return cmds.file(q=True,sn=True)              


def checkState():
# check if there are unsaved changes
    fileCheckState = cmds.file(q=True, modified=True)

    # if there are, save them first ... then we can proceed 
    if fileCheckState:
      # This is maya's native call to save, with dialogs, etc.
      # No need to write your own.
      if dlg.warning("warning", "Scene Not Saved", "Scene Not Saved, Do you want to save it first?"):
        cmds.SaveScene()
      pass
    else:
      pass
      
      

def reference_scene(path = None):      
    if os.path.exists(path):
        namesspace = files.file_name_no_extension(files.file_name(path))
        return cmds.file(path, r = True, f = True, ns = namesspace, esn = False)    
        
def import_scene(path = None):      
    if os.path.exists(path):
        namesspace = files.file_name_no_extension(files.file_name(path))
        return cmds.file(path, i = True, f = True, ns = namesspace, esn = False)    
        

def list_referenced_files():
    results = []
    links = cmds.filePathEditor(query=True, listDirectories="")
    for link in links:
        pairs =  cmds.filePathEditor(query=True, listFiles=link, withAttribute=True, status=True)
        '''
        paris: list of strings ["file_name node status ...", "file_name node status ...",...]
        we need to make this large list of ugly strings (good inforamtion seperated by white space) into a dictionry we can use
        '''        
        l = len(pairs)
        items = l/3
        order = {}
        index = 0
        
        '''
        order: dict of {node: [file_name, status],...}
        '''
        
        for i in range(0,items):
            order[pairs[index+1]] = [os.path.join(link,pairs[index]),pairs[index+2]]
            index = index + 3  
                    
        for key in order:            
            # for each item in the dict, if the status is 0, repath it
            if order[key][1] == "1": 
                results.append(order[key][0])
                    
                    
        return results
            
     
def relink_pathes(project_path = None):
    results = []
    links = cmds.filePathEditor(query=True, listDirectories="")
    for link in links:
        pairs =  cmds.filePathEditor(query=True, listFiles=link, withAttribute=True, status=True)
        '''
        paris: list of strings ["file_name node status ...", "file_name node status ...",...]
        we need to make this large list of ugly strings (good inforamtion seperated by white space) into a dictionry we can use
        '''        
        l = len(pairs)
        items = l/3
        order = {}
        index = 0
        
        '''
        order: dict of {node: [file_name, status],...}
        '''
        
        for i in range(0,items):
            order[pairs[index+1]] = [pairs[index],pairs[index+2]]
            index = index + 3  
                        
        for key in order:            
            # for each item in the dict, if the status is 0, repath it
            if order[key][1] == "0": 
                if repath(key,order[key][0],project_path):
                    results.append(key)
                    
                    
        return results

    
    
def repath(node, file, project_path):
    matches = []
    for root, dirnames, filenames in os.walk(project_path):
        for x in filenames:
            if x == file:
                matches.append([root,os.path.join(root, x)]) 
            elif x.split(".")[0] == file.split(".")[0]: #---> this second option is used when a file is useing ##### padding, we can match by name only
                
                x_ext = x.split(".")[len(x.split("."))-1]
                file_ext = file.split(".")[len(file.split("."))-1]
                if x_ext == file_ext:
                    matches.append([root,os.path.join(root, x)])
                
                
    if len(matches)>0:   
        return cmds.filePathEditor(node, repath=matches[0][0])      
     
    return None                           

    
def snapshot(path = None, width = 96, height = 96):
    current_image_format = cmds.getAttr("defaultRenderGlobals.imageFormat")
    cmds.setAttr("defaultRenderGlobals.imageFormat", 32)
    #path = "/Users/liorbenhorin/Library/Preferences/Autodesk/maya/2015-x64/scripts/pipeline/thumb.png"
    cmds.playblast(cf = path, fmt="image", frame = cmds.currentTime( query=True ), orn=False, wh = [width,height], p=100, v=False)
    cmds.setAttr("defaultRenderGlobals.imageFormat", current_image_format)
    
    if os.path.isfile(path):
        return path
    else:
        return False
    

def create_scriptjob(parent = None, event = None, script = None):
    if event and script:
        return cmds.scriptJob(e=[event,script], ro=False, p = parent)
        
def kill_scriptjob(job = None):
    if job:
        return cmds.scriptJob(kill = job, f = True)       

def new_scene_script(parent = None, script = None):
    return create_scriptjob(parent = parent, event = "NewSceneOpened", script = script)   

def open_scene_script(parent = None, script = None):
    return create_scriptjob(parent = parent, event = "SceneOpened", script = script)   

def new_scene_from_selection(project_path = None, mode = "include"):
    temp_file = os.path.join(project_path, "scenes", "temp_%s.ma"%(id_generator()))
    logging.info(temp_file)
    sel = cmds.ls(sl=True)
    if len(sel)>0:
        if mode == "include":
            saved_file = cmds.file(temp_file, type='mayaAscii', exportSelected=True, expressions=True, constraints=True, channels=True, constructionHistory=True, shader=True)    
        if mode == "exclude":
            saved_file = cmds.file(temp_file, type='mayaAscii', exportSelected=True, expressions=False, constraints=False, channels=False, constructionHistory=False, shader=True)
        
        if saved_file:
            open_scene(saved_file)
            return saved_file
    
    return None


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def maya_version():
    return cmds.about(version=True)
    
def set_fps(fps = None):
    fps_string = "pal"
    if fps == 25:
        fps_string = "pal"
    if fps == 24:
        fps_string = "film"
    if fps == 30:
        fps_string = "ntsc"                
    cmds.currentUnit(t=fps_string)


def clean_up_file():
    
    # import references

    refs = cmds.ls(type='reference')
    for i in refs:
        rFile = cmds.referenceQuery(i, f=True)
        cmds.file(rFile, importReference=True, mnr=True)    
        
    defaults = ['UI', 'shared']

    # Used as a sort key, this will sort namespaces by how many children they have.
    def num_children(ns):
        return ns.count(':')

    namespaces = [ns for ns in cmds.namespaceInfo(lon=True, r=True) if ns not in defaults]
    # We want to reverse the list, so that namespaces with more children are at the front of the list.
    namespaces.sort(key=num_children, reverse=True)

    for ns in namespaces:

        if namespaces.index(ns)+1 < len(namespaces):
            parent_ns = namespaces[namespaces.index(ns)+1]   
            cmds.namespace(mv=[ns,parent_ns], f=True) 
            cmds.namespace(rm=ns) 
        else:
            cmds.namespace(mv=[ns,":"], f=True)  
            cmds.namespace(rm=ns) 
	
    # remove ngSkinTools custom nodes
    from ngSkinTools.layerUtils import LayerUtils 
    LayerUtils.deleteCustomNodes()
    
    # remove RRM proxies
    if cmds.objExists("RRM_MAIN"):
        cmds.select("RRM_MAIN",hi=True)
        proxies = cmds.ls(sl=True)
        cmds.lockNode(proxies,lock=False)
        cmds.delete(proxies)
        
        if cmds.objExists("RRM_ProxiesLayer"):
            cmds.delete("RRM_ProxiesLayer")
            
def viewMassage(text = None):
            cmds.inViewMessage( amg="Pipeline: " + text, pos='topCenter', fade=True, fst = 3000 )
        