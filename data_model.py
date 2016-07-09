
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
            return    QtCore.QModelIndex() 
             
        parent = self.itemFromIndex( parentIndex )
        return  self.createIndex( row, column, parent.child( row ) ) 
     


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
        #parentNode = self.getNode(parent)
        print position
        print rows
        self.beginInsertRows(parent, position, position + rows - 1)
        
        '''
        for row in range(rows):
            
            childCount = parentNode.childCount()
            childNode = dt.Node("untitled" + str(childCount))
            success = parentNode.insertChild(position, childNode)
        '''
        self.endInsertRows()
        #self.dataChanged.emit( parent, parent )
        return True


    def removeRows( self, row, count, parentIndex ):
        '''Remove a number of rows from the model at the given row and parent.'''
        self.beginRemoveRows( parentIndex, row, row+count-1 )
        parent = self.itemFromIndex( parentIndex )
        for x in range( count ):
            parent.removeChild( row )
        self.endRemoveRows()
        self.dataChanged.emit( parentIndex, parentIndex )
        return True
    '''
    def removeRows(self, position, rows, parent=QtCore.QModelIndex()):

        parentNode = self.getNode(parent)
        self.beginRemoveRows(parent, position, position + rows - 1)
        
        for row in range(rows):
            success = parentNode.removeChild(position)
            
        self.endRemoveRows()
        
        self.dataChanged.emit( parent, parent )
        return success
    '''
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

        parent_index =  self.parent(indices[0])
        item = self.itemFromIndex( indices[0] )

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
        dropParent = self.itemFromIndex( parentIndex )
        dropParent.addChild( item )
        print dropParent
        #if dropParent.name == "ROOT":
        self.insertRows( dropParent.childCount()-1, 1, parentIndex )
            
        self.dataChanged.emit( parentIndex, parentIndex )
         
        return True 
       

class CustomSortFilterProxyModel(QtGui.QSortFilterProxyModel):
    """
    Implements a QSortFilterProxyModel that allows for custom
    filtering. Add new filter functions using addFilterFunction().
    New functions should accept two arguments, the column to be
    filtered and the currently set filter string, and should
    return True to accept the row, False otherwise.
    Filter functions are stored in a dictionary for easy
    removal by key. Use the addFilterFunction() and 
    removeFilterFunction() methods for access.
    The filterString is used as the main pattern matching
    string for filter functions. This could easily be expanded
    to handle regular expressions if needed.
    """
    def __init__(self, parent=None):
        super(CustomSortFilterProxyModel, self).__init__(parent)
        self.filterString = ''
        self.filterFunctions = {} 

    def setFilterString(self, text):
        """
        text : string
            The string to be used for pattern matching.
        """
        self.filterString = text.lower()
        self.invalidateFilter()

    def addFilterFunction(self, name, new_func):
        """
        name : hashable object
            The object to be used as the key for
            this filter function. Use this object
            to remove the filter function in the future.
            Typically this is a self descriptive string.
        new_func : function
            A new function which must take two arguments,
            the row to be tested and the ProxyModel's current
            filterString. The function should return True if
            the filter accepts the row, False otherwise.
            ex:
            model.addFilterFunction(
                'test_columns_1_and_2',
                lambda r,s: (s in r[1] and s in r[2]))
        """
        self.filterFunctions[name] = new_func
        self.invalidateFilter()

    def removeFilterFunction(self, name):
        """
        name : hashable object
        
        Removes the filter function associated with name,
        if it exists.
        """
        if name in self.filterFunctions.keys():
            del self.filterFunctions[name]
            self.invalidateFilter()

    def filterAcceptsRow(self, row_num, parent):
        """
        Reimplemented from base class to allow the use
        of custom filtering.
        """
        model = self.sourceModel()
        # The source model should have a method called row()
        # which returns the table row as a python list.
        tests = [func(model.row(row_num), self.filterString)
                 for func in self.filterFunctions.values()]
        return not False in tests
        
        
class OutlinerModel( QtCore.QAbstractItemModel ):
    '''A drag and drop enabled, editable, hierarchical item model.'''
     
    def __init__( self, root ):
        '''Instantiates the model with a root item.'''
        super( OutlinerModel, self ).__init__()
        self.root = root
         
    def itemFromIndex( self, index ):
        '''Returns the TreeItem instance from a QModelIndex.'''
        return index.internalPointer() if index.isValid() else self.root
         
    def rowCount( self, index ):
        '''Returns the number of children for the given QModelIndex.'''
        item = self.itemFromIndex( index )
        return item.numChildren()
     
    def columnCount( self, index ):
        '''This model will have only one column.'''
        return 1
     
    def flags( self, index ):
        '''Valid items are selectable, editable, and drag and drop enabled. Invalid indices (open space in the view)
        are also drop enabled, so you can drop items onto the top level.
        '''
        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsDropEnabled
         
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsDropEnabled | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable
        
    def supportedDropActions( self ):
        '''Items can be moved and copied (but we only provide an interface for moving items in this example.'''
        return QtCore.Qt.MoveAction | QtCore.Qt.CopyAction
     
    def headerData( self, section, orientation, role ):
        if role == QtCore.Qt.DisplayRole:
            if section == 0:
                return "Scenegraph"
            else:
                return "Typeinfo"
        
        
        
        '''
        if section == 0 and orientation == QtCore.Qt.Horizontal:
            if role == QtCore.Qt.DisplayRole:
                return 'Joints'
        return ""
        '''
     
    def data( self, index, role ):
        
        node = index.internalPointer()
        
        '''Return the display name of the PyNode from the item at the given index.'''
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            item = self.itemFromIndex( index )
            return item.displayName
        if role == QtCore.Qt.DecorationRole:
            if index.column() == 0:
                resource = node.resource()
                return QtGui.QIcon(QtGui.QPixmap(resource))
                             
    def setData( self, index, value, role ):
        '''Set the name of the PyNode from the item being edited.'''
        item = self.itemFromIndex( index )
        item.displayName = str( value.toString() )
        self.dataChanged.emit( QtCore.QModelIndex(), QtCore.QModelIndex() )
        return True
         
    def index( self, row, column, parentIndex ):
        '''Creates a QModelIndex for the given row, column, and parent.'''
        if not self.hasIndex( row, column, parentIndex ):
            return QtCore.QModelIndex()
             
        parent = self.itemFromIndex( parentIndex )
        return self.createIndex( row, column, parent.childAtRow( row ) )
     
    def parent( self, index ):
        '''Returns a QMoelIndex for the parent of the item at the given index.'''
        item = self.itemFromIndex( index )
        parent = item.parent
        if parent == self.root:
            return QtCore.QModelIndex()
        return self.createIndex( parent.row(), 0, parent )
     
    def insertRows( self, row, count, parentIndex ):
        '''Add a number of rows to the model at the given row and parent.'''
        self.beginInsertRows( parentIndex, row, row+count-1 )
        self.endInsertRows()
        return True
     
    def removeRows( self, row, count, parentIndex ):
        '''Remove a number of rows from the model at the given row and parent.'''
        self.beginRemoveRows( parentIndex, row, row+count-1 )
        parent = self.itemFromIndex( parentIndex )
        for x in range( count ):
            parent.removeChildAtRow( row )
        self.endRemoveRows()
        return True
     
     
    def mimeData( self, indices ):
        '''Encode serialized data from the item at the given index into a QMimeData object.'''
        data = ''
        item = self.itemFromIndex( indices[0] )
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
        dropParent = self.itemFromIndex( parentIndex )
        dropParent.addChild( item )
        self.insertRows( dropParent.numChildren()-1, 1, parentIndex )
        self.dataChanged.emit( parentIndex, parentIndex )
        return True        
        