
from PySide import QtCore, QtGui, QtXml
import cPickle
import os
import functools

import data as dt
reload(dt)

def set_icons():
    localIconPath = os.path.join(os.path.dirname(__file__), 'icons/treeview/')
    if not os.path.exists(localIconPath):
        return 
    global branch_more
    global branch_closed
    global branch_open
    global branch_end
    global vline
    
    branch_more = os.path.join(localIconPath,"branch-more.svg")
    branch_closed = os.path.join(localIconPath,"branch-closed.svg")
    branch_open = os.path.join(localIconPath,"branch-open.svg")
    branch_end = os.path.join(localIconPath,"branch-end.svg")
    vline = os.path.join(localIconPath,"vline.svg")
                    
    
set_icons()

class customTreeView(QtGui.QTreeView):
    def __init__(self,parent = None,proxyModel = None):
        super(customTreeView, self).__init__(parent)
        self._proxyModel = proxyModel
        self.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.setAlternatingRowColors(True)
        self._state = None
        self._ignoreExpentions = False
        
        self.setStyleSheet('''  
                           
                           QTreeView::item:focus {
                           }
                           QTreeView::branch:has-siblings:!adjoins-item {
                                border-image:url(''' + vline + ''') 0;
                           }
                           
                           QTreeView::branch:has-siblings:adjoins-item {
                                border-image:url(''' + branch_more + ''') 0;
                           }
                           
                           QTreeView::branch:!has-children:!has-siblings:adjoins-item {
                                border-image:url(''' + branch_end + ''') 0;
                           }

                           QTreeView::branch:has-children:!has-siblings:closed,
                           QTreeView::branch:closed:has-children:has-siblings {
                                border-image: none;
                                image:url(''' + branch_closed + ''') 0;
                           }

                           QTreeView::branch:open:has-children:!has-siblings,
                           QTreeView::branch:open:has-children:has-siblings  {
                                border-image: none;
                                image: url(''' + branch_open + ''') 0;
                           }
                           

                           
                            ''')


    
    def saveState(self):
        if self._ignoreExpentions == True:
            return  
                 
        def rec( dict, mdl, index):
            
            for row in range(mdl.rowCount(index)):
                 
                   
                i = mdl.index(row,0, index)
                node = mdl.data(i, 165)
                
                if self.isExpanded(i):
                    dict[node] = True
                else:
                    dict[node] = False  
                      
                rec(dict, mdl, i)     
            
        
        mdl = self.model()
        self.expended_states = {}
        rec(self.expended_states,mdl,self.rootIndex())

        
    def restoreState(self):    

        def rec(  mdl, index):
            
            for row in range(mdl.rowCount(index)):
                 
                   
                i = mdl.index(row,0, index)
                node = mdl.data(i, 165)
                
                if self.expended_states[node] == True:
                    self.setExpanded(i, True)

                     
                rec( mdl, i)     
                    
        self.collapseAll()
        mdl = self.model()
        rec(mdl,self.rootIndex())        
        
    def dropEvent(self, event):
        super(customTreeView,self).dropEvent(event)
        #QTreeView.dropEvent(self, evt)
        if not event.isAccepted():
            # qdnd_win.cpp has weird behavior -- even if the event isn't accepted
            # by target widget, it sets accept() to true, which causes the executed
            # action to be reported as "move", which causes the view to remove the
            # source rows even though the target widget didn't like the drop.
            # Maybe it's better for the model to check drop-okay-ness during the
            # drag rather than only on drop; but the check involves not-insignificant work.
            event.setDropAction(QtCore.Qt.IgnoreAction)
                
        self._proxyModel.invalidate()

   
    def contextMenuEvent(self, event):
        
        handled = True
        index = self.indexAt(event.pos())
        menu = QtGui.QMenu()        
        node = None
        mdl =  self.model().sourceModel()
        
        
        if index.isValid():
            src = index.model().mapToSource(index)                  
            node =  mdl.getNode(src)
            
        actions = [] 
        print mdl.persistentIndexList() 
          
        if node:

            if node.typeInfo() == "NODE": 
                actions.append(QtGui.QAction("Create new Asset", menu, triggered = functools.partial(self.create_new_asset,node) ))
                actions.append(QtGui.QAction("Create new Component", menu, triggered = functools.partial(self.create_new_component,node) ))
                actions.append(QtGui.QAction("Delete", menu, triggered = functools.partial(self.delete,mdl, src,node) ))
                
            elif node.typeInfo() == "ASSET":
                actions.append(QtGui.QAction("Create new Component", menu, triggered = functools.partial(self.create_new_component,node) ))
                actions.append(QtGui.QAction("Delete", menu, triggered = functools.partial(self.delete,mdl, src,node) ))
                
            elif node.typeInfo() == "COMPONENT":
                actions.append(QtGui.QAction("Delete", menu, triggered = functools.partial(self.delete,mdl, src, node) ))
                

        else:
            actions.append(QtGui.QAction("Create new folder", menu, triggered = functools.partial(self.create_new_folder,mdl.rootNode) ))
            actions.append(QtGui.QAction("Create new Asset", menu, triggered = functools.partial(self.create_new_asset,mdl.rootNode) ))
            actions.append(QtGui.QAction("Create new Component", menu, triggered = functools.partial(self.create_new_component,mdl.rootNode) ))
        
        menu.addActions(actions)      

        if handled:

            menu.exec_(event.globalPos())
            event.accept() #TELL QT IVE HANDLED THIS THING
            
        else:
            event.ignore() #GIVE SOMEONE ELSE A CHANCE TO HANDLE IT
                   
        return


    def delete(self, model, index,node):
        node.delete()
        parentIndex = model.parent(index)
        if node._children != []:
            model.removeRows(node.row(),model.rowCount(index),parentIndex)
        else:
            model.removeRows(node.row(),1,parentIndex)

    def create_new_folder(self, parent):

        node = dt.Node("folder",parent)
        self._proxyModel.invalidate()

    def create_new_asset(self, parent):
        node = dt.AssetNode("asset","",parent)
        self._proxyModel.invalidate()
    
    def create_new_component(self, parent):
        node = dt.ComponentNode("component","",parent)
        self._proxyModel.invalidate()

class filterSortModel(QtGui.QSortFilterProxyModel):
    def __init__(self,parent = None):
        
        super(filterSortModel, self).__init__(parent)
        self._treeView = None
        
    @property
    def treeView(self):
        if self._treeView:
            return self._treeView
        else:
            return None
            
    @treeView.setter
    def treeView(self, object):
        self._treeView = object
                    
    def filterAcceptsRow(self,sourceRow,sourceParent):
        if super(filterSortModel,self).filterAcceptsRow(sourceRow,sourceParent):
            return True
        
        return self.hasAcceptedChildren(sourceRow,sourceParent)

    def hasAcceptedChildren(self,sourceRow,sourceParent):
        model=self.sourceModel()
        sourceIndex=model.index(sourceRow,0,sourceParent)
        if not sourceIndex.isValid():
            return False
        indexes=model.rowCount(sourceIndex)
        for i in range(indexes):
            if self.filterAcceptsRow(i,sourceIndex):
                return True
        
        return False

    def setFilterRegExp(self, exp):
              
        super(filterSortModel, self).setFilterRegExp(exp)
        if self.treeView:
            if len(exp)>0:        
                self.treeView._ignoreExpentions = True
                self.treeView.expandAll()
                self.treeView._ignoreExpentions = False
            else:
                self.treeView._ignoreExpentions = True
                self.treeView.restoreState()          
                self.treeView._ignoreExpentions = False         

            
            
class SceneGraphModel(QtCore.QAbstractItemModel):
    
    
    sortRole   = QtCore.Qt.UserRole
    filterRole = QtCore.Qt.UserRole + 1
    expendedRole = QtCore.Qt.UserRole + 2
    
    """INPUTS: Node, QObject"""
    def __init__(self, root, parent=None):
        super(SceneGraphModel, self).__init__(parent)
        self._rootNode = root
        self._tempIndex = None
        
    @property
    def rootNode(self):
        return self._rootNode

    """INPUTS: QModelIndex"""
    """OUTPUT: int"""
    def rowCount(self, parent):
        if not parent.isValid():
            parentNode = self._rootNode
        else:
            parentNode = parent.internalPointer()

        return parentNode.childCount()

    """INPUTS: QModelIndex"""
    """OUTPUT: int"""
    def columnCount(self, parent):
        return 1
    

    
    """INPUTS: QModelIndex, int"""
    """OUTPUT: QVariant, strings are cast to QString which is a QVariant"""
    def data(self, index, role):
        
        if not index.isValid():
            return None

        node = index.internalPointer()

        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            return node.data(index.column())
 
        if role == QtCore.Qt.DecorationRole:
            if index.column() == 0:
                resource = node.resource()
                return QtGui.QIcon(QtGui.QPixmap(resource))
            
        if role == SceneGraphModel.sortRole:
            return node.typeInfo()

        if role == SceneGraphModel.filterRole:
            return node.typeInfo()

        if role == QtCore.Qt.SizeHintRole:
            return QtCore.QSize(0,19)
        
        # this is for expending state - the result must be uniqe!!!
        if role == 165:
            return node.name
        
        if role == SceneGraphModel.expendedRole:
            print "R"
            return self.isExpended(index)
               
        #if role == QtCore.Qt.FontRole:
         #  if node.typeInfo() == "COMPONENT":
          #     boldFont = QtGui.QFont()
           #    boldFont.setBold(True)
            #   return boldFont

    """INPUTS: QModelIndex, QVariant, int (flag)"""
    def setData(self, index, value, role=QtCore.Qt.EditRole):

        if index.isValid():
            
            node = index.internalPointer()
            
            if role == QtCore.Qt.EditRole:
                node.setData(index.column(), value)
                self.dataChanged.emit(index, index)
            if role == SceneGraphModel.expendedRole:
                node.expendedState(self.isExpended(index))
                self.dataChanged.emit(index, index)               
                return True
            
        return False

    
    """INPUTS: int, Qt::Orientation, int"""
    """OUTPUT: QVariant, strings are cast to QString which is a QVariant"""
    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if section == 0:
                return "Project"
            else:
                return "Type"

    """INPUTS: QModelIndex"""
    """OUTPUT: int (flag)"""

            
    
    """INPUTS: QModelIndex"""
    """OUTPUT: int (flag)"""
    def flags(self, index):
        
        if not index.isValid():

            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsDropEnabled 

        if index.isValid():
            node = self.getNode(index)
            if node.typeInfo() == "COMPONENT":
                return  QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable
    
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsDropEnabled | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable    
    
    """INPUTS: QModelIndex"""
    """OUTPUT: QModelIndex"""
    """Should return the parent of the node with the given QModelIndex"""
    def parent(self, index):
        
        node = self.getNode(index)
        parentNode = node.parent()
        
        if parentNode == self._rootNode:
            return QtCore.QModelIndex()
        
        return self.createIndex(parentNode.row(), 0, parentNode)
        
    """INPUTS: int, int, QModelIndex"""
    """OUTPUT: QModelIndex"""
    """Should return a QModelIndex that corresponds to the given row, column and parent node"""
    '''
    def index(self, row, column, parent):
        
        parentNode = self.getNode(parent)

        childItem = parentNode.child(row)


        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()
    
    '''
    '''
    def itemFromIndex( self, index ):
        return index.internalPointer() if index.isValid() else self._rootNode
    '''  

    
    def index( self, row, column, parentIndex ):
        
        if not self.hasIndex( row, column, parentIndex ):
            return    QtCore.QModelIndex() 
             
        parent = self.getNode( parentIndex )
        return  self.createIndex( row, column, parent.child( row ) ) 
    ''


    """CUSTOM"""
    """INPUTS: QModelIndex"""
    def getNode(self, index):
        if index.isValid():
            node = index.internalPointer()
            if node:
                return node
            
        return self._rootNode

    
    """INPUTS: int, int, QModelIndex"""
    def insertRows(self, position, rows, parent=QtCore.QModelIndex()):
        #parentNode = self.getNode(parent)

        self.beginInsertRows(parent, position, position + rows - 1)
        
        '''
        for row in range(rows):
            
            childCount = parentNode.childCount()
            childNode = dt.Node("untitled" + str(childCount))
            success = parentNode.insertChild(position, childNode)
        '''
        self.endInsertRows()
        return True


    def removeRows( self, row, count, parentIndex ):

        '''Remove a number of rows from the model at the given row and parent.'''
        self.beginRemoveRows( parentIndex, row, row+count-1 )
        parent = self.getNode( parentIndex )
        for x in range( count ):
            parent.removeChild( row )
        self.endRemoveRows()
        self.dataChanged.emit( parentIndex, parentIndex )
        return True

    def supportedDropActions( self ):

        return QtCore.Qt.MoveAction | QtCore.Qt.CopyAction
     

    def mimeData( self, indices ):
        '''Encode serialized data from the item at the given index into a QMimeData object.'''
        
        data = ''

        parent_index =  self.parent(indices[0])
        item = self.getNode( indices[0] )
        self._tempIndex = indices[0]
        try:
            data += cPickle.dumps( item )

        except:
            pass

        mimedata = QtCore.QMimeData()
        mimedata.setData( 'application/x-qabstractitemmodeldatalist', data ) 
   
        return mimedata
     
    def dropMimeData( self, mimedata, action, row, column, parentIndex ):
        '''Handles the dropping of an item onto the model.
         
        De-serializes the data into a TreeItem instance and inserts it into the model.
        '''
        if not mimedata.hasFormat( 'application/x-qabstractitemmodeldatalist' ):
            return False
            
        print self.rootNode
        item = cPickle.loads( str( mimedata.data( 'application/x-qabstractitemmodeldatalist' ) ) )
        dropParent = self.getNode( parentIndex )
        
        # do not allow a folder to be dropped on an asset...
        if dropParent.typeInfo() == "ASSET":
            if item.typeInfo() == "NODE":
                return False

               
        dropParent.addChild( item )
        self.insertRows( dropParent.childCount()-1, 1, parentIndex )
            
        self.dataChanged.emit( parentIndex, parentIndex )
         
        return True 
       


        