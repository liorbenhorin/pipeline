
from PySide import QtXml, QtGui
import os

def set_icons():
    localIconPath = os.path.join(os.path.dirname(__file__), 'icons')
    if not os.path.exists(localIconPath):
        return 
    global folder_icon
    global cube_icon
    global cube_icon_full
    
    folder_icon = os.path.join(localIconPath, "%s.svg"%"folder")
    cube_icon = os.path.join(localIconPath, "%s.svg"%"cube")    
    cube_icon_full = os.path.join(localIconPath, "%s.svg"%"cube-fill") 

set_icons()

class Node(object):
    
    def __init__(self, name, parent=None):
        
        super(Node, self).__init__()
        
        self._name = name
        self._children = []
        self._parent = parent

        
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
        return "NODE"

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
        
        child = self._children.pop(position)
        child._parent = None

        return True

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
    
    def __repr__(self):
        return self.log() + "\n END"
    

    def data(self, column):
        
        if   column is 0: return self.name
        elif column is 1: return None#self.typeInfo()
    
    def setData(self, column, value):
        print value
        if   column is 0: self.name = value#.toPyObject()
        elif column is 1: pass
    
    def resource(self):
        return folder_icon
        



class AssetNode(Node):
    
    def __init__(self, name, component, parent=None):
        super(AssetNode, self).__init__(name, parent)
      
        self._component = component

    def typeInfo(self):
        return "ASSET"

    @property
    def component(self):
        return self._component
        
    @component.setter
    def component(self, value):
        self._component = value

   
    def resource(self):
        return cube_icon_full
        

        
class ComponentNode(Node):
    
    def __init__(self, name, component, parent=None):
        super(ComponentNode, self).__init__(name, parent)
      
        self._component = component

    def typeInfo(self):
        return "COMPONENT"

    @property
    def component(self):
        return self._component
        
    @component.setter
    def component(self, value):
        self._component = value

   
    def resource(self):
        return cube_icon
        
        
