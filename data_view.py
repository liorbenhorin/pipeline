
from PySide import QtCore, QtGui, QtXml
import cPickle
import os
import functools

import config as cfg
reload(cfg)

import data as dt
reload(dt)

import data_model as dtm
reload(dtm)

import modules.files as files

import modules.jsonData as data

import dialogue as dlg


global counter


def setComboValue(QComboBox, String):
    index = QComboBox.findText(String, QtCore.Qt.MatchFixedString)
    if index >= 0:
        QComboBox.setCurrentIndex(index)
        return True
    return False


def remap_value(x, oMin, oMax, nMin, nMax):

    #range check
    if oMin == oMax:
        print "Warning: Zero input range"
        return None

    if nMin == nMax:
        print "Warning: Zero output range"
        return None

    #check reversed input range
    reverseInput = False
    oldMin = min( oMin, oMax )
    oldMax = max( oMin, oMax )
    if not oldMin == oMin:
        reverseInput = True

    #check reversed output range
    reverseOutput = False
    newMin = min( nMin, nMax )
    newMax = max( nMin, nMax )
    if not newMin == nMin :
        reverseOutput = True

    portion = (x-oldMin)*(newMax-newMin)/(oldMax-oldMin)
    if reverseInput:
        portion = (oldMax-x)*(newMax-newMin)/(oldMax-oldMin)

    result = portion + newMin
    if reverseOutput:
        result = newMax - portion

    return result

class RoleComboBoxDelegate(QtGui.QItemDelegate):

    def __init__(self, parent):
        QtGui.QItemDelegate.__init__(self, parent)
        self.cb = None

    def createEditor(self, parent, option, index):

        cb = QtGui.QComboBox(parent)
        roles = [cfg._admin_,cfg._super_,cfg._standard_]
        cb.addItems(roles)
        return cb

    def setEditorData(self, editor, index):
            cb = editor
            string = index.data(QtCore.Qt.EditRole)
            i = cb.findText(string)
            if i>= 0:
                cb.setCurrentIndex(i)
            else:
                cb.setCurrentIndex(0)

    def setModelData(self, editor, model, index ):
        cb = editor
        model.setData(index, cb.currentText(), QtCore.Qt.EditRole)

class EditProjectButtonDelegate(QtGui.QItemDelegate):

    def __init__(self, parent):
        QtGui.QItemDelegate.__init__(self, parent)

    def paint(self, painter, option, index):

        if not self.parent().indexWidget(index):


            label = "Edit"
            icon = cfg.edit_icon


            button = QtGui.QPushButton(
                label,
                index.data(),
                self.parent(),
                clicked=self.parent().editProject
            )

            button.setIconSize(QtCore.QSize(20, 20))
            button.setIcon(QtGui.QIcon(icon))
            self.parent().setIndexWidget(index, button)

class SetProjectButtonDelegate(QtGui.QItemDelegate):

    def __init__(self, parent):
        QtGui.QItemDelegate.__init__(self, parent)

    def paint(self, painter, option, index):

        if not self.parent().indexWidget(index):


            label = "Set project"
            icon = cfg.set_icon


            button = QtGui.QPushButton(
                label,
                index.data(),
                self.parent(),
                clicked=self.parent().setProject
            )

            button.setIconSize(QtCore.QSize(20, 20))
            button.setIcon(QtGui.QIcon(icon))
            self.parent().setIndexWidget(index, button)

class Project_Levels_View(QtGui.QTableView):
    def __init__(self, parent = None):
        super(Project_Levels_View, self).__init__(parent)

        self.verticalHeader().setHidden(True)
        self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)

    def setModel(self, model = None):
        super(Project_Levels_View, self).setModel(model)

        self.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)

class Project_Users_View(QtGui.QTableView):
    def __init__(self, parent = None):
        super(Project_Users_View, self).__init__(parent)

        self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)

    def setModel(self, model = None):
        super(Project_Users_View, self).setModel(model)
        self.setItemDelegateForColumn(2, RoleComboBoxDelegate(self))
        self.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)

    def contextMenuEvent(self, event):

        index = self.indexAt(event.pos())
        menu = QtGui.QMenu()

        actions = []
        actions.append(QtGui.QAction("New user", menu, triggered=functools.partial(self.new_user, index)))
        actions.append(QtGui.QAction("Import users from a json file", menu, triggered = self.import_users ))

        if index.isValid():
            actions.append(QtGui.QAction("Remove user", menu, triggered=functools.partial(self.remove_user, index)))
        menu.addActions(actions)

        menu.exec_(event.globalPos())
        event.accept()  # TELL QT IVE HANDLED THIS THING
        return

    def remove_user(self, index):
        row = index.row()
        parent = index.parent()
        self.model().removeRows(row, 1, parent)

    def new_user(self, index):
        user = dt.UserNode("New user", "1234", cfg._admin_)
        if index.isValid():
            row = index.row()
        else:
            row = len(self.model().items)

        self.model().insertRows(row+1,1,QtCore.QModelIndex(),node = user)

    def import_users(self):
        path = QtGui.QFileDialog.getOpenFileName(self, "Select the users file", filter="json files (*.json)")
        if path[0]:
            users_file = data.jsonDict(path=str(path[0]))
            users_file = users_file.read()
            print users_file, "="
            self.setModel(None)
            users = []
            for key in users_file:
                users.append(dt.UserNode(key, users_file[key][0], users_file[key][1]))

            if users:
                self.setModel(dtm.Users_Model(users))


class Projects_View(QtGui.QTableView):
    def __init__(self, parentWidget = None, parent = None):
        super(Projects_View, self).__init__(parent)

        self.parent = parent
        self.parentWidget = parentWidget

        self.setAlternatingRowColors(True)
        self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.setWordWrap(True)
        self.verticalHeader().setResizeMode(QtGui.QHeaderView.Fixed)
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.horizontalHeader().hide()
        self.verticalHeader().hide()
        self.setSortingEnabled(True)

        # Set the delegate for column 0 of our table
        self._proxyModel = None

    def addSlider(self):

        self._slider = IconScaleSlider(self)
        self.parentWidget.layout().addWidget(self._slider)
        self._slider.listSlider.sliderMoved.connect(self.icons_size)
        self.icons_size(32)

    def icons_size(self, int):
        self.setIconSize(QtCore.QSize(int, int))
        self.update()

    def clearModel(self):
        self.setModel(None)
        if self._proxyModel:
            self._proxyModel.setSourceModel(None)
            self._proxyModel = None


    def setModel_(self, model = None):
        self.clearModel()
        if model:


            self._proxyModel = dtm.Projects_ProxyModel()
            self._proxyModel.setSourceModel(model)
            self.setModel(self._proxyModel)
            # size the load button column
            self.horizontalHeader().resizeSection(2,100)
            self.horizontalHeader().setResizeMode(2,QtGui.QHeaderView.Fixed)
            self.horizontalHeader().resizeSection(1, 100)
            self.horizontalHeader().setResizeMode(1, QtGui.QHeaderView.Fixed)
            self.horizontalHeader().setResizeMode(0,QtGui.QHeaderView.Stretch)


            # setup the buttons for loading and more options with delegates
            self.setItemDelegateForColumn(1, EditProjectButtonDelegate(self))
            self.setItemDelegateForColumn(2,  SetProjectButtonDelegate(self))


            self.setCurrentIndex(self.model().sourceModel().index(0, 0, None))

            return True

        self.setModel(None)
        return None
            #self.setCurrentIndex(self.model().index(0,0, None))


    def editProject(self):
        button = self.sender()
        index = self.indexAt(button.pos())
        index = self.model().mapToSource(index)
        if self.model().sourceModel().items[0].typeInfo() == cfg._new_:
            self.model().sourceModel().items[0].parent().initialVersion()
        else:
            self.model().sourceModel().getNode(index).edit()
            self.setCurrentIndex(index)

    def setProject(self):

        button = self.sender()
        index = self.indexAt(button.pos())
        index = self.model().mapToSource(index)
        if self.model().sourceModel().items[0].typeInfo() == cfg._new_:
            self.model().sourceModel().items[0].parent().initialVersion()
        else:
            self.model().sourceModel().getNode(index).set()
            self.setCurrentIndex(index)


class loadButtonDelegate(QtGui.QItemDelegate):
    """
    A delegate that places a fully functioning QPushButton in every
    cell of the column to which it's applied
    """
    def __init__(self, parent):
        # The parent is not an optional argument for the delegate as
        # we need to reference it in the paint method (see below)
        QtGui.QItemDelegate.__init__(self, parent)
 
    def paint(self, painter, option, index):
        # This method will be called every time a particular cell is
        # in view and that view is changed in some way. We ask the 
        # delegates parent (in this case a table view) if the index
        # in question (the table cell) already has a widget associated 
        # with it. If not, create one with the text for this index and
        # connect its clicked signal to a slot in the parent view so 
        # we are notified when its used and can do something. 
        if not self.parent().indexWidget(index):
            soure_index = self.parent().model().mapToSource(index)
            if self.parent().model().sourceModel().getNode(soure_index).typeInfo() == cfg._new_:
                label = ""
                icon = cfg.new_icon
            else:
                label = ""
                icon = cfg.open_icon

            button = QtGui.QPushButton(
                label,
                self.parent(),
                clicked=self.parent().MultiButtonClicked
            )

            button.setIconSize(QtCore.QSize(20, 20))

            button.setIcon(QtGui.QIcon(icon))

            self.parent().setIndexWidget(index, button)

class Versions_View(QtGui.QTreeView):
    def __init__(self, parentWidget = None, parent = None):
        super(Versions_View, self).__init__(parent)

        self.parent = parent
        self.parentWidget = parentWidget

        self.setAlternatingRowColors(True)
        self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.setWordWrap(True)

        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

        self.setSortingEnabled(True)
        self.setMouseTracking(True)

        # Set the delegate for column 0 of our table
        self._proxyModel = None
        self.header().setHidden(True)
        self.setStyleSheet('''

            QTreeView::item:hover {
                background: #101010;
            }
            QTreeView {
                outline: 0;
            }
            ''')

    def addSlider(self):

        self._slider = IconScaleSlider(self)
        self.parentWidget.layout().addWidget(self._slider)
        self._slider.listSlider.sliderMoved.connect(self.icons_size)
        self.icons_size(32)


    def icons_size(self, int):
        self.setIconSize(QtCore.QSize(int, int))
        self.header().resizeSection(0, int)
        self.header().setResizeMode(0, QtGui.QHeaderView.Fixed)
        try:
            self.model().sourceModel()._rowHeight = int
        except:
            pass
        self.update()

    def clearModel(self):
        self.setModel(None)
        if self._proxyModel:
            self._proxyModel.setSourceModel(None)
            self._proxyModel = None


    def setModel_(self, model = None):
        self.clearModel()
        if model:

            model._rowHeight = self._slider.listSlider.value()
            self._proxyModel = dtm.Versions_ProxyModel()
            self._proxyModel.setSourceModel(model)

            self._proxyModel.setDynamicSortFilter(True)
            self._proxyModel.setSortRole(dtm.Versions_Model.sortRole)
            self.setModel(self._proxyModel)

            self.setIndentation(0)

            self.proxyModel = self.model()
            self.sourceModel = self.proxyModel.sourceModel()

            self.header().resizeSection(0, self._slider.listSlider.value())
            self.header().setResizeMode(0, QtGui.QHeaderView.Fixed)
            self.header().resizeSection(1, 32)
            self.header().setResizeMode(1, QtGui.QHeaderView.Fixed)

            self.header().setStretchLastSection(False)
            self.header().setResizeMode(2, QtGui.QHeaderView.Stretch)
            self.header().setResizeMode(3, QtGui.QHeaderView.Stretch)

            self.header().resizeSection(4, 32)
            self.header().setResizeMode(4, QtGui.QHeaderView.Fixed)
            self.header().resizeSection(5, 32)
            self.header().setResizeMode(5, QtGui.QHeaderView.Fixed)

            # setup the buttons for loading and more options with delegates
            self.setItemDelegateForColumn(5,  loadButtonDelegate(self))
            self.sortByColumn(1, QtCore.Qt.DescendingOrder)

            self.update()

    def MultiButtonClicked(self):
        # This slot will be called when our button is clicked.
        # self.sender() returns a refence to the QPushButton created
        # by the delegate, not the delegate itself.
        button = self.sender()
        index = self.indexAt(button.pos())
        index = self.model().mapToSource(index)
        if self.model().sourceModel().getNode(index).typeInfo() == cfg._new_:
            node = self.model().sourceModel().getNode(index).parent()
            node.initialVersion()
            self._proxyModel.invalidate()

        else:
            self.model().sourceModel().getNode(index).load()
            self.parent.set_thumbnail(self.model().sourceModel().getNode(index).resource)
            self.parent.version = self.model().sourceModel().getNode(index)
            self.setCurrentIndex(self.model().mapFromSource(index))

    def contextMenuEvent(self, event):

        handled = True
        index = self.indexAt(event.pos())
        menu = QtGui.QMenu()
        node = None

        if index.isValid():
            src = self.asModelIndex(index)
            node = self.asModelNode(src)

        actions = []

        if node and not node._deathrow:

            if node.typeInfo() == cfg._version_:

                actions.append(QtGui.QAction("Explore...", menu,
                                             triggered=functools.partial(self.explore, src)))
            else:

                event.accept()
                return

        else:
            event.accept()
            return

        menu.addActions(actions)

        menu.exec_(event.globalPos())
        event.accept()

        return

    def explore(self, index):
        node = self.asModelNode(index)
        node.explore()


    def deletActionClicked(self):
        # This slot will be called when our button is clicked.
        # self.sender() returns a refence to the QPushButton created
        # by the delegate, not the delegate itself.
        button = self.sender().parent()
        index = self.indexAt(button.pos())
        index = self.model().mapToSource(index)
        self.model().sourceModel().getNode(index).delete_me()

    def asModelIndex(self, index):
        return self.proxyModel.mapToSource(index)

    def asModelNode(self, index):
        return self.sourceModel.getNode(index)


    @property
    def proxyModel(self):
        return self._proxyModel

    @proxyModel.setter
    def proxyModel(self, model):
        self._proxyModel = model

    @property
    def sourceModel(self):
        return self._sourceModel

    @sourceModel.setter
    def sourceModel(self, model):
        self._sourceModel = model



class Masters_View(Versions_View):
    def __init__(self, parentWidget = None, parent = None):
        super(Masters_View, self).__init__(parentWidget, parent)


    def setModel_(self, model = None):
        self.clearModel()
        if model:

            model._rowHeight = self._slider.listSlider.value()
            self._proxyModel = dtm.Masters_ProxyModel()
            self._proxyModel.setSourceModel(model)
            self._proxyModel.setDynamicSortFilter(True)
            self._proxyModel.setSortRole(dtm.Masters_Model.sortRole)
            self.setModel(self._proxyModel)

            self.setIndentation(0)
            self.expandAll()

            self.header().resizeSection(0, self._slider.listSlider.value())
            self.header().setResizeMode(0, QtGui.QHeaderView.Fixed)


            self.header().resizeSection(1, 32)
            self.header().setResizeMode(1, QtGui.QHeaderView.Fixed)

            self.header().setStretchLastSection(False)

            self.header().setResizeMode(2, QtGui.QHeaderView.Stretch)
            self.header().setResizeMode(3, QtGui.QHeaderView.Stretch)
            self.header().setResizeMode(4, QtGui.QHeaderView.Stretch)

            self.header().resizeSection(5, 32)
            self.header().setResizeMode(5, QtGui.QHeaderView.Fixed)
            self.header().resizeSection(6, 32)
            self.header().setResizeMode(6, QtGui.QHeaderView.Fixed)

            self.setItemDelegateForColumn(6,  loadButtonDelegate(self))

            self.sortByColumn(1, QtCore.Qt.DescendingOrder)

            self.proxyModel = self.model()
            self.sourceModel = self.proxyModel.sourceModel()
            #self.update()


    def MultiButtonClicked(self):
        # This slot will be called when our button is clicked.
        # self.sender() returns a refence to the QPushButton created
        # by the delegate, not the delegate itself.
        button = self.sender()
        index = self.indexAt(button.pos())
        index = self.model().mapToSource(index)
        if self.model().sourceModel().getNode(index).typeInfo() == cfg._new_:
            parent_index = index.parent()
            node = self.model().sourceModel().getNode(index).parent()
            self.model().sourceModel().removeRows(index.row(),1, parent_index)
            node.initialVersion()
        else:
            self.model().sourceModel().getNode(index).load()
            self.parent.set_thumbnail(self.model().sourceModel().getNode(index).resource)
            self.parent.version = self.model().sourceModel().getNode(index)
            self.setCurrentIndex(self.model().mapFromSource(index))

    def contextMenuEvent(self, event):

        handled = True
        index = self.indexAt(event.pos())
        menu = QtGui.QMenu()
        node = None

        if index.isValid():
            src = self.asModelIndex(index)
            node = self.asModelNode(src)

        actions = []

        if node and not node._deathrow:

            if node.typeInfo() == cfg._master_:

                actions.append(QtGui.QAction("Explore...", menu,
                                             triggered=functools.partial(self.explore, src)))
            else:

                event.accept()
                return

        else:
            event.accept()
            return

        menu.addActions(actions)

        menu.exec_(event.globalPos())
        event.accept()

        return


class IconScaleSlider(QtGui.QWidget):
    def __init__(self, parent):
        super(IconScaleSlider, self).__init__(parent)


        self.large_lable = QtGui.QLabel()
        self.large_lable.setMaximumSize(QtCore.QSize(16, 16))
        self.large_lable.setPixmap(cfg.large_icon)
        self.small_lable = QtGui.QLabel()
        self.small_lable.setMaximumSize(QtCore.QSize(16, 16))
        self.small_lable.setPixmap(cfg.small_icon)
        self.slideWidget = QtGui.QWidget()
        self.slideWidget.setMaximumHeight(20)
        self.slideLayout = QtGui.QHBoxLayout()
        self.slideLayout.setContentsMargins(0, 0, 0, 0)

        self.slideLayout.setAlignment(QtCore.Qt.AlignRight)

        self.listSlider = QtGui.QSlider()
        self.listSlider.setOrientation(QtCore.Qt.Horizontal)
        self.listSlider.setMaximumWidth(80)
        self.listSlider.setMinimumWidth(80)
        self.listSlider.setMaximumHeight(25)
        self.listSlider.setMinimum(32)
        self.listSlider.setMaximum(96)
        self.listSlider.setValue(32)


        self.slideLayout.addWidget(self.small_lable)
        self.slideLayout.addWidget(self.listSlider)
        self.slideLayout.addWidget(self.large_lable)

        self.setMinimumHeight(25)
        self.setLayout(self.slideLayout)



#
class Project_Tree_View(QtGui.QTreeView):
    percentage_complete = QtCore.Signal(int)
    update = QtCore.Signal()

    def __init__(self,parent = None):
        super(Project_Tree_View, self).__init__(parent)

        global counter

        # display options
        self.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)
        self.setDragEnabled( True )
        self.setAcceptDrops( True )
        self.setDragDropMode( QtGui.QAbstractItemView.InternalMove )
        self.setDropIndicatorShown(True)
        self.resizeColumnToContents(True) 

        # self.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)

        #local variables
        self.pipelineUI = self.parent()
        self._ignoreExpentions = False
        self._expended_states = None        
        self._userSelection = None       
        self._tableView = None
        self._proxyModel = None
        self._sourceModel = None
        self._tree_as_flat_list = None
        
        #stylesheet 
        self.setStyleSheet('''  
                           
                           QTreeView::item:focus {
                           }
                           QTreeView::item:hover {
                                background: #101010;
                           }
                           QTreeView {
                                outline: 0;
                           }
                           QTreeView::branch:has-siblings:!adjoins-item {
                                border-image:url(''' + cfg.vline + ''') 0;
                           }
                           
                           QTreeView::branch:has-siblings:adjoins-item {
                                border-image:url(''' + cfg.branch_more + ''') 0;
                           }
                           
                           QTreeView::branch:!has-children:!has-siblings:adjoins-item {
                                border-image:url(''' + cfg.branch_end + ''') 0;
                           }

                           QTreeView::branch:has-children:!has-siblings:closed,
                           QTreeView::branch:closed:has-children:has-siblings {
                                border-image: none;
                                image:url(''' + cfg.branch_closed + ''') 0;
                           }

                           QTreeView::branch:open:has-children:!has-siblings,
                           QTreeView::branch:open:has-children:has-siblings  {
                                border-image: none;
                                image: url(''' + cfg.branch_open + ''') 0;
                           }''')
    

        self.changed = False
        self.update.connect(self.model_changed)

    def model_changed(self):
        if self.changed == False:
            self.changed = True


    def setModel(self,model):

        super(Project_Tree_View, self).setModel(model)

        if model:
            self.changed = False

            self.proxyModel = self.model()
            self.sourceModel = self.proxyModel.sourceModel()

            '''
            this will expend the tree only on the first level, which should be
            the projects name folder
            the rest will be collapsed
            '''

            self.initialExpension()


            '''
            save the expended state of the tree
            '''
            self.saveState()


            self.header().setStretchLastSection(False)

            self.header().setResizeMode(0, QtGui.QHeaderView.Stretch)

            self.header().resizeSection(1, 100)
            self.header().setResizeMode(1, QtGui.QHeaderView.Fixed)



    def initialExpension(self):
        if self.model():
            self.collapseAll()
            return
            for row in range(self.model().rowCount(self.rootIndex())):
                x = self.model().index(row, 0, self.rootIndex())
                self.setExpanded(x, True)

    @property
    def tableView(self):
        return self._tableView
    
    @tableView.setter
    def tableView(self, view):
        self._tableView = view 

    @property
    def proxyModel(self):
        return self._proxyModel
    
    @proxyModel.setter
    def proxyModel(self, model):
        self._proxyModel = model        

    @property
    def sourceModel(self):
        return self._sourceModel
    
    @sourceModel.setter
    def sourceModel(self, model):
        self._sourceModel = model   


    @property
    def userSelection(self):
        return self._userSelection
    
    @userSelection.setter
    def userSelection(self, selection):
        self._userSelection = selection   

    def asProxyIndex(self,index):
        return self.proxyModel.index(0,0,index)

    
    def asModelIndex(self, index):
        return self.proxyModel.mapToSource(index)

    def fromProxyIndex(self, index):
        return self.proxyModel.mapFromSource(index)

    def asModelNode(self, index):
        return self.sourceModel.getNode(index)
        
        
        
    def modelIndexFromNode(self, node):
        return self.sourceModel.indexFromNode(node,self.rootIndex())
    
    def selectRoot(self):
        
        self.setCurrentIndex(self.asProxyIndex(self.rootIndex()))
        #self.tableView.update(self.selectionModel().selection())    
        self.saveSelection()
        

    def saveSelection(self):
        
        if len(self.selectedIndexes())>0:
            self.userSelection = self.asModelIndex(self.selectedIndexes()[0])
    
    def saveState(self):
        '''
        recursive function to save the expention state fo the tree to a dictionary
        '''
    
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
                   
        self._expended_states = {}
        rec(self._expended_states,self.proxyModel,self.rootIndex())

        
    def restoreState(self):  
          
        '''
        recursive function to restore the expention state fo the tree to a dictionary
        '''
        def rec(  mdl, index):
            
            for row in range(mdl.rowCount(index)):
                 
                   
                i = mdl.index(row,0, index)
                node = mdl.data(i, 165)
                
                if node in self._expended_states:
                    if self._expended_states[node] == True:
                        self.setExpanded(i, True)

                     
                rec( mdl, i)     
                            
        self.collapseAll()
        rec(self.proxyModel,self.rootIndex())                
        self.restoreSelection()

    def restoreSelection(self):

        index = self.fromProxyIndex(self.userSelection)
        self.select(index)
        self.updateTable( index)
        #self.selectionModel().select(index, QtGui.QItemSelectionModel.ClearAndSelect)
    
    def select(self, index):
        '''
        selects a tree branch and expand the parant branch to see the selected branch    
        '''
        modelIndex = self.sourceModel.parent(self.asModelIndex(index))
        proxyIndex = self.fromProxyIndex(modelIndex)
        self.setExpanded(proxyIndex, True)
        self.selectionModel().select(index, QtGui.QItemSelectionModel.ClearAndSelect)
        
        
    def dropEvent(self, event):

        super(Project_Tree_View, self).dropEvent(event)
        #QTreeView.dropEvent(self, evt)
        if not event.isAccepted():
            # qdnd_win.cpp has weird behavior -- even if the event isn't accepted
            # by target widget, it sets accept() to true, which causes the executed
            # action to be reported as "move", which causes the view to remove the
            # source rows even though the target widget didn't like the drop.
            # Maybe it's better for the model to check drop-okay-ness during the
            # drag rather than only on drop; but the check involves not-insignificant work.
            event.setDropAction(QtCore.Qt.IgnoreAction)
        
        '''
        if the drop is coming from the contents view - this is how i handle this...
        it's UGLY, but for now it's the only way i can make this work...
        '''   
        #print event.possibleActions() , "<<"   
        if event.source().__class__.__name__ == 'PipelineContentsView':        
                                 
            i = self.indexAt(event.pos())         
            model_index = self.asModelIndex(i)
            model_id = self.sourceModel.getNode(model_index).id
            model_node = self.sourceModel.getNode(model_index)
           
               
            if model_index.isValid():
                
                mime = event.mimeData()
                source = event.source()
                
                item = cPickle.loads( str( mime.data( 'application/x-qabstractitemmodeldatalist' ) ) )
                item_index = self.sourceModel.indexFromNode( item , QtCore.QModelIndex())
                item_parent = self.sourceModel.parent( item_index )
                item_id = item.id
                
                
                '''
                ignore drops of folders into assets
                '''
                if model_node.typeInfo() == cfg._asset_:
                    if item.typeInfo() == cfg._folder_ or item.typeInfo() == cfg._asset_:
                        
                        event.setDropAction(QtCore.Qt.IgnoreAction)
                        event.ignore()
                        return 
                
                
                '''
                this is to make sure the dropped item is not already a child in the downstream of branches
                '''
                descending_id = []
                for i in self.sourceModel.listHierarchy(item_index):
                    descending_id.append(self.sourceModel.getNode(i).id)
                
                if model_id in descending_id:
                    
                    event.setDropAction(QtCore.Qt.IgnoreAction)
                    event.ignore()
                    return
                
                else:
                    
                    
                    
                    
                    
                    source.clearModel()
                    self.sourceModel.removeRows(item_index.row(),1,item_parent)            
                    self._proxyModel.invalidate()

                    self.sourceModel.dropMimeData(mime, event.dropAction,0,0,model_index)
                    source.restoreTreeViewtSelection() 
                    return       
        
        # this was required when i misused the insert rows function of the model...
        #self._proxyModel.invalidate()


    '''
    here i am detecting if a drop is coming from the contents view, to mark it as acepted, otherwise the drop will be blocked.
    it's UGLY, but for now it's the only way i can make this work...
    '''  
    def dragEnterEvent(self, event):

        super(Project_Tree_View, self).dragEnterEvent(event)

        if event.source().__class__.__name__ == 'PipelineContentsView':        
            return event.setAccepted(True)

    '''
    def dragMoveEvent(self, event):

        super(pipelineTreeView,self).dragMoveEvent(event)
        #return event.setAccepted(True)
    '''
    
    def projectRootIndex(self):
        modelRootIndex = self.asModelIndex(self.rootIndex())
        return modelRootIndex
        # get the first childe of the model's root                                   
        #return self.sourceModel.index(0,0,modelRootIndex)



    
    # def mouseReleaseEvent(self, event):
    #
    #     super(pipelineTreeView, self).mouseReleaseEvent(event)
    #     self.saveSelection()
    #     #self.tableView.update(self.selectionModel().selection())
    #     event.accept
   
    def contextMenuEvent(self, event):
        
        handled = True
        index = self.indexAt(event.pos())
        menu = QtGui.QMenu()        
        node = None
       
        if index.isValid():
            src = self.asModelIndex(index)
            node = self.asModelNode(src)

        actions = []  
          
        if node and not node._deathrow:

            if node.typeInfo() != cfg._stage_:

                level_name, level_type = node.level_options

                if node.typeInfo() == cfg._root_:

                    actions.append(QtGui.QAction("Create tree...", menu,
                                  triggered=functools.partial(self.create_new_tree, src)))

                if level_type == cfg._folder_:
                    actions.append(
                        QtGui.QAction("Create new {0}".format(level_name), menu,
                                      triggered=functools.partial(self.create_new_folder, src,level_name )))

                elif level_type == cfg._asset_:
                    actions.append(QtGui.QAction("Create new {0}".format(level_name), menu,
                                                 triggered=functools.partial(self.create_new_asset, src, level_name)))

                elif level_type == cfg._stage_:
                    actions.append(QtGui.QAction("Create new {0}".format(level_name), menu,
                                                 triggered=functools.partial(self.create_new_stage, src)))

                elif node.typeInfo() == cfg._asset_:
                    actions.append(QtGui.QAction("Create new %s"%(cfg._stage_), menu, triggered = functools.partial(self.create_new_stage, src) ))


            if not node.typeInfo() == cfg._root_:
                actions.append(QtGui.QAction("Delete", menu, triggered=functools.partial(self.delete, src)))

        else:
            event.accept()
            return

        menu.addActions(actions)      

        menu.exec_(event.globalPos())
        event.accept()

        return

    '''
    functions to add/remove tree nodes
    this is we will want some user input...
    
    '''
    def delete(self,  index):
        # clear the table view              
        #self.tableView.update(QtGui.QItemSelection())
        
        node = self.asModelNode(index)
        node.deathrow()
        # parentIndex = self.sourceModel.parent(index)
        # self.sourceModel.removeRows(node.row(),1,parentIndex, kill=True)
        self._proxyModel.invalidate()
        #
        # self.updateTable( self.fromProxyIndex(parentIndex))
        self.update.emit()
        return True

    def create_new_tree(self, parent):
        global counter
        global total_items
        counter = 0
        total_items = 0
        parent_node = self.sourceModel.getNode(parent)

        depth_list = self.sourceModel.listAncestos(parent)
        ancestors = []
        for i in depth_list:
            ancestors.append(self.sourceModel.getNode(i))

        def rec(items, p, stages, name_format):

            global counter
            global total_items
            """ recursive function for generating a tree out of the instructions list called items
            the function creates nodes by instruction in the first item in the list, then while the list is longer then 1,
            it sends the list againg but without the current item
            the parent is the currently created node"""
            times = items[0][2]
            name = items[0][1]
            padding = items[0][3]

            for i in range(times):
                base_folder_name = name

                number = files.set_padding(i, padding)
                if base_folder_name != "":
                    folder_name = "{0}{1}".format(base_folder_name, number) if times > 1 else base_folder_name
                else:
                    folder_name = "{0}".format(number) if times > 1 else "unnamed_folder"

                # skip = False
                # for child in parent_node.children:
                #     if child.name == folder_name:
                #         skip = True
                # if skip:
                #     print "folder exists!"
                #     continue

                i = self.sourceModel.indexFromNode(p, QtCore.QModelIndex())
                depth_list = self.sourceModel.listAncestos(i)

                path = os.path.join(p.path, folder_name)

                if len(items) == 1:
                    node = dt.AssetNode(folder_name, path=path, parent=p, virtual=True,
                                        section=p.section)

                    self.sourceModel.insertRows(0, 0, parent=i, node=node)
                    self._proxyModel.invalidate()
                    counter += 1
                    # QtGui.QApplication.processEvents()
                    # #print remap(current, 0, total_items, 0, 100)
                    # self.percentage_complete.emit(remap(current, 0, total_items, 0, 100))

                    '''for an asset, generate stages:'''

                    new_index = self.sourceModel.indexFromNode(node, QtCore.QModelIndex())
                    for s in stages:
                        if stages[s]:
                            path = os.path.join(p.path, folder_name, s)
                            # formatDepth
                            stageNode = dt.StageNode(s, parent=node, path=path, virtual=True,
                                                     name_format=name_format, section=p.section,
                                                     project=self.pipelineUI.project, depth=len(depth_list))
                            # if node is not False:
                            self._sourceModel.insertRows(0, 0, parent=new_index, node=stageNode)
                            self._proxyModel.invalidate()
                            #counter += 1
                            # QtGui.QApplication.processEvents()
                            # #print remap(current, 0, total_items, 0, 100)
                            # self.percentage_complete.emit(remap(current, 0, total_items, 0, 100))

                else:
                    node = dt.FolderNode(folder_name, path=path, parent=p, virtual=True,
                                     section=p.section, project=self.pipelineUI.project,
                                     depth=len(depth_list))


                    self.sourceModel.insertRows(0, 0, parent=i, node=node)
                    self._proxyModel.invalidate()
                    counter += 1



                if len(items) > 1:

                    QtGui.QApplication.processEvents()

                    print remap_value(counter, 0, total_items, 0, 100), "--->", counter, "--->", total_items
                    self.percentage_complete.emit(remap_value(counter, 0, total_items, 0, 100))
                    l = list(items[1:])
                    rec(l, node, stages, name_format)
                else:
                    pass



        folderDlg = dlg.newTreeDialog(project=self.pipelineUI.project, section = parent_node.section)
        result = folderDlg.exec_()
        res = folderDlg.result()
        if result == QtGui.QDialog.Accepted:
            levels = res["levels"]

            total_current_level = levels[0][2]
            total_items = total_current_level

            for i in range(1, len(levels)):
                total_current_level = (total_current_level * levels[i][2])
                total_items += total_current_level

            rec(levels, parent_node, res["stages"], res["name_format"])
            self.update.emit()
            self.percentage_complete.emit(0)



    def create_new_folder(self, parent, string):

        parent_node = self.sourceModel.getNode(parent)


        depth_list = self.sourceModel.listAncestos(parent)
        ancestors = []
        for i in depth_list:
            ancestors.append(self.sourceModel.getNode(i))

        folderDlg = dlg.newFolderDialog(string = string)
        result = folderDlg.exec_()
        res = folderDlg.result()
        if result == QtGui.QDialog.Accepted:
            base_folder_name = res["name"]


            for i in range(0,res["quantity"]):
                QtGui.QApplication.processEvents()
                self.percentage_complete.emit(remap_value(i, 0, res["quantity"], 0, 100))

                number = files.set_padding(i, res["padding"])
                if base_folder_name != "":
                    folder_name = "{0}{1}".format(base_folder_name, number) if res["quantity"] > 1 else base_folder_name
                else:
                    folder_name = "{0}".format(number) if res["quantity"] > 1 else "unnamed_folder"


                skip = False
                for child in parent_node.children:
                    if child.name == folder_name:
                        skip = True
                if skip:
                    print "folder exists!"
                    continue

                path = os.path.join(parent_node.path, folder_name)
                node = dt.FolderNode(folder_name, path=path, parent=parent_node, virtual = True, section = parent_node.section, project = self.pipelineUI.project, depth = len(ancestors))

                self.sourceModel.insertRows(0, 0, parent=parent, node=node)
                self._proxyModel.invalidate()


            self.update.emit()
            self.percentage_complete.emit(0)



    def create_new_asset(self, parent, string):
        parent_node = self.sourceModel.getNode(parent)

        depth_list = self.sourceModel.listAncestos(parent)
        ancestors = []
        for i in depth_list:
            ancestors.append(self.sourceModel.getNode(i))

        assetDlg = dlg.newAssetDialog(stages = self.pipelineUI.project.stages[parent_node.section], ancestors = ancestors, string = string, project = self.pipelineUI.project)
        result = assetDlg.exec_()
        res = assetDlg.result()
        if result == QtGui.QDialog.Accepted:
            base_folder_name = res["name"]
            for i in range(0, res["quantity"]):
                QtGui.QApplication.processEvents()
                self.percentage_complete.emit(remap_value(i, 0, res["quantity"], 0, 100))
                number = files.set_padding(i, res["padding"])
                if base_folder_name != "":
                    folder_name = "{0}{1}".format(base_folder_name, number) if res["quantity"] > 1 else base_folder_name
                else:
                    folder_name = "{0}".format(number) if res["quantity"] > 1 else "unnamed_folder"

                skip = False
                for child in parent_node.children:
                    if child.name == folder_name:
                        skip = True
                if skip:
                    print "folder exists!"
                    continue

                path = os.path.join(parent_node.path, folder_name)
                node = dt.AssetNode(folder_name, path=path, parent=parent_node, virtual=True, section = parent_node.section)
                # if node is not False:
                self.sourceModel.insertRows(0, 0, parent=parent, node=node)
                self._proxyModel.invalidate()



                new_index = self.sourceModel.indexFromNode(node, QtCore.QModelIndex())
                for s in res["stages"]:
                    if res["stages"][s]:
                        path = os.path.join(parent_node.path, folder_name, s)
                        #formatDepth
                        stageNode = dt.StageNode(s, parent=node, path=path, virtual=True, name_format = res["name_format"], section = parent_node.section, project = self.pipelineUI.project, depth = len(ancestors))
                        # if node is not False:
                        self._sourceModel.insertRows(0, 0, parent=new_index, node=stageNode)
                        self._proxyModel.invalidate()


            self.update.emit()
            self.percentage_complete.emit(0)




    def create_new_stage(self, parent):


        parent_node = self.sourceModel.getNode(parent)

        depth_list = self.sourceModel.listAncestos(parent)
        ancestors = []
        for i in depth_list:
            ancestors.append(self.sourceModel.getNode(i))

        new_stages = []
        for stage in self.pipelineUI.project.stages[parent_node.section]:
            if stage not in parent_node.stages:
                new_stages.append(stage)

        if new_stages:

            assetDlg = dlg.newStageDialog(parent_name=parent_node.name, stages=new_stages, ancestors=ancestors, project = self.pipelineUI.project)
            result = assetDlg.exec_()
            res = assetDlg.result()
            if result == QtGui.QDialog.Accepted:
                for s in res["stages"]:
                    if res["stages"][s]:
                        path = os.path.join(parent_node.path, s)
                        # formatDepth

                        stageNode = dt.StageNode(s, parent=parent_node, asset_name = parent_node.name, path=path, virtual=True, name_format=res["name_format"], section = parent_node.section, settings = self.pipelineUI.settings)
                        # if node is not False:
                        self._sourceModel.insertRows(0, 0, parent=parent, node=stageNode)
                        self._proxyModel.invalidate()

                self.update.emit()



    @property
    def tree_as_flat_list(self):
        return self._tree_as_flat_list
    
    @tree_as_flat_list.setter 
    def tree_as_flat_list(self, list):
        self._tree_as_flat_list = list

    def list_flat_hierarchy(self):

        list = []
        for i in self.sourceModel.listHierarchy(QtCore.QModelIndex()):
            list.append(self.sourceModel.getNode(i))
        
        self.tree_as_flat_list = list

    def filterContents(self):
        
        if self.tree_as_flat_list:
            #self.tableView.clearModel()
            
            model = dtm.PipelineContentsModel(self.tree_as_flat_list)
            #self.tableView.populateTable(model)
            

    def commit(self):
        print "commit tree:"
        self.sourceModel.rootNode.commit()
        self.changed = False


class Dresser_View(Project_Tree_View):

    def __init__(self,parent = None):
        super(Dresser_View, self).__init__(parent)

        # global counter
        #
        # # display options
        # self.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        # self.setAlternatingRowColors(True)
        # self.setSortingEnabled(True)
        # self.setDragEnabled( True )
        # self.setAcceptDrops( True )
        # self.setDragDropMode( QtGui.QAbstractItemView.InternalMove )
        # self.setDropIndicatorShown(True)
        # self.resizeColumnToContents(True)
        #
        # # self.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        #
        # #local variables
        # self.pipelineUI = self.parent()
        # self._ignoreExpentions = False
        # self._expended_states = None
        # self._userSelection = None
        # self._tableView = None
        # self._proxyModel = None
        # self._sourceModel = None
        # self._tree_as_flat_list = None
        #
        # #stylesheet
        # self.setStyleSheet('''
        #
        #                    QTreeView::item:focus {
        #                    }
        #                    QTreeView::item:hover {
        #                         background: #101010;
        #                    }
        #                    QTreeView {
        #                         outline: 0;
        #                    }
        #                    QTreeView::branch:has-siblings:!adjoins-item {
        #                         border-image:url(''' + cfg.vline + ''') 0;
        #                    }
        #
        #                    QTreeView::branch:has-siblings:adjoins-item {
        #                         border-image:url(''' + cfg.branch_more + ''') 0;
        #                    }
        #
        #                    QTreeView::branch:!has-children:!has-siblings:adjoins-item {
        #                         border-image:url(''' + cfg.branch_end + ''') 0;
        #                    }
        #
        #                    QTreeView::branch:has-children:!has-siblings:closed,
        #                    QTreeView::branch:closed:has-children:has-siblings {
        #                         border-image: none;
        #                         image:url(''' + cfg.branch_closed + ''') 0;
        #                    }
        #
        #                    QTreeView::branch:open:has-children:!has-siblings,
        #                    QTreeView::branch:open:has-children:has-siblings  {
        #                         border-image: none;
        #                         image: url(''' + cfg.branch_open + ''') 0;
        #                    }''')
        #
        #
        # self.changed = False
        # self.update.connect(self.model_changed)


    def setModel(self,model):

        super(Dresser_View, self).setModel(model)

        if model:
            self.changed = False

            self.proxyModel = self.model()
            self.sourceModel = self.proxyModel.sourceModel()

            '''
            this will expend the tree only on the first level, which should be
            the projects name folder
            the rest will be collapsed
            '''
            self.initialExpension()
            '''
            save the expended state of the tree
            '''
            self.saveState()


            self.header().setStretchLastSection(False)

            self.header().setResizeMode(0, QtGui.QHeaderView.Stretch)

            self.header().resizeSection(1, 100)
            self.header().setResizeMode(1, QtGui.QHeaderView.Fixed)



    def initialExpension(self):
        if self.model():
            self.collapseAll()
            for row in range(self.model().rowCount(self.rootIndex())):
                x = self.model().index(row, 0, self.rootIndex())
                self.setExpanded(x, True)


    def contextMenuEvent(self, event):

        handled = True
        index = self.indexAt(event.pos())
        menu = QtGui.QMenu()
        node = None

        if index.isValid():
            src = self.asModelIndex(index)
            node = self.asModelNode(src)

        actions = []

        if node and not node._deathrow:

                if node.typeInfo() == cfg._stage_:

                    actions.append(QtGui.QAction("Reference to current", menu,
                                  triggered=functools.partial(self.reference_to_current, src)))
                else:

                    event.accept()
                    return

        else:
            event.accept()
            return

        menu.addActions(actions)

        menu.exec_(event.globalPos())
        event.accept()

        return

    def reference_to_current(self, index):
        node = self.asModelNode(index)
        node.reference_master_to_current()



class ComboWidget(QtGui.QWidget):
    def __init__(self,
                 parent_layout = None,
                 parent = None):
        
        super(ComboWidget, self).__init__(parent)
        #self.parent = parent
        
        #self._parent = parent_box
        self.setHidden(True)
        self._parent_layout = parent_layout  

        # UI
        self.setMaximumHeight(30)  
        self.layout = QtGui.QVBoxLayout(self)
        self.layout.setAlignment(QtCore.Qt.AlignLeft)
        self.comboBox = QtGui.QComboBox(parent)
        self.comboBox.setIconSize(QtCore.QSize(24 ,24)  ) 
        self.comboBox.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.layout.addWidget(self.comboBox)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout) 
        self._parent_layout.addWidget(self)


    def remove(self):
        self.setParent(None)
        self.deleteLater()
        self._child = None
        del self

class ComboStaticWidget(ComboWidget):
    def __init__(self,
                 settings = None,
                 items = None,
                 parent_layout = None,
                 parent = None):
        
        super(ComboStaticWidget, self).__init__(parent_layout, parent)
        
        self.parent = parent
        self._settings = settings
        self._items = items
        self._model = None
        self.createModel()
        self.setHidden(False)

    def createModel(self):
        
        list = [dt.CatagoryNode("stage")]
        
        [list.append(dt.DummyNode(i)) for i in self._items]
        
        RemoveOption = False
        
        # if list:
        #     RemoveOption = True
        #
        # list.append(dt.AddNode("Add..."))
        #
        # if RemoveOption:
        #     list.append(dt.AddNode("Remove..."))
        
        self._model = dtm.List_Model(list)
        self.comboBox.setModel(self._model)  
        
        self.comboBox.currentIndexChanged.connect(self.update)
        
    def update(self):
        self._settings.stage = self.comboBox.currentText()

        try:
            self.parent.dynamicCombo._box_list[-1].stageScan()
        except:
            pass

class ComboDynamicWidget(ComboWidget):
    def __init__(self,
                 settings = None,
                 project = None,
                 path = None,
                 stage = None,
                 box_list = None,
                 parent_box = None,
                 parent_layout = None,
                 parent = None):
        
        super(ComboDynamicWidget, self).__init__(parent_layout, parent)
               
        # Local and init calls
        self.parent = parent
        self._settings = settings
        self._project = project
        self._level = None
        self._subdirectories = None
        self._path = None
        self._stage = None
        self._parent_box = parent_box
        self._parent_layout = parent_layout
        
        self._box_list = box_list
        self._box_list.append(self)

        self._node = None
        self._level = "n/a"

        if path and stage:
            self._path = path
            self._stage = stage
            self.listDirectory()




        self._child = None            
        self._model = None
        self.section = None
        
        # Init calls
        self.createModel()              
                    
        # connections                
        self.comboBox.currentIndexChanged.connect(self.update)
        self.setHidden(False)


    def navigate(self, items):
        current = self
        for i in range(0, len(items)):
            if setComboValue(current.comboBox, items[i]):
                current.update()
                #QtGui.QApplication.processEvents()
                current = current._child



    def listDirectory(self):
        dir = self._path
        dirs = files.list_dir_folders(dir)   

              
        if dirs:
            
            self._subdirectories = dirs
            
            relative_path = os.path.relpath(dir, self.parent.project.path)
            depth = relative_path.count(os.sep)
            
            if self._stage in self._project.stages["asset"]:
                options = self._project.levels["asset"]
                self.section = cfg._assets_
                if len(options) >  depth:
                    self._level = options[depth]

                    return
                
            if self._stage in self._project.stages["animation"]:
                options = self._project.levels["animation"]
                if len(options) > depth:
                    self._level = options[depth]
                    self.section = cfg._animation_
                    return
          
        self._level = "n/a"
                

    def createModel(self):
        
        list = [dt.CatagoryNode("<{}>".format(self._level))]

        if self._level != "n/a":
            if self._subdirectories:
                for i in range(len(self._subdirectories)):
                    n = os.path.split(self._subdirectories[i])[1]
                    list.append(dt.FolderNode(n))
        
        RemoveOption = False
        
        # if list:
        #     RemoveOption = True
        #
        # list.append(dt.AddNode("Add..."))
        #
        # if RemoveOption:
        #     list.append(dt.AddNode("Remove..."))
        
        self._model = dtm.List_Model(list)
        self.comboBox.setModel(self._model)    

      

    def addChild(self, path):
        
        if files.list_dir_folders(path):
            widget = ComboDynamicWidget(
                                 settings = self._settings,
                                 project = self._project,
                                 path = path,
                                 stage = self._stage,
                                 box_list = self._box_list,
                                 parent_box = self,
                                 parent_layout = self._parent_layout,
                                 parent = self.parent)
            self._child = widget   
 
    def update(self):



        self.removeChild()
        
        scan = self.stageScan()

        if scan is not True:
            '''
            if the folder is a stage folder don't list it and return True
            '''
            self.addChild(scan)


    def stageScan(self):

        path = os.path.join(self._path, self.comboBox.currentText())

        self._node = None


        if dt.assetDir(path):


            '''
            if the path is an assets folder
            '''

            p = self._parent_box._node if self._parent_box else self._node

            self._node = dt.AssetNode(os.path.split(path)[1], parent=p, path=os.path.join(path),
                                      project=self._project,
                                      settings=self._settings, pipelineUI=self.parent, section = self.section)

            for dir in files.list_dir_folders(path):

                '''
                scan each folder to see if it is a stage folder
                '''

                if dt.stageDir(os.path.join(path,dir)):
                    if dir == self._settings.stage:

                        '''
                        if its a stage, see if it is a match to the current selected stage, if so, set it as the current stage folder
                        '''


                        stage = dt.StageNode(dir, parent=self._node , path=os.path.join(path,dir), project=self._project,
                                     settings=self._settings, pipelineUI= self.parent, section = self.section)

                        self.parent.stageNode(stage)
                        self.parent.updateVersionsTable()
                        self.parent.updateMastersTable()
                        return True

                    #self.parent.stageNode(None)
                    #self.parent.updateVersionsTable()
                    #return True

            self.parent.stageNode(None)
            self.parent.updateVersionsTable()
            self.parent.updateMastersTable()
            return True


        if self._parent_box:
            self._node = dt.FolderNode(os.path.split(path)[1], parent=self._parent_box._node, path=path, project=self._project,
                                   settings=self._settings, pipelineUI=self.parent)
        else:
            self._node = dt.FolderNode(os.path.split(path)[1], parent=None, path=path, project=self._project,
                                       settings=self._settings, pipelineUI=self.parent)

        self.parent.stageNode(None)
        self.parent.updateVersionsTable()
        self.parent.updateMastersTable()
        return path


       
    def removeChild(self):
        
        if self._child:

            c = self._child
            
            # recursive to all childs
            c.removeChild()
            c.setParent(None)
            c.deleteLater()
            self._child = None
            del c


    def remove(self):
        self.removeChild()
        self.setParent(None)
        self.deleteLater()
        self._child = None
        del self






            