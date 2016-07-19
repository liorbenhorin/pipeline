
from PySide import QtCore, QtGui, QtXml
import cPickle
import os
import functools

import data as dt
reload(dt)

import data_model as dtm
reload(dtm)

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

    global folder_icon
    global cube_icon
    global cube_icon_full
    global add_icon
    global large_image_icon
    folder_icon = os.path.join(localIconPath, "%s.svg"%"folder")
    cube_icon = os.path.join(localIconPath, "%s.svg"%"cube")    
    cube_icon_full = os.path.join(localIconPath, "%s.svg"%"cube-fill") 
    add_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"add"))
    large_image_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"large_image")) 
                    
    
set_icons()


        
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
            self.parent().setIndexWidget(
                index, 
                QtGui.QPushButton(
                    "Open",
                    index.data(), 
                    self.parent(), 
                    clicked=self.parent().loadButtonClicked
                )
            )     

class OptionsButtonDelegate(QtGui.QItemDelegate):
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
            
            
            button = QtGui.QPushButton(
                    index.data(), 
                    self.parent()
                )
            
            self.parent().setIndexWidget(index, button)  

            menu = QtGui.QMenu(button)
            deleteAction = QtGui.QAction("Delete",button, triggered = self.parent().deletActionClicked) 
            menu.addAction( deleteAction )          
            button.setMenu(menu)
    
class PipelineVersionsView(QtGui.QTableView):
    def __init__(self,parent = None):
        super(PipelineVersionsView, self).__init__(parent)
        self.setAlternatingRowColors(True)
        #self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection) 
        self.setWordWrap(True)
        #self.setShowGrid(False)
        self.verticalHeader().setResizeMode(QtGui.QHeaderView.Fixed)        
        #self.icons_size(32)       
        #self.setMinimumWidth(250)
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        #self.setSortingEnabled(True)
        #self.horizontalHeader().setOffset(10)
        #self.verticalHeader().hide()        
        self.setSortingEnabled(True)

        # Set the delegate for column 0 of our table
        self.setItemDelegateForColumn(3,  loadButtonDelegate(self))
        self.setItemDelegateForColumn(4,  OptionsButtonDelegate(self))
        

    def setModel(self,model):

        super(PipelineVersionsView,self).setModel(model)
        # size the options button column
        self.horizontalHeader().resizeSection(4,25)
        self.horizontalHeader().setResizeMode(4,QtGui.QHeaderView.Fixed)   
        # size the load button column
        self.horizontalHeader().resizeSection(3,60)
        self.horizontalHeader().setResizeMode(3,QtGui.QHeaderView.Fixed)   
        # size the note button column
        self.horizontalHeader().resizeSection(2,25)
        self.horizontalHeader().setResizeMode(2,QtGui.QHeaderView.Fixed)
              
        self.horizontalHeader().setResizeMode(0,QtGui.QHeaderView.Stretch)
        self.horizontalHeader().setResizeMode(1,QtGui.QHeaderView.Stretch)        


 
         
    @QtCore.Slot()
    def loadButtonClicked(self):
        # This slot will be called when our button is clicked. 
        # self.sender() returns a refence to the QPushButton created
        # by the delegate, not the delegate itself.
        button = self.sender()
        index = self.indexAt(button.pos())
        print self.model().getNode(index).name, " load --->" , self.model().getNode(index).number

    @QtCore.Slot()
    def deletActionClicked(self):
        # This slot will be called when our button is clicked. 
        # self.sender() returns a refence to the QPushButton created
        # by the delegate, not the delegate itself.
        button = self.sender().parent()
        index = self.indexAt(button.pos())
        print self.model().getNode(index).name, " delete action on --->" , self.model().getNode(index).number


class PipelineContentsView(QtGui.QTableView):
    def __init__(self,parent = None):
        super(PipelineContentsView, self).__init__(parent)
        
        #display options
        
        self.setAlternatingRowColors(True)
        self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection) 
        self.setWordWrap(True)
        self.setShowGrid(False)
        self.verticalHeader().setResizeMode(QtGui.QHeaderView.Fixed)        
        self.icons_size(32)       
        #self.setMinimumWidth(250)
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.setSortingEnabled(True)
        self.horizontalHeader().setOffset(10)
        self.verticalHeader().hide()
        
        self.setSortingEnabled(True)
        self.setDragEnabled( True )
        self.setAcceptDrops( True )
        self.setDragDropMode( QtGui.QAbstractItemView.DragDrop )#QtGui.QAbstractItemView.DragDrop )InternalMove

        #local variables
        self._treeView = None        
        self._treeProxyModel = None
        self._treeSourceModel = None
        
        self._treeParent = None
        self._treeParentIndex = None

        self._versionsView = None


    def dropEvent(self, event):

        #super(PipelineContentsView,self).dropEvent(event)
        '''
        if not event.isAccepted():
            # qdnd_win.cpp has weird behavior -- even if the event isn't accepted
            # by target widget, it sets accept() to true, which causes the executed
            # action to be reported as "move", which causes the view to remove the
            # source rows even though the target widget didn't like the drop.
            # Maybe it's better for the model to check drop-okay-ness during the
            # drag rather than only on drop; but the check involves not-insignificant work.
            event.setDropAction(QtCore.Qt.IgnoreAction)
        '''
        
        '''
        this event is catching drops onto the contents view
        
        '''     
        treeModel = self.treeSourceModel
        i = self.indexAt(event.pos())

        #if i.isValid():
            
        if event.source().__class__.__name__ == "PipelineContentsView":
            '''
            this is intercepting drops from within this view
            '''    
 
            drop_node = self.model().getNode(i)
            tree_index = treeModel.indexFromNode(drop_node, QtCore.QModelIndex())
            
            if tree_index.isValid():
                
                

                
                tree_node = treeModel.getNode(tree_index)
                mime = event.mimeData()
                
                
                item = cPickle.loads( str( mime.data( 'application/x-qabstractitemmodeldatalist' ) ) )
                item_index = treeModel.indexFromNode( item , QtCore.QModelIndex())
                item_parent = treeModel.parent( item_index )
                
                
                '''
                ignore drops of folders into assets
                '''
                if tree_node.typeInfo() == _asset_:
                    if item.typeInfo() == _folder_ or item.typeInfo() == _asset_:
                        
                        event.setDropAction(QtCore.Qt.IgnoreAction)
                        event.ignore()
                        return 

                '''
                ignore drag drop for stages
                '''
                if tree_node.typeInfo() == _stage_:

                        event.setDropAction(QtCore.Qt.IgnoreAction)
                        event.ignore()
                        return 

                         
                
                treeModel.removeRows(item_index.row(),1,item_parent)            
                self.treeView._proxyModel.invalidate()

                treeModel.dropMimeData(mime, event.dropAction,0,0,tree_index)
                 
                event.accept() 
                self.update(self.treeView.selectionModel().selection())    
                return
    
        
        elif event.source().__class__.__name__ == "pipelineTreeView":
            
            '''
            this is intercepting drops from within the tree view
            '''  
                        
            mime = event.mimeData()
            item = cPickle.loads( str( mime.data( 'application/x-qabstractitemmodeldatalist' ) ) )
            item_index = treeModel.indexFromNode( item , QtCore.QModelIndex())
            item_parent = treeModel.parent( item_index )            
            
            '''
            make sure the dropped item is not the root of the table
            '''
            HierarchyNodes = []
            for i in treeModel.listAncestos(self._treeParentIndex):
                HierarchyNodes.append(treeModel.getNode(i).id)
            
            print HierarchyNodes
            print item.id
            if item.id in HierarchyNodes:
                
                event.setDropAction(QtCore.Qt.IgnoreAction)
                event.ignore()
                return
                
            else:    
                '''
                the droped item is an ancestor of the the table root
                '''
                
                treeModel.removeRows(item_index.row(),0,item_parent)            
                self.treeView._proxyModel.invalidate()

                treeModel.dropMimeData(mime, event.dropAction,0,0,self._treeParentIndex)                
                self.treeView._proxyModel.invalidate()
                event.accept()
                x = self.treeView.fromProxyIndex(self._treeParentIndex)
                selection = QtGui.QItemSelection(x, x)        
                print treeModel.rowCount(self._treeParentIndex), "<-- rowcount"
                self.update(selection)
                self.treeView.setExpanded(x, True)
                
                return
        

    @property
    def versionsView(self):
        return self._versionsView
    
    @versionsView.setter
    def versionsView(self, view):
        self._versionsView = view


    @property
    def treeView(self):
        return self._treeView
    
    @treeView.setter
    def treeView(self, view):
        self._treeView = view

    @property
    def treeProxyModel(self):
        if self._treeProxyModel:
            return self._treeProxyModel
        
        return None
    
    @treeProxyModel.setter
    def treeProxyModel(self, model):
        self._treeProxyModel = model        

    @property
    def treeSourceModel(self):
        if self._treeSourceModel:
            return self._treeSourceModel
            
        return None
    
    @treeSourceModel.setter
    def treeSourceModel(self, model):
        self._treeSourceModel = model   

    def init_treeView(self):
        self.treeProxyModel = self.treeView.model()
        self.treeSourceModel = self.treeProxyModel.sourceModel()        

    def asTreeIndex(self, index):
        node = self.getNode(index)
        return self.treeSourceModel.indexFromNode(node,self.treeView.rootIndex())

    def icons_size(self, int):
        self.setIconSize(QtCore.QSize(int ,int)  )       
        self.verticalHeader().setDefaultSectionSize(int )
               
    def getNode(self, index):
        return self.model().getNode(index)

    def asTreeModelIndex(self, index):
        return self.treeView.asModelIndex(index)  


    def selection(self, selction, selection2):
        print selction, "-->", selction2
        print "signal"
        return
        if len(selection.indexes())>0:
            # using only the first selection for this task
            index = selection.indexes()[0]
             
            if index.isValid():
                node = self.getNode(index)
                
                treeIndex = self.asTreeIndex(index)
                #print treeIndex, " <--- table clicked"
                
                if node.typeInfo() == _stage_:
                    self.updateVersionsTable(node)
                else:
                    self.updateVersionsTable()  
                          
    '''
    def mouseReleaseEvent(self, event):
        super(PipelineContentsView, self).mouseReleaseEvent(event)
        index = self.indexAt(event.pos())
        if index.isValid():
            node = self.getNode(index)
            
            treeIndex = self.asTreeIndex(index)
            #print treeIndex, " <--- table clicked"
            
            if node.typeInfo() == _stage_:
                self.updateVersionsTable(node)
            else:
                self.updateVersionsTable()
                
            event.accept()
            return
                
        event.ignore()
        return'''

    
    def mousePressEvent(self, event):

        super(PipelineContentsView, self).mousePressEvent(event)
        index = self.indexAt(event.pos())
        if index.isValid():
            node = self.getNode(index)
            
            treeIndex = self.asTreeIndex(index)
            #print treeIndex, " <--- table clicked"
            
            if node.typeInfo() == _stage_:
                self.updateVersionsTable(node)
            else:
                self.updateVersionsTable()
                
            event.accept()
            return
                
        event.ignore()
        return
    
    '''
    updates the table view with a new model
    the model is a custom table model, bulit from the childs of the selected branch in the treeview
    
    index: QItemSelection
    '''
      
    def update(self, selection):
        #if the selection is not empty
        if len(selection.indexes())>0:
            # using only the first selection for this task
            index = selection.indexes()[0]
             
            if index.isValid():
                '''
                the index is from the tree's proxymodel
                we need to convert it to the source index
                '''
                
                treeModel = self.treeSourceModel
                src = self.asTreeModelIndex(index) 
                node =  self.treeView.asModelNode(src)

                contenetsList = []
    
                self._treeParentIndex = src
                self._treeParent = node
                                
                for row in range(treeModel.rowCount(src)):

                    item_index = treeModel.index(row,0,src)
                    treeNode = treeModel.getNode(item_index) 
                    #print treeNode, "---", row
                    contenetsList.append(treeNode)

                # ----> this is the section to append 'add' buttons to the list
                #
                #list.append(dt.AddComponent("new"))  
                #if node.typeInfo() == "NODE":                   
                #    list.append(dt.AddAsset("new")) 
                #    list.append(dt.AddFolder("new"))  
                    
                model = dtm.PipelineContentsModel(contenetsList)
                self.populateTable(model)
                self.updateVersionsTable()

    def populateTable(self, model = None):
               
         
        if model:         
            self.setModel(model)

            # resize the table headers to the new content
            self.horizontalHeader().setResizeMode(0,QtGui.QHeaderView.Stretch)#ResizeToContents)
            self.horizontalHeader().setResizeMode(1,QtGui.QHeaderView.Stretch)
        
            return True
                           
        # in case the selection is empty, or the index was invalid, clear the table            
        self.setModel(dtm.PipelineContentsModel([dt.DummyNode("")]))  
        self.horizontalHeader().setResizeMode(0,QtGui.QHeaderView.Stretch)#ResizeToContents)
        self.horizontalHeader().setResizeMode(1,QtGui.QHeaderView.Stretch)      
        #self.clearModel()        
        return False
    
    def clearModel(self):
        self.setModel(None)

    
    def mouseDoubleClickEvent(self, event):
        
        
        index = self.indexAt(event.pos())
        node = None
        if index.isValid():

            
            tableModelNode = self.model().getNode(index)  
            src = self.asTreeIndex(index)
            node =  self.treeSourceModel.getNode(src)
            
        if node:
            if tableModelNode.typeInfo() != _stage_:   
                '''
                ---> double click on a folder or asset to open it
                '''
                treeIndex = self.treeView.fromProxyIndex(self.asTreeIndex(index))       
                self.setTreeViewtSelection(treeIndex)  
                self.treeView.saveSelection()
                
                event.accept()
                return 
            else:
                '''
                -----> double click on a component... what shoud we do?
                '''
                super(PipelineContentsView, self).mouseDoubleClickEvent(event)
                event.accept()
                return
        
        event.accept()
        return

            
    def contextMenuEvent(self, event):
     
        handled = True
        node = None
        index = self.indexAt(event.pos())
        menu = QtGui.QMenu()            
        actions = []
        append_defult_options = True
        
        if index.isValid():
            
            tableModelNode = self.model().getNode(index)                
            src = self.asTreeIndex(index)                 
            node =  self.treeSourceModel.getNode(src)
            
            if tableModelNode.typeInfo() == _dummy_:
                append_defult_options = True
            else:
                append_defult_options = False    
            
                   
        if node:
            
               
            if node.typeInfo() == _folder_: 
                actions.append(QtGui.QAction("Delete", menu, triggered = functools.partial(self.delete, src) ))

                
            if node.typeInfo() == _asset_:
                actions.append(QtGui.QAction("Delete", menu, triggered = functools.partial(self.delete, src) ))

                
            if node.typeInfo() == _stage_:
                actions.append(QtGui.QAction("Delete", menu, triggered = functools.partial(self.delete, src) ))
                        
        
        if append_defult_options:
            
            if self._treeParent.typeInfo() == _asset_:
                           
                actions.append(QtGui.QAction("Create new %s"%(_stage_), menu, triggered = functools.partial(self.create_new_stage,self._treeParentIndex) ))
            
            elif self._treeParent.typeInfo() == _folder_:
            
                actions.append(QtGui.QAction("Create new %s"%(_folder_), menu, triggered = functools.partial(self.create_new_folder, self._treeParentIndex) ))
                actions.append(QtGui.QAction("Create new %s"%(_asset_), menu, triggered = functools.partial(self.create_new_asset,self._treeParentIndex) ))
   
        menu.addActions(actions)      
       
        #if handled:
            
        menu.exec_(event.globalPos())
         #TELL QT IVE HANDLED THIS THING
            
        #else:
            #event.ignore() #GIVE SOMEONE ELSE A CHANCE TO HANDLE IT
        
        event.accept()           
        return


    def setTreeViewtSelection(self,index):
        
        self.treeView.select(index)
        selection = QtGui.QItemSelection(index, index)        
        self.update(selection)    


    def restoreTreeViewtSelection(self):
        # restore the table from the tree with up to date data
        # using the tree view's last selection
        self.treeView.restoreSelection()
        treeLastIndex =  self.treeView.fromProxyIndex(self.treeView.userSelection)       
        self.setTreeViewtSelection(treeLastIndex)
        
      

    def delete(self,  index):
        # clear the table before the action to prevent data being invalid
        self.clearModel()
        self.treeView.delete(index)        
        self.restoreTreeViewtSelection()
        #i = self.asTreeIndex(index)
        #ii = self.treeView.fromProxyIndex(i)
        #self.updateTable(ii)

    def create_new_folder(self, parent):
        self.clearModel()             
        self.treeView.create_new_folder(parent)               
        self.restoreTreeViewtSelection()        

    def create_new_asset(self, parent):
        
        self.clearModel()             
        self.treeView.create_new_asset(parent)              
        self.restoreTreeViewtSelection()
               
    def create_new_stage(self, parent):
        
        self.clearModel()             
        self.treeView.create_new_stage(parent)              
        self.restoreTreeViewtSelection()
        
    def updateTable(self, index):
        selection = QtGui.QItemSelection(index, index)        
        self.update(selection)

    def updateVersionsTable(self, node = None):
        
        if self.versionsView:
            if node:
                versionModel = dtm.PipelineVersionsModel(node._versions)
                self.versionsView.setModel(versionModel)
            else:
                try:
                    del versionModel
                except:
                    pass
                self.versionsView.setModel(None)
                   
class pipelineTreeView(QtGui.QTreeView):
    def __init__(self,parent = None):
        super(pipelineTreeView, self).__init__(parent)
        
        # display options
        self.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)
        self.setDragEnabled( True )
        self.setAcceptDrops( True )
        self.setDragDropMode( QtGui.QAbstractItemView.InternalMove )
        self.setDropIndicatorShown(True)
        self.resizeColumnToContents(True) 
                
        #local variables

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

        super(pipelineTreeView,self).setModel(model)
        
        self.proxyModel = self.model()
        self.sourceModel = self.proxyModel.sourceModel()        
        
        '''
        this will expend the tree only on the first level, which should be
        the projects name folder
        the rest will be collapsed
        '''
        
        
        self.expandAll()
        i =  self.model().index(0,0,self.rootIndex())
        
        for row in range(self.model().rowCount(i)):
            x = self.model().index(row,0,i)
            self.setExpanded(x,False)
        
        
        
        
        
        '''
        save the expended state of the tree
        '''
        self.saveState()


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
        self.tableView.update(self.selectionModel().selection())    
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

        super(pipelineTreeView,self).dropEvent(event)
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
                if model_node.typeInfo() == _asset_:
                    if item.typeInfo() == _folder_ or item.typeInfo() == _asset_:
                        
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

        super(pipelineTreeView,self).dragEnterEvent(event)

        if event.source().__class__.__name__ == 'PipelineContentsView':        
            return event.setAccepted(True)

    '''
    def dragMoveEvent(self, event):

        super(pipelineTreeView,self).dragMoveEvent(event)
        #return event.setAccepted(True)
    '''
    
    def projectRootIndex(self):
        modelRootIndex = self.asModelIndex(self.rootIndex())
        # get the first childe of the model's root                                   
        return self.sourceModel.index(0,0,modelRootIndex)
      
    
    def mouseReleaseEvent(self, event):
        
        super(pipelineTreeView, self).mouseReleaseEvent(event)
        self.saveSelection()
        self.tableView.update(self.selectionModel().selection())
        event.accept
   
    def contextMenuEvent(self, event):
        
        handled = True
        index = self.indexAt(event.pos())
        menu = QtGui.QMenu()        
        node = None
       
        if index.isValid():
            src = self.asModelIndex(index)
            node = self.asModelNode(src)

        actions = []  
          
        if node:

            if node.typeInfo() == _folder_: 
                actions.append(QtGui.QAction("Create new %s"%(_asset_), menu, triggered = functools.partial(self.create_new_asset, src) ))
                actions.append(QtGui.QAction("Create new %s"%(_folder_), menu, triggered = functools.partial(self.create_new_folder, src) ))
                actions.append(QtGui.QAction("Delete", menu, triggered = functools.partial(self.delete, src) ))
                
            elif node.typeInfo() == _asset_:
                actions.append(QtGui.QAction("Create new %s"%(_stage_), menu, triggered = functools.partial(self.create_new_stage, src) ))
                actions.append(QtGui.QAction("Delete", menu, triggered = functools.partial(self.delete, src) ))

        else:
            actions.append(QtGui.QAction("Create new %s"%(_folder_), menu, triggered = functools.partial(self.create_new_folder,self.projectRootIndex()) ))
            actions.append(QtGui.QAction("Create new %s"%(_asset_), menu, triggered = functools.partial(self.create_new_asset,self.projectRootIndex()) ))

        menu.addActions(actions)      
        

        #if handled:

        menu.exec_(event.globalPos())
        event.accept() #TELL QT IVE HANDLED THIS THING
            
        #else:
            #event.ignore() #GIVE SOMEONE ELSE A CHANCE TO HANDLE IT
                   
        return

    '''
    functions to add/remove tree nodes
    this is we will want some user input...
    
    '''
    def delete(self,  index):
        # clear the table view              
        self.tableView.update(QtGui.QItemSelection())
        
        node = self.asModelNode(index)
        parentIndex = self.sourceModel.parent(index)
        self.sourceModel.removeRows(node.row(),1,parentIndex, kill=True)
        self._proxyModel.invalidate()
        
        #self.updateTable( parentIndex)
        self.updateTable( self.fromProxyIndex(parentIndex))
        return True
        
    def create_new_folder(self, parent):
        node = dt.FolderNode(_folder_)        
        self.sourceModel.insertRows( 0, 1, parent = parent , node = node)
        self._proxyModel.invalidate()
        self.updateTable( self.fromProxyIndex(parent))
        
    def create_new_asset(self, parent):
        node = dt.AssetNode(_asset_)
        self._sourceModel.insertRows( 0, 1, parent = parent , node = node)
        self._proxyModel.invalidate()
        self.updateTable( self.fromProxyIndex(parent))
        
    def create_new_stage(self, parent):
        node = dt.StageNode(_stage_)
        self._sourceModel.insertRows( 0, 1, parent = parent , node = node)
        self._proxyModel.invalidate()
        self.updateTable( self.fromProxyIndex(parent))

    def updateTable(self, index):
        selection = QtGui.QItemSelection(index, index)        
        self.tableView.update(selection)

    @property
    def tree_as_flat_list(self):
        return self._tree_as_flat_list
    
    @tree_as_flat_list.setter 
    def tree_as_flat_list(self, list):
        self._tree_as_flat_list = list

    def list_flat_hierarchy(self):
        print "<---listing"
        list = []
        for i in self.sourceModel.listHierarchy(QtCore.QModelIndex()):
            list.append(self.sourceModel.getNode(i))
        
        self.tree_as_flat_list = list

    def filterContents(self):
        
        if self.tree_as_flat_list:
            self.tableView.clearModel()
            
            model = dtm.PipelineContentsModel(self.tree_as_flat_list)
            self.tableView.populateTable(model)
            

    