
from PySide import QtCore, QtGui, QtXml
import cPickle

import data as dt
reload(dt)

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
                return "Scenegraph"
            else:
                return "Typeinfo"

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

    def itemFromIndex( self, index ):
        '''Returns the TreeItem instance from a QModelIndex.'''
        return index.internalPointer() if index.isValid() else self._rootNode
      

    
    def index( self, row, column, parentIndex ):
        '''Creates a QModelIndex for the given row, column, and parent.'''
        if not self.hasIndex( row, column, parentIndex ):
            return QtCore.QModelIndex()
             
        parent = self.itemFromIndex( parentIndex )
        return self.createIndex( row, column, parent.child( row ) )
     


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
        print "insertRows"
        parentNode = self.getNode(parent)
        
        self.beginInsertRows(parent, position, position + rows - 1)
        
        for row in range(rows):
            
            childCount = parentNode.childCount()
            childNode = dt.Node("untitled" + str(childCount))
            success = parentNode.insertChild(position, childNode)
        
        self.endInsertRows()

        return success

    def removeRows(self, position, rows, parent=QtCore.QModelIndex()):
        print "removeRows"
        parentNode = self.getNode(parent)
        self.beginRemoveRows(parent, position, position + rows - 1)
        
        for row in range(rows):
            success = parentNode.removeChild(position)
            
        self.endRemoveRows()
        
        return success

    def supportedDropActions( self ):

        return QtCore.Qt.MoveAction | QtCore.Qt.CopyAction
     



    '''    
    def mimeTypes( self ):

        types =  'application/x-qabstractitemmodeldatalist' 
        return types
    ''' 
    def mimeData( self, indices ):
        '''Encode serialized data from the item at the given index into a QMimeData object.'''
        
        data = ''
        item = self.itemFromIndex( indices[0] )
        try:
            data += cPickle.dumps( item )
        except:
            pass
            
            
        print item  
        print ">>>><<<<<"  
        mimedata = QtCore.QMimeData()
        mimedata.setData( 'application/x-qabstractitemmodeldatalist', data ) 
        print data                   
        print mimedata    
        #mimedata = QtCore.QMimeData()
        #mimedata.setData( 'application/x-qabstractitemmodeldatalist', data )
        return mimedata
     
    def dropMimeData( self, mimedata, action, row, column, parentIndex ):
        '''Handles the dropping of an item onto the model.
         
        De-serializes the data into a TreeItem instance and inserts it into the model.
        '''
        if not mimedata.hasFormat( 'application/x-qabstractitemmodeldatalist' ):
            return False
        item = cPickle.loads( str( mimedata.data( 'application/x-qabstractitemmodeldatalist' ) ) )
        dropParent = self.itemFromIndex( parentIndex )
        dropParent.addChild( item )
        self.insertRows( dropParent.numChildren()-1, 1, parentIndex )
        self.dataChanged.emit( parentIndex, parentIndex )
        return True        