'''

PIPELINE 

1.0.0-beta

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

from PySide import QtCore, QtGui
from shiboken import wrapInstance
import maya.OpenMayaUI as omui
import maya.OpenMaya as OpenMaya
#import maya.cmds as cmds
import os
import pysideuic
import xml.etree.ElementTree as xml
from cStringIO import StringIO
#import pymel.core as pm
#import maya.mel as mel
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from maya.app.general.mayaMixin import MayaQDockWidget
from maya.OpenMayaUI import MQtUtil
#import operator
import warnings
import time
from timeit import default_timer as timer
#import collections
import logging
#import webbrowser
#import glob
import sys
#import inspect
#import functools


global start_time
global end_time
start_time = timer()

import modules.maya_warpper as maya
reload(maya)

import modules.jsonData as data
reload(data)


import data as dt
reload(dt)

import modules.files as files
reload(files)

import data_model as dtm
reload(dtm)

import data as dt
reload(dt)

import data_model as dtm
reload(dtm)

import data_view as dtv
reload(dtv)

global _node_
global _root_
global _stage_
global _asset_
global _folder_
global _dummy_
global _new_
global _catagory_

_catagory_ = "catagory"
_new_ = "new"
_node_ = "node"
_root_ = "root"
_stage_ = "stage"
_asset_ = "asset"
_folder_ = "folder"
_dummy_ = "dummy"


'''
import modules.maya_warpper as maya
reload(maya)
import modules.track as track
reload(track)
'''
import dialogue as dlg
reload(dlg)


global treeModel

log_file = os.path.join(os.path.dirname(__file__), 'pipeline_log.txt')
log = logging.getLogger(__name__)
hdlr = logging.StreamHandler(stream=sys.stdout)
hdlr = logging.FileHandler(log_file, mode = 'w')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
log.handlers[:] = [hdlr]
log.setLevel(logging.DEBUG)
log.info(os.path.realpath(__file__))
'''
             
def standard_error_report_handler():
    
    py_file_dir = os.path.dirname(__file__)                       
    log_file = os.path.join(py_file_dir, 'error_reports','ERROR REPORT - %s.txt'%(time.strftime("%Y-%m-%d %H-%M-%S")))           
    files.assure_path_exists(log_file)            
    exp_hdlr = logging.StreamHandler(stream=sys.stdout)
    exp_hdlr = logging.FileHandler(log_file, mode = 'w')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    exp_hdlr.setFormatter(formatter)            
    log.addHandler(exp_hdlr)  
    log.info('ERROR REPORT - %s.txt'%(time.strftime("%Y-%m-%d %H-%M-%S")))          
    log.info('Platform - %s'%(files.os_qeury()))
    log.info('Maya version - %s'%maya.maya_version())
    log.info('Pipeline version - %s'%version)
    py_file = os.path.realpath(__file__)           
    log.info('pipeline.py path - %s'%py_file)
    return exp_hdlr, log_file
    

def exception_report(file=None,settings_file=None):
    if file:
        string = files.read(file)
        errorDlg = dlg.ErrorReport(plainText = string)
        note = errorDlg.exec_()
        text, usertext, dont_ask = errorDlg.result()
        try:
            if dont_ask:
                UiWindow.ui.actionBug_reports.setChecked(False)                
            else:
                UiWindow.ui.actionBug_reports.setChecked(True)    
        except:
            log.info("ui is not loaded - 'don't show this again' settings is not saved")
                
        if note == QtGui.QDialog.Accepted:
            import modules.email as email
            body = usertext + '\n\n\n' + text
            email.mailto('liorbenhorin@gmail.com', subject='Pipeline error report - %s.txt'%(time.strftime("%Y-%m-%d %H-%M-%S")), body=body)

def try_execpt(fn):

    def wrapped(self,*args,**kwargs):
        try:
            return fn(self,*args,**kwargs)
            
        except StandardError:
            exc_info = sys.exc_info()
            exp_hdlr, log_file = standard_error_report_handler()

            if 'UiWindow' in globals():
                try:
                    UiWindow.log_settings()
                except:
                    log.info("unable to log the settings")
            else:
                log.info("cannot log anything - ui is not loaded")
                    
            try:
                
                self.log()
                log.info("exception at %s.%s"%(self.__class__.__name__, fn.__name__), exc_info=True)
                log.removeHandler(exp_hdlr) 
            except:
                log.info("exception at %s - faild to log more information"%(fn.__name__), exc_info=True)
                log.removeHandler(exp_hdlr) 
            
            try:
                if UiWindow.ui.actionBug_reports.isChecked():
                    exception_report(log_file)
            except:
                exception_report(log_file)

            raise StopIteration
                        
    return wrapped
    
  
def exceptions_handler(decorator):
    def decorate(cls):
        for name, fn in inspect.getmembers(cls, inspect.ismethod):
            if name is not 'log':
                setattr(cls, name, decorator(fn))
               
        return cls
    return decorate    

def handle_uncaught_exception(exc_type, exc_value, exc_traceback):
        
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
        
    # this will prevent for loop error from getting printed to screen    
    if issubclass(exc_type, StopIteration):
        log.info("quitting iteration")
        return        
    
    exp_hdlr, log_file = standard_error_report_handler()
    general_log()
    log.info("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))    
    log.removeHandler(exp_hdlr) 
    exception_report(log_file)


sys.excepthook = handle_uncaught_exception
'''

def loadUiType(uiFile):
    """
    :author: Jason Parks
    Pyside lacks the "loadUiType" command, so we have to convert the ui file to py code in-memory first
    and then execute it in a special frame to retrieve the form_class.
    """
    parsed = xml.parse(uiFile)
    widget_class = parsed.find('widget').get('class')
    form_class = parsed.find('class').text
    
    with open(uiFile, 'r') as f:
        o = StringIO()
        frame = {}
            
        pysideuic.compileUi(f, o, indent=0)
        pyc = compile(o.getvalue(), '<string>', 'exec')
        exec pyc in frame
            
        #Fetch the base_class and form class based on their type in the xml from designer
        form_class = frame['Ui_%s'%form_class]
        base_class = getattr(QtGui, widget_class)
    return form_class, base_class

 
def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtGui.QWidget)
           

'''
global variables setup
'''
main_uiFile = os.path.join(os.path.dirname(__file__), 'ui', 'pipeline_main_UI.ui')
main_form_class, main_base_class = loadUiType(main_uiFile)
 
projects_uiFile = os.path.join(os.path.dirname(__file__), 'ui', 'pipeline_projects_UI.ui')       
projects_form_class, projects_base_class = loadUiType(projects_uiFile)

create_edit_project_uiFile = os.path.join(os.path.dirname(__file__), 'ui', 'pipeline_create_edit_project_UI.ui')
create_edit_project_form_class, create_edit_project_base_class = loadUiType(create_edit_project_uiFile)

version = '1.0.10-NFR'


def set_icons():
    global localIconPath 
    
    localIconPath = os.path.join(os.path.dirname(__file__), 'icons')
    if not os.path.exists(localIconPath):
        log.info("icons folder not found: %s"%localIconPath)
        return 
    
        
    global offline_icon
    global catagory_icon
    global asset_icon
    global component_icon
    global new_icon
    global delete_icon
    global load_icon
    global unload_icon
    global project_icon
    global users_icon
    global settings_icon
    global set_icon
    global yes_icon
    global no_icon
    global search_icon
    global edit_icon
    global delete_folder_icon
    global new_folder_icon
    global open_icon
    global save_icon
    global save_master_icon
    global add_icon
    global down_arrow_icon
    global import_icon
    global export_icon
    global help_icon
    global anim_icon
    global asset_mode_icon
    global reload_icon
    global shutter_icon
    global camrea_icon
    global play_icon
    global comment_icon
    global large_icon
    global small_icon
    
    global large_image_icon
    global large_image_icon_dark
    global large_image_icon_click
    global large_image_icon_click_dark
    global wide_image_icon
    global wide_image_icon_click  
    global wide_image_icon_dark
    global wide_image_icon_click_dark

        
    offline_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"offline"))
    catagory_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"catagory"))
    asset_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"asset"))
    component_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"component"))
    new_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"new"))
    delete_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"delete"))
    load_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"load"))
    unload_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"unload"))
    project_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"project"))
    users_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"users"))
    settings_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"settings"))
    set_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"set"))
    yes_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"yes"))
    no_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"no"))
    search_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"search"))
    edit_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"edit"))
    delete_folder_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"delete_folder"))
    new_folder_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"new_folder"))     
    open_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"open"))    
    save_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"save"))  
    save_master_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"save_master"))  
    add_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"add"))
    down_arrow_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"down_arrow"))
    import_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"import"))
    export_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"export"))
    help_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"help"))
    anim_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"anim"))
    asset_mode_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"asset_mode"))
    reload_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"reload"))
    shutter_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"shutter"))
    camrea_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"camera"))
    play_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"play"))
    comment_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"comment"))
    
    large_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"large"))
    small_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"small"))
    
    
    large_image_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"large_image")) 
    large_image_icon_dark = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"large_image_dark")) 
    large_image_icon_click = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"large_image_click")) 
    large_image_icon_click_dark = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"large_image_click_dark")) 
    
    wide_image_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"wide_image")) 
    wide_image_icon_click = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"wide_image_click")) 
    wide_image_icon_dark = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"wide_image_dark")) 
    wide_image_icon_click_dark = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"wide_image_click_dark")) 


# declare all the global icons  variables  
set_icons()

def set_padding(int, padding):
    return str(int).zfill(padding)


class QLabelButton(QtGui.QLabel):
    '''
        custom QLbael the can send clicked signal
    '''
    def __init(self, parent):
        QtGui.QLabel.__init__(self, parent)

    def mouseReleaseEvent(self, ev):
        click = ev.pos()
        if self.mask().contains(click):
            self.emit(QtCore.SIGNAL('clicked()'))


class alpha_button(QtGui.QWidget):
    '''
        custom QLbael the can send clicked signal, only from the pixmap are that has 100% alpha
        used for the thumbnail transperent icon button
    '''
       
    def __init__(self, parent, alpha):
        super(alpha_button, self).__init__(parent)     
        self.pixmap = alpha

        self.button = QLabelButton(self)
        self.button.setPixmap(self.pixmap)
        self.button.setScaledContents(True)
        self.button.setMask(self.pixmap.mask())
        self.connect(self.button, QtCore.SIGNAL('clicked()'), self.onClick)

    def onClick(self):
        self.emit(QtCore.SIGNAL('clicked()'))

    def set_pixmap(self, pixmap):
        self.button.setPixmap(pixmap)
        self.button.setScaledContents(True)
        self.button.setMask(pixmap.mask())
        
        
class pipeline_data(object):
    def __init__(self,**kwargs):
        self.data_file = None
        self.data_file_path = None
        
        
        for key in kwargs:
            if key == "path":
                self.data_file_path = kwargs[key]
                
        if self.data_file_path:        
            self.set_data_file(self.data_file_path)


    def set_data_file(self,path): 
        if os.path.isfile(path):          
            self.data_file = data.jsonDict(path = path) 
            return True
        else:
            log.debug ("Invalid path to data file")




class pipeline_project(pipeline_data):
    def __init__(self,**kwargs):
        #super(pipeline_project, self,).__init__()
        pipeline_data.__init__(self, **kwargs)



        self.project_file = None
        if self.data_file:
            self.project_file = self.data_file.read()

        self.project_file_name = 'project.json'
   
        self.settings = None
        for key in kwargs:
            if key == "settings":
                self.settings = kwargs[key] 
   
        
    def create(self, 
               project_path, 
               name = "My_Project",
               padding = 3,
               file_type = "ma",
               fps = 25,
               users = {"Admin":(1234,"admin")},
               playblast_outside = False):
        
        project_settings_file = os.path.join(project_path, self.project_file_name) 
        
        project_key = data.id_generator()
        project_data = {}
        project_data["project_name"] = name
        project_data["project_key"] = project_key
        project_data["padding"] = padding
        project_data["fps"] = fps
        project_data["defult_file_type"] = file_type
        project_data["users"] = users
        project_data["playblast_outside"] = playblast_outside
                     
        folders = ["assets","images","scenes","sourceimages","data","movies","autosave","movies","scripts",
                   "sound", "clips", "renderData", "cache"]
        
        for folder in folders:
            project_data[folder] = folder
            files.create_directory(os.path.join(project_path, folder)) 
            
        #render folders:
        r_folders = ["renderData", "depth", "iprimages", "shaders"]
        for r_folder in r_folders[1:]:
            files.create_directory(os.path.join(project_path, r_folders[0], r_folder))
        
        fur_folders = ["renderData", "fur", "furFiles", "furImages", "furEqualMap", "furAttrMap", "furShadowMap" ]
        for f_folder in fur_folders[2:]:
            files.create_directory(os.path.join(project_path, fur_folders[0], fur_folders[1], f_folder))
         
        #cache folders:
        c_folders = ["cache", "particles", "nCache", "bifrost"]
        for c_folder in c_folders[1:]:
            files.create_directory(os.path.join(project_path, c_folders[0], c_folder))            

        fl_folders = ["cache", "nCache", "fluid"]
        for fl_folder in fl_folders[2:]:
            files.create_directory(os.path.join(project_path, fl_folders[0], fl_folders[1], fl_folder))              

        
        self.data_file = data.jsonDict().create(project_settings_file, project_data)  
        self.project_file = self.data_file.read()
        
        return self 



    def project_file_key(self, key = None):
        if self.project_file:
            return self.project_file[key]
        else:
            return None
        
    @property
    def project_name(self):
        if self.project_file:
            return self.project_file["project_name"]
        else:
            return None           

    @property
    def project_fps(self):
        if self.project_file:
            if "fps" in self.project_file.keys():
                return self.project_file["fps"]
            else:
                return None  
        else:
            return None  


    @project_fps.setter
    def project_fps(self,fps):
       
        if self.data_file:
            data = {}
            data["fps"] = fps
            self.data_file.edit(data)
            self.project_file = self.data_file.read()


    @property
    def project_key(self):
        if self.project_file:
            return self.project_file["project_key"]
        else:
            return None  

    @property
    def project_padding(self):
        if self.project_file:
            return self.project_file["padding"]
        else:
            return None 
            
    @property
    def project_file_type(self):
        if self.project_file:
            return self.project_file["defult_file_type"]
        else:
            return None             


    @project_file_type.setter
    def project_file_type(self,type):
       
        if self.data_file:
            data = {}
            data["defult_file_type"] = type
            self.data_file.edit(data)
            self.project_file = self.data_file.read()
    
    @property
    def movie_file_type(self):
        if self.project_file:
            return "mov"
        else:
            return None    

    @property
    def project_users(self):
        if self.project_file:
            if "users" in self.project_file.keys():
                return self.project_file["users"]
            else:
                return None    
        else:
            return None  

    @project_users.setter
    def project_users(self,users):
       
        if self.data_file:
            data = {}
            data["users"] = users
            self.data_file.edit(data)
            self.project_file = self.data_file.read()


    @property
    def playblast_outside(self):
        if self.project_file:
            if "playblast_outside" in self.project_file.keys():
                return self.project_file["playblast_outside"]
            else:
                return False    
        else:
            return None  

    @playblast_outside.setter
    def playblast_outside(self,playblast_outside):
        

        old_path = self.playblasts_path
                      
        if self.data_file:
            data = {}
            data["playblast_outside"] = playblast_outside
            self.data_file.edit(data)
            self.project_file = self.data_file.read()

            files.dir_move(old_path, self.playblasts_path)
            
        
            


    @property
    def assets_dir(self):
        if self.project_file:
            return self.project_file_key(key = "assets")
        else:
            return None  





    def catagories(self, project_path = None):
        if self.project_file:

            if os.path.exists(project_path):
                if self.assets_dir:
                    assets_catagories_path = os.path.join(project_path, self.assets_dir)
                    return files.list_dir_folders(assets_catagories_path)
        return None         

    def assets(self, project_path = None, catagory_name = None):
        if self.project_file:

            if os.path.exists(project_path):
                if self.assets_dir:
                    catagory_path = os.path.join(project_path,self.assets_dir, catagory_name)
                    if os.path.exists(catagory_path):
                        return files.list_dir_folders(catagory_path)
        return None  

    def components(self, project_path = None, catagory_name = None, asset_name = None):
        if self.project_file:

            if os.path.exists(project_path):
                if self.assets_dir:
                    asset_path = os.path.join(project_path,self.assets_dir, catagory_name, asset_name)
                    if os.path.exists(asset_path):
                        return files.list_dir_folders(asset_path)
        return None  
    
    @property
    def scenes_path(self):
        if self.settings:
            path = os.path.join(self.settings.current_project_path,"scenes")
            if os.path.exists(path):
                return path
        return None

    @property
    def playblasts_path(self):
        if self.settings:
            if self.playblast_outside:            
                path = os.path.join(os.path.dirname(self.settings.current_project_path),"%s_playblasts"%(self.project_name))
           
            else:
                path = os.path.join(self.settings.current_project_path,"playblasts")
            
            
            return path
        return None
    
    @property
    def sequences(self):
        if self.project_file:
             
            path = self.scenes_path
            if os.path.exists(path):
                folders = files.list_dir_folders(path)
                sequences = []
                for folder in folders:
                    if os.path.isfile(os.path.join(path, folder, "sequence.json")):
                        sequences.append(folder)
                return sequences
        return None  

    def shots(self, sequence_name = None):
        if self.project_file:
            if sequence_name:
                path = os.path.join(self.scenes_path, sequence_name)
                if os.path.exists(path):
                    return files.list_dir_folders(path)
        
        return None 



    def create_sequence(self, sequence_name = None):
        
        for sequence in self.sequences:
            if sequence_name == sequence:
                dlg.massage("critical", "Sorry", "This sequence exsists" )
                return False

        path = os.path.join(self.scenes_path, sequence_name)    
        if files.create_directory(path):
            files.create_dummy(path, "sequence.json")
            return True


    def delete_sequence(self, sequence_name = None):

        path = os.path.join(self.scenes_path,sequence_name)       
        if files.delete(path):
            
            path = os.path.join(self.playblasts_path,sequence_name)   
            if files.delete(path):
                
                return True
            
            return True
            
        
        return False  

    def delete_shot(self, sequence_name = None, shot_name = None):

        path = os.path.join(self.scenes_path,sequence_name, shot_name)       
        if files.delete(path):
            
            path = os.path.join(self.playblasts_path,sequence_name, shot_name)   
            if files.delete(path):
                
                return True
            
            return True
        
        return False  

    def create_shot(self, sequence_name = None, shot_name = None, create_from = None):
        for shot in self.shots(sequence_name = sequence_name):
            if shot_name == shot:
                dlg.massage("critical", "Sorry", "This Shot exsists" )
                return False

        path = os.path.join(self.scenes_path,sequence_name,shot_name)       
        if files.create_directory(path):
            shot = pipeline_shot().create(path, sequence_name, shot_name, self, self.settings, create_from)
            return shot
 

    def create_catagory(self, project_path = None, catagory_name = None):
        for catagory in self.catagories(project_path = project_path):
            if catagory_name == catagory:
                dlg.massage("critical", "Sorry", "This Catagory exsists" )
                return False

        path = os.path.join(project_path,self.assets_dir,catagory_name)       
        if files.create_directory(path):
            return True
        
    def delete_catagory(self, project_path = None, catagory_name = None):

        path = os.path.join(project_path,self.assets_dir,catagory_name)       
        if files.delete(path):
            return True
        
        return False    

    def create_asset(self, project_path = None, catagory_name = None, asset_name = None):
        for asset in self.assets(project_path = project_path, catagory_name = catagory_name):
            if asset_name == asset:
                dlg.massage("critical", "Sorry", "This Asset exsists" )
                return False

        path = os.path.join(project_path,self.assets_dir,catagory_name,asset_name)       
        if files.create_directory(path):
            return True
            
    def delete_asset(self, project_path = None, catagory_name = None, asset_name = None):

        path = os.path.join(project_path,self.assets_dir,catagory_name,asset_name)       
        if files.delete(path):
            return True
        
        return False  

    def create_component(self, project_path = None, catagory_name = None, asset_name = None, component_name = None, create_from = None):
        for component in self.components(project_path = project_path, catagory_name = catagory_name, asset_name = asset_name):
            if component_name == component:
                dlg.massage("critical", "Sorry", "This Component exsists" )
                return False

        path = os.path.join(project_path,self.assets_dir,catagory_name,asset_name, component_name)       
        if files.create_directory(path):
            component = pipeline_component().create(path, catagory_name, asset_name, component_name, self, self.settings, create_from)
            return component

    def delete_component(self, project_path = None, catagory_name = None, asset_name = None, component_name = None):

        path = os.path.join(project_path,self.assets_dir,catagory_name,asset_name, component_name)       
        if files.delete(path):
            return True
        
        return False  


    def rename_sequence(self, project_path = None,sequence_name = None, new_name=True):
                
        for shot in self.shots( sequence_name ):
            
            path = os.path.join(project_path,self.scenes_path,sequence_name,shot,  ("%s.%s"%(shot,"pipe")))
            if os.path.isfile(path):
                shot_object = pipeline_shot(path = path, project = self, settings = self.settings) 
                shot_object.rename_sequence(new_name)
        
        path = os.path.join(project_path,self.scenes_path,sequence_name)       
        path = files.file_rename(path,new_name) 
        
        return True  

    def rename_catagory(self, project_path = None, catagory_name = None, new_name=True):
        
        for asset in self.assets(project_path = project_path, catagory_name = catagory_name):
        
            for component in self.components(project_path, catagory_name, asset):
                
                path = os.path.join(project_path,self.assets_dir,catagory_name,asset, component, ("%s.%s"%(component,"pipe")))
                if os.path.isfile(path):
                    component_object = pipeline_component(path = path, project = self, settings = self.settings) 
                    component_object.catagory_name = new_name
        
        path = os.path.join(project_path,self.assets_dir,catagory_name)       
        path = files.file_rename(path,new_name) 
        
        return True  

    def rename_asset(self, project_path = None, catagory_name = None, asset_name = None, new_name=True):
                
        for component in self.components(project_path, catagory_name, asset_name):
            path = os.path.join(project_path,self.assets_dir,catagory_name,asset_name, component, ("%s.%s"%(component,"pipe")))
            if os.path.isfile(path):
                component_object = pipeline_component(path = path, project = self, settings = self.settings) 
                component_object.rename_asset(new_name)

        
        path = os.path.join(project_path,self.assets_dir,catagory_name,asset_name)       
        path = files.file_rename(path,new_name)   
        
        return True
    


    @property
    def masters(self):
        if self.project_file:
            masters = {}            
            project_path = self.settings.current_project_path
            
            for catagory in self.catagories(project_path=project_path):                
                for asset in self.assets(project_path=project_path, catagory_name = catagory):                    
                    for component in self.components(project_path = project_path, catagory_name = catagory, asset_name = asset):                    
                        component_object = pipeline_component                        
                        component_file_path = os.path.join(project_path,
                            self.assets_dir,
                            catagory,
                            asset,
                            component,
                            "%s.%s"%(component,"pipe")
                            )
            
                        component_object = pipeline_component(path = component_file_path, project = self, settings = self.settings)
                        if component_object.component_public_state:
                            master_padded_version = set_padding(0, self.project_padding)
                            master_file = component_object.master
                            if master_file:
                                masters["%s_%s"%(asset,component)] = [master_file, 
                                                     component_object.thumbnail, 
                                                     component_object.author("masters",master_padded_version), 
                                                     component_object.date_created("masters",master_padded_version),
                                                     ]
                            
                        del component_object
                           
            return masters        
        else:            
            return None

    @property
    def stages(self):
        stages = {}
        stages["asset"] = ["model","rig","clip","shading","lightning"]
        stages["animation"] = ["layout","Shot"]   
        return stages
    
    @property
    def levels(self):
        levels = {}
        levels["asset"] = ["type","asset","stage","ccc"]
        levels["animation"] = ["Ep","Seq"]
        return levels
                


    def log(self):
        
        log.info("logging project '%s'"%(self.project_name))       
        
        project_path = self.settings.current_project_path
        
        log.info("project local path %s"%project_path)
                
        [ log.info("  %s"%files.reletive_path(project_path,f)) for f in files.list_all(self.settings.current_project_path) if isinstance(files.list_all(self.settings.current_project_path),list) ]
                               
        log.info("project data file: %s"%self.data_file_path)
        
        log.info(self.data_file.print_nice())

        log.info("end logging project ")    
                            

                            

class pipeline_settings(pipeline_data):
    def __init__(self,**kwargs):
        pipeline_data.__init__(self, **kwargs)
 
        self.settings_file = None
        if self.data_file:
            self.settings_file = self.data_file.read()
        
       
    def create(self, path):
        
        projects = {}
                               
        settings_data = {}
        settings_data["user"] = [None,None]
        settings_data["project_premissions"] = None
        settings_data["current_project"] = None
        settings_data["projects"] = projects
        settings_data["current_open_file"] = None
        
        selection = {}
        selection["catagory"] = None
        selection["asset"] = None
        selection["component"] = None
        selection["sequence"] = None
        selection["shot"] = None
        
        settings_data["selection"] = selection
                     
        
        self.data_file = data.jsonDict().create(path, settings_data)  
        self.settings_file = self.data_file.read()
        
        return self 
    
    @property  
    def projects(self):
        
        if self.settings_file:
            return self.settings_file["projects"]
    
    @projects.setter
    def projects(self,projects):
       
        if self.data_file:
            data = {}
            data["projects"] = projects
            self.data_file.edit(data)
            self.settings_file = self.data_file.read()
    
    def project_path(self, project_key = None):
        
        if self.settings_file:
            return self.projects[project_key][0]
            

    @property
    def current_project(self):
        
        if self.settings_file:
            current_project_key = self.settings_file["current_project"]
            if current_project_key:
                return current_project_key
            else:
                return None
        else:
            return None  

    @current_project.setter
    def current_project(self,project_key):
 
        if self.data_file:
            data = {}
            data["current_project"] = project_key
            self.data_file.edit(data)
            self.settings_file = self.data_file.read()

    
    @property
    def current_project_path(self):

        if self.settings_file:
            projects_dict = self.settings_file["projects"]
            if self.current_project in projects_dict:
                return projects_dict[self.current_project][0]
            else:
                warnings.warn("No active project")
                return None

    @property
    def current_project_status(self):

        if self.settings_file:
            projects_dict = self.settings_file["projects"]
            if self.current_project:
                return projects_dict[self.current_project][1]
            else:
                warnings.warn("No active project")
                return None
                
    @property
    def current_project_name(self):

        if self.settings_file:
            projects_dict = self.settings_file["projects"]
            if self.current_project:
                return projects_dict[self.current_project][2]
            else:
                warnings.warn("No active project")
                return None
    @property
    def current_open_file(self):

        if self.settings_file:
            return self.settings_file["current_open_file"]
 
    @current_open_file.setter
    def current_open_file(self,file):

        if self.data_file:
            data = {}
            data["current_open_file"] = file
            self.data_file.edit(data)
            self.settings_file = self.data_file.read()

    @property
    def selection(self):

        if self.settings_file:
            return self.settings_file["selection"]
 
    @selection.setter
    def selection(self,selection):

        if self.data_file:
            data = {}
            data["selection"] = selection
            self.data_file.edit(data)
            self.settings_file = self.data_file.read()

    @property
    def catagory_selection(self):
        data = self.selection
        return data["catagory"]

    @catagory_selection.setter
    def catagory_selection(self,selection):
        data = self.selection
        data["catagory"] = selection
        self.selection = data

    @property
    def asset_selection(self):
        data = self.selection
        return data["asset"]

    @asset_selection.setter
    def asset_selection(self,selection):
        data = self.selection
        data["asset"] = selection
        self.selection = data

    @property
    def component_selection(self):
        data = self.selection
        return data["component"]

    @component_selection.setter
    def component_selection(self,selection):
        data = self.selection
        data["component"] = selection
        self.selection = data

    @property
    def sequence_selection(self):
        data = self.selection
        return data["sequence"]

    @sequence_selection.setter
    def sequence_selection(self,selection):
        data = self.selection
        data["sequence"] = selection
        self.selection = data
        

    @property
    def shot_selection(self):
        data = self.selection
        return data["shot"]

    @shot_selection.setter
    def shot_selection(self,selection):
        data = self.selection
        data["shot"] = selection
        self.selection = data

    @property  
    def user(self):
        
        if self.settings_file:
            return self.settings_file["user"]

    @user.setter
    def user(self,user):

        if self.data_file:
            data = {}
            data["user"] = user
            self.data_file.edit(data)
            self.settings_file = self.data_file.read()

    @property  
    def role(self):
                
        if self.settings_file:
            role = self.settings_file["project_premissions"]
            if role == "admin":
                return 0
            if role == "rigger":
                return 1
            if role == "animator":
                return 2
            if role == "guest":
                return 3           
            
    @role.setter
    def role(self,premissions):

        if self.data_file:
            data = {}
            data["project_premissions"] = premissions
            self.data_file.edit(data)
            self.settings_file = self.data_file.read()
    
    @property 
    def role_name(self):        
        if self.settings_file:
            return self.settings_file["project_premissions"]

    @property
    def playblast_format(self):
        if self.settings_file:
            try:
                return self.settings_file["playblast_format"]
            except:
                return "movie"

    @playblast_format.setter
    def playblast_format(self,format):
        if self.data_file:
            data = {}
            data["playblast_format"] = format
            self.data_file.edit(data)
            self.settings_file = self.data_file.read()
        

    @property
    def playblast_compression(self):
        if self.settings_file:
            try:
                return self.settings_file["playblast_compression"]
            except:
                return "H.264"

    @playblast_compression.setter
    def playblast_compression(self,type):
        if self.data_file:
            data = {}
            data["playblast_compression"] = type
            self.data_file.edit(data)
            self.settings_file = self.data_file.read()        


    @property
    def playblast_hud(self):
        if self.settings_file:
            try:
                return self.settings_file["playblast_hud"]
            except:
                return True

    @playblast_hud.setter
    def playblast_hud(self,type):
        if self.data_file:
            data = {}
            data["playblast_hud"] = type
            self.data_file.edit(data)
            self.settings_file = self.data_file.read()

    @property
    def playblast_offscreen(self):
        if self.settings_file:
            try:
                return self.settings_file["playblast_offscreen"]
            except:
                return False

    @playblast_offscreen.setter
    def playblast_offscreen(self,type):
        if self.data_file:
            data = {}
            data["playblast_offscreen"] = type
            self.data_file.edit(data)
            self.settings_file = self.data_file.read()


    @property
    def playblast_scale(self):
        if self.settings_file:
            try:
                return self.settings_file["playblast_scale"]
            except:
                return 50

    @playblast_scale.setter
    def playblast_scale(self,int):
        if self.data_file:
            data = {}
            data["playblast_scale"] = int
            self.data_file.edit(data)
            self.settings_file = self.data_file.read()


    @property
    def bug_reports(self):
        if self.settings_file:
            try:
                return self.settings_file["bug_reports"]
            except:
                return True
        else:
            return True

    @bug_reports.setter
    def bug_reports(self,bool):
        if self.data_file:
            data = {}
            data["bug_reports"] = bool
            self.data_file.edit(data)
            self.settings_file = self.data_file.read()


    @property
    def stage(self):
        if self.settings_file:
            try:
                return self.settings_file["stage"]
            except:
                return True
        else:
            return True

    @stage.setter
    def stage(self,value):
        if self.data_file:
            data = {}
            data["stage"] = value
            self.data_file.edit(data)
            self.settings_file = self.data_file.read()


    @property
    def rootDir(self):
        if self.settings_file:
            try:
                return self.settings_file["rootDir"]
            except:
                return None
        else:
            return None

    @rootDir.setter
    def rootDir(self, value):
        if self.data_file:
            data = {}
            data["rootDir"] = value
            self.data_file.edit(data)
            self.settings_file = self.data_file.read()


    @property
    def client(self):
        if self.settings_file:
            try:
                return self.settings_file["client"]
            except:
                return None
        else:
            return None


    @client.setter
    def client(self, value):
        if self.data_file:
            data = {}
            data["client"] = value
            self.data_file.edit(data)
            self.settings_file = self.data_file.read()

    def log(self):
        log.info("logging settings")
        log.info("settings data file: %s"%self.data_file_path)        
        log.info(self.data_file.print_nice())        
        log.info("end logging settings")


class pipeLineUI(MayaQWidgetDockableMixin, QtGui.QMainWindow):
    def __init__(self, parent=None):
        
        self.deleteInstances()
        
        super(pipeLineUI, self).__init__(parent)      
        self.setWindowFlags(QtCore.Qt.Tool)                
        form_class, base_class = main_form_class, main_base_class
        
        self.ui = form_class()
        self.ui.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        
        global version
        self.setWindowTitle("Pipeline - %s"%(version))

              
        
        
        self.set_icons()
        '''
        self.ui.assets_splitter.setSizes([150,600])
        self.ui.scenes_splitter.setSizes([150,600])

        #connect ui
        self.ui.actionAbout.triggered.connect(self.about)
        self.ui.actionBug_reports.toggled.connect(self.send_bug_reports)
        self.ui.actionDocumentation.triggered.connect(self.documentation)
        
        self.ui.actionFiles_repath.triggered.connect(self.repath)
        self.ui.actionCollect_component.triggered.connect(self.collect_component)
        self.disable(self.ui.actionCollect_component)
        
        '''
        self.ui.users_pushButton.clicked.connect(self.login_window)
        self.ui.projects_pushButton.clicked.connect(self.projects_window)
        #self.ui.asset_component_files_tabWidget.currentChanged.connect(self.update_component_files_tab)
        self.ui.stage_note_label.mousePressEvent = self.version_note
        #self.ui.shot_notes_label.mousePressEvent = self.shot_note   
        self.ui.save_version_pushButton.clicked.connect(self.version_save)
        self.ui.save_master_pushButton.clicked.connect(self.master_save)
        self.ui.import_version_pushButton.clicked.connect(self.version_import)                
        #self.ui.import_shot_version_pushButton.clicked.connect(self.shot_import)  
        #self.ui.save_shot_version_pushButton.clicked.connect(self.shot_version_save)
        #self.ui.playblast_shot_pushButton.clicked.connect(self.shot_record_playblast)
        #self.ui.asset_scenes_switch_pushButton.clicked.connect(self.asset_scenes_switch)
        self.ui.publicMaster_checkBox.clicked.connect(self.public_master_toggle)
        
        self.playblast_menu = QtGui.QMenu(parent = self.ui.playblast_shot_pushButton)
        self.playblast_shot = QtGui.QAction("Record Playblast",self)
        self.playblast_shot.triggered.connect(self.shot_record_playblast)
        self.playblast_menu.addAction(self.playblast_shot)  
        self.playblast_menu.addSeparator() 
        self.playblast_shot_options = QtGui.QAction("Playblast options",self)
        self.playblast_shot_options.triggered.connect(self.shot_record_playblast_options)
        self.playblast_menu.addAction(self.playblast_shot_options)   
        self.ui.playblast_shot_pushButton.setMenu(self.playblast_menu)     
        #self.ui.playblast_shot_pushButton.addAction(self.ui.playblast_shot_options)
        #self.ui.playblast_shot_options.triggered.connect(self.shot_record_playblast_options)
        '''
        #create menus
        self.catagories_menu = QtGui.QMenu(parent = self.ui.catagory_pushButton)
        self.catagories_menu.addAction(new_folder_icon,'New',self.create_catagory)       
        self.catagories_menu.addSeparator()   
        self.rename_category_action = QtGui.QAction("Rename",self)
        self.rename_category_action.triggered.connect(self.category_rename)
        self.catagories_menu.addAction(self.rename_category_action)
        self.catagories_menu.addSeparator()                  
        self.delete_catagory_action = QtGui.QAction("Delete",self)
        self.delete_catagory_action.triggered.connect(self.delete_catagory)
        self.delete_catagory_action.setIcon(QtGui.QIcon(delete_folder_icon)) 
        self.catagories_menu.addAction(self.delete_catagory_action)
        self.ui.catagory_pushButton.setMenu(self.catagories_menu)

        self.assets_menu = QtGui.QMenu(parent = self.ui.asset_pushButton)
        self.assets_menu.addAction(new_folder_icon,'New',self.create_asset)
        self.assets_menu.addSeparator()   
        self.rename_asset_action = QtGui.QAction("Rename",self)
        self.rename_asset_action.triggered.connect(self.asset_rename)
        self.assets_menu.addAction(self.rename_asset_action)
        self.assets_menu.addSeparator()  
        self.delete_asset_action = QtGui.QAction("Delete",self)
        self.delete_asset_action.triggered.connect(self.delete_asset)
        self.delete_asset_action.setIcon(QtGui.QIcon(delete_folder_icon)) 
        self.assets_menu.addAction(self.delete_asset_action)
        self.ui.asset_pushButton.setMenu(self.assets_menu)

        self.component_menu = QtGui.QMenu(parent = self.ui.component_pushButton)
        self.component_menu.addAction(new_folder_icon,'New',self.create_component)
        self.component_menu.addAction(new_folder_icon,'New from current scene',self.create_component_from_current_scene)
        self.component_menu.addAction(new_folder_icon,'New from current selection',self.create_component_from_current_selection)
        self.component_menu.addAction(new_folder_icon,'New from file',self.create_component_from_file)
        self.component_menu.addSeparator()   
        self.rename_component_action = QtGui.QAction("Rename",self)
        self.rename_component_action.triggered.connect(self.component_rename)
        self.component_menu.addAction(self.rename_component_action)
        self.component_menu.addSeparator()  
        self.delete_component_action = QtGui.QAction("Delete",self)
        self.delete_component_action.triggered.connect(self.delete_component)
        self.delete_component_action.setIcon(QtGui.QIcon(delete_folder_icon)) 
        self.component_menu.addAction(self.delete_component_action)
        self.ui.component_pushButton.setMenu(self.component_menu)
        
        self.sequence_menu = QtGui.QMenu(parent = self.ui.sequence_pushButton)
        self.sequence_menu.addAction(new_folder_icon,'New',self.create_sequence )
        
        self.sequence_menu.addSeparator()   
        self.rename_sequence_action = QtGui.QAction("Rename",self)
        self.rename_sequence_action.triggered.connect(self.sequence_rename)
        self.sequence_menu.addAction(self.rename_sequence_action)
        self.sequence_menu.addSeparator()  
        
        
        self.delete_sequence_action = QtGui.QAction("Delete",self)
        self.delete_sequence_action.triggered.connect(self.delete_sequence)
        self.delete_sequence_action.setIcon(QtGui.QIcon(delete_folder_icon)) 
        self.sequence_menu.addAction(self.delete_sequence_action)
        self.ui.sequence_pushButton.setMenu(self.sequence_menu)

        self.shot_menu = QtGui.QMenu(parent = self.ui.shot_pushButton)
        self.shot_menu.addAction(new_folder_icon,'New',self.create_shot)       
        self.shot_menu.addAction(new_folder_icon,'New from current scene',self.create_shot_from_current_scene)
        self.shot_menu.addAction(new_folder_icon,'New from file',self.create_shot_from_file)
        self.shot_menu.addSeparator()  
  
        self.rename_shot_action = QtGui.QAction("Rename",self)
        self.rename_shot_action.triggered.connect(self.shot_rename)
        self.shot_menu.addAction(self.rename_shot_action)
        self.shot_menu.addSeparator()  
        
                 
        self.delete_shot_action = QtGui.QAction("Delete",self)
        self.delete_shot_action.triggered.connect(self.delete_shot)
        self.delete_shot_action.setIcon(QtGui.QIcon(delete_folder_icon)) 
        self.shot_menu.addAction(self.delete_shot_action)
        self.ui.shot_pushButton.setMenu(self.shot_menu)
        '''
        #customize widgets
        '''
        self.thumbnail_button()
        
        boldFont=QtGui.QFont()
        boldFont.setBold(True)         
        self.ui.component_name_label.setFont(boldFont)
        
        self.disable(self.ui.component_frame)
        self.disable(self.ui.shot_frame)
        self.ui.component_info_label.setText("No selection")
        self.ui.component_note_label.setText("No selection")
        self.ui.shot_info_label.setText("No selection")
        self.ui.shot_notes_label.setText("No selection")
        self.ui.component_name_label.setText("No Selection")
        self.ui.shot_name_label.setText("No Selection")
        
        self.disable(self.ui.component_pushButton)
        self.disable(self.ui.asset_pushButton)
        self.disable(self.ui.shot_pushButton)
        self.disable(self.delete_catagory_action)
        self.disable(self.delete_asset_action)
        self.disable(self.delete_component_action)
        self.disable(self.delete_sequence_action)
        self.disable(self.delete_shot_action)
        self.disable(self.rename_category_action)
        self.disable(self.rename_asset_action)
        self.disable(self.rename_component_action)
        
        #hide the shots panel so the assets panel will show up on init
        self.ui.scenes_main_widget.setHidden(True)
        
        #setup all the tabels    
        self.init_categoryTable()
        self.init_assetsTable()
        self.init_componentsTable()
        self.init_component_mastersTable()
        self.init_component_versionsTable()        
        self.init_sequencesTable()
        self.init_shotsTable()
        self.init_publishedAssetsTable()
        self.init_shots_versionsTable()
        self.init_shots_playblastsTable()
        
        '''
    
        '''
        
        >>> startup:
            finds the settings file or create one
            
            if there is no user logged in then make sure no project is loaded            
        
        
        '''
        self.init_settings()  
        self._decode_users()
        
        if self.settings.user[0] is not None:
            self.ui.users_pushButton.setText(self.settings.user[0])
        else:
            self.ui.users_pushButton.setText("Not logged In") 
            #self.unload_project()
            #maya.viewMassage("No user is logged in")
  
        
        if self.verify_projects(): # make sure projects are where the settings file say they are, if not marks them 'offline'       
            self.set_project() # if the user logged in matchs with the settings active project, create a project object
        
        
        
        '''
        project object:
            containg all data relevent to the project:
                users, assets, shots, etc
        '''
        self.init_current_project()   #init the ui tabels with the project's data    
    
        '''
        
        if a there is a file open when the script is starting, 
        try to find if the file is part of the project, 
        if so, navigate the ui to the component/shot
        
        >>> this is very important for workflow! if a user is working on a file, and closes the script,
            then later returns to the script to save version, the button will work as expected and save the version to 
            the correct component
        '''     
        
        '''
        self.init_assets_selection()  
        self.setObjectName("pipeline_beta")
        self.open_scene_script = None
        self.toggle_scene_open_script()  
              
        end_time = timer()    
        log.info( "loaded in: %s"%(round((end_time - start_time),2)) )                 
        track.event(name = "PipelineUI_init", maya_version = maya.maya_version(), pipeline_version = version, startup_time = round((end_time - start_time),2))
        '''

        self._versionsView = None
        self._stage = None
        
        self.tree()
    
    def tree(self):

        
        self.ui.searchIcon_label.setPixmap(search_icon)
        
        '''
        import modules
        '''
            
    
    
        '''
        MODELS
        '''
        
        '''
        generate some tree nodes for testing
        '''
        
        _root = dt.RootNode("root", path = self.settings.current_project_path)
        assets = dt.FolderNode("assets", path = os.path.join(self.settings.current_project_path, 'assets'), parent = _root)
        assets.model_tree()
        scenes = dt.FolderNode("scenes", path = os.path.join(self.settings.current_project_path, 'scenes'), parent = _root)
        scenes.model_tree()
        #root = dt.FolderNode("Diving",_root)
        #char = dt.FolderNode("Charachters", root)
        #dog = dt.AssetNode("Dog", char)
        #Animation = dt.FolderNode("Animation", root)
        #rig = dt.StageNode("Rig", parent = dog)
        #model = dt.StageNode("Model", parent = dog)
        #sorted = dt.StageNode("Sorted_component", parent = dog)
        
        '''
        creating the tree model,
        it's the main tree model object, its global so it is deleted every restart of Pipeline
        '''
        
        treeModel = dtm.PipelineProjectModel(_root) 
        
        
        '''
        _proxymodel is the sortFilterProxyModel object that is connected to the tree model
        
        '''
        
        self._proxyModel = dtm.PipelineProjectProxyModel()      
        self._proxyModel.setSourceModel(treeModel)
        self._proxyModel.setDynamicSortFilter(True)
        self._proxyModel.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self._proxyModel.setSortRole(0)
        self._proxyModel.setFilterRole(0)
        self._proxyModel.setFilterKeyColumn(0)
        
        '''
        VIEWS
        
        '''
        
        #self.list = dtv.PipelineContentsView()        
        self.tree = dtv.pipelineTreeView(self) 
        self.tree.setModel( self._proxyModel )
         
        
        #connect the tree to the table views and vice versa     
        #self.tree.tableView = self.list 
        #self.list.treeView = self.tree      
        
        self.tree.setModel( self._proxyModel )
        #self.list.init_treeView()        
        self._proxyModel.treeView = self.tree

        #connect the tree and the table signals
        #QtCore.QObject.connect(self.list, QtCore.SIGNAL("clicked(QModelIndex)"), self.list.click)
        QtCore.QObject.connect(self.ui.assetsFilter_lineEdit, QtCore.SIGNAL("textChanged(QString)"), self._proxyModel.setFilterRegExp)
        QtCore.QObject.connect(self.tree, QtCore.SIGNAL("expanded(QModelIndex)"), self.tree.saveState)
        QtCore.QObject.connect(self.tree, QtCore.SIGNAL("collapsed(QModelIndex)"), self.tree.saveState)        
        #QtCore.QObject.connect(self.ui.assetsFilter_lineEdit, QtCore.SIGNAL("textChanged()"), self.list.click)

        self.selModel = self.tree.selectionModel()
        self.tree.clicked.connect( self.tree.saveSelection ) 
        #self.selModel.selectionChanged.connect( self.list.update )        
        
        # select the tree root
        self.tree.selectRoot()
        #verticalLayout_18
        '''
        UI LAYOUTS, SPLITTER, AND ICONS SCALE SLIDER
        '''
        self.navWidget = QtGui.QWidget()        
        h_layout = QtGui.QVBoxLayout()   
        h_layout.setContentsMargins(0, 0, 0, 0)      
        self.navWidget.setLayout(h_layout) 
        h_layout.addWidget(self.tree)
        '''       
        self.splitter1 = QtGui.QSplitter()
        self.splitter1.setOrientation(QtCore.Qt.Horizontal)         
        self.splitter1.setHandleWidth(10)
        self.splitter1.setChildrenCollapsible(True)
        self.splitter1.addWidget(self.tree)
        self.splitter1.addWidget(self.list)        
        '''
        
        #self.stagesView = dtv.PipelineStagesView()#QtGui.QListView()
        #self.navWidget.
        #h_layout.addWidget(self.stagesView)
        #self.ui.project_widget.setHeight(200)
        
        #self.ui.stages_version_splitter.setSizes([150,600])
        #self.ui.stages_version_splitter.setSizes([150,600])
        '''
        large_lable = QtGui.QLabel()
        large_lable.setMaximumSize(QtCore.QSize(16, 16)) 
        large_lable.setPixmap(large_icon)
        small_lable = QtGui.QLabel()
        small_lable.setMaximumSize(QtCore.QSize(16, 16)) 
        small_lable.setPixmap(small_icon)
            
        slideWidget = QtGui.QWidget() 
        slideWidget.setMaximumHeight(20)
        slideLayout = QtGui.QHBoxLayout()
        slideLayout.setContentsMargins(0, 0, 0, 0)        
        slideWidget.setLayout(slideLayout)
        slideLayout.setAlignment(QtCore.Qt.AlignRight)
                
        self.listSlider = QtGui.QSlider()
        self.listSlider.setOrientation(QtCore.Qt.Horizontal)
        self.listSlider.setMaximumWidth(80)
        self.listSlider.setMinimumWidth(80)
        self.listSlider.setMaximumHeight(10)
        self.listSlider.setMinimum(32)
        self.listSlider.setMaximum(96)
        self.listSlider.setValue(32)
        #self.listSlider.valueChanged.connect(self.list.icons_size) 

        slideLayout.addWidget(small_lable)
        slideLayout.addWidget(self.listSlider)
        slideLayout.addWidget(large_lable)
        h_layout.addWidget(slideWidget)'''

        # add to the designer ui
        self.ui.verticalLayout_18.addWidget(self.navWidget)
        # ----> temp!!! hide the old selection options
        #self.ui.assets_selection_frame.setHidden(True)

        self.versionsView = dtv.PipelineVersionsView(parentWidget = self.ui.versionsTab,  parent = self)
        #self.list.versionsView = self.versionsTable

        self.ui.versionsTabLayout.addWidget(self.versionsView)
        self.versionsView.addSlider()

        self._dataMapper = QtGui.QDataWidgetMapper()
        # self._dataMapper.setModel(treeModel)
        # self._dataMapper.addMapping(self.mapLabel, 0, QtCore.QByteArray("text"))
        # self._dataMapper.setRootIndex(QtCore.QModelIndex())
        # self._dataMapper.toFirst()
   
        if self.settings.current_project_path:
            levels = [None]
            self._stageNode = None
            self.ui.navBarLayout.setAlignment(QtCore.Qt.AlignLeft)



            #def setModel(self, proxyModel):
            #self._proxyModel = proxyModel


            #self._dataMapper.addMapping(self.uiX, 2)

            
            

            self.stageCombo = dtv.ComboStaticWidget(
                                          settings = self.settings,
                                          items = self.project.stages["asset"] + self.project.stages["animation"],
                                          parent_layout = self.ui.navBarLayout,
                                          parent = self)

            self.stageSelect()
            self.stageCombo.comboBox.currentIndexChanged.connect(self.stageChanged)
            

            #dir = os.path.join(self.settings.current_project_path, self.stageType()) 
            '''
            self.dynamicCombo = dtv.ComboDynamicWidget(
                                                     settings = self.settings,                       
                                                     project = self.project,
                                                     path = dir,
                                                     stage = "model",
                                                     box_list = [],
                                                     parent_box = None,
                                                     parent_layout = self.ui.navBarLayout,
                                                     parent = self)  
            

            '''
            self.updateVersionsTable()
            #self.stageSelect()
            
    def stageSelect(self):

        index = self.stageCombo.comboBox.findText(self.settings.stage)
        if index != -1:
            self.stageCombo.comboBox.setCurrentIndex(index)

        dir = os.path.join(self.settings.current_project_path, "assets")

        self._stage = self.settings.stage
        self.dynamicCombo = dtv.ComboDynamicWidget(
                                                 settings = self.settings,
                                                 project = self.project,
                                                 path = dir,
                                                 stage = self.settings.stage,
                                                 box_list = [],
                                                 parent_box = None,
                                                 parent_layout = self.ui.navBarLayout,
                                                 parent = self)


        
            
    def stageType(self):

        if self.stageCombo.comboBox.currentText() in self.project.stages["asset"]:
            return "asset"
        
        if self.stageCombo.comboBox.currentText() in self.project.stages["animation"]:
            return "animation" 
        
        return None

    def stageTypeName(self ):

        if self.stageType() == "asset":
            return "assets"
        if self.stageType() == "animation":
            return "scenes"
                    
        return None
   
    def stageChanged(self):
        self.settings.stage = self.stageCombo.comboBox.currentText()
        type = self.stageType()

        #self._stage = self.stageCombo.comboBox.currentText()
        current = self.dynamicCombo._box_list[0]._stage

        if type:
            if current not in self.project.stages[type]:
                self.dynamicCombo.kill()
                self.stageSelect()
                return

            return

        self.dynamicCombo.kill()
        self.stageSelect()



        
    @property
    def versionsView(self):
        return self._versionsView
    
    @versionsView.setter
    def versionsView(self, view):
        self._versionsView = view        


    def stageNode(self, node):

        if node:
            self._stageNode = node
        else:
            self._stageNode = None

    def setVersionSelection(self, index, oldIndex):
        self._dataMapper.setCurrentModelIndex(index)

    def updateVersionsTable(self):

        if self.versionsView and self._stageNode:
            Model = self._stageNode.versiosnModel
            self.versionsView.setModel_(Model)


            self._dataMapper.setModel(Model)
            self._dataMapper.addMapping(self.ui.stage_path_label, 3, QtCore.QByteArray("text"))
            self._dataMapper.addMapping(self.ui.stage_author_label, 0, QtCore.QByteArray("text"))
            self._dataMapper.addMapping(self.ui.stage_note_label, 4, QtCore.QByteArray("text"))
            self._dataMapper.toFirst()
            QtCore.QObject.connect(self.versionsView.selectionModel(), QtCore.SIGNAL("currentRowChanged(QModelIndex, QModelIndex)"), self.setVersionSelection)# self._dataMapper,  QtCore.SLOT("setCurrentModelIndex(QModelIndex)"))


            self.ui.stage_widget.setEnabled(True)
            return True


        self.versionsView.setModel_(None)
        self._dataMapper.setModel(None)
        self.ui.stage_path_label.setText("Stage path")
        self.ui.stage_author_label.setText("Stage author")
        self.ui.stage_note_label.setText("Stage note")
        self.ui.stage_widget.setEnabled(False)
        return False

        
    def selectInScene(self):
        pass
        
    def set_icons(self):
        
        for button in [
                       self.ui.projects_pushButton,
                       self.ui.users_pushButton,
                       self.ui.save_version_pushButton,
                       self.ui.save_master_pushButton,
                       self.ui.import_version_pushButton,
                       self.ui.playblast_shot_pushButton
                       ]:
            
            button.setIconSize(QtCore.QSize(20,20)) 
        
     
        self.ui.projects_pushButton.setIcon(QtGui.QIcon(project_icon))
        self.ui.users_pushButton.setIcon(QtGui.QIcon(users_icon))

        self.ui.save_version_pushButton.setIcon(QtGui.QIcon(save_icon))
        self.ui.save_master_pushButton.setIcon(QtGui.QIcon(save_master_icon))
        self.ui.import_version_pushButton.setIcon(QtGui.QIcon(import_icon))       

        self.ui.playblast_shot_pushButton.setIcon(QtGui.QIcon(camrea_icon))
                
        self.ui.comp_icon_label.setPixmap(new_icon.scaled(16,16))
        self.ui.comp_user_label.setPixmap(users_icon.scaled(16,16))
        self.ui.comp_note_label.setPixmap(edit_icon.scaled(16,16))        
    


        

    def init_settings(self):
  
        
        self.settings_file_name = 'settings.json'
                      
        file = os.path.join(os.path.dirname(__file__), self.settings_file_name)

        
        if os.path.isfile(file): 
                   
            self.settings = pipeline_settings(path = file)                                         
            return

        self.settings = pipeline_settings().create(path = file)
    

    def verify_projects(self):
        self.project = None
        projects = self.settings.projects
        
        if projects:            
            for p in projects:                                    
                project_file_path = os.path.join(self.settings.project_path(project_key = p),"project.json")  
                                
                if os.path.isfile(project_file_path):                    
                    project = pipeline_project(path = project_file_path)                    
                    project_key = project.project_key
                    
                    if p == project_key:
                        projects[p][1] = "ONLINE"
                    else:
                        projects[p][1] = "OFFLINE"                        
                    
                    del project
                
                else:
                    projects[p][1] = "OFFLINE"
                    
            self.settings.projects = projects
                        
            if self.settings.current_project_status == "OFFLINE":
                self.update_current_open_project(None)
                return False
                
        return True

    def set_project(self,**kwargs):  
        from_pm = False
        if "from_projects_manager" in kwargs:
            from_pm = kwargs["from_projects_manager"]
            
            
        if self.settings.current_project:            
            self.project = pipeline_project(path = os.path.join(self.settings.current_project_path,"project.json"), settings = self.settings)
            

                                       
            self.settings.role = None
            username = self.settings.user[0]
            password = self.settings.user[1]
            
            if self.project.project_users != None:
                if username in self.project.project_users:
                    if self.project.project_users[username][0] == password:
                        self.settings.role = self.project.project_users[username][1]
                        self.ui.users_pushButton.setText("%s : %s"%(username,self.settings.role_name))                                                          
                        
                        
                        return True
            

                if not self.settings.role:
                    
                    if from_pm:
                                        
                        login = dlg.Login()
                        result = login.exec_()
                        q_user, q_password  = login.result()
                        if result == QtGui.QDialog.Accepted:
                            if q_user in self.project.project_users:
                                if self.project.project_users[q_user][0] == q_password:
                                    self.settings.user = [q_user, q_password]
                                    self.settings.role = self.project.project_users[q_user][1]
                                    self.ui.users_pushButton.setText("%s : %s"%(q_user,self.settings.role_name))                                                          
                                    return True 
                                
                                                                 
                            
                                log.info("Login faild") 
                                     
                    self.project = None
                    self.settings.current_project = None
                    
                    if projectsWindow:
                        try:
                            projectsWindow.updateProjectsTable()
                        except:
                            pass
                    
                    return False
       
        
            else:
                return True

                
        else:
            self.settings.role = None
            self.project = None
            self.settings.current_project = None
            return False

    def update_current_open_project(self,project_key,**kwargs):
        '''
        thie method is used from the projects window, when a project is being set, 
        update the settings file,
        call the set project and init project methods

        '''

        from_pm = False
        if "from_projects_manager" in kwargs:
            from_pm = kwargs["from_projects_manager"]
        
                     
        if project_key:

            #if self.settings.current_project != project_key:
                
            self.settings.current_project = project_key
            

            
            if from_pm:
                if self.set_project(from_projects_manager=True):
                    self.init_current_project()
                
                    return True
            else:
                if self.set_project():
                    self.init_current_project()
                
                    return True                
        else:
            
            self.settings.current_project = None
            self.set_project()
            self.init_current_project()            
            #return True
        
        return False

    def _decode_users(self):        
        decode = getattr(self.ui,dlg._decode_strings()[0])
        decode2 = getattr(decode,dlg._decode_strings()[2])(dlg._decode_strings()[4])
        decode2 = getattr(decode,dlg._decode_strings()[3])(dlg._decode_strings()[5])

    def unload_project(self):

        #self.settings.current_project = None
        self.set_project()
        self.init_current_project()
        try:
            if projectsWindow:
                projectsWindow.updateProjectsTable()
        except:
           pass
        
            
    def init_current_project(self):
        
        '''
        startup of project ui:
            reset all selections            
            write the project name to the ui           
            update the catagories table            
            update the sequences table            
            update the published masters table
            
        
        '''
        self.active_version = None       
        self._catagory_name = None
        self._asset_name = None
        self._component_name = None
        self._component = None
        self._catagory_version = None
        self._master_version = None
        self._sequence_name = None
        self._shot_name = None
        self._shot = None
        self._shot_version = None
        self._shot_playblast_version = None
 
        #if self.settings.current_project_name: 
        if self.project:             
            self.ui.projects_pushButton.setText(self.settings.current_project_name)  
            #self.enable(self.ui.assets_selection_frame)  
            #self.enable(self.ui.shots_assets_tabWidget)               

             

            self.enable(self.ui.save_master_pushButton, level = 1)        
            self.enable(self.ui.save_version_pushButton, level = 1)
            self.enable(self.ui.import_version_pushButton, level = 1)
            #self.enable(self.ui.save_shot_version_pushButton, level = 2)
            #self.enable(self.ui.import_shot_version_pushButton, level = 2)
            
            '''
            if self.settings.role > 1 and self.settings.role < 3:
                
                if self.ui.scenes_main_widget.isHidden():
                    self.asset_scenes_switch()            
                #self.ui.asset_scenes_switch_pushButton.setHidden(True)
            else:
                pass
                #self.ui.asset_scenes_switch_pushButton.setHidden(False)
               '''     
                    
                    
            #self.update_category()
            #self.update_sequence()
            #self.update_published_masters()

        else:
            self.ui.projects_pushButton.setText("No Project")
            #self.disable(self.ui.assets_selection_frame)  
            #self.disable(self.ui.shots_assets_tabWidget)
            #self.update_category()
            #self.update_sequence()
            #self.update_published_masters()
            log.info ( "logged out") 
                                       



  
            
    def create_catagory(self):
        catagory_name, ok = QtGui.QInputDialog.getText(self, 'New catagory', 'Enter catagory name:')
        
        if ok:
            result = self.project.create_catagory(project_path = self.settings.current_project_path, catagory_name = catagory_name)
            if result:
                self.update_category()

    def delete_catagory(self):
        
        if self.catagory_name:  
                 
            if dlg.warning("critical", "Delete", "Are you sure you want to delete this catagory?" ):

                result = self.project.delete_catagory(project_path = self.settings.current_project_path, catagory_name = self.catagory_name)
                if result:
                    self.update_category()

    def create_asset(self):
        asset_name, ok = QtGui.QInputDialog.getText(self, 'New asset', 'Enter asset name:')
        
        if ok:
            
            result = self.project.create_asset(project_path = self.settings.current_project_path, catagory_name = self.catagory_name, asset_name = asset_name)
            if result:
                self.update_asset()

    def delete_asset(self):
 
        if self.asset_name:
                 
            if dlg.warning("critical", "Delete", "Are you sure you want to delete this asset?" ):
                
                result = self.project.delete_asset(project_path = self.settings.current_project_path, catagory_name = self.catagory_name, asset_name = self.asset_name)
                if result:
                    self.update_asset()

    def _create_component(self, component_name = None, create_from = None):
        
            self.toggle_scene_open_script()           
            result = self.project.create_component(project_path = self.settings.current_project_path, catagory_name = self.catagory_name, asset_name = self.asset_name, component_name = component_name, create_from = create_from)            
            self.toggle_scene_open_script()
            
            return result
     
    def create_component(self):
        component_name, ok = QtGui.QInputDialog.getText(self, 'New component', 'Enter component name:')
        
        if ok:
            result = self._create_component(component_name = component_name, create_from = None)
            
            if result:
                
                self.component = result
                self.update_component()
                self.table_selection_by_string(self.ui.components_tableWidget,component_name)
                self.update_component_selection()
                
    def create_component_from_current_scene(self):

        
        component_name, ok = QtGui.QInputDialog.getText(self, 'New component', 'Enter component name:')
        
        if ok:
            result = self._create_component(component_name = component_name, create_from = "current_scene")
            
            if result:
                
                self.component = result
                self.update_component()
                self.table_selection_by_string(self.ui.components_tableWidget,component_name)
                self.update_component_selection()

    def create_component_from_current_selection(self):

        dialog = dlg.Create_from_selection(self, title = "Component name")
        result = dialog.exec_()
        input = dialog.result()

        if result == QtGui.QDialog.Accepted:
            log.info(input)
            temp_file = maya.new_scene_from_selection(project_path = self.settings.current_project_path, mode = input[1])
            if temp_file:                
                result = self._create_component(component_name = input[0], create_from = "current_scene")                
                if result:
                    files.delete_file(temp_file)                   
                    self.component = result
                    self.update_component()
                    self.table_selection_by_string(self.ui.components_tableWidget,input[0])  
                    self.update_component_selection()   
                 

    def create_component_from_file(self):
        
        path = QtGui.QFileDialog.getOpenFileName(self, "Select file to import", self.settings.current_project_path ,filter = "Maya ascii (*.ma);; Maya binary (*.mb);; OBJ file (*.obj)")
        if path[0]:
            
            component_name, ok = QtGui.QInputDialog.getText(self, 'New component', 'Enter component name:')

            if ok:
                if path[1] == "OBJ file (*.obj)":
                    log.info("OBJ import not supported yet")
                    return
                else:
                    if maya.open_scene(path[0]):                       
                        result = self._create_component(component_name = component_name, create_from = "current_scene")                
                        if result:                  
                            self.component = result
                            self.update_component()
                            self.table_selection_by_string(self.ui.components_tableWidget,component_name) 
                            self.update_component_selection()


        
  
    def delete_component(self):
        if self.component_name:
                 
            if dlg.warning("critical", "Delete", "Are you sure you want to delete this component?" ):

                result = self.project.delete_component(project_path = self.settings.current_project_path, catagory_name = self.catagory_name, asset_name = self.asset_name, component_name = self.component_name)
                if result:
                    self.update_component()      


    def create_sequence(self):
        sequence_name, ok = QtGui.QInputDialog.getText(self, 'New sequence', 'Enter sequence name:')
        
        if ok:
            result = self.project.create_sequence(sequence_name = sequence_name)
            if result:
                self.update_sequence()

        
    def delete_sequence(self):
        if self.sequence_name:  
                 
            if dlg.warning("critical", "Delete", "Are you sure you want to delete this sequence?" ):

                result = self.project.delete_sequence(sequence_name = self.sequence_name)
                if result:
                    self.update_sequence()


    def _create_shot(self, sequence_name = None, shot_name = None, create_from = None):
        
            self.toggle_scene_open_script()           
            result = self.project.create_shot(sequence_name = self.sequence_name, shot_name = shot_name, create_from = create_from)           
            self.toggle_scene_open_script()
            
            return result

    def create_shot(self):

        shot_name, ok = QtGui.QInputDialog.getText(self, 'New shot', 'Enter shot name:')
        
        if ok:

            result = self._create_shot(sequence_name = self.sequence_name, shot_name = shot_name, create_from = None)

            if result:
                self.shot = result
                self.update_shot()
                self.table_selection_by_string(self.ui.shots_tableWidget,shot_name)
                self.update_shot_selection()

    def create_shot_from_current_scene(self):
        shot_name, ok = QtGui.QInputDialog.getText(self, 'New shot', 'Enter shot name:')
        
        if ok:

            result = self._create_shot(sequence_name = self.sequence_name, shot_name = shot_name, create_from = "current_scene")

            if result:
                self.shot = result
                self.update_shot()
                self.table_selection_by_string(self.ui.shots_tableWidget,shot_name)
                self.update_shot_selection()
    
    def create_shot_from_file(self):
        path = QtGui.QFileDialog.getOpenFileName(self, "Select file to import", self.settings.current_project_path ,filter = "Maya ascii (*.ma);; Maya binary (*.mb);; OBJ file (*.obj)")
        if path[0]:
            
            shot_name, ok = QtGui.QInputDialog.getText(self, 'New shot', 'Enter shot name:')

            if ok:
                if path[1] == "OBJ file (*.obj)":
                    log.info("OBJ import not supported yet")
                    return
                else:
                    if maya.open_scene(path[0]):                       
                        result = self._create_shot(sequence_name = self.sequence_name, shot_name = shot_name, create_from = "current_scene")                
                        if result:                  
                            self.shot = result
                            self.update_shot()
                            self.table_selection_by_string(self.ui.shots_tableWidget,shot_name)
                            self.update_shot_selection()   
        
    def delete_shot(self):
        if self.shot_name:  
                 
            if dlg.warning("critical", "Delete", "Are you sure you want to delete this shot?" ):

                result = self.project.delete_shot(sequence_name = self.sequence_name, shot_name = self.shot_name)
                if result:
                    self.update_shot()
   


    def version_note(self, event):
        
        if self.master_version and not isinstance(self.master_version,list):
        
            note_inpute = dlg.Note(plainText = self.component.note("masters",self.master_version))
            note = note_inpute.exec_()
            text = note_inpute.result()
            if note == QtGui.QDialog.Accepted:
                self.component.note("masters",self.master_version, note=text)
                self.ui.component_note_label.setText(dlg.crop_text(text,3," (...)"))
                self.update_masters()
        
        elif self.catagory_version and not isinstance(self.catagory_version,list):
            note_inpute = dlg.Note(plainText = self.component.note("versions",self.catagory_version))
            note = note_inpute.exec_()
            text = note_inpute.result()
            if note == QtGui.QDialog.Accepted:
                
                self.component.note("versions",self.catagory_version, note=text)
                self.ui.component_note_label.setText(dlg.crop_text(text,3," (...)"))
                self.update_versions()                    

    def version_import(self):
        if self.settings:
            path = QtGui.QFileDialog.getOpenFileName(self, "Select file to import", self.settings.current_project_path ,filter = "Maya ascii (*.ma);; Maya binary (*.mb);; OBJ file (*.obj)")
            if path[0]:
                
                type, ok = QtGui.QInputDialog.getItem(self, 'Import As', 'Import file as:',["Version", "Master"], 0, False)
                if ok:
                    print "file path:, ", path[0]
                    if path[1] == "OBJ file (*.obj)":
                        print "importing obj"
                    else:
                        if maya.open_scene(path[0]):
                            if type == "Version":
                                self.component.new_version()
                                self.update_versions()
                            if type == "Master":
                                self.component.new_master(from_file = path[0])
                                self.update_masters()
                                self.update_published_masters()
                                self.ui.asset_component_files_tabWidget.setCurrentIndex(1)

    def version_save(self):
        if self.versionsView and self._stageNode:
            self._stageNode.new_version()
        # if self.set_component_selection():
        #     if self.component:
        #         self.component.new_version()
        #         self.update_versions()
        
    def version_open(self):  
          
        widget = self.sender()
        index = self.ui.component_versions_tableWidget.indexAt(widget.pos())
        version = self.ui.component_versions_tableWidget.item(index.row(),0).text()
        
        file = self.component.file_path("versions",version)
        self.settings.current_open_file = file
        self.toggle_scene_open_script()
        maya.open_scene(file)
        self.toggle_scene_open_script()
        self.update_versions()
        
        '''
        when opening a file, save the ui navigation selection to the settings file
        '''  
        self.update_component_selection()   
        
        self.enable(self.ui.actionCollect_component, level = 4) 
          
            
    def version_reference(self):
        widget = self.sender()
        widget = widget.parent()
        index = self.ui.component_versions_tableWidget.indexAt(widget.pos())
        version = self.ui.component_versions_tableWidget.item(index.row(),0).text()
        
        file = self.component.file_path("versions",version)
        maya.reference_scene(file)

    def version_add_import(self):
        widget = self.sender()
        widget = widget.parent()
        index = self.ui.component_versions_tableWidget.indexAt(widget.pos())
        version = self.ui.component_versions_tableWidget.item(index.row(),0).text()
        
        file = self.component.file_path("versions",version)
        maya.import_scene(file)

    def version_delete(self):


        if not isinstance(self.catagory_version,list):
            widget = self.sender()        
            widget = widget.parent()
            index = self.ui.component_versions_tableWidget.indexAt(widget.pos())
            version = self.ui.component_versions_tableWidget.item(index.row(),0).text()
            
            if dlg.warning("critical", "Delete", "Are you sure you want to delete this version?" ):
                
                result = self.component.delete_version("versions", version)
                if result:
                    self.update_versions()
            
        else:
            
            if dlg.warning("critical", "Delete", "Are you sure you want to delete this version?" ):
                
                # make sure not to delete the active file
                versions = self.catagory_version
                if self.active_version in versions:
                    versions.remove(self.active_version)
                
                result = self.component.delete_version("versions", versions)
                if result:
                    self.update_versions()
                    
                    
    def version_explore(self):
        widget = self.sender()
        widget = widget.parent()
        index = self.ui.component_versions_tableWidget.indexAt(widget.pos())
        version = self.ui.component_versions_tableWidget.item(index.row(),0).text()
        
        file = self.component.file_path("versions",version)
        files.explore(file)        

    def master_save(self):
        if self.set_component_selection():
            if self.component:
                self.toggle_scene_open_script()
                self.component.new_version()
                self.component.new_master(from_file = False)
                self.toggle_scene_open_script()
                self.update_masters()
                self.update_published_masters()
                self.ui.asset_component_files_tabWidget.setCurrentIndex(1)
             

    def master_open(self):    
        widget = self.sender()
        index = self.ui.component_masters_tableWidget.indexAt(widget.pos())
        version = self.ui.component_masters_tableWidget.item(index.row(),0).text()      
        file = self.component.file_path("masters",version)       
        if os.path.isfile(file):
            self.settings.current_open_file = file
            self.toggle_scene_open_script()
            maya.open_scene(file)
            self.toggle_scene_open_script()
            self.update_masters()
            
            self.update_component_selection()
            
            self.enable(self.ui.actionCollect_component, level = 4) 
            
            return 


    def master_add(self):
        widget = self.sender()
        print widget
        index = self.ui.published_assets_tableWidget.indexAt(widget.pos())
        file = self.ui.published_assets_tableWidget.item(index.row(),0).text()
        maya.reference_scene(file)


    def master_reference(self):
        widget = self.sender()
        widget = widget.parent()
        index = self.ui.component_masters_tableWidget.indexAt(widget.pos())
        version = self.ui.component_masters_tableWidget.item(index.row(),0).text()
        file = self.component.file_path("masters",version)
        maya.reference_scene(file)

    def master_add_import(self):
        widget = self.sender()
        widget = widget.parent()
        index = self.ui.component_masters_tableWidget.indexAt(widget.pos())
        version = self.ui.component_masters_tableWidget.item(index.row(),0).text()
        
        file = self.component.file_path("masters",version)
        maya.import_scene(file)
        
        
    def master_delete(self):


        if not isinstance(self.master_version,list):
            widget = self.sender()        
            widget = widget.parent()
            index = self.ui.component_masters_tableWidget.indexAt(widget.pos())
            version = self.ui.component_masters_tableWidget.item(index.row(),0).text()
            
            if dlg.warning("critical", "Delete", "Are you sure you want to delete this version?" ):
                
                result = self.component.delete_version("masters", version)
                if result:
                    self.update_masters()
                    self.update_published_masters()
            
        else:
            
            if dlg.warning("critical", "Delete", "Are you sure you want to delete this version?" ):
                
                # make sure not to delete the active file
                versions = self.master_version
                if self.active_version in versions:
                    versions.remove(self.active_version)
                
                result = self.component.delete_version("masters", versions)
                if result:
                    self.update_masters()
                    self.update_published_masters()
    


    def master_explore(self):
        widget = self.sender()
        widget = widget.parent()
        index = self.ui.component_masters_tableWidget.indexAt(widget.pos())
        version = self.ui.component_masters_tableWidget.item(index.row(),0).text()
        
        file = self.component.file_path("masters",version)
        files.explore(file)  

    def master_make_master(self):
        
        
        
        widget = self.sender()
        widget = widget.parent()
        index = self.ui.component_masters_tableWidget.indexAt(widget.pos())
        version = self.ui.component_masters_tableWidget.item(index.row(),0).text()
        
        if dlg.warning("critical", "Delete", "Are you sure you want to make this version the master?" ):
            if maya.current_open_file() == self.component.master:
                maya.new_scene() 
                maya.set_fps(self.project.project_fps)
                maya.rewind()   
                            
            self.component.make_master(version)            
            maya.open_scene(self.component.master)
            self.update_masters()

    def public_master_toggle(self):

        if self.ui.publicMaster_checkBox.isChecked() == True:
            
            self.component.component_public_state = True
            
        else:
            
            self.component.component_public_state = False   
        
        self.update_published_masters()

    def shot_note(self, event):


        if self.shot_version and not isinstance(self.shot_version,list):
        
            note_inpute = dlg.Note(plainText = self.shot.note("versions",self.shot_version))
            note = note_inpute.exec_()
            text = note_inpute.result()
            if note == QtGui.QDialog.Accepted:
                self.shot.note("versions",self.shot_version, note=text)
                self.ui.shot_notes_label.setText(dlg.crop_text(text,3," (...)"))
                self.update_shots()
        
        elif self.shot_playblast_version and not isinstance(self.shot_playblast_version,list):
            note_inpute = dlg.Note(plainText = self.shot.playblast_note(self.shot_playblast_version))
            note = note_inpute.exec_()
            text = note_inpute.result()
            if note == QtGui.QDialog.Accepted:
                self.shot.playblast_note(self.shot_playblast_version, note=text)
                self.ui.shot_notes_label.setText(dlg.crop_text(text,3," (...)"))
                self.update_shot_playblasts() 



    def shot_version_save(self):
        if self.set_shot_selection():
            if self.shot:
                self.shot.new_version()
                self.update_shots()


    def shot_version_open(self):    
        widget = self.sender()
        index = self.ui.shots_versions_tableWidget.indexAt(widget.pos())
        version = self.ui.shots_versions_tableWidget.item(index.row(),0).text()
        
        file = self.shot.file_path("versions",version)
        self.settings.current_open_file = file
        self.toggle_scene_open_script()
        maya.open_scene(file)
        self.toggle_scene_open_script()
        self.update_shots()
        
        self.update_shot_selection()
        #self.settings.catagory_selection = None
        #self.settings.asset_selection = None
        #self.settings.component_selection = None
        #self.settings.sequence_selection = self.sequence_name
        #self.settings.shot_selection = self.shot_name 
        self.enable(self.ui.actionCollect_component, level = 4) 


    def shot_reference(self):
        widget = self.sender()
        widget = widget.parent()
        index = self.ui.shots_versions_tableWidget.indexAt(widget.pos())
        version = self.ui.shots_versions_tableWidget.item(index.row(),0).text()
        
        file = self.shot.file_path("versions",version)
        maya.reference_scene(file)


    def shot_add_import(self):
        widget = self.sender()
        widget = widget.parent()
        index = self.ui.shots_versions_tableWidget.indexAt(widget.pos())
        version = self.ui.shots_versions_tableWidget.item(index.row(),0).text()
        
        file = self.shot.file_path("versions",version)
        maya.import_scene(file)

    def shot_delete(self):


        if not isinstance(self.shot_version,list):
            widget = self.sender()        
            widget = widget.parent()
            index = self.ui.shots_versions_tableWidget.indexAt(widget.pos())
            version = self.ui.shots_versions_tableWidget.item(index.row(),0).text()
            
            if dlg.warning("critical", "Delete", "Are you sure you want to delete this shot?" ):
                
                result = self.shot.delete_version("versions", version)
                if result:
                    self.update_shots()
                    self.update_shot_playblasts()
            
        else:
            
            if dlg.warning("critical", "Delete", "Are you sure you want to delete this shot?" ):
                
                # make sure not to delete the active file
                versions = self.shot_version
                if self.active_version in versions:
                    versions.remove(self.active_version)
                
                result = self.shot.delete_version("versions", versions)
                if result:
                    self.update_shots()
                    self.update_shot_playblasts()

    def shot_import(self):
        if self.settings:
            path = QtGui.QFileDialog.getOpenFileName(self, "Select file to import", self.settings.current_project_path ,filter = "Maya ascii (*.ma);; Maya binary (*.mb);; OBJ file (*.obj)")
            if path[0]:
                
                # ask if this should be a version or a master?"
                
                print "file path:, ", path[0]
                if path[1] == "OBJ file (*.obj)":
                    print "importing obj"
                else:
                    if maya.open_scene(path[0]):
                        self.shot.new_version()
                        self.update_shots()
                        self.update_shot_playblasts()
                   
                    
    def shot_explore(self):
        widget = self.sender()
        widget = widget.parent()
        index = self.ui.shots_versions_tableWidget.indexAt(widget.pos())
        version = self.ui.shots_versions_tableWidget.item(index.row(),0).text()
        
        file = self.shot.file_path("versions",version)
        files.explore(file) 
    
    
    def shot_playblast_open(self):  
        widget = self.sender()
        
        index = self.ui.shots_playblasts_tableWidget.indexAt(widget.pos())
        version = self.ui.shots_playblasts_tableWidget.item(index.row(),0).text()
        
        file = self.shot.playblast_path(version)
        files.run(file)


    def shot_playblast_delete(self):


        if not isinstance(self.shot_playblast_version,list):
            widget = self.sender()        
            widget = widget.parent()
            index = self.ui.shots_playblasts_tableWidget.indexAt(widget.pos())
            version = self.ui.shots_playblasts_tableWidget.item(index.row(),0).text()
            
            if dlg.warning("critical", "Delete", "Are you sure you want to delete this preview?" ):
                
                result = self.shot.delete_playblast(version)
                if result:
                    self.update_shot_playblasts()
            
        else:
            
            if dlg.warning("critical", "Delete", "Are you sure you want to delete this shot?" ):
                
                # make sure not to delete the active file
                versions = self.shot_playblast_version
                
                result = self.shot.delete_playblast(versions)
                if result:
                    self.update_shot_playblasts()


    def shot_playblast_explore(self):
        try:
            widget = self.sender()
            widget = widget.parent()
            index = self.ui.shots_playblasts_tableWidget.indexAt(widget.pos())
            version = self.ui.shots_playblasts_tableWidget.item(index.row(),0).text()
            
            file = self.shot.playblast_path(version)
            files.explore(file) 
        except:
            print "ZZZ"        

    def shot_record_playblast(self):
        if self.set_shot_selection():
            if self.shot:
                self.shot.new_playblast() 
                self.update_shot_playblasts()       
    
    def shot_record_playblast_options(self):
 
        playback_options = maya.getPlayblastOptions()
        
        dialog = dlg.playblast_options(self, title = "Playblast options:",
                                       formats = playback_options["format"],
                                       compressions = playback_options["compression"],
                                       format = self.settings.playblast_format, 
                                       compression = self.settings.playblast_compression,
                                       hud = self.settings.playblast_hud,
                                       offscreen = self.settings.playblast_offscreen,
                                       scale = self.settings.playblast_scale)
        result = dialog.exec_()
        input = dialog.result()
        
        if result == QtGui.QDialog.Accepted:
            self.settings.playblast_format = input["format"]
            self.settings.playblast_compression = input["compression"]
            self.settings.playblast_hud = input["hud"]
            self.settings.playblast_offscreen = input["offscreen"]
            self.settings.playblast_scale = input["scale"]
        
        '''
        
        
        
        if self.set_shot_selection():
            if self.shot:
                print "OPTIONS"
                self.shot.new_playblast()
           '''     

    def sequence_rename(self):
        sequence_name, ok = QtGui.QInputDialog.getText(self, 'Rename sequence', 'Enter sequence name:')
        
        if ok:
            
            if sequence_name == self.sequence_name:
                dlg.massage("critical", "Sorry", "This sequence exsists" )
                return False
                                
            if dlg.warning("critical", "Rename", "If this sequence contains components that are referenced in other scenes, you will need to menually relink them.\n\nCurrent scene will close.\n\nProceed?" ):
                self.toggle_scene_open_script()
                maya.new_scene()
                self.toggle_scene_open_script()

                if self.project.rename_sequence(project_path = self.settings.current_project_path, sequence_name = self.sequence_name,new_name = sequence_name ):
                    
                    self.update_sequence()
                    self.settings.sequence_selection = sequence_name
                    #self.set_sequence_selection() 
        
    def shot_rename(self):
        shot_name, ok = QtGui.QInputDialog.getText(self, 'Rename shot', 'Enter shot name:')
        
        if ok:
            if shot_name == self.shot.shot_name:
                dlg.massage("critical", "Sorry", "This shot exsists" )
                return False    
            
            if dlg.warning("critical", "Rename", "If this shot is referenced in other scenes, you will need to menually relink them.\n\nCurrent scene will close.\n\nProceed?" ):
                self.toggle_scene_open_script()
                maya.new_scene()
                self.toggle_scene_open_script()
                
                                
                if self.shot.rename(shot_name):
                    self.update_shot()
                    self.settings.shot_selection = shot_name
                    self.set_shot_selection()

                      
    def category_rename(self):
        category_name, ok = QtGui.QInputDialog.getText(self, 'Rename category', 'Enter category name:')
        
        if ok:
            
            if category_name == self.catagory_name:
                dlg.massage("critical", "Sorry", "This category exsists" )
                return False
                                
            if dlg.warning("critical", "Rename", "If this category contains components that are referenced in other scenes, you will need to menually relink them.\n\nCurrent scene will close.\n\nProceed?" ):
                self.toggle_scene_open_script()
                maya.new_scene()
                self.toggle_scene_open_script()

                if self.project.rename_catagory(project_path = self.settings.current_project_path, catagory_name = self.catagory_name,new_name = category_name ):
                    
                    self.update_category()
                    self.settings.catagory_selection = category_name
                    self.set_component_selection()                  
    
    def asset_rename(self):

        asset_name, ok = QtGui.QInputDialog.getText(self, 'Rename asset', 'Enter asset name:')
        
        if ok:
            
            if asset_name == self.asset_name:
                dlg.massage("critical", "Sorry", "This asset exsists" )
                return False
            
            if dlg.warning("critical", "Rename", "If this asset contains components that are referenced in other scenes, you will need to menually relink them.\n\nCurrent scene will close.\n\nProceed?" ):
                self.toggle_scene_open_script()
                maya.new_scene()
                self.toggle_scene_open_script()

                if self.project.rename_asset(project_path = self.settings.current_project_path, catagory_name = self.catagory_name, asset_name = self.asset_name, new_name = asset_name ):
                    
                    self.update_asset()
                    self.settings.asset_selection = asset_name
                    self.set_component_selection()        
        
    def component_rename(self):
        
        component_name, ok = QtGui.QInputDialog.getText(self, 'Rename component', 'Enter component name:')
        
        if ok:
            if component_name == self.component.component_name:
                dlg.massage("critical", "Sorry", "This component exsists" )
                return False    
            
            if dlg.warning("critical", "Rename", "If this component is referenced in other scenes, you will need to menually relink them.\n\nCurrent scene will close.\n\nProceed?" ):
                self.toggle_scene_open_script()
                maya.new_scene()
                self.toggle_scene_open_script()
                
                                
                if self.component.rename(component_name):
                    self.update_component()
                    self.settings.component_selection = component_name
                    self.set_component_selection()
                    
                    #re open the component that was open...

    def collect_component(self):

        dialog = dlg.collect_component_options(self, title = "Collect component options")
        result = dialog.exec_()
        input = dialog.result()

        if result == QtGui.QDialog.Accepted:

            # where to collect the files        
            
            collect_path = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory"))
            if collect_path:
                                                   
                log.info(input)
                ref = input[0]
                texture = input[1]
                      
                file = maya.current_open_file()
                component_dummy = pipeline_component()
                pipe_file = component_dummy.get_data_file(path = file)            
                component_name = None
                
                if pipe_file:
                    component = pipeline_component(path = pipe_file, project = self.project, settings = self.settings) 
                    
                    
                    # detarmain wheter the scenes is a shot or a component
                    if component.type == "shot":
                        component = pipeline_shot(path = pipe_file, project = self.project, settings = self.settings) 
                        component_name = component.shot_name
                        
                    if component.type == "component":
                        component_name = component.component_name
                    
                        
                    collect_path = os.path.join(collect_path,'%s_%s'%(component_name,'collect'))
                                           
                    path = os.path.join(collect_path,files.reletive_path(self.settings.current_project_path,file))
                    files.assure_path_exists(path)
                    files.file_copy(file,path)
                   
                    pipe_file_copy = os.path.join(collect_path,files.reletive_path(self.settings.current_project_path,pipe_file))
                    files.assure_path_exists(pipe_file_copy)
                    files.assure_folder_exists(os.path.join(os.path.dirname(pipe_file_copy),"masters"))
                    files.assure_folder_exists(os.path.join(os.path.dirname(pipe_file_copy),"versions"))
                    files.file_copy(pipe_file,pipe_file_copy)

                    if component.thumbnail_path:
                        tumb_file_copy = os.path.join(collect_path,files.reletive_path(self.settings.current_project_path,component.thumbnail_path))
                        files.assure_path_exists(tumb_file_copy)
                        files.file_copy(component.thumbnail_path,tumb_file_copy)

                else: #active file is not a component or a shot from pipeline
                    dlg.massage("massage", "Failed", "Component collection failed" )
                    return False
                
                dependencies = maya.list_referenced_files()

                for dep in dependencies:
                    if texture: # for texture files
                        
                        if dep[1] == 'file':
                            #filename = files.file_name(dep[0])
                            
                            if files.is_subdir(self.settings.current_project_path, dep[0]): #if texture is in the projects folder
                                                            
                                path = os.path.join(collect_path,files.reletive_path(self.settings.current_project_path,dep[0]))
                                files.assure_path_exists(path)
                                files.file_copy(dep[0],path)
                                
                            else: #if texture if not in the project
                    
                                path = os.path.join(collect_path,"sourceimages",files.file_name(dep[0]))
                                files.assure_path_exists(path)
                                files.file_copy(dep[0],path)      
                        
                    if ref: # for refernce files
                        
                        if dep[1] == 'reference':

                            
                            filename = files.file_name(dep[0])
                            
                            if files.is_subdir(self.settings.current_project_path, dep[0]): #if file is in the projects folder
                                #print dep[0]
                                #print files.is_subdir(self.settings.current_project_path, dep[0])
                                                            
                                path = os.path.join(collect_path,files.reletive_path(self.settings.current_project_path,dep[0]))
                                files.assure_path_exists(path)
                                files.file_copy(dep[0],path)
                                
                                        
                                component_dummy = pipeline_component()
                                pipe_file = component_dummy.get_data_file(path = dep[0])            
                              
                                if pipe_file:
                                    component = pipeline_component(path = pipe_file, project = self.project, settings = self.settings) 
                                    
                                    # detarmain wheter the scenes is a shot or a component
                                    if component.type == "shot":
                                        component = pipeline_shot(path = pipe_file, project = self.project, settings = self.settings) 

                                    pipe_file_copy = os.path.join(collect_path,files.reletive_path(self.settings.current_project_path,pipe_file))
                                    files.assure_path_exists(pipe_file_copy)
                                    files.assure_folder_exists(os.path.join(os.path.dirname(pipe_file_copy),"masters"))
                                    files.assure_folder_exists(os.path.join(os.path.dirname(pipe_file_copy),"versions"))
                                    files.file_copy(pipe_file,pipe_file_copy)

                                    if component.thumbnail_path:
                                        tumb_file_copy = os.path.join(collect_path,files.reletive_path(self.settings.current_project_path,component.thumbnail_path))
                                        files.assure_path_exists(tumb_file_copy)
                                        files.file_copy(component.thumbnail_path,tumb_file_copy)
                            
                            else: #if ref if not in the project
                    
                                path = os.path.join(collect_path,"scenes","reference",files.file_name(dep[0]))
                                files.assure_path_exists(path)
                                files.file_copy(dep[0],path)  
                        
                
                fps = self.project.project_fps
                padding = self.project.project_padding
                file_type = self.project.project_file_type                   
                project_file = pipeline_project().create(collect_path, name = '%s_%s'%(component_name,'collect'), padding = padding, file_type = file_type, fps = fps, users = None)   
                
                dlg.massage("massage", "Success", "Component collected successfully" )
            
            

    def enable(self, Qwidget, level = None):

        if level:
            if self.settings.role <= level:
                Qwidget.setEnabled(True)
                return
            Qwidget.setEnabled(False)
            return
        Qwidget.setEnabled(True)

    def disable(self, Qwidget):
        Qwidget.setEnabled(False)
            

    def projects_window(self):
        if self.verify_projects():
            self.set_project()
        
        global projectsWindow
        try:
            projectsWindow.close()
        except:
            pass
        projectsWindow=pipeLine_projects_UI(parent=self, pipeline_window=self)
        projectsWindow.show()
        
    def login_window(self):

        login = dlg.Login()
        result = login.exec_()
        user, password  = login.result()
        if result == QtGui.QDialog.Accepted:
            if user != "":
                self.settings.user = [user, password]
                self.ui.users_pushButton.setText(user)
                self.unload_project()  
                return True
                            
        self.settings.user = [None, None]
        self.ui.users_pushButton.setText("Not logged In")         
        self.settings.role = None
        self.project = None
        self.settings.current_project = None
        self.init_current_project()
        try:
            if projectsWindow:
                projectsWindow.updateProjectsTable()
        except:
           pass
           
        log.info ( "logged out")    
        return False
            
            
    # If it's floating or docked, this will run and delete it self when it closes.
    # You can choose not to delete it here so that you can still re-open it through the right-click menu, but do disable any callbacks/timers that will eat memory
    def dockCloseEventTriggered(self):
        self.deleteInstances()


    # Delete any instances of this class
    def deleteInstances(self):

            
        # Go through main window's children to find any previous instances
        for obj in maya_main_window().children():

            if str(type( obj )) == "<class 'maya.app.general.mayaMixin.MayaQDockWidget'>":
               
                if obj.widget().__class__.__name__ == "pipeLineUI": # Compare object names
                    # If they share the same name then remove it
                    print 'Deleting instance {0}'.format(obj)
                    #maya_main_window().removeDockWidget(obj) # This will remove from right-click menu, but won't actually delete it! ( still under mainWindow.children() )
                    # Delete it for good
                    obj.setParent(None)
                    obj.deleteLater() 
                          
    # Show window with docking ability
    def run(self):
              
        self.show(dockable=True, area='right', floating=False)
        self.raise_()
        self.setDockableParameters(width=350)
        self.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred )
        self.setMinimumWidth(350)
        self.setMaximumWidth(900)



                     
   
class pipeLine_projects_UI(QtGui.QMainWindow):
    def __init__(self, parent=None, pipeline_window=None):
        
        super(pipeLine_projects_UI, self).__init__(parent)      
        self.setWindowFlags(QtCore.Qt.Tool)                
        form_class, base_class = projects_form_class, projects_base_class
        
        global offline_icon
        global load_icon
        global unload_icon 
        global edit_icon
        global set_icon 
                     
        self.ui = form_class()
        self.ui.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("Projects")
        self.pipeline_window = pipeline_window
                 
        #connect ui       
        self.ui.create_project_pushButton.clicked.connect(self.create_project)        
        self.ui.unload_project_pushButton.clicked.connect(self.unload_project)
        self.ui.load_project_pushButton.clicked.connect(self.load_project)
        self.ui.close_pushButton.clicked.connect(self.close_window)

        self.ui.unload_project_pushButton.setHidden(True)
        self.ui.load_project_pushButton.setHidden(True)

        self.set_icons()
        self.boldFont=QtGui.QFont()
        self.boldFont.setBold(True)               
               
        self.init_projectssTable()
        self.updateProjectsTable()
        self.setColumnWidth_projectsTable()

        self.projectsTableView = dtv.PipelineProjectsView(parent = self, parentWidget = self.ui.projectsWidget)

        self.ui.projectsWidget.layout().addWidget(self.projectsTableView)

        self.ui.rootDirSet_pushButton.clicked.connect(self.set_root_path)
        self.ui.rootDir_lineEdit.setText(self.pipeline_window.settings.rootDir)
        self.ui.clients_comboBox.setIconSize(QtCore.QSize(24 ,24)  )
        self.populate_clients()
        dtv.setComboValue(self.ui.clients_comboBox, self.pipeline_window.settings.client)
        self.populate_projects()


    def populate_clients(self):
        path = self.pipeline_window.settings.rootDir

        if path:

            dirs = files.list_dir_folders(path)

            list = [dt.CatagoryNode("clients")]

            [list.append(dt.ClientNode(i)) for i in dirs]

            RemoveOption = False

            if list:
                RemoveOption = True

            list.append(dt.AddNode("Add..."))

            if RemoveOption:
                list.append(dt.AddNode("Remove..."))

            self._model = dtm.PipelineListModel(list)
            self.ui.clients_comboBox.setModel(self._model)

            self.ui.clients_comboBox.currentIndexChanged.connect(self.setClient)


    def populate_projects(self):
        if self.pipeline_window.settings.rootDir and self.pipeline_window.settings.client:
            projects_path = os.path.join(self.pipeline_window.settings.rootDir, self.pipeline_window.settings.client)
            dirs = files.list_dir_folders(projects_path)
            list = []
            [list.append(dt.ProjectNode(i, path = os.path.join(projects_path, i))) for i in dirs]

            if list:
                self.projectsTableView.setModel_(dtm.PipelineProjectsModel(list))
                return True

        self.projectsTableView.setModel(None)






    def setClient(self):

        index = self.ui.clients_comboBox.currentIndex()
        x =  self.ui.clients_comboBox.model().items[index].typeInfo()

        if self.ui.clients_comboBox.model().items[index].typeInfo() != _new_ and self.ui.clients_comboBox.model().items[
            index].typeInfo() != _catagory_:
            self.pipeline_window.settings.client = self.ui.clients_comboBox.currentText()

        else:
            self.pipeline_window.settings.client = None

        self.populate_projects()




    def set_root_path(self):
        path = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory"))
        if os.path.isdir(path):
            self.ui.rootDir_lineEdit.setText(path)
            self.pipeline_window.settings.rootDir = path

    def set_icons(self):
        self.ui.create_project_pushButton.setIcon(QtGui.QIcon(new_icon))
        self.ui.create_project_pushButton.setIconSize(QtCore.QSize(20,20))
        self.ui.load_project_pushButton.setIcon(QtGui.QIcon(load_icon))
        self.ui.load_project_pushButton.setIconSize(QtCore.QSize(20,20))        
        self.ui.unload_project_pushButton.setIcon(QtGui.QIcon(unload_icon))
        self.ui.unload_project_pushButton.setIconSize(QtCore.QSize(20,20))            
        self.ui.close_pushButton.setIcon(QtGui.QIcon(no_icon))
        self.ui.close_pushButton.setIconSize(QtCore.QSize(20,20))    

    def create_project(self):
        self.create_edit_project()
    
    def edit_project(self):
        widget = self.sender()
        index = self.ui.projects_tableWidget.indexAt(widget.pos())
        wanted_project_key = str(self.ui.projects_tableWidget.item(index.row(),4).text())
        
        projects = self.pipeline_window.settings.projects        
        path = os.path.join(projects[wanted_project_key][0],"project.json")        
        self.create_edit_project(project_file = pipeline_project(path = path, settings = self.pipeline_window.settings))       
        
    def create_edit_project(self, **kwargs):
        project_file = None
        for key in kwargs:
            if key == "project_file":
                project_file = kwargs[key]        
        
        
        global create_edit_projectsWindow
        try:
            create_edit_projectsWindow.close()
        except:
            pass

        create_edit_projectsWindow=pipeLine_create_edit_project_UI(parent=self,projects_window = self,project_file = project_file)
        create_edit_projectsWindow.show()
        
    def relink_project(self):
        widget = self.sender()
        index = self.ui.projects_tableWidget.indexAt(widget.pos())
        wanted_project_key = str(self.ui.projects_tableWidget.item(index.row(),4).text())
        
        path = QtGui.QFileDialog.getOpenFileName(self, "Select *.json file", filter = "pipe files (*.json)")
        if os.path.isfile(path[0]):
            
            project_path = os.path.dirname(str(path[0])) 
            project_file = data.jsonDict(path=str(path[0]))
            project_name = project_file.read("project_name")["project_name"] 
            project_key = project_file.read("project_key")["project_key"] 

            if wanted_project_key == project_key:
                
                projects = self.pipeline_window.settings.projects
                edited_projects = data.edit_key(dict = projects,key = project_key,value = [project_path, "ONLINE",project_name])

                if edited_projects is not None:
                    self.pipeline_window.settings.projects = projects
                    self.updateProjectsTable()
                    self.setColumnWidth_projectsTable()
            else:
                dlg.massage("critical", "Sorry", "The selected *.json file dose not match the selected project" )
        else:
            dlg.massage("critical", "Sorry", "No file selected" )
        
    def unload_project(self):
        row = self.ui.projects_tableWidget.currentRow()
        if row != -1:
            project_key = str(self.ui.projects_tableWidget.item(row,4).text())
            projects = self.pipeline_window.settings.projects
            del projects[project_key]
            
            if project_key == self.pipeline_window.settings.current_project:
                #self.pipeline_window.settings.current_project = None
                self.pipeline_window.update_current_open_project(None)
            
            self.pipeline_window.settings.projects = projects
            self.updateProjectsTable()
            self.setColumnWidth_projectsTable()

    def load_project(self):
        path = QtGui.QFileDialog.getOpenFileName(self, "Select *.json file", filter = "pipe files (*.json)")
        if path[0]:
            project_path = os.path.dirname(str(path[0]))        
            project_file = data.jsonDict(path=str(path[0]))
            project_name = project_file.read("project_name")["project_name"]
            project_key = project_file.read("project_key")["project_key"]
            
            self.add_project(project_name = project_name, project_path = project_path, project_key = project_key)

    def add_project(self,project_name = None,project_path = None, project_key = None):
        
        projects = self.pipeline_window.settings.projects    

         
        projects[project_key] = [project_path, "ONLINE", project_name]
        self.pipeline_window.settings.projects = projects

        
        self.updateProjectsTable()
        return True        

    

    def set_project_button(self):
            
        widget = self.sender()
        index = self.ui.projects_tableWidget.indexAt(widget.pos())
        project_key = self.ui.projects_tableWidget.item(index.row(),4).text()

        self.set_project(project_key = project_key)
        
    def set_project(self,project_key = None):
        import pymel.core as pm
        import maya.mel as mel
        if project_key:
            projects = self.pipeline_window.settings.projects      
            project_path = projects[project_key][0]
            project_Name = projects[project_key][2]

            if self.pipeline_window.update_current_open_project(project_key,from_projects_manager=True):
                
                #if self.pipeline_window.settings.current_project:
                    
                pm.workspace.open(project_path)
                pm.workspace.chdir(project_path)

                raw_project_path = project_path.replace("\\", "\\\\")
                melCmd = "setProject \""+ raw_project_path +"\";"
                try:
                    mel.eval(melCmd)
                except:
                    pass
                                             
                self.pipeline_window.ui.projects_pushButton.setText(project_Name)                
                self.updateProjectsTable()
                
                log.info ( "project changed to: %s"%project_Name)                
            
            else:
                log.info ( "Cannot set project") 
                
       
    def updateProjectsTable(self):
        self.ui.projects_tableWidget.clearContents()
        
        projects = self.pipeline_window.settings.projects
        
  
        self.ui.projects_tableWidget.setRowCount(len(projects))
        
        active_color = QtGui.QColor()
        active_color.setNamedColor("green")
        
        for index, key in enumerate(projects):
            
            project_status = projects[key][1]
            active_project = True if self.pipeline_window.settings.current_project == key and project_status == "ONLINE" else False

                      
            project_name = QtGui.QTableWidgetItem(projects[key][2])            
            project_name.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
            project_name.setFont(self.boldFont)
            if active_project:
                project_name.setBackground(active_color) 
                
            self.ui.projects_tableWidget.setItem(index,0,project_name)
        
            if project_status == "OFFLINE":
                
                offlineButtonItem = QtGui.QPushButton(project_status)
                offlineButtonItem.setIcon(QtGui.QIcon(offline_icon))
                offlineButtonItem.setIconSize(QtCore.QSize(20,20))
                
                self.ui.projects_tableWidget.setCellWidget(index,1,offlineButtonItem)
                offlineButtonItem.clicked.connect(self.relink_project)
                
            else:   
                status = QtGui.QTableWidgetItem(project_status)
                status.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
                if active_project:
                    status.setBackground(active_color) 
                self.ui.projects_tableWidget.setItem(index,1,status)            
            
            if project_status == "ONLINE":
                
                editButtonItem = QtGui.QPushButton( "Edit")
                editButtonItem.setIcon(QtGui.QIcon(edit_icon))
                editButtonItem.setIconSize(QtCore.QSize(20,20))
                self.ui.projects_tableWidget.setCellWidget(index,2,editButtonItem)
                editButtonItem.clicked.connect(self.edit_project)
                if not active_project:
                    editButtonItem.setEnabled(False)
                if self.pipeline_window.settings.role > 0:
                    editButtonItem.setEnabled(False)
                    
            '''
            if active_project:
                active = QtGui.QTableWidgetItem("Active")
                active.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
                active.setFont(self.boldFont)
                active.setBackground(active_color) 
                self.ui.projects_tableWidget.setItem(index,3,active)   
            else:
            '''
            if project_status == "ONLINE":
                setButtonItem = QtGui.QPushButton("Set Project")                  
                setButtonItem.clicked.connect(self.set_project_button)                         
                setButtonItem.setIcon(QtGui.QIcon(set_icon))
                setButtonItem.setIconSize(QtCore.QSize(20,20))        
                self.ui.projects_tableWidget.setCellWidget(index,3,setButtonItem)                        
      
            key = QtGui.QTableWidgetItem(key)
            key.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
            self.ui.projects_tableWidget.setItem(index,4,key)


    def init_projectssTable(self):        
        self.ui.projects_tableWidget.horizontalHeader().setVisible(False)
        self.ui.projects_tableWidget.verticalHeader().setVisible(False)
        self.ui.projects_tableWidget.setWordWrap(False)
        self.ui.projects_tableWidget.setColumnCount(5)
        self.ui.projects_tableWidget.setRowCount(1)
        self.ui.projects_tableWidget.setHorizontalHeaderLabels(["Name","Status","Edit","Set"])
        self.ui.projects_tableWidget.verticalHeader().setDefaultSectionSize(30);
        self.ui.projects_tableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.ui.projects_tableWidget.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.ui.projects_tableWidget.setFocusPolicy(QtCore.Qt.NoFocus)
    
    def setColumnWidth_projectsTable(self):        

        self.ui.projects_tableWidget.horizontalHeader().setResizeMode(0, QtGui.QHeaderView.Fixed )
        self.ui.projects_tableWidget.horizontalHeader().resizeSection(0,200)
        self.ui.projects_tableWidget.horizontalHeader().setResizeMode(1, QtGui.QHeaderView.ResizeToContents )
        self.ui.projects_tableWidget.horizontalHeader().resizeSection(1,200)
        self.ui.projects_tableWidget.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.ui.projects_tableWidget.horizontalHeader().setResizeMode(2, QtGui.QHeaderView.Fixed )        
        self.ui.projects_tableWidget.horizontalHeader().resizeSection(2,100)
        self.ui.projects_tableWidget.horizontalHeader().setResizeMode(3, QtGui.QHeaderView.Fixed )
        self.ui.projects_tableWidget.horizontalHeader().resizeSection(3,100)
        self.ui.projects_tableWidget.horizontalHeader().setResizeMode(4, QtGui.QHeaderView.Fixed )
        self.ui.projects_tableWidget.horizontalHeader().resizeSection(4,0)

    def close_window(self):
        self.close()

class pipeLine_create_edit_project_UI(QtGui.QMainWindow):
    def __init__(self, parent=None, projects_window = None, **kwargs):
         
        super(pipeLine_create_edit_project_UI, self).__init__(parent)      
        self.setWindowFlags(QtCore.Qt.Tool)                
        form_class, base_class = create_edit_project_form_class, create_edit_project_base_class
               
        self.ui = form_class()
        self.ui.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("Create Project")        
        self.projects_window = projects_window
        
        self.setMaximumHeight(500)
        
        self.project_file_name = 'project.json'
        self.project_name = "My_Project"

        self.path = None
        self.project_file = None

        for key in kwargs:
            if key == "project_file":
                self.project_file = kwargs[key]
                 
        #connect ui
        self.roles = ["admin","guest","rigger","animator"]            
        self.init_usersTable()       
        self.ui.set_project_path_pushButton.clicked.connect(self.set_project_path)
        
        if not self.project_file:
            self.ui.create_edit_project_pushButton.setText("Create")
            self.ui.create_edit_project_pushButton.clicked.connect(self.create_project)
            self.init_new_project()
        else:
            self.ui.create_edit_project_pushButton.setText("Edit")
            self.ui.create_edit_project_pushButton.clicked.connect(self.edit_project)    
            self.ui.static_widget.setHidden(True)        
            self.init_edit_project()
            
            self.ui.set_project_path_pushButton.setEnabled(False)
            self.ui.padding_spinBox.setEnabled(False)
            self.ui.project_name_lineEdit.setEnabled(False)
            self.ui.project_path_lineEdit.setEnabled(False)

            self.ui.playblast_sister_dir_checkBox.setChecked(self.project_file.playblast_outside)
            
           
        self.ui.cancel_pushButton.clicked.connect(self.cancel)                
        

        self.playblast_help_button()
        
        
        self.boldFont=QtGui.QFont()
        self.boldFont.setBold(True)  
        self.set_icons()
        

        self.updateUsersTable()

            
    def playblast_help_button(self):
        
        self.playblast_help_label = QtGui.QLabel()
        sizepolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed)
        sizepolicy.setHeightForWidth(self.playblast_help_label.sizePolicy().hasHeightForWidth())
        self.playblast_help_label.setSizePolicy(sizepolicy)
        self.playblast_help_label.setMinimumSize(QtCore.QSize(30, 30)) 
       
        self.ui.horizontalLayout_3.addWidget(self.playblast_help_label)
        self.ui.horizontalLayout_3.setContentsMargins(0,0,0,0)               
                       
        layout = QtGui.QHBoxLayout(self.playblast_help_label)
        layout.setContentsMargins(0,0,0,0)
        
        
        self.playblast_help = alpha_button(self,help_icon)  
        self.playblast_help.set_pixmap(help_icon)      
        sizepolicy2 = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed)
        sizepolicy2.setHeightForWidth(self.playblast_help.sizePolicy().hasHeightForWidth())
        self.playblast_help.setSizePolicy(sizepolicy2)
        self.playblast_help.setMinimumSize(QtCore.QSize(30, 30))          
        self.playblast_help.button.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.playblast_help)        
        self.connect(self.playblast_help, QtCore.SIGNAL('clicked()'), self.playblast_help_popup)
        
        self.spacer = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.ui.horizontalLayout_3.addItem(self.spacer)
        

    def playblast_help_popup(self):
        dlg.massage("massage","Playblasts","Playblasts can consume a lot of disk space,\nWhen working on a project on a shared disk or cloud, This can slow the syncing proccess.\nHave more control by keeping them in a sister directory.")

    def set_icons(self):
        self.ui.create_edit_project_pushButton.setIcon(QtGui.QIcon(yes_icon))
        self.ui.create_edit_project_pushButton.setIconSize(QtCore.QSize(20,20))

        self.ui.set_project_path_pushButton.setIcon(QtGui.QIcon(search_icon))
        self.ui.set_project_path_pushButton.setIconSize(QtCore.QSize(20,20))
               
        self.ui.cancel_pushButton.setIcon(QtGui.QIcon(no_icon))
        self.ui.cancel_pushButton.setIconSize(QtCore.QSize(20,20))

    def init_new_project(self):
        self.ui.project_name_lineEdit.setText(self.project_name)
        self.users = {}
        self.users["Admin"] = ["1234", self.roles[0]] 

    def init_edit_project(self):
        self.ui.project_name_lineEdit.setText(self.project_file.project_name)
        if self.project_file.project_users != None:        
            self.users = self.project_file.project_users  
            self.ui.users_checkBox.setChecked(True)
        else:
            self.users = {}
            self.users["Admin"] = ["1234", self.roles[0]]  
                       
        self.ui.padding_spinBox.setValue(self.project_file.project_padding)
        
        type = "Maya Ascii (*.ma)"
                
        if self.project_file.project_file_type == "mb":
            type = "Maya Binary (*.mb)"
        
        fps = "PAL (25fps)"
            
        if self.project_file.project_fps == 24: 
            fps = "Film (24fps)"            
        if self.project_file.project_fps == 30: 
            fps =  "NTSC (30fps)"
                      
        
        i = self.ui.file_type_comboBox.findText(type, QtCore.Qt.MatchFixedString)
        if i >= 0:
         self.ui.file_type_comboBox.setCurrentIndex(i)

        i = self.ui.fps_comboBox.findText(fps, QtCore.Qt.MatchFixedString)
        if i >= 0:
         self.ui.fps_comboBox.setCurrentIndex(i)
        

    
    def set_project_path(self):
        path = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.ui.project_path_lineEdit.setText(os.path.join(path,str(self.ui.project_name_lineEdit.text())))



    def init_usersTable(self):        
        self.ui.users_tableWidget.horizontalHeader().setVisible(True)
        self.ui.users_tableWidget.verticalHeader().setVisible(False)
        self.ui.users_tableWidget.setWordWrap(False)
        self.ui.users_tableWidget.setColumnCount(4)
        self.ui.users_tableWidget.setRowCount(1)
        self.ui.users_tableWidget.setHorizontalHeaderLabels(["Username","password","Role","Action"])
        self.ui.users_tableWidget.verticalHeader().setDefaultSectionSize(30);
        self.ui.users_tableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.ui.users_tableWidget.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.ui.users_tableWidget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ui.users_tableWidget.horizontalHeader().setResizeMode(0, QtGui.QHeaderView.Stretch )
        self.ui.users_tableWidget.horizontalHeader().resizeSection(0,200)
        self.ui.users_tableWidget.horizontalHeader().setResizeMode(1, QtGui.QHeaderView.Stretch )
        self.ui.users_tableWidget.horizontalHeader().resizeSection(1,200)
        self.ui.users_tableWidget.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)     
        self.ui.users_tableWidget.horizontalHeader().resizeSection(2,200)
        self.ui.users_tableWidget.horizontalHeader().setResizeMode(3, QtGui.QHeaderView.Fixed )
        self.ui.users_tableWidget.horizontalHeader().resizeSection(3,50)



    def updateUsersTable(self):
        self.ui.users_tableWidget.clearContents()
        self.ui.users_tableWidget.setRowCount(len(self.users)+1)

        admin_username = QtGui.QTableWidgetItem("Admin")                       
        admin_username.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
        admin_username.setFont(self.boldFont)
        self.ui.users_tableWidget.setItem(0,0,admin_username)

        admin_password = QtGui.QTableWidgetItem(self.users["Admin"][0])            
        self.ui.users_tableWidget.setItem(0,1,admin_password)

        role = QtGui.QTableWidgetItem("admin")                       
        role.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
        role.setFont(self.boldFont)
        self.ui.users_tableWidget.setItem(0,2,role)  
        
        users = self.users
        del users["Admin"]

        if users:
            for index, key in enumerate(users):
                            
                username = QtGui.QTableWidgetItem(key)                       
                username.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
                username.setFont(self.boldFont)
                self.ui.users_tableWidget.setItem(index+1,0,username)
                
                password = QtGui.QTableWidgetItem(users[key][0])            
                self.ui.users_tableWidget.setItem(index+1,1,password)
                
                role = users[key][1]            
                
                roles_combo = QtGui.QComboBox()
                roles_combo.setEditable(False)
                roles_combo.addItems(self.roles)
                
                self.ui.users_tableWidget.setCellWidget(index+1,2,roles_combo)            
                i = roles_combo.findText(role, QtCore.Qt.MatchFixedString)
                if i >= 0:
                    roles_combo.setCurrentIndex(i)
      
                deleteButtonItem = QtGui.QPushButton("")
                deleteButtonItem.setIcon(QtGui.QIcon(no_icon))
                deleteButtonItem.setIconSize(QtCore.QSize(20,20))            
                self.ui.users_tableWidget.setCellWidget(index+1,3,deleteButtonItem)
                deleteButtonItem.clicked.connect(self.remove_user)
        

        empty_item1 = QtGui.QTableWidgetItem("")
        empty_item1.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
        empty_item2 = QtGui.QTableWidgetItem("")
        empty_item2.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
        empty_item3 = QtGui.QTableWidgetItem("")
        empty_item3.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )        
        self.ui.users_tableWidget.setItem(len(self.users)+1,0,empty_item1)
        self.ui.users_tableWidget.setItem(len(self.users)+1,1,empty_item2)
        self.ui.users_tableWidget.setItem(len(self.users)+1,2,empty_item3)
        
        newButtonItem = QtGui.QPushButton("")
        newButtonItem.setIcon(QtGui.QIcon(add_icon))
        newButtonItem.setIconSize(QtCore.QSize(20,20))            
        self.ui.users_tableWidget.setCellWidget(len(self.users)+1,3,newButtonItem)
        newButtonItem.clicked.connect(self.add_user)

    def add_user(self):
        self.set_users_dict()
        
        username, ok = QtGui.QInputDialog.getText(self, 'New User', 'Enter User name:')
        
        if ok:        
            if username not in self.users and username != "":
                self.users[username] = ["",self.roles[1]]       
                self.updateUsersTable()
            else:
                print "User name exists..."

    def remove_user(self):
        widget = self.sender()
        index = self.ui.users_tableWidget.indexAt(widget.pos())
        username = str(self.ui.users_tableWidget.item(index.row(),0).text())
     
        self.set_users_dict()

        del self.users[username]     
        self.updateUsersTable()



    def set_users_dict(self):
        users = {}
        rows = self.ui.users_tableWidget.rowCount() - 1
        for row in range(0,rows):
           if row == 0:
               users[self.ui.users_tableWidget.item(row,0).text()] = [self.ui.users_tableWidget.item(row,1).text() , self.ui.users_tableWidget.item(row,2).text() ] 
  
           else:
               users[self.ui.users_tableWidget.item(row,0).text()] = [self.ui.users_tableWidget.item(row,1).text() , self.ui.users_tableWidget.cellWidget(row,2).currentText()   ] 
        
        self.users = users
        
            

    def create_project(self):
        if self.ui.users_checkBox.isChecked() == True:
            self.set_users_dict()
            self.projects_window.pipeline_window.settings.user = ["Admin", self.users["Admin"][0]] 
            self.projects_window.pipeline_window.ui.users_pushButton.setText("%s : %s"%("Admin","admin")) 
        else:
            self.users = None
   
        project_path = str(self.ui.project_path_lineEdit.text())        
        project_name = str(self.ui.project_name_lineEdit.text())


        padding = self.ui.padding_spinBox.value()
        
        if self.ui.file_type_comboBox.currentText() == "Maya Ascii (*.ma)":
            file_type = "ma"
        if self.ui.file_type_comboBox.currentText() == "Maya Binary (*.mb)":
            file_type = "mb" 
                
        if self.ui.fps_comboBox.currentText() == "PAL (25fps)":
            fps = 25
        if self.ui.fps_comboBox.currentText() == "Film (24fps)":
            fps = 24            
        if self.ui.fps_comboBox.currentText() == "NTSC (30fps)":
            fps = 30
        
        playblast_outside = False 
        if self.ui.playblast_sister_dir_checkBox.isChecked():
            playblast_outside = True    
            
        self.project_file = pipeline_project().create(project_path, name = project_name, padding = padding, file_type = file_type, fps = fps, users = self.users, playblast_outside = playblast_outside)        
        self.projects_window.add_project(project_name = project_name, project_path = project_path, project_key = self.project_file.project_key)        
        
            
        self.projects_window.set_project(project_key = self.project_file.project_key)
        self.close()


    def edit_project(self):
        if self.ui.users_checkBox.isChecked() == True:
            self.set_users_dict()
            self.projects_window.pipeline_window.settings.user = ["Admin", self.users["Admin"][0]]  
            
            self.projects_window.pipeline_window.ui.users_pushButton.setText("%s : %s"%("Admin","admin")) 
        else:
            self.users = None

        
        
        if self.ui.file_type_comboBox.currentText() == "Maya Ascii (*.ma)":
            file_type = "ma"
        if self.ui.file_type_comboBox.currentText() == "Maya Binary (*.mb)":
            file_type = "mb" 
                
        if self.ui.fps_comboBox.currentText() == "PAL (25fps)":
            fps = 25
        if self.ui.fps_comboBox.currentText() == "Film (24fps)":
            fps = 24            
        if self.ui.fps_comboBox.currentText() == "NTSC (30fps)":
            fps = 30

        self.project_file.project_users = self.users
        self.project_file.project_file_type = file_type
        self.project_file.project_fps = fps
        
        playblast_outside = False 
        if self.ui.playblast_sister_dir_checkBox.isChecked():
            playblast_outside = True 
            
        self.project_file.playblast_outside = playblast_outside
        
        self.projects_window.set_project(project_key = self.project_file.project_key)
        self.close()
             
    def cancel(self):
        self.close()


        
def show():

    try:
        print "delete model"
        del treeModel

    except:
        print "cant delete model"
    
    #about = dlg.test2()#(None,"About",
    #about.exec_() 
    #return
    
    global UiWindow
    UiWindow=pipeLineUI(parent=maya_main_window())
    UiWindow.run()
    
    return UiWindow
