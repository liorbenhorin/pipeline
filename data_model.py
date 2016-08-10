from PySide import QtCore, QtGui
import cPickle

import config as cfg
reload(cfg)

class List_Model(QtCore.QAbstractListModel):

    MIMEDATA = 'application/x-qabstractitemmodeldatalist'

    def __init__(self, items = [], parent = None):
        QtCore.QAbstractListModel.__init__(self, parent)
        self.__items = items

    @property
    def items(self):
        return self.__items

    def rowCount(self, parent):
        return len(self.__items)


    def data(self, index, role):


        if role == QtCore.Qt.EditRole:
            return self.__items[index.row()].name


        if role == QtCore.Qt.DecorationRole:
            resource = self.__items[index.row()].resource
            return QtGui.QIcon(QtGui.QPixmap(resource))

        if role == QtCore.Qt.DisplayRole:

            row = index.row()
            return self.__items[row].name


    def flags(self, index):

        if index.isValid():
            return  QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    """CUSTOM"""
    """INPUTS: QModelIndex"""
    def getNode(self, index):
        if index.isValid():
            return self.__items[index.row()]

        return None

    def setData(self, index, value, role = QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:

            row = index.row()

            if role == QtCore.Qt.EditRole:
                self.__items[row].name = value
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
            value = self.__items[position]
            self.__items.remove(value)

        self.endRemoveRows()
        return True

class Project_Model(QtCore.QAbstractItemModel):

    MIMEDATA = 'application/x-qabstractitemmodeldatalist'
    sortRole   = QtCore.Qt.UserRole
    filterRole = QtCore.Qt.UserRole + 1
    expendedRole = QtCore.Qt.UserRole + 2

    """INPUTS: Node, QObject"""
    def __init__(self, root, parent=None):
        super(Project_Model, self).__init__(parent)
        self._rootNode = root
        self._tempIndex = None

    def staticIndex(self, index):
        return QtCore.QPersistentModelIndex(index)


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
        return 2



    """INPUTS: QModelIndex, int"""
    """OUTPUT: QVariant, strings are cast to QString which is a QVariant"""
    def data(self, index, role):

        if not index.isValid():
            return None

        node = index.internalPointer()


        if role == QtCore.Qt.SizeHintRole:
            return QtCore.QSize(40, 22)

        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:

            return node.data(index.column())


        if role == QtCore.Qt.ForegroundRole:

                if node._virtual or node._deathrow:
                    return QtGui.QColor(150,150,150)

                if node.typeInfo() == cfg._stage_:
                    return QtGui.QColor("#afa0e7")


        if role == QtCore.Qt.FontRole:
            font = QtGui.QFont()

            if index.column() == 0:
                if node._virtual:
                    font.setItalic(True)
                    font.setBold(True)
                if node._deathrow:
                    font.setItalic(True)



            if index.column() == 1:
                font.setItalic(True)

            return font

        if role == QtCore.Qt.DecorationRole:
            if index.column() == 0:
                if not node._deathrow:
                    resource = node.resource
                    return QtGui.QIcon(QtGui.QPixmap(resource))
                else:
                    return QtGui.QIcon(QtGui.QPixmap(cfg.delete_folder_icon))


        if role == Project_Model.sortRole:
            return node.typeInfo()

        if role == Project_Model.filterRole:
            return node.typeInfo()

        # if role == QtCore.Qt.SizeHintRole:
        #     return QtCore.QSize(0,19)

        # this is for expending state - the result must be uniqe!!!
        if role == 165:
            return node.id

        if role == Project_Model.expendedRole:

            return self.isExpended(index)


    """INPUTS: QModelIndex, QVariant, int (flag)"""
    def setData(self, index, value, role=QtCore.Qt.EditRole):

        if index.isValid():

            node = index.internalPointer()

            if role == QtCore.Qt.EditRole:
                node.setData(index.column(), value)
                self.dataChanged.emit(index, index)
            if role == Project_Model.expendedRole:
                node.expendedState(self.isExpended(index))
                self.dataChanged.emit(index, index)
                return True

        return False


    """INPUTS: int, Qt::Orientation, int"""
    """OUTPUT: QVariant, strings are cast to QString which is a QVariant"""
    def headerData(self, section, orientation, role):

        # if role == QtCore.Qt.DecorationRole:
        #
        #     if section == 0:
        #         icon = QtGui.QIcon(cube_icon_full)
        #
        #         return icon


        if role == QtCore.Qt.SizeHintRole:
            return QtCore.QSize(40, 24)

        if role == QtCore.Qt.DisplayRole:
            if section == 0:
                return "Structure"
            elif section == 1:
                return "Level"

    """INPUTS: QModelIndex"""
    """OUTPUT: int (flag)"""



    """INPUTS: QModelIndex"""
    """OUTPUT: int (flag)"""
    def flags(self, index):

        if not index.isValid():

            return QtCore.Qt.ItemIsEnabled #| QtCore.Qt.ItemIsDropEnabled

        if index.isValid():
            node = self.getNode(index)
            if node._deathrow:
                return QtCore.Qt.NoItemFlags

            if node.typeInfo() == cfg._root_:
                return  QtCore.Qt.ItemIsEnabled |QtCore.Qt.ItemIsSelectable

            #if node.typeInfo() == _stage_:
            #    return  QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable #| QtCore.Qt.ItemIsEditable# | QtCore.Qt.ItemIsDropEnabled | QtCore.Qt.ItemIsDragEnabled |

    """INPUTS: QModelIndex"""
    """OUTPUT: QModelIndex"""
    """Should return the parent of the node with the given QModelIndex"""
    def parent(self, index):

        node = self.getNode(index)
        parentNode = node.parent()

        if parentNode == self._rootNode:
            return QtCore.QModelIndex()

        if parentNode:
            return self.createIndex(parentNode.row(), 0, parentNode)

        else:
            return QtCore.QModelIndex()

    """INPUTS: int, int, QModelIndex"""
    """OUTPUT: QModelIndex"""
    """Should return a QModelIndex that corresponds to the given row, column and parent node"""


    def index( self, row, column, parentIndex ):

        if not self.hasIndex( row, column, parentIndex ):
            return    QtCore.QModelIndex()

        parent = self.getNode( parentIndex )
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
    def insertRows(self, position, rows, parent=QtCore.QModelIndex(), node = None):
        parentNode = self.getNode(parent)

        self.beginInsertRows(parent, position, position + rows - 1)


        for row in range(rows):

            childCount = parentNode.childCount()
            childNode = node
            success = parentNode.insertChild(position, childNode)

        self.endInsertRows()
        return True


    def removeRows( self, row, count, parentIndex, **kwargs ):

        '''Remove a number of rows from the model at the given row and parent.'''
        self.beginRemoveRows( parentIndex, row, row+count-1 )
        parent = self.getNode( parentIndex )
        for x in range( count ):

            # remove rows is being called in every drop action,
            # we need to know if the remove is with the intention to actually delete the data in the nodes

            if "kill" in kwargs:
                if kwargs["kill"] == True:
                    parent.child(row).delete()


            parent.removeChild( row )
        self.endRemoveRows()
        self.dataChanged.emit( parentIndex, parentIndex )
        return True

    def supportedDropActions( self ):

        return  QtCore.Qt.CopyAction | QtCore.Qt.MoveAction


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
        mimedata.setData(Project_Model.MIMEDATA, data)

        return mimedata

    def dropMimeData( self, mimedata, action, row, column, parentIndex ):

        '''Handles the dropping of an item onto the model.

        De-serializes the data into a TreeItem instance and inserts it into the model.
        '''
        if not mimedata.hasFormat(Project_Model.MIMEDATA):
            return False

        item = cPickle.loads(str(mimedata.data(Project_Model.MIMEDATA)))
        dropParent = self.getNode( parentIndex )

        # do not allow a folder to be dropped on an asset...
        if dropParent.typeInfo() == cfg._asset_:
            if item.typeInfo() == cfg._folder_ or item.typeInfo() == cfg._asset_:
                return False

        if dropParent.typeInfo() == cfg._root_:
            return False


        #dropParent.addChild( item )
        self.insertRows( dropParent.childCount(), 1, parent = parentIndex , node = item)

        self.dataChanged.emit( parentIndex, parentIndex )

        return True


    def indexFromNode(self, node, rootIndex):
        '''
        recursive function to get Index from a node,
        we use a unique node id to do this
        the id is stored as a UserRole int 165

        '''
        def rec(d, index):

            for row in range(self.rowCount(index)):


                i = self.index(row,0, index)
                id = self.data(i, 165)
                if id == node.id:
                    d.append(i)
                else:
                    pass

                rec(d, i)


        data = []
        rec(data, rootIndex)
        if len(data)>0:
            return data[0]
        else:
            # if the node is not in the tree return an empty index
            return QtCore.QModelIndex()

    def listAncestos(self, index):
        '''
        returns a list of all parents all the way to the top level, from the given index
        '''
        def rec(d, index):

            i = self.parent(index)
            if i != QtCore.QModelIndex():
                d.append(self.parent(index))
                rec(d, i)
            else:
                return

        data = [index]
        #for i in range(self.rowCount(index)):
        #    data.append(self.index(i, 0, index))

        rec(data, index)
        if len(data)>0:
            return data
        else:
            # if the node is not in the tree return an empty index
            return [QtCore.QModelIndex()]


    def listHierarchy(self, index):
        '''
        returns a flat list of all descending childs from the given index
        '''
        def rec(d, index):

            if self.rowCount(index)>0:

                for row in range(self.rowCount(index)):

                    i = self.index(row,0, index)
                    d.append(i)
                    rec(d, i)
            else:
                 pass

        data = [index]
        rec(data, index)
        return data

class Dresser_Model(Project_Model):

    """INPUTS: Node, QObject"""
    def __init__(self, root, parent=None):
        super(Dresser_Model, self).__init__(root, parent )


    """INPUTS: QModelIndex, int"""
    """OUTPUT: QVariant, strings are cast to QString which is a QVariant"""
    def data(self, index, role):

        if not index.isValid():
            return None

        node = index.internalPointer()


        if role == QtCore.Qt.SizeHintRole:
            return QtCore.QSize(40, 22)

        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:

            return node.data(index.column())


        if role == QtCore.Qt.ForegroundRole:

                if node._virtual or node._deathrow:
                    return QtGui.QColor(150,150,150)

                if node.typeInfo() == cfg._stage_:
                    return QtGui.QColor("#afa0e7")


        if role == QtCore.Qt.FontRole:
            font = QtGui.QFont()

            if index.column() == 0:
                if node._virtual:
                    font.setItalic(True)
                    font.setBold(True)
                if node._deathrow:
                    font.setItalic(True)



            if index.column() == 1:
                font.setItalic(True)

            return font

        if role == QtCore.Qt.DecorationRole:
            if index.column() == 0:
                if node.typeInfo() == cfg._stage_:
                    resource = node.thumbnail
                    return QtGui.QIcon(QtGui.QPixmap(resource))

                if not node._deathrow:
                    resource = node.resource
                    return QtGui.QIcon(QtGui.QPixmap(resource))

                else:
                    return QtGui.QIcon(QtGui.QPixmap(cfg.delete_folder_icon))


        if role == Project_Model.sortRole:
            return node.typeInfo()

        if role == Project_Model.filterRole:
            return node.typeInfo()

        # if role == QtCore.Qt.SizeHintRole:
        #     return QtCore.QSize(0,19)

        # this is for expending state - the result must be uniqe!!!
        if role == 165:
            return node.id

        if role == Project_Model.expendedRole:

            return self.isExpended(index)


    """INPUTS: int, Qt::Orientation, int"""
    """OUTPUT: QVariant, strings are cast to QString which is a QVariant"""
    def headerData(self, section, orientation, role):


        if role == QtCore.Qt.SizeHintRole:
            return QtCore.QSize(40, 24)

        if role == QtCore.Qt.DisplayRole:
            if section == 0:
                return "Assets"
            elif section == 1:
                return "Level"

class Versions_Model(Project_Model):


    """INPUTS: Node, QObject"""
    def __init__(self, root, parent=None):
        super(Versions_Model, self).__init__(root, parent)

    """INPUTS: QModelIndex"""
    """OUTPUT: int"""
    def columnCount(self, parent):
        return 6

    """INPUTS: QModelIndex, int"""
    """OUTPUT: QVariant, strings are cast to QString which is a QVariant"""
    def data(self, index, role):

        if not index.isValid():
            return None

        node = index.internalPointer()

        if role == QtCore.Qt.SizeHintRole:
            return QtCore.QSize(40,self._rowHeight)

        if role == QtCore.Qt.EditRole:
            if node.typeInfo() != cfg._new_:
                if index.column() == 0:
                    return node.fullName
                if index.column() == 1:
                    return node.author
                if index.column() == 2:
                    return node.note

            return node.data(index.column())

        if role == QtCore.Qt.DisplayRole:
            if node.typeInfo() != cfg._new_:
                if index.column() == 1:
                    return node.number

                if index.column() == 2:
                    return node.author

                if index.column() == 3:
                    return node.date

        if role == QtCore.Qt.DecorationRole:
            if index.column() == 0:
                resource = node.resource
                return QtGui.QIcon(QtGui.QPixmap(resource))

            if node.typeInfo() != cfg._new_:

                if index.column() == 4:
                    resource = node.note_decoration
                    return QtGui.QIcon(QtGui.QPixmap(resource))

        if role == Versions_Model.sortRole:
            return node.number

        if role == Versions_Model.filterRole:
            return node.number

        if role == QtCore.Qt.SizeHintRole:
            return QtCore.QSize(0,19)

        # this is for expending state - the result must be uniqe!!!
        if role == 165:
            return node.id

        if role == Project_Model.expendedRole:

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
            if role == Project_Model.expendedRole:
                node.expendedState(self.isExpended(index))
                self.dataChanged.emit(index, index)
                return True

        return False


    """INPUTS: QModelIndex"""
    """OUTPUT: int (flag)"""
    def flags(self, index):

        if not index.isValid():

            return QtCore.Qt.ItemIsEnabled #| QtCore.Qt.ItemIsDropEnabled

        if index.isValid():
            node = self.getNode(index)

            if node.typeInfo() == cfg._root_:
                return  QtCore.Qt.ItemIsEnabled |QtCore.Qt.ItemIsSelectable

            #if node.typeInfo() == _stage_:
            #    return  QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable #| QtCore.Qt.ItemIsEditable# | QtCore.Qt.ItemIsDropEnabled | QtCore.Qt.ItemIsDragEnabled |

class Masters_Model(Project_Model):


    """INPUTS: Node, QObject"""
    def __init__(self, root, parent=None):
        super(Masters_Model, self).__init__(root, parent)


    """INPUTS: QModelIndex"""
    """OUTPUT: int"""
    def columnCount(self, parent):
        return 7



    """INPUTS: QModelIndex, int"""
    """OUTPUT: QVariant, strings are cast to QString which is a QVariant"""
    def data(self, index, role):

        if not index.isValid():
            return None

        node = index.internalPointer()

        if role == QtCore.Qt.SizeHintRole:
            return QtCore.QSize(40,self._rowHeight)

        if role == QtCore.Qt.EditRole:
            if node.typeInfo() != cfg._new_:
                if index.column() == 0:
                    return node.fullName
                if index.column() == 1:
                    return node.author
                if index.column() == 2:
                    return node.note

            return node.data(index.column())

        if role == QtCore.Qt.DisplayRole:
            if node.typeInfo() != cfg._new_:
                if index.column() == 1:
                    return node.name

                if index.column() == 2:
                    return node.author

                if index.column() == 3:
                    return node.date
                if index.column() == 4:
                    if isinstance(node.origin, list):
                        return "Origin @ {0} {1}".format(node.origin[0], node.origin[1])
                    else:
                        return "Origin @ n/a"

        if role == QtCore.Qt.DecorationRole:
            if index.column() == 0:
                resource = node.resource
                return QtGui.QIcon(QtGui.QPixmap(resource))
            if index.column() == 1:
                if not isinstance(node.name, int):
                    resource = node.master_icon
                    return QtGui.QIcon(QtGui.QPixmap(resource))

            if node.typeInfo() != cfg._new_:

                if index.column() == 5:
                    resource = node.note_decoration
                    return QtGui.QIcon(QtGui.QPixmap(resource))

        if role == Versions_Model.sortRole:
            return node.number

        if role == Versions_Model.filterRole:
            return node.number

        if role == QtCore.Qt.SizeHintRole:
            return QtCore.QSize(0,19)

        # this is for expending state - the result must be uniqe!!!
        if role == 165:
            return node.id

        if role == Project_Model.expendedRole:

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
            if role == Project_Model.expendedRole:
                node.expendedState(self.isExpended(index))
                self.dataChanged.emit(index, index)
                return True

        return False




    """INPUTS: QModelIndex"""
    """OUTPUT: int (flag)"""
    def flags(self, index):

        if not index.isValid():

            return QtCore.Qt.ItemIsEnabled #| QtCore.Qt.ItemIsDropEnabled

        if index.isValid():
            node = self.getNode(index)

            if node.typeInfo() == cfg._root_:
                return  QtCore.Qt.ItemIsEnabled |QtCore.Qt.ItemIsSelectable

            #if node.typeInfo() == _stage_:
            #    return  QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable #| QtCore.Qt.ItemIsEditable# | QtCore.Qt.ItemIsDropEnabled | QtCore.Qt.ItemIsDragEnabled |

class Projects_Model(QtCore.QAbstractTableModel):

    # MIMEDATA = 'application/x-qabstractitemmodeldatalist'

    def __init__(self, items = [], parent = None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.__items = items

    @property
    def items(self):
        return self.__items

    def headerData(self, section, orientation, role):

        if role == QtCore.Qt.DisplayRole:

            if orientation == QtCore.Qt.Horizontal:
                if section == 0:
                    return "Name"



    def rowCount(self, parent):
        return len(self.__items)

    def columnCount(self, parent):
        return 3

    def data(self, index, role):


        if role == QtCore.Qt.EditRole:
            row = index.row()
            if self.__items[row].typeInfo() != cfg._new_:
                row = index.row()
                if index.column() == 0:
                    return self.__items[row].name

            return self.__items[index.row()].name


        if role == QtCore.Qt.DecorationRole:
            row = index.row()
            if self.__items[row].typeInfo() != cfg._new_:
                if index.column() == 0:
                    resource = self.__items[index.row()].resource
                    return QtGui.QIcon(QtGui.QPixmap(resource))

        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            if self.__items[row].typeInfo() != cfg._new_:
                if index.column() == 0:
                    return self.__items[row].name


    def index(self, row, column, parent):
        if not self.hasIndex(row, column):
            return QtCore.QModelIndex()

        return self.createIndex(row, column)

    def flags(self, index):

        if index.isValid():

            if self.getNode(index).typeInfo() == cfg._dummy_:
                return QtCore.Qt.NoItemFlags

        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDropEnabled | QtCore.Qt.ItemIsDragEnabled

    """CUSTOM"""
    """INPUTS: QModelIndex"""
    def getNode(self, index):
        if index.isValid():
            return self.__items[index.row()]

        return None

    def setData(self, index, value, role = QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:

            row = index.row()

            if role == QtCore.Qt.EditRole:
                self.__items[row].name = value
                self.dataChanged.emit(index, index)

                return True


        return False

    #=====================================================#
    #INSERTING & REMOVING
    #=====================================================#
    def insertRows(self, position, rows, parent = QtCore.QModelIndex(), node = None):
        self.beginInsertRows(parent, position, position + rows - 1)
        if node:
            self.__items.insert(position, node)
        self.endInsertRows()

        return True

    def removeRows(self, position, rows, parent = QtCore.QModelIndex()):
        self.beginRemoveRows(parent, position, position + rows - 1)

        for i in range(rows):
            value = self.__items[position]
            self.__items.remove(value)

        self.endRemoveRows()
        return True

class Levels_Model(Projects_Model):

    # MIMEDATA = 'application/x-qabstractitemmodeldatalist'

    def __init__(self, items = [], parent = None):
        super(Levels_Model, self).__init__(items, parent)
        # QtCore.QAbstractTableModel.__init__(self, parent)
        self.__items = items


    def headerData(self, section, orientation, role):

        if role == QtCore.Qt.DisplayRole:

            if orientation == QtCore.Qt.Horizontal:
                if section == 0:
                    return "Section"
                else:
                    return "{0} {1}".format("level", str(section))
            else:
                return



    def columnCount(self, parent):
        return 7

    def data(self, index, role):
        row = index.row()

        if role == QtCore.Qt.EditRole:
            if len(self.__items[row]._levels) > index.column()-1:
                if self.__items[row]._levels[index.column()-1] != "":
                    return self.__items[row]._levels[index.column()-1]
                else:
                    return "n/a"
            else:
                return "n/a"


        if role == QtCore.Qt.DecorationRole:
            if index.column() == 0:
                resource = self.__items[index.row()].resource
                return QtGui.QIcon(QtGui.QPixmap(resource))

        if role == QtCore.Qt.DisplayRole:


            if index.column() == 0:
                return self.__items[row].name

            else:
                if len(self.__items[row]._levels) > index.column() - 1:
                    if self.__items[row]._levels[index.column()-1] != "":
                        return self.__items[row]._levels[index.column()-1]

            #return "n/a"

    def flags(self, index):

        if index.isValid():

            if index.column() == 0:
                return QtCore.Qt.ItemIsEnabled

            return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable



    def setData(self, index, value, role = QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:

            row = index.row()
            column = index.column()
            if role == QtCore.Qt.EditRole:
                if column == 0:
                    self.__items[row].name = value
                    self.dataChanged.emit(index, index)

                    return True
                else:
                    self.__items[row]._levels[column-1] = value
                    self.dataChanged.emit(index, index)

                    return True


        return False

class Stages_Model(Projects_Model):

    def __init__(self, items = [], parent = None):

        super(Stages_Model, self).__init__(items, parent)
        self.__items = items


    def headerData(self, section, orientation, role):

        if role == QtCore.Qt.DisplayRole:

            if orientation == QtCore.Qt.Horizontal:
                if section == 0:
                    return "Section"
                else:
                    return "{0} {1}".format("Stage", str(section))
            else:
                return

    def columnCount(self, parent):
        return 7

    def data(self, index, role):
        row = index.row()

        if role == QtCore.Qt.EditRole:
            if len(self.__items[row]._levels) > index.column()-1:
                if self.__items[row]._levels[index.column()-1] != "":
                    return self.__items[row]._levels[index.column()-1]
                else:
                    return "n/a"
            else:
                return "n/a"


        if role == QtCore.Qt.DecorationRole:
            if index.column() == 0:
                resource = self.__items[index.row()].resource
                return QtGui.QIcon(QtGui.QPixmap(resource))

        if role == QtCore.Qt.DisplayRole:


            if index.column() == 0:
                return self.__items[row].name

            else:
                if len(self.__items[row]._levels) > index.column() - 1:
                    if self.__items[row]._levels[index.column()-1] != "":
                        return self.__items[row]._levels[index.column()-1]

            #return "n/a"

    def flags(self, index):

        if index.isValid():

            if index.column() == 0:
                return QtCore.Qt.ItemIsEnabled

            return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def setData(self, index, value, role = QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:

            row = index.row()
            column = index.column()
            if role == QtCore.Qt.EditRole:
                if column == 0:
                    self.__items[row].name = value
                    self.dataChanged.emit(index, index)

                    return True
                else:
                    self.__items[row]._levels[column-1] = value
                    self.dataChanged.emit(index, index)

                    return True


        return False

class Users_Model(Projects_Model):


    def __init__(self, items = [], parent = None):
        super(Users_Model, self).__init__(items, parent)
        self.__items = items


    def headerData(self, section, orientation, role):

        if role == QtCore.Qt.DisplayRole:

            if orientation == QtCore.Qt.Horizontal:
                if section == 0:
                    return "Username"
                if section == 1:
                    return "Password"
                if section == 2:
                    return "Role"

            if orientation == QtCore.Qt.Vertical:
                item = self.__items[section]
                return self.__items.index(item)

    def columnCount(self, parent):
        return 3

    def data(self, index, role):
        row = index.row()

        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:

            if index.column() == 0:
                return self.__items[row].name
            if index.column() == 1:
                return self.__items[row]._password
            if index.column() == 2:
                return self.__items[row]._role


    def flags(self, index):

        if index.isValid():

            return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def setData(self, index, value, role = QtCore.Qt.EditRole):

        row = index.row()
        column = index.column()
        if role == QtCore.Qt.EditRole:

            if column == 0:
                self.__items[row].name = value
                self.dataChanged.emit(index, index)

                return True
            if column == 1:
                self.__items[row]._password = value
                self.dataChanged.emit(index, index)

                return True
            if column == 2:
                self.__items[row]._role = value
                self.dataChanged.emit(index, index)

                return True


        return False

class Project_ProxyModel(QtGui.QSortFilterProxyModel):
    def __init__(self,parent = None):
        
        super(Project_ProxyModel, self).__init__(parent)
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

        if super(Project_ProxyModel, self).filterAcceptsRow(sourceRow, sourceParent):


            #if self.sourceModel().getNode(id).typeInfo() == _stage_:
            #    return False

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

        super(Project_ProxyModel, self).setFilterRegExp(exp)
        if self.treeView:


            if len(exp)>0:
                '''
                i dont need to read the tree in each text change
                only once
                ----> this can be more elegant
                '''
                if len(exp) == 1:
                    self.treeView.list_flat_hierarchy()

                self.treeView.filterContents()

                self.treeView._ignoreExpentions = True
                self.treeView.expandAll()
                self.treeView._ignoreExpentions = False
            else:
                self.treeView._ignoreExpentions = True
                self.treeView.restoreState()
                self.treeView._ignoreExpentions = False

class Simple_ProxyModel(QtGui.QSortFilterProxyModel):
    def __init__(self, parent = None):
        super(Simple_ProxyModel, self).__init__(parent)

        self.setDynamicSortFilter(True)
        self.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.setSortRole(0)
        self.setFilterRole(0)
        self.setFilterKeyColumn(0)

class Versions_ProxyModel(Simple_ProxyModel):
    def __init__(self, parent=None):
        super(Versions_ProxyModel, self).__init__(parent)

    def filterAcceptsRow(self, sourceRow, sourceParent):
        # hide components from the treeview
        id = self.sourceModel().index(sourceRow, 0, sourceParent)

        if super(Versions_ProxyModel, self).filterAcceptsRow(sourceRow, sourceParent):

             if self.sourceModel().getNode(id).typeInfo() == cfg._version_ or self.sourceModel().getNode(id).typeInfo() == cfg._new_:
                    return True

             return False

class Projects_ProxyModel(Simple_ProxyModel):
    def __init__(self, parent=None):
        super(Projects_ProxyModel, self).__init__(parent)

class Masters_ProxyModel(Simple_ProxyModel):
    def __init__(self, parent=None):
        super(Masters_ProxyModel, self).__init__(parent)


    def filterAcceptsRow(self, sourceRow, sourceParent):
        # hide components from the treeview
        id = self.sourceModel().index(sourceRow, 0, sourceParent)

        if super(Masters_ProxyModel, self).filterAcceptsRow(sourceRow, sourceParent):

             if self.sourceModel().getNode(id).typeInfo() == cfg._master_:
                    return True

             return False




   