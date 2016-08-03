
from PySide import QtXml, QtGui, QtCore
import os
import time

import data_model as dtm
reload(dtm)

#import modules.data as data
#reload(data)
import modules.files as files
reload(files)
import modules.jsonData as data
reload(data)
import modules.maya_warpper as maya
reload(maya)

global _node_
global _root_
global  _stage_
global _asset_
global _folder_
global _dummy_
global _new_
global _catagory_
global _assets_
global _animation_
global _admin_
_admin_ = "admin"
_assets_ = "asset"
_animation_ = "animation"
_catagory_ = "catagory"
_new_ = "new"
_node_ = "node"
_root_ = "root"
_stage_ = "stage"
_asset_ = "asset"
_folder_ = "folder" 
_dummy_ = "dummy"
_version_ = "version"


def set_icons():
    localIconPath = os.path.join(os.path.dirname(__file__), 'icons')
    if not os.path.exists(localIconPath):
        return 
        
    global folder_icon
    global cube_icon
    global add_cube_icon
    global dummy_icon
    
    global cube_icon_full
    global add_icon
    global large_image_icon
    global client_icon
    global large_image_icon_dark
    global comment_icon
    global comment_full_icon
    global new_icon
    global creation_icon

    creation_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "creation"))
    new_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "new"))
    comment_icon = os.path.join(localIconPath, "%s.svg" % "comment")
    comment_full_icon = os.path.join(localIconPath, "%s.svg" % "comment_full")
    client_icon = os.path.join(localIconPath, "%s.svg" % "client")
    folder_icon = os.path.join(localIconPath, "%s.svg"%"folder")
    cube_icon = os.path.join(localIconPath, "%s.svg"%"cube") 
    add_cube_icon = os.path.join(localIconPath, "%s.svg"%"add_cube")     
    cube_icon_full = os.path.join(localIconPath, "%s.svg"%"cube-fill") 
    add_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"add"))
    large_image_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"large_image"))
    large_image_icon_dark = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "large_image_dark"))
    dummy_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"braces"))



set_icons()

class Metadata_file():
    
    def __init__(self,**kwargs):

        self.data_file = None
        self.data_file_path = None

        for key in kwargs:
            if key == "path":
                self.data_file_path = os.path.join(kwargs[key])
                
        if self.data_file_path:        
            self.set_data_file(self.data_file_path)

    def set_data_file(self,path):
        if os.path.isfile(path):
            self.data_file = data.jsonDict(path = path)

            return True
        else:
            pass


class Node(QtCore.QObject, object):
    
    def __init__(self, name,  parent=None, **kwargs):
        super(Node, self).__init__()
        
        self._name = name
        self._children = []
        self._parent = parent
        self.expendedState = False
        self._resource = folder_icon
        self._id = data.id_generator()
        self._virtual = False
        self._deathrow = False

        if parent is not None:
            parent.addChild(self)


    def attrs(self):

        classes = self.__class__.__mro__

        kv = {}

        for cls in classes:
            for k, v in cls.__dict__.iteritems():
                if isinstance(v, property):
                    #print "Property:", k.rstrip("_"), "\n\tValue:", v.fget(self)
                    kv[k] = v.fget(self)

        return kv

    def asXml(self):
        
        doc = QtXml.QDomDocument()
        

        node = doc.createElement(self.typeInfo())
        doc.appendChild(node)

        attrs = self.attrs().iteritems()
        
        for k, v in attrs:
            node.setAttribute(k, v) 
  
       
        for i in self._children:
            i._recurseXml(doc, node)

        return doc.toString(indent=4)


    def _recurseXml(self, doc, parent):
        node = doc.createElement(self.typeInfo())
        parent.appendChild(node)

        attrs = self.attrs().iteritems()
        
        for k, v in attrs:
            node.setAttribute(k, v)

        for i in self._children:
            i._recurseXml(doc, node)

    
    def typeInfo(self):
        return _node_

    def addChild(self, child):
        self._children.append(child)
        child._parent = self

    def insertChild(self, position, child):
        
        if position < 0 or position > len(self._children):
            return False
        
        self._children.insert(position, child)
        child._parent = self
        return True

    def removeChild(self, position):
        
        if position < 0 or position > len(self._children):
            return False
        
        if self._children != []:
            child = self._children.pop(position)
            #child.delete()
            child._parent = None

            return True
        else:
            return False
            
    @property
    def name(self):
        return self._name
                
    @name.setter
    def name(self, value):
        self._name = value

    def child(self, row):
        return self._children[row]

    def childCount(self):
        return len(self._children)

    def parent(self):
        return self._parent
    
    def row(self):
        if self._parent is not None:
            return self._parent._children.index(self)


    def log(self, tabLevel=-1):

        output     = ""
        tabLevel += 1
        
        for i in range(tabLevel):
            output += "\t"
        
        output += "|------" + self._name + "\n"
        
        for child in self._children:
            output += child.log(tabLevel)
        
        tabLevel -= 1
        output += "\n"
        
        return output
      

    def data(self, column):
        
        if   column is 0: return self.name
        elif column is 1: return self.typeInfo()#len(self._children)
    
    def setData(self, column, value):
        #print value
        if   column is 0: pass#self.name = value
        elif column is 1: pass

    @property
    def resource(self):
        return self._resource


    @resource.setter
    def resource(self, icon):
        self._resource = icon

    def delete(self):

        self.delete_me()
        
        for child in self._children:
            
            child.delete()

    def delete_me(self):

        if hasattr(self, '_path'):
            if self._path:
                files.delete(self._path)

        print "***DELETE ALL IN" + self._name + "\n"

    def commit(self):
        self.commit_me()
        if self._deathrow:
            self.delete()

            return False

        for child in self._children:
            child.commit()

    def commit_me(self):
        create = False
        if self.__class__.__name__ == "FolderNode":
            create = True
        elif self.__class__.__name__ == "AssetNode":
             create = True
        elif self.__class__.__name__ == "StageNode":
            create = True

        if create:
            create_mathod = getattr(self, "create", None)
            #print "calling create method:"
            if callable(create_mathod):
                if self._virtual:
                    self.create(path=self._path)
                    #print "creating! --> ", self._path, "<--"
                else:
                    pass
                    #print "already real --> ", self._path, "<--"
                return

    def deathrow(self):
        self.deathrow_me()

        for child in self._children:
            child.deathrow()        #print "not a folder"

    def deathrow_me(self):
        self._deathrow = True


    @property
    def expendedState(self):
        return self._expendedState
    @expendedState.setter
    def expendedState(self, state):    
        self._expendedState = state

    @property
    def id(self):
        return self._id


class RootNode(Node):#, Metadata_file):
    
    def __init__(self, name, parent=None, **kwargs):


        Node.__init__(self, name, parent, **kwargs)


        self.name = name
        self.resource = folder_icon
        self._section = None

        #Metadata_file.__init__(self, **kwargs)


        self.data_file = None
        self.data_file_path = None

        for key in kwargs:
            if key == "path":
                self._path = kwargs[key]
                self.data_file_path = os.path.join(kwargs[key],"%s.%s"%(self.name,"json"))
            if key == "virtual":
                self._virtual = kwargs[key]
            if key == "section":
                self._section = kwargs[key]

        if self.data_file_path:
            self.set_data_file(self.data_file_path)



    def set_data_file(self, path):
        if os.path.isfile(path):
            self.data_file = data.jsonDict(path=path)

            return True
        else:
            pass

            
    def create(self, path = None):
        if files.create_directory(path):  
            self.path = path          
            return self
        else:
            return False

    @property
    def sTypeInfo(self):
        if self.data_file:
            return self.data_file["typeInfo"]

    @property
    def path(self):
        return self._path
                
    @path.setter
    def path(self, path):
        self._path = path  
    
    def typeInfo(self):
        return _root_


    @property
    def section(self):
        return self._section


    def model_tree(self):
        
        '''
        returns a flat list of all descending childs from the given index
        '''     
        def rec(path, parent):
            if path:
                folders = files.list_dir_folders(path)
                if folders:
                    for dir in folders: 
                        p  = os.path.join(path,dir)
 
                        if assetDir( p ):
                            node = AssetNode(os.path.split(p)[1], path=p, parent = parent, section = self.section)
                            rec(p, node)
                        elif stageDir( p ):
                            node = StageNode(os.path.split(p)[1],  path=p, parent = parent, section = self.section)
                        else:                         
                            node = FolderNode(os.path.split(p)[1], path=p, parent = parent, section = self.section)
                            rec(p, node)
                else:
                    pass

        rec(self.path, self)




class FolderNode(RootNode):
    
    def __init__(self, name,  parent=None, **kwargs):
        super(FolderNode, self).__init__(name, parent, **kwargs)

        self.resource = folder_icon if not self._virtual else  creation_icon
        
    def typeInfo(self):
        return _folder_




class AssetNode(RootNode):
    
    def __init__(self, name,  parent=None, **kwargs):
        super(AssetNode, self).__init__(name, parent, **kwargs)

        self.resource = cube_icon_full if not self._virtual else  creation_icon

    def create(self, path = None):
        super(AssetNode, self).create(path)
        #if node:
        dict = {}
        dict["typeInfo"] = _asset_
        dict[_asset_] = self.name

        path = os.path.join(path,"%s.%s"%(self.name,"json"))

        self.data_file = data.jsonDict().create(path, dict)
        self.data_file = self.data_file.read()
        return self

    @property
    def stages(self):
        stages = []

        for dir in files.list_dir_folders(self._path):

            if stageDir(os.path.join(self._path, dir)):
                stages.append(dir)

        return stages
        
    def typeInfo(self):
        return _asset_


        

# class StageNode(RootNode):
#
#     def __init__(self, name, stage = None, parent=None, **kwargs):
#         super(StageNode, self).__init__(name, parent, **kwargs)
#
#         self._stage = stage
#
#     def create(self, stage = None, path = None):
#         node = super(StageNode, self).create(path)
#         if node:
#
#             dict = {}
#             dict["typeInfo"] = "_stage_"
#             dict["stage"] = stage
#
#             self._stage = stage
#
#             path = os.path.join(path,"%s.%s"%("stage","json"))
#
#             self.data_file = data.jsonDict().create(path, dict)
#             self.data_file = self.data_file.read()
#             return node
#
#     @property
#     def stage(self):
#         return self._stage
#
#     @stage.setter
#     def stage(self, value):
#         self._stage = value
#
#     def typeInfo(self):
#         return _stage_
#
#
#     def resource(self):
#         return large_image_icon


class VersionNode(Node):

    def __init__(self, name,path = None,  number = None, author = None, date = None, note = None, stage = None, parent=None):
        super(VersionNode, self).__init__(name, parent)

        self._path = path
        self._number = number
        self._date = date
        self._note = note
        self._author = author
        self._stage = stage

        self.resource = large_image_icon_dark

        if os.path.isfile(self.thumbnail_file):
            self.resource = self.thumbnail_file

    @property
    def thumbnail_file(self):
        filename = files.file_name(self._path)
        filename = files.file_name_no_extension(filename)
        path = os.path.join(self._stage.tumbnails_path, "%s.%s" % (filename, "png"))
        return path

    def snapshot(self):
        files.assure_path_exists(self.thumbnail_file)
        snapshot = maya.snapshot(path=self.thumbnail_file, width=96, height=96)
        self.resource = snapshot
        return snapshot

    @property
    def stage(self):
        return self._stage

    @property
    def number(self):
        return self._number if self._number else "n/a"

    @property
    def date(self):
        return self._date if self._date else "n/a"

    @property
    def author(self):
        return self._author if self._author else "n/a"

    @property
    def note(self):
        return self._note if self._note else "n/a"

    @note.setter
    def note(self, note):
        self._note = note

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path):
        self._path = path

    @property
    def fullName(self):
        return "%s > %s : %s %s"%(self.stage.parent().name, self.stage.name, "Version",self.number)

    def typeInfo(self):
        return _version_



    def load(self):
        maya.open_scene(self.path)

    def delete_me(self):
        files.delete(self.path)
        self.stage.removeVersionData(self.number)

    @property
    def note_decoration(self):
        if self._note:
            return comment_full_icon
        else:
            return None
            #return comment_icon



class CatagoryNode(Node):

    def __init__(self, name, parent=None):
        super(CatagoryNode, self).__init__(name, parent)

        self.resource = dummy_icon

    def typeInfo(self):
        return _catagory_



class DummyNode(Node):

    def __init__(self, name, parent=None):
        super(DummyNode, self).__init__(name, parent)

        self.resource = dummy_icon

    def typeInfo(self):
        return _dummy_

class LevelsNode(Node):

    def __init__(self, name, parent=None):
        super(LevelsNode, self).__init__(name, parent)

        self.resource = dummy_icon
        self._levels = []
        for i in range(6):
            self._levels.append("")

    def setLevels(self, list):
        for index, item in enumerate(list):
            self._levels[index] = item

    def typeInfo(self):
        return _dummy_

class StagesNode(Node):

    def __init__(self, name, parent=None):
        super(StagesNode, self).__init__(name, parent)

        self.resource = dummy_icon
        self._levels = []
        for i in range(6):
            self._levels.append("")

    def setLevels(self, list):
        for index, item in enumerate(list):
            self._levels[index] = item

    def typeInfo(self):
        return _dummy_


class UserNode(Node):

    def __init__(self, name, password = None, role = None, parent=None):
        super(UserNode, self).__init__(name, parent)

        self.resource = dummy_icon
        self._password = password
        self._role = role

    def setLevels(self, list):
        for index, item in enumerate(list):
            self._levels[index] = item

    def typeInfo(self):
        return _dummy_

class ClientNode(Node):

    def __init__(self, name, path = None, parent=None):
        super(ClientNode, self).__init__(name, parent)
        self._path = path

        self.resource = client_icon

    @property
    def path(self):
        return self._path

    def typeInfo(self):
        return _dummy_




class AddNode(Node):
    def __init__(self, name, parent=None):
        super(AddNode, self).__init__(name, parent)

        self.resource = add_icon

    def typeInfo(self):
        return _new_


class NewNode(Node):

    def __init__(self, name,  parent=None):
        super(NewNode, self).__init__(name, parent)
        self.resource = add_icon

        # for key in kwargs:
        #     if key == "name_format":
        #         self._name_format = kwargs[key]
        #     if key == "section":
        #         self._section = kwargs[key]

    def typeInfo(self):
        return _new_


# class project(object):
#     def __init__(self, project_path):
#
#         stages = {}
#         stages["asset"] = ["model","rig","clip","shandeing","lightning"]
#         stages["animation"] = ["layout","Shot"]
#
#         levels = {}
#         levels["asset"] = ["type","asset","stage","ccc"]
#         levels["animation"] = ["Ep","Seq"]
#
#
#         self.project = {}
#         self.project["project_path"] = project_path
#
#
#         self.project["levels"] = levels
#         self.project["stages"] = stages
#
#         self.project["current_stage"] = None

#
# class Asset(Metadata_file):
#     def __init__(self,**kwargs):
#         Metadata_file.__init__(self, **kwargs)
#
#         self.project = None
#         for key in kwargs:
#             if key == "project":
#                 self.project = kwargs[key]
#
#
#         self.settings = None
#         for key in kwargs:
#             if key == "settings":
#                 self.settings = kwargs[key]
#
#
#
#     def create(self, path, name):
#         data = {}
#         data["typeInfo"] = "_asset_"
#
#         path = os.path.join(path,"%s.%s"%(name,"json"))
#
#         self.data_file = data.jsonDict().create(path, data)
#         self.data_file = self.data_file.read()
#
#         return self


class StageNode(RootNode):

    edited = QtCore.Signal()

    def __init__(self, name, parent=None, **kwargs):

        RootNode.__init__(self, name, parent, **kwargs)

        changed = QtCore.Signal()

        self.project = None
        for key in kwargs:
            if key == "project":
                self.project = kwargs[key]

        self.settings = None
        for key in kwargs:
            if key == "settings":
                self.settings = kwargs[key]

        self.pipelineUI = None

        self._name_format = 2
        for key in kwargs:
            if key == "pipelineUI":
                self.pipelineUI = kwargs[key]
                self.edited.connect(self.pipelineUI.updateVersionsTable)
            if key == "name_format":
                self._name_format = kwargs[key]
            #

        if self.data_file:
            self.stage_file = self.data_file.read()


        self.resource = new_icon if not self._virtual else  creation_icon

    def create(self,  path=None):
        super(StageNode, self).create(path)
        #if node:
        dict = {}
        dict["typeInfo"] = _stage_
        dict[_stage_] = self.name
        dict[_asset_] = self.parent().name
        dict["name_format"] = self._name_format
        self.name_format = self._name_format

        path = os.path.join(path, "%s.%s" % (self.name, "json"))

        self.data_file = data.jsonDict().create(path, dict)
        self.stage_file = self.data_file.read()

        return self

    @property
    def name_format(self):
        if self.stage_file:
            return self.stage_file["name_format"]

    @name_format.setter
    def name_format(self, value):
        self._name_format = value

    @property
    def stage(self):
        return self._stage

    @stage.setter
    def stage(self, value):
        self._stage = value

    def typeInfo(self):
        return _stage_


    def formatFileName(self):

        depth = self.name_format
        node = self.parent()
        levels = [self.name, node.name]

        for i in range(depth):
            node = node.parent()
            levels.append(node.name)


        return "_".join(reversed(levels))

    def padding(self, int):
        return files.set_padding(int, self.project.project_padding)

    def initialVersion(self):



        files.assure_folder_exists(self.versions_path)


        maya.new_scene()
        maya.set_fps(self.project.project_fps)
        maya.rewind()

        version_number = self.padding(1)

        file_name = "%s_%s.%s" % (self.formatFileName(), version_number, "ma")

        scene_path = maya.save_scene_as(path=self.versions_path, file_name=file_name)

        first_version = {}
        first_version["date"] = "%s %s %s" % (time.strftime("%d/%m"),"@", time.strftime("%H:%M"))
        first_version["author"] = "no user"# self.settings.user[0]
        first_version["note"] = None

        versions = {}
        versions[version_number] = first_version

        data = {}
        data["versions"] = versions
        self.data_file.edit(data)
        self.stage_file = self.data_file.read()

        self.edited.emit()
        #self.pipelineUI.updateVersionsTable()
        return
        '''
        self.project = project
        self.settings = settings
        
        versions_path = os.path.join(path, "versions")       
        masters_path = os.path.join(path, "masters")
        tumbnails_path =  os.path.join(path, "tumbnails") 
        
        for folder_path in [versions_path, masters_path, tumbnails_path]:
            files.create_directory(folder_path)

        if not create_from:
            maya.new_scene()
            maya.set_fps(self.project.project_fps)
            maya.rewind()
            
        elif create_from == "current_scene":
            pass    
            
        version_number = set_padding(1,self.project.project_padding)
        
        file_name = "%s_%s_%s.%s"%(asset_name,component_name,version_number,"ma")    
        
        scene_path = maya.save_scene_as(path = versions_path, file_name = file_name )       
        
        first_version = {}
        first_version["path"] = scene_path
        first_version["date_created"] = "%s %s"%(time.strftime("%d/%m/%Y"),time.strftime("%H:%M:%S"))
        first_version["author"] = self.settings.user[0]
        first_version["note"] = "No notes"
        
        versions = {}
        versions[version_number] = first_version
        
        masters = {}
                               
        component_data = {}
        component_data["component_name"] = component_name
        component_data["asset_name"] = asset_name
        component_data["catagory_name"] = catagory_name
        component_data["versions"] = versions
        component_data["masters"] = masters
        
        path = os.path.join(path,"%s.%s"%(component_name,"pipe"))           
        self.data_file = data.pickleDict().create(path, component_data)  
        self.data_file = self.data_file.read()
       
        return self
        '''

    def new_version(self):
        print "new v!"
        if self.project:
            if self.data_file:

                #versions = self.versions
                #versions = self.versions
                #if versions:
                #    last = versions[-1]
                #else:
                #    last = 0

                last_version = self._children[-1]

                version_number = set_padding(last_version.name+1, self.project.project_padding)

                file_name = "%s_%s.%s" % (self.formatFileName(), version_number, "ma")

                scene_path = maya.save_scene_as(path=self.versions_path, file_name=file_name)

                new_version = {}
                new_version["date"] = "%s %s %s" % (time.strftime("%d/%m"),"@", time.strftime("%H:%M"))
                new_version["author"] = "no user"  # self.settings.user[0]
                new_version["note"] = None

                versions = self.versions_
                versions[version_number] = new_version
                self.versions_ = versions



                self.edited.emit()


    def removeVersionData(self, padded_number):
        if padded_number in self.stage_file["versions"]:
            edit = self.stage_file["versions"]
            del edit[padded_number]
            self.data_file.edit(edit)
            self.stage_file = self.data_file.read()

        self.edited.emit()

    @property
    def stage_path(self):
        if self.data_file:
            
            return os.path.dirname(self.data_file_path)

        else:
            return None  

    @property
    def versions_path(self):
        if self.data_file:
            if self.settings:                             
                return os.path.join(self.stage_path, "versions") 
        else:
            return None  

    @property
    def masters_path(self):
        if self.data_file:
            if self.settings:                             
                return os.path.join(self.stage_path, "masters") 
        else:
            return None  
   

    @property
    def tumbnails_path(self):
        if self.data_file:
            if self.settings:                             
                return os.path.join(self.stage_path, "tumbnails") 
        else:
            return None  

    @property  
    def versions_(self):
        if self.stage_file:
            if "versions" in self.stage_file:
                return self.stage_file["versions"]
            else:
                return None
    
    @versions_.setter
    def versions_(self,versions):
       
        if self.data_file:
            data = {}
            data["versions"] = versions
            self.data_file.edit(data)
            self.stage_file = self.data_file.read()



    @property  
    def masters_(self):
        if self.data_file:
            return self.data_file["masters"]
    
    @masters_.setter
    def masters_(self,masters):
       
        if self.data_file:
            data = {}
            data["masters"] = masters
            self.data_file.edit(data)
            self.data_file = self.data_file.read()

    @property
    def component_name(self):
        if self.data_file:
            try:
                return self.data_file["component_name"]
            except:
                return None
        else:
            return None  
            
    @component_name.setter
    def component_name(self,name):
        if self.data_file:
            data = {}
            data["component_name"] = name
            self.data_file.edit(data)
            self.data_file = self.data_file.read()
        else:
            return None              

    @property
    def catagory_name(self):
        if self.data_file:
            return self.data_file["catagory_name"]
        else:
            return None  

    @catagory_name.setter
    def catagory_name(self,name):
        if self.data_file:
            data = {}
            data["catagory_name"] = name
            self.data_file.edit(data)
            self.data_file = self.data_file.read()
        else:
            return None 

    @property
    def asset_name(self):
        if self.data_file:
            return self.data_file["asset_name"]
        else:
            return None  



    @asset_name.setter
    def asset_name(self,name):
        if self.data_file:
            data = {}
            data["asset_name"] = name
            self.data_file.edit(data)
            self.data_file = self.data_file.read()
        else:
            return None  


    @property
    def component_public_state(self):
        if self.data_file:
            if "component_public_state" in self.data_file:
                return self.data_file["component_public_state"]
            else:
                # for legacy components, if no public state key exists, then the component is public
                return True
        else:
            return None  
            
    @component_public_state.setter
    def component_public_state(self,state):
        if self.data_file:
            data = {}
            data["component_public_state"] = state
            self.data_file.edit(data)
            self.data_file = self.data_file.read()
        else:
            return None 


    def path(self, type, version):
        if self.data_file:
            try:                
                version_data = self.data_file[type][version]
                return version_data["path"]
            except:
                return None
            
        else:
            return None  

    def author(self, type, version):
        
        if self.data_file:
            try:
                version_data = self.data_file[type][version]
                return version_data["author"]
            except:
                return None

        else:
            return None  


    def date_created(self, type, version):
        if self.data_file:
            try:
                version_data = self.data_file[type][version]
                return version_data["date_created"]
            except:
                return None
            
        else:
            return None  

    def note(self, type, version, **kwargs):
        if self.data_file:
            
            note = None
            for key in kwargs:
                if key == "note":
                    note = kwargs[key]
            
            if note:
                  
                data = self.data_file.read()
                data[type][version]["note"] = note    
                self.data_file.edit(data)
                self.data_file = self.data_file.read()
                
                return True
                                                
            else:
                
                try:
                    version_data = self.data_file[type][version]
                    return version_data["note"]
                except:
                    return None
            
        else:
            return None  
 
    def size(self, type, version):
        
        if self.data_file:            
            size_mb = files.file_size_mb(self.file_path(type, version))
            if size_mb:
                return ("{0:.1f}".format(size_mb))   
            else:
                # maybe this is the master file
                size_mb = files.file_size_mb(self.master)
                if size_mb:
                    return ("{0:.1f}".format(size_mb))     
        else:
            return None          
        
    def file_path(self, type, version):
        if self.data_file:
            if self.settings:
                if type == "masters" and version == str(set_padding(0,self.project.project_padding)):
                    return self.master
                    
                versions_path = os.path.join(self.settings.current_project_path, self.project.assets_dir,self.catagory_name,self.asset_name,self.component_name,type)
                version_file = "%s_%s_%s.%s"%(self.asset_name,self.component_name,version,"ma") if type == "versions" else "%s_%s_%s_%s.%s"%(self.asset_name,self.component_name,"MASTER",version,"ma")                
                return os.path.join(versions_path, version_file)  
        else:
            return None    
    
    @property
    def versions(self):
        if self.project:
            if self.data_file:
                versions = files.list_directory(self.versions_path,self.project.project_file_type)
                if versions:
                    versions_dict = files.dict_versions(versions,self.project.project_padding)
                    
                    version_nodes = []                 


                    for key in versions_dict:
                        skip = False
                        if self._children:
                            if isinstance(self._children, list):
                                for c in self._children:
                                    if c.path == versions_dict[key]:
                                        skip = True
                            else:
                                if self._children.path == versions_dict[key]:
                                    skip = True

                        if not skip:
                            padded_number = self.padding(key)
                            author = "n/a"
                            note = "n/a"
                            date = "n/a"
                            versions_data = self.versions_
                            if versions_data:

                                if padded_number in versions_data:
                                    thisVersion = versions_data[padded_number]
                                    if "author" in thisVersion:
                                        author = thisVersion["author"]
                                    if "note" in thisVersion:
                                        note = thisVersion["note"]
                                    if "date" in thisVersion:
                                        date = thisVersion["date"]

                        # version_nodes.append(VersionNode(key, path = versions_dict[key], author = author ,number = padded_number, date = date, note = note, stage = self))


                            VersionNode(key, parent=self, path=versions_dict[key], author=author,
                                    number=padded_number, date=date, note=note, stage=self)

                    return True

        self._newNode = NewNode("new...", parent = self)
        return None

    @property
    def versiosnModel(self):

        self.versions
        return dtm.PipelineVersionsModel2(self)


    @property
    def emptyVersions(self):
        #, name_format = self._name_format, section = self._section
        return [NewNode("new...", parent = self)]


    def last_version(self):
        if self.project:
            if self.data_file:
                if self.settings:

                    sorted_versions = self.versions
                    if sorted_versions:
                            return sorted_versions[-1]
                        

                

    
    
    def delete_version(self, type, version):
        if self.data_file:
            if self.settings:
                versions = self.versions_ if type == "versions" else self.masters_
                if not isinstance(version, list):

                    files.delete(self.file_path(type, version))
                                                                              
                    if version in versions:
                        del versions[version]
                    if type == "versions":    
                        self.versions_ = versions
                    else:
                        self.masters_ = versions 
                    
                else:
                    for v in version:
                        files.delete(self.file_path(type, v))
                        
                        if v in versions:
                            del versions[v]
                        
                    if type == "versions":    
                        self.versions_ = versions
                    else:
                        self.masters_ = versions 
                                        
                return True                                    
        else:
            return None   
    
    @property
    def masters(self):
        if self.project:
            if self.data_file:
                if self.settings:
                   
                    masters = files.list_directory(self.masters_path,self.project.project_file_type)
                    
                    if masters:
                        masters_dict = files.dict_versions(masters,self.project.project_padding)
                        
                        sorted_masters = files.sort_version(masters_dict)
                        return sorted_masters
                    else:
                        return None


    @property
    def master(self):
        if self.project:
            if self.data_file:
                if self.settings:
                    master_name = "%s_%s_%s.%s"%(self.asset_name,self.component_name,"MASTER","ma")
                    
                    master_file = os.path.join(self.stage_path,master_name) 
                    if os.path.isfile(master_file):
                        return master_file
        return None
        
    '''
    @property
    def thumbnail(self):
        if self.project:
            if self.data_file:
                if self.settings:
                    thumbnail_name = os.path.join(self.tumbnails_path,"%s.%s"%(self.component_name,"png"))
                    if os.path.isfile(thumbnail_name):
                        return QtGui.QPixmap(thumbnail_name)
        
        return large_image_icon
    '''
    @property
    def thumbnail(self):
        file = self.thumbnail_path
        if file:
            return QtGui.QPixmap(file)
        
        return large_image_icon

    @property
    def thumbnail_path(self):
        if self.project:
            if self.data_file:
                if self.settings:
                    thumbnail_name = os.path.join(self.tumbnails_path,"%s.%s"%(self.component_name,"png"))
                    if os.path.isfile(thumbnail_name):
                        return thumbnail_name
        
        return None

        
    def new_master(self, from_file = False):
        if self.project:
            if self.data_file:
                if self.settings:
                                    
                    new_master = {}
                    new_master["date_created"] = "%s %s"%(time.strftime("%d/%m/%Y"),time.strftime("%H:%M:%S"))
                    new_master["author"] = self.settings.user[0]
                    new_master["note"] = "No notes"  
                              
                    if self.masters:
                        # master versions existst
                        
                        masters = self.masters
                        last = masters[len(masters)-1]
                        version_number = set_padding(last+1,self.project.project_padding)                
                   
                    else:
                        
                        # this will be the first master
                        version_number = set_padding(1,self.project.project_padding)                
                    
                    maya.clean_up_file()
                    
                    
                    file_name = "%s_%s_%s_%s.%s"%(self.asset_name,self.component_name,"MASTER",version_number,"ma")                                                       
                    if not from_file:                    
                        scene_path = maya.save_scene_as(path = self.masters_path, file_name = file_name )                         
                    else:                      
                        scene_path = os.path.join(self.masters_path,file_name)
                        files.file_copy(from_file, scene_path )
                        
                    new_master["path"] = scene_path    
                    masters = self.masters_ 
                    masters[str(set_padding(0,self.project.project_padding))] = new_master 
                    masters[version_number] = new_master
                    
                    self.masters_ = masters 
                                    
                    master_name = "%s_%s_%s.%s"%(self.asset_name,self.component_name,"MASTER","ma")
                    master_file = os.path.join(self.settings.current_project_path,self.project.assets_dir,self.catagory_name,self.asset_name,self.component_name,master_name) 
                    files.file_copy(scene_path, master_file)

                    maya.open_scene(master_file)
 
                    

    def make_master(self, version):
                
        source = self.file_path("masters",version)

        if source:
            files.file_copy(source, self.master)

            new_master = {}
            new_master["date_created"] = self.date_created("masters",version)
            
            new_master["author"] =  self.author("masters",version)
            new_master["note"] = self.note("masters",version) 

            masters = self.masters_ 
            masters[str(set_padding(0,self.project.project_padding))] = new_master 

            self.masters_ = masters 
            
            return True
        
        return False

    def rename(self, new_name):
         
        #asset_path = os.path.dirname(files.dir_rename(os.path.dirname(self.data_file_path),new_name))
        #componentes = files.list_dir_folders(asset_path)
        #if new_name in componentes:
        #    dlg.massage("critical", "Sorry", "This Component exsists" )
        #    return False
        
        versions = {}
        for version in self.versions:
            version_number = set_padding(version,self.project.project_padding) 
            versions[version] = [self.file_path("versions",version_number), "%s_%s_%s"%(self.asset_name,new_name,version_number)] 
            files.file_rename(versions[version][0],versions[version][1])

        if self.master:
            masters = {}
            for version in self.masters:
                version_number = set_padding(version,self.project.project_padding) 
                masters[version] = [self.file_path("masters",version_number), "%s_%s_%s_%s"%(self.asset_name,new_name,"MASTER",version_number)] 
                files.file_rename(masters[version][0],masters[version][1])

                
            master = [self.master, "%s_%s_%s"%(self.asset_name,new_name,"MASTER")]
            files.file_rename(master[0],master[1])
         
        thumb_path = os.path.join(self.tumbnails_path,"%s.%s"%(self.component_name,"png"))   
        if os.path.isfile(thumb_path):
            files.file_rename(thumb_path,new_name) 

        self.component_name = new_name
        path = files.file_rename(self.data_file_path,new_name)        
        
        stage_path = files.dir_rename(os.path.dirname(self.data_file_path),new_name)  
     
        self.set_data_file(os.path.join(stage_path,"%s.%s"%(new_name,"pipe")))
        self.data_file = self.data_file.read()
        
        return True
        
    def rename_asset(self, new_name):
         
        
        versions = {}
        for version in self.versions:
            version_number = set_padding(version,self.project.project_padding) 
            versions[version] = [self.file_path("versions",version_number), "%s_%s_%s"%(new_name,self.component_name,version_number)] 
            files.file_rename(versions[version][0],versions[version][1])

        if self.master:
            masters = {}
            for version in self.masters:
                version_number = set_padding(version,self.project.project_padding) 
                masters[version] = [self.file_path("masters",version_number), "%s_%s_%s_%s"%(new_name,self.component_name,"MASTER",version_number)] 
                files.file_rename(masters[version][0],masters[version][1])

                
            master = [self.master, "%s_%s_%s"%(new_name,self.component_name,"MASTER")]
            files.file_rename(master[0],master[1])
        
        self.asset_name = new_name       
        return True
                

    def get_data_file(self,path = None):
                
        if path:
            dir = os.path.dirname(path)
            file = os.path.join(dir,"*.pipe")
            
            
            if len(glob.glob(file)) == 1: #if its a master
                return glob.glob(file)[0]                        

            dir = os.path.dirname(dir)
            file = os.path.join(dir,"*.pipe")
                                       
            if len(glob.glob(file)) == 1: #if its a version
                return glob.glob(file)[0]  
            
            return None
            
        return None        

    @property
    def type(self):
        
        if self.component_name:
            return "component"
        
        
        shot = pipeline_shot(path = self.data_file_path, project = self.project, settings = self.settings)

        if shot:
            if shot.shot_name:
                return "shot"
            
        return None    

    def log(self):

        if self.settings:
            self.settings.log()
        
        log.info("logging component '%s' at asset '%s' at catagory '%s'"%(self.component_name,self.asset_name,self.catagory_name))       
        
        log.info("component path %s"%self.stage_path)
                
        [ log.info("  %s"%f) for f in files.list_all(self.stage_path) if isinstance(files.list_all(self.stage_path),list) ]
                               
        log.info("compnnent data file: %s"%self.data_file_path)
        
        log.info(self.data_file.print_nice())

        log.info("end logging component ")

class ProjectNode(RootNode):

    loaded = QtCore.Signal()

    def __init__(self,name, parent=None, **kwargs):

        RootNode.__init__(self, name, parent, **kwargs)


        self.project_file = None
        if self.data_file:
            self.project_file = self.data_file.read()

        self.settings = None
        for key in kwargs:
            if key == "settings":
                self.settings = kwargs[key]


        self.pipelineUI = None
        for key in kwargs:
            if key == "pipelineUI":
                self.pipelineUI = kwargs[key]
                self.loaded.connect(self.pipelineUI.updateCurrentProject)

    def create(self,
               path = None,
               padding = 3,
               file_type = "ma",
               fps = 25,
               users = {"0":["Admin","1234","admin"]},
               levels = {},
               stages = {},
               suffix = None):


        project_key = data.id_generator()
        project_data = {}
        project_data["project_name"] = self.name
        project_data["project_key"] = project_key
        project_data["padding"] = padding
        project_data["fps"] = fps
        project_data["defult_file_type"] = file_type
        project_data["users"] = users
        project_data["suffix"] = suffix
        #project_data["playblast_outside"] = playblast_outside

        folders = ["assets","images","scenes","sourceimages","data","movies","autosave","movies","scripts",
                   "sound", "clips", "renderData", "cache"]

        for folder in folders:
            project_data[folder] = folder
            files.create_directory(os.path.join(path, folder))

        #render folders:
        r_folders = ["renderData", "depth", "iprimages", "shaders"]
        for r_folder in r_folders[1:]:
            files.create_directory(os.path.join(path, r_folders[0], r_folder))

        fur_folders = ["renderData", "fur", "furFiles", "furImages", "furEqualMap", "furAttrMap", "furShadowMap" ]
        for f_folder in fur_folders[2:]:
            files.create_directory(os.path.join(path, fur_folders[0], fur_folders[1], f_folder))

        #cache folders:
        c_folders = ["cache", "particles", "nCache", "bifrost"]
        for c_folder in c_folders[1:]:
            files.create_directory(os.path.join(path, c_folders[0], c_folder))

        fl_folders = ["cache", "nCache", "fluid"]
        for fl_folder in fl_folders[2:]:
            files.create_directory(os.path.join(path, fl_folders[0], fl_folders[1], fl_folder))


        # stages = {}
        # stages["asset"] = ["model", "rig", "clip", "shading", "lightning"]
        # stages["animation"] = ["layout", "Animation"]

        project_data["stages"] = stages

        # levels = {}
        # levels["asset"] = ["type", "asset", "stage", "ccc"]
        # levels["animation"] = ["Ep", "Seq"]

        project_data["levels"] = levels

        self._path = path
        data_path = os.path.join(path, "%s.%s" % (self.name, "json"))

        self.data_file = data.jsonDict().create(data_path, project_data)
        self.project_file = self.data_file.read()


        return self

    def edit(self):
        print "eding the project"

    def set(self):
        if self.data_file:
            import pymel.core as pm
            import maya.mel as mel

            if 1==1: # do some test to see if we can set this projet

                pm.workspace.open(self.path)
                pm.workspace.chdir(self.path)

                raw_project_path = self.path.replace("\\", "\\\\")
                melCmd = "setProject \"" + raw_project_path + "\";"
                try:
                    mel.eval(melCmd)
                except:
                    pass

                print "project changed to: %s" % self.name

                self.loaded.emit()
                return True

        else:
            print "Cannot set project"
            return None

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
    def playblasts_path(self):
        if self.settings:
            if self.playblast_outside:
                path = os.path.join(os.path.dirname(self.settings.current_project_path),"%s_playblasts"%(self.project_name))

            else:
                path = os.path.join(self.settings.current_project_path,"playblasts")


            return path
        return None


    # @property
    # def stages(self):
    #     stages = {}
    #     stages["asset"] = ["model","rig","clip","shading","lightning"]
    #     stages["animation"] = ["layout","Shot"]
    #     return stages
    #
    # @property
    # def levels(self):
    #     levels = {}
    #     levels["asset"] = ["type","asset","stage","ccc"]
    #     levels["animation"] = ["Ep","Seq"]
    #     return levels


    @property
    def stages(self):
        if self.project_file:
            return self.project_file["stages"]
        else:
            return None

    @stages.setter
    def stages(self, dict):
        if self.data_file:
            data = {}
            data["stages"] = dict
            self.data_file.edit(data)
            self.project_file = self.data_file.read()


    @property
    def levels(self):
        if self.project_file:
            return self.project_file["levels"]
        else:
            return None


    @levels.setter
    def levels(self, dict):
        if self.data_file:
            data = {}
            data["levels"] = dict
            self.data_file.edit(data)
            self.project_file = self.data_file.read()


def stageDir(dir):

    if os.path.exists(dir):
        if os.path.isfile(os.path.join(dir, "%s.%s" % (os.path.split(dir)[1], "json"))):
            '''
            further verify if the stage.json file is actually related to the path
            '''
            j = Metadata_file(path=os.path.join(dir, "%s.%s" % (os.path.split(dir)[1], "json")))
            info = j.data_file.read()
            if info:
                typeInfo = info["typeInfo"]
                if typeInfo == _stage_:
                    return True

    return False

def assetDir(dir):

    if os.path.exists(dir):
        if os.path.isfile(os.path.join(dir, "%s.%s" % (os.path.split(dir)[1], "json"))):
            '''
            further verify if the asset.json file is actually related to the path
            '''
            j = Metadata_file(path=os.path.join(dir, "%s.%s" % (os.path.split(dir)[1], "json")))
            info = j.data_file.read()
            if info:
                typeInfo = info["typeInfo"]
                if typeInfo == _asset_:

                    return True

    return False


def set_padding(int, padding):
    return str(int).zfill(padding)