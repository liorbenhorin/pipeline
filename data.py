
from PySide import QtXml, QtGui
import os

import modules.data as data
reload(data)

global _node_
global _root_
global  _stage_
global _asset_
global _folder_
global _dummy_

_node_ = "node"
_root_ = "root"
_stage_ = "stage"
_asset_ = "asset"
_folder_ = "folder" 
_dummy_ = "dummy"


def set_icons():
    localIconPath = os.path.join(os.path.dirname(__file__), 'icons')
    if not os.path.exists(localIconPath):
        return 
    global folder_icon
    global cube_icon
    global add_cube_icon
    
    global cube_icon_full
    global add_icon
    global large_image_icon
    folder_icon = os.path.join(localIconPath, "%s.svg"%"folder")
    cube_icon = os.path.join(localIconPath, "%s.svg"%"cube") 
    add_cube_icon = os.path.join(localIconPath, "%s.svg"%"add_cube")     
    cube_icon_full = os.path.join(localIconPath, "%s.svg"%"cube-fill") 
    add_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"add"))
    large_image_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"large_image")) 
set_icons()

class Node(object):
    
    def __init__(self, name, parent=None):
        
        super(Node, self).__init__()
        
        self._name = name
        self._children = []
        self._parent = parent
        self.expendedState = False
        self._id = data.id_generator()
        
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
        elif column is 1: return None
    
    def setData(self, column, value):
        print value
        if   column is 0: self.name = value
        elif column is 1: pass
    
    def resource(self):
        return folder_icon
        
    def delete(self):

        self.delete_me()
        
        for child in self._children:
            
            child.delete()

    def delete_me(self):
        print "***DELETE ALL IN" + self._name + "\n"
    
    @property
    def expendedState(self):
        return self._expendedState
    @expendedState.setter
    def expendedState(self, state):    
        self._expendedState = state

    @property
    def id(self):
        return self._id


class RootNode(Node):
    
    def __init__(self, name, parent=None):
        super(RootNode, self).__init__(name, parent)
        self.name = name
    
    def typeInfo(self):
        return _root__
  
    def resource(self):
        return folder_icon


class FolderNode(Node):
    
    def __init__(self, name,  parent=None):
        super(FolderNode, self).__init__(name, parent)
      

    def typeInfo(self):
        return _folder_
          
    def resource(self):
        return folder_icon


class AssetNode(Node):
    
    def __init__(self, name,  parent=None):
        super(AssetNode, self).__init__(name, parent)
      

    def typeInfo(self):
        return _asset_
          
    def resource(self):
        return cube_icon_full
        

        
class StageNode(Node):
    
    def __init__(self, name, stage = None, parent=None):
        super(StageNode, self).__init__(name, parent)
      
        self._stage = stage

    def typeInfo(self):
        return _stage_

    @property
    def stage(self):
        return self._stage
        
    @stage.setter
    def stage(self, value):
        self._stage = value

   
    def resource(self):
        return large_image_icon
        
                    

class DummyNode(Node):
    
    def __init__(self, name, parent=None):
        super(DummyNode, self).__init__(name, parent)


    def typeInfo(self):
        return _dummy_
  
    def resource(self):
        return None               
                