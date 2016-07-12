
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


class customListView(QtGui.QListView):
    def __init__(self,parent = None,proxyModel = None):
        super(customListView, self).__init__(parent)
        
        self.setViewMode(QtGui.QListView.IconMode)
        self._tree = None
        self._treeSortModel = None
        self._treeModel = None
               
    def treeView(self, view):
        self._tree = view
        self._treeSortModel = view.model()
        self._treeModel = self._treeSortModel.sourceModel()

    def change(self, index):

        node = self.model().getNode(index)
        print node.name
        treeIndex = self._treeModel.indexFromNode(node,self._tree.rootIndex())
        print self._treeModel.getNode(treeIndex).name
        
    def update(self, index, col):
        
        mdl =  self._tree.model().sourceModel()
        src = index.model().mapToSource(index)                  
 
        
        list = []
        
        for row in range(mdl.rowCount(src)):

            item_index = mdl.index(row,0,src)
            node = mdl.getNode(item_index)
            
            #if node.typeInfo() == "COMPONENT" or node.typeInfo() == "ASSET": 
            list.append(node)
            
        if len(list) > 0:
            listModel = componentsModel(list)            
            self.setModel(listModel)
            
            return True
            
        self.setModel(None)
        return None

'''            
class ListTreeView(QtGui.QTreeView):
    def __init__(self,parent = None,proxyModel = None):
        super(ListTreeView, self).__init__(parent)
        #self._proxyModel = proxyModel
        #self.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.setAlternatingRowColors(True)
        #self.expandAll()
        #self.setIndentation(0)
        #self.header().hide() 

    def update(self, treeView , index, col):
        print "UPDATE"
        mdl = treeView.model()
        #src = index.model().mapToSource(index)
        #self.setRootIndex(index)
        #return

        
        src = index.model().mapToSource(index)                  
        
        
        this_id = self.model().mapFromSource(src)       
        self.setRootIndex(this_id)
        self.model().invalidate()     
        self.expandAll()
        #print mdl.getNode(id).name , " ---> index"
        
        return'''
        
                    
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


    def setModel(self,model):
        super(customTreeView,self).setModel(model)
        
        self.expandAll()
        i =  self.model().index(0,0,self.rootIndex())
        
        for row in range(self.model().rowCount(i)):
            x = self.model().index(row,0,i)
            self.setExpanded(x,False)
        
        self.saveState()
    
    
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
          
        if node:

            if node.typeInfo() == "NODE": 
                actions.append(QtGui.QAction("Create new Asset", menu, triggered = functools.partial(self.create_new_asset,node) ))
                #actions.append(QtGui.QAction("Create new Component", menu, triggered = functools.partial(self.create_new_component,node) ))
                actions.append(QtGui.QAction("Delete", menu, triggered = functools.partial(self.delete,mdl, src,node) ))
                
            elif node.typeInfo() == "ASSET":
                #actions.append(QtGui.QAction("Create new Component", menu, triggered = functools.partial(self.create_new_component,node) ))
                actions.append(QtGui.QAction("Delete", menu, triggered = functools.partial(self.delete,mdl, src,node) ))
                
            #elif node.typeInfo() == "COMPONENT":
            #    actions.append(QtGui.QAction("Delete", menu, triggered = functools.partial(self.delete,mdl, src, node) ))
                

        else:
            actions.append(QtGui.QAction("Create new folder", menu, triggered = functools.partial(self.create_new_folder,mdl.rootNode) ))
            actions.append(QtGui.QAction("Create new Asset", menu, triggered = functools.partial(self.create_new_asset,mdl.rootNode) ))
            #actions.append(QtGui.QAction("Create new Component", menu, triggered = functools.partial(self.create_new_component,mdl.rootNode) ))
        
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
    
    #def create_new_component(self, parent):
    #    node = dt.ComponentNode("component","",parent)
    #    self._proxyModel.invalidate()

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

        # hide components from the treeview
        id =  self.sourceModel().index(sourceRow,0,sourceParent)    

        if super(filterSortModel,self).filterAcceptsRow(sourceRow,sourceParent): 
            
            if self.sourceModel().getNode(id).typeInfo() == "COMPONENT":
                return False
                      
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

'''
class list_filterSortModel(QtGui.QSortFilterProxyModel):
    def __init__(self,parent = None):
        
        super(list_filterSortModel, self).__init__(parent)
                    
    def filterAcceptsRow(self,sourceRow,sourceParent):
        #print self.sourceModel().sourceModel()
        
        #i = self.mapToSource(sourceParent)
        #id = self.sourceModel().mapToSource(i)
        #print i
        #print id
        print sourceParent , " | ",sourceRow," -----> INDEX"
        Model = self.sourceModel().sourceModel()
        flatModel = self.sourceModel()
        print Model , "<-- MODEL ", flatModel , "<--- flat"
        flatIndex = self.mapToSource(sourceParent)
        
        treeIndex = flatModel.mapToSource(flatIndex)
        print treeIndex , "<-- MODEL ", flatIndex , "<--- flat"
        
        node = Model.getNode(treeIndex)
        print node.name
        
        
        #print sModel
        #print sourceParent
        #print sourceRow
        #id =  self.sourceModel().sourceModel().index(sourceRow,0,sourceParent)    
        #print sModel.getNode(id).name
        if super(list_filterSortModel,self).filterAcceptsRow(sourceRow,sourceParent): 
            print ">>"
            
            
            return True
         #print self.sourceModel().sourceModel().getNode(id).name
            
            #if self.sourceModel().sourceModel().getNode(id).typeInfo() == "COMPONENT":
                #return False
        
            #if self.sourceModel().sourceModel().getNode(id).typeInfo() == "NODE":
            #    return False
                #return True
        
        return self.hasAcceptedChildren(sourceRow,sourceParent)

    def hasAcceptedChildren(self,sourceRow,sourceParent):
        print ">"
        model=self.sourceModel()
        sourceIndex=model.index(sourceRow,0,sourceParent)
        if not sourceIndex.isValid():
            return False
        indexes=model.rowCount(sourceIndex)
        for i in range(indexes):
            
            if self.filterAcceptsRow(i,sourceIndex):
                return True
        
        return False
'''
'''
class FlatProxyModel(QtGui.QAbstractProxyModel):
    @QtCore.Slot(QtCore.QModelIndex, QtCore.QModelIndex)
    def sourceDataChanged(self, topLeft, bottomRight):
        self.dataChanged.emit(self.mapFromSource(topLeft), \
                              self.mapFromSource(bottomRight))
    def buildMap(self, model, parent = QtCore.QModelIndex(), row = 0):
        if row == 0:
            self.m_rowMap = {}
            self.m_indexMap = {}
        rows = model.rowCount(parent)
        for r in range(rows):
            index = model.index(r, 0, parent)
            #print('row', row, 'item', model.data(index))
            self.m_rowMap[index] = row
            self.m_indexMap[row] = index
            row = row + 1
            if model.hasChildren(index):
                row = self.buildMap(model, index, row)
        return row
        
    def setSourceModel(self, model):
        self.m_indexMap = {}
        QtGui.QAbstractProxyModel.setSourceModel(self, model)
        self.buildMap(model)
        #print(flush = True)
        model.dataChanged.connect(self.sourceDataChanged)
        
    def mapFromSource(self, index):
        if index not in self.m_rowMap: return QtCore.QModelIndex()
        #print('mapping to row', self.m_rowMap[index], flush = True)
        return self.createIndex(self.m_rowMap[index], index.column())
    def mapToSource(self, index):
        if not index.isValid() or index.row() not in self.m_indexMap:
            return QtCore.QModelIndex()
        #print('mapping from row', index.row(), flush = True)
        return self.m_indexMap[index.row()]
   
    def columnCount(self, parent):
        #return 1
        return QtGui.QAbstractProxyModel.sourceModel(self).columnCount(self.mapToSource(parent))
    
            
    def rowCount(self, parent):
        #print('rows:', len(self.m_rowMap), flush=True)
        return len(self.m_rowMap) if not parent.isValid() else 0
    def index(self, row, column, parent):
        #print('index for:', row, column)#, flush=True)
        if parent.isValid(): return QtCore.QModelIndex()
        i = self.createIndex(row, column)
        return i
    def parent(self, index):
        return QtCore.QModelIndex()
    def __init__(self, parent = None):
        super(FlatProxyModel, self).__init__(parent)
 '''           
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
            return node.id
        
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
            
        item = cPickle.loads( str( mimedata.data( 'application/x-qabstractitemmodeldatalist' ) ) )
        dropParent = self.getNode( parentIndex )
        
        # do not allow a folder to be dropped on an asset...
        if dropParent.typeInfo() == "ASSET":
            if item.typeInfo() == "NODE" or item.typeInfo() == "ASSET":
                return False

               
        dropParent.addChild( item )
        self.insertRows( dropParent.childCount()-1, 1, parentIndex )
            
        self.dataChanged.emit( parentIndex, parentIndex )
         
        return True 
       

    def indexFromNode(self, node, rootIndex):

                 
        def rec(d, index):
            
            for row in range(self.rowCount(index)):
                 
                   
                i = self.index(row,0, index)
                id = self.data(i, 165)
                if id == node.id:
                    d.append(i)
                else:
                    pass#d.append(False)
                          
                rec(d, i)     
            
        
        data = []
        rec(data, rootIndex)
        return data[0]#list(filter(().__ne__, data))[0]





class componentsModel(QtCore.QAbstractListModel):
    
    def __init__(self, components = [], parent = None):
        QtCore.QAbstractListModel.__init__(self, parent)
        self.__components = components



    def headerData(self, section, orientation, role):
        
        if role == QtCore.Qt.DisplayRole:
            
            if orientation == QtCore.Qt.Horizontal:
                return QtCore.QString("Palette")
            else:
                return QtCore.QString("Color %1").arg(section)


    def rowCount(self, parent):
        return len(self.__components)


    def data(self, index, role):
        
        
        if role == QtCore.Qt.EditRole:
            return self.__components[index.row()].name
        
        
        if role == QtCore.Qt.DecorationRole:
            if index.column() == 0:
                resource = self.__components[index.row()].resource()
                return QtGui.QIcon(QtGui.QPixmap(resource))
              
        if role == QtCore.Qt.DisplayRole:
            
            row = index.row()
            return self.__components[row].name


    def flags(self, index):
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        
    """CUSTOM"""
    """INPUTS: QModelIndex"""
    def getNode(self, index):
        if index.isValid():
            return self.__components[index.row()]

        return None        
        
    def setData(self, index, value, role = QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            
            row = index.row()
            #color = QtGui.QColor(value)
            
            #if color.isValid():
            #    self.__components[row] = color
            #    self.dataChanged.emit(index, index)
            #    return True

            
            if role == QtCore.Qt.EditRole:
                self.__components[row].name = value #node.setData(index.column(), value)
                self.dataChanged.emit(index, index)
             
                return True

            
        return False

    #=====================================================#
    #INSERTING & REMOVING
    #=====================================================#
    def insertRows(self, position, rows, parent = QtCore.QModelIndex()):
        self.beginInsertRows(parent, position, position + rows - 1)

        self.endInsertRows()
        
        return True
   
    def removeRows(self, position, rows, parent = QtCore.QModelIndex()):
        self.beginRemoveRows(parent, position, position + rows - 1)
        
        for i in range(rows):
            value = self.__components[position]
            self.__components.remove(value)
             
        self.endRemoveRows()
        return True
        