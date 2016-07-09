
from PySide import QtCore, QtGui, QtXml
import cPickle


import data as dt
reload(dt)

class customTreeView(QtGui.QTreeView):
    def __init__(self,parent = None,proxyModel = None):
        super(customTreeView, self).__init__(parent)
        self._proxyModel = proxyModel
        
        self.setAlternatingRowColors(True)
        
        #self.setStyleSheet(
        '''
                           
                           QTreeView::branch:has-siblings:!adjoins-item {
                                border-image:url(/Users/liorbenhorin/Documents/Projects/2016/GitHub/pipeline/vline.svg) 0;
                           }
                           
                           QTreeView::branch:has-siblings:adjoins-item {
                                border-image:url(/Users/liorbenhorin/Documents/Projects/2016/GitHub/pipeline/branch-more.svg) 0;
                           }
                           
                           QTreeView::branch:!has-children:!has-siblings:adjoins-item {
                                border-image:url(/Users/liorbenhorin/Documents/Projects/2016/GitHub/pipeline/branch-end.svg) 0;
                           }

                           QTreeView::branch:has-children:!has-siblings:closed,
                           QTreeView::branch:closed:has-children:has-siblings {
                                border-image: none;
                                image:url(/Users/liorbenhorin/Documents/Projects/2016/GitHub/pipeline/branch-closed.svg) 0;
                           }

                           QTreeView::branch:open:has-children:!has-siblings,
                           QTreeView::branch:open:has-children:has-siblings  {
                                border-image: none;
                                image: url(/Users/liorbenhorin/Documents/Projects/2016/GitHub/pipeline/branch-open.svg) 0;
                           }
                                                               
                           '''#)
                           
        
    def dropEvent(self, event):
        super(customTreeView,self).dropEvent(event)
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
            self.treeView.expandAll()

            
            
class SceneGraphModel(QtCore.QAbstractItemModel):
    
    
    sortRole   = QtCore.Qt.UserRole
    filterRole = QtCore.Qt.UserRole + 1
    
    """INPUTS: Node, QObject"""
    def __init__(self, root, parent=None):
        super(SceneGraphModel, self).__init__(parent)
        self._rootNode = root


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
        return 2
    

    
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


    """INPUTS: QModelIndex, QVariant, int (flag)"""
    def setData(self, index, value, role=QtCore.Qt.EditRole):

        if index.isValid():
            
            node = index.internalPointer()
            
            if role == QtCore.Qt.EditRole:
                node.setData(index.column(), value)
                self.dataChanged.emit(index, index)
                return True
            
        return False

    
    """INPUTS: int, Qt::Orientation, int"""
    """OUTPUT: QVariant, strings are cast to QString which is a QVariant"""
    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if section == 0:
                return "Name"
            else:
                return "Type"

    """INPUTS: QModelIndex"""
    """OUTPUT: int (flag)"""

            
    
    """INPUTS: QModelIndex"""
    """OUTPUT: int (flag)"""
    def flags(self, index):
        
        if not index.isValid():

            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsDropEnabled 


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
        dropParent.addChild( item )
        self.insertRows( dropParent.childCount()-1, 1, parentIndex )
            
        self.dataChanged.emit( parentIndex, parentIndex )
         
        return True 
       

