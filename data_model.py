
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
        self.setMinimumWidth(250)
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
                if tree_node.typeInfo() == "ASSET":
                    if item.typeInfo() == "NODE" or item.typeInfo() == "ASSET":
                        
                        event.setDropAction(QtCore.Qt.IgnoreAction)
                        event.ignore()
                        return 

                '''
                ignore drops of folders into assets or components
                '''
                if tree_node.typeInfo() == "COMPONENT":

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

    def mouseReleaseEvent(self, event):
        super(PipelineContentsView, self).mouseReleaseEvent(event)
        index = self.indexAt(event.pos())
        if index.isValid():
            node = self.getNode(index)
            if not node.typeInfo() == "ADD-COMPONENT" and not node.typeInfo() == "ADD-ASSET" and not node.typeInfo() == "ADD-FOLDER":
                treeIndex = self.asTreeIndex(index)
                print treeIndex, " <--- table clicked"
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
         
                if len(contenetsList) > 0:         
                    self.setModel(PipelineContentsModel(contenetsList))
                
                    # resize the table headers to the new content
                    self.horizontalHeader().setResizeMode(0,QtGui.QHeaderView.Stretch)#ResizeToContents)
                    self.horizontalHeader().setResizeMode(1,QtGui.QHeaderView.Stretch)
                
                    return True
                         
        # in case the selection is empty, or the index was invalid, clear the table            
        self.setModel(PipelineContentsModel([dt.DummyNode("")]))  
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
            if tableModelNode.typeInfo() != "COMPONENT":   
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
            
            if tableModelNode.typeInfo() == "DUMMY":
                append_defult_options = True
            else:
                append_defult_options = False    
            
                   
        if node:
            
            if tableModelNode.typeInfo()[0:3] != "ADD":
                
                
                
                if node.typeInfo() == "NODE": 
                    actions.append(QtGui.QAction("Delete", menu, triggered = functools.partial(self.delete, src) ))

                    
                if node.typeInfo() == "ASSET":
                    actions.append(QtGui.QAction("Delete", menu, triggered = functools.partial(self.delete, src) ))

                    
                if node.typeInfo() == "COMPONENT":
                    actions.append(QtGui.QAction("Delete", menu, triggered = functools.partial(self.delete, src) ))
                
                
                '''
                ---> this is for if we use the table buttons to add nodes to the tree...
            
                
                if tableModelNode.typeInfo() == "ADD-COMPONENT":
                    actions.append(QtGui.QAction("Create new Component", menu, triggered = functools.partial(self.create_new_component,self._treeParent) ))
                elif tableModelNode.typeInfo() == "ADD-ASSET":
                    actions.append(QtGui.QAction("Create new Asset", menu, triggered = functools.partial(self.create_new_asset,self._treeParent) ))  
                elif tableModelNode.typeInfo() == "ADD-FOLDER":
                    actions.append(QtGui.QAction("Create new folder", menu, triggered = functools.partial(self.create_new_folder,self._treeParent) ))     
                '''
       
        
        if append_defult_options:
                           
            actions.append(QtGui.QAction("Create new Component", menu, triggered = functools.partial(self.create_new_component,self._treeParentIndex) ))
            
            if self._treeParent.typeInfo() == "NODE":
            
                actions.append(QtGui.QAction("Create new folder", menu, triggered = functools.partial(self.create_new_folder, self._treeParentIndex) ))
                actions.append(QtGui.QAction("Create new Asset", menu, triggered = functools.partial(self.create_new_asset,self._treeParentIndex) ))
   
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
               
    def create_new_component(self, parent):
        
        self.clearModel()             
        self.treeView.create_new_component(parent)              
        self.restoreTreeViewtSelection()
        
    def updateTable(self, index):
        selection = QtGui.QItemSelection(index, index)        
        self.update(selection)

                   
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
        '''
        self.viewport().installEventFilter(self)

    def eventFilter(self, object, event):
        if object is self.viewport():
            if event.type() == QtCore.QEvent.DragMove:
                print "Moved!"
            elif event.type() == QtCore.QEvent.Drop:
                print "Dropped!"
        
        return super(pipelineTreeView, self).eventFilter(object, event)
    '''
    
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
                if model_node.typeInfo() == "ASSET":
                    if item.typeInfo() == "NODE" or item.typeInfo() == "ASSET":
                        
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

            if node.typeInfo() == "NODE": 
                actions.append(QtGui.QAction("Create new Asset", menu, triggered = functools.partial(self.create_new_asset, src) ))
                actions.append(QtGui.QAction("Create new Folder", menu, triggered = functools.partial(self.create_new_folder, src) ))
                actions.append(QtGui.QAction("Delete", menu, triggered = functools.partial(self.delete, src) ))
                
            elif node.typeInfo() == "ASSET":

                actions.append(QtGui.QAction("Delete", menu, triggered = functools.partial(self.delete, src) ))
                

        else:
            actions.append(QtGui.QAction("Create new folder", menu, triggered = functools.partial(self.create_new_folder,self.projectRootIndex()) ))
            actions.append(QtGui.QAction("Create new Asset", menu, triggered = functools.partial(self.create_new_asset,self.projectRootIndex()) ))

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
        node = dt.Node("folder")        
        self.sourceModel.insertRows( 0, 1, parent = parent , node = node)
        self._proxyModel.invalidate()
        self.updateTable( self.fromProxyIndex(parent))
        
    def create_new_asset(self, parent):
        node = dt.AssetNode("asset","")
        self._sourceModel.insertRows( 0, 1, parent = parent , node = node)
        self._proxyModel.invalidate()
        self.updateTable( self.fromProxyIndex(parent))
        
    def create_new_component(self, parent):
        node = dt.ComponentNode("component","")
        self._sourceModel.insertRows( 0, 1, parent = parent , node = node)
        self._proxyModel.invalidate()
        self.updateTable( self.fromProxyIndex(parent))

    def updateTable(self, index):
        selection = QtGui.QItemSelection(index, index)        
        self.tableView.update(selection)


class PipelineProjectModel(QtCore.QAbstractItemModel):
    
    MIMEDATA = 'application/x-qabstractitemmodeldatalist'
    sortRole   = QtCore.Qt.UserRole
    filterRole = QtCore.Qt.UserRole + 1
    expendedRole = QtCore.Qt.UserRole + 2
    
    """INPUTS: Node, QObject"""
    def __init__(self, root, parent=None):
        super(PipelineProjectModel, self).__init__(parent)
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
            
        if role == PipelineProjectModel.sortRole:
            return node.typeInfo()

        if role == PipelineProjectModel.filterRole:
            return node.typeInfo()

        if role == QtCore.Qt.SizeHintRole:
            return QtCore.QSize(0,19)
        
        # this is for expending state - the result must be uniqe!!!
        if role == 165:
            return node.id
        
        if role == PipelineProjectModel.expendedRole:

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
            if role == PipelineProjectModel.expendedRole:
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
            
            if node.typeInfo() == "ROOT":
                return  QtCore.Qt.ItemIsEnabled |QtCore.Qt.ItemIsSelectable
            
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
        mimedata.setData( PipelineProjectModel.MIMEDATA , data ) 
   
        return mimedata
     
    def dropMimeData( self, mimedata, action, row, column, parentIndex ):

        '''Handles the dropping of an item onto the model.
         
        De-serializes the data into a TreeItem instance and inserts it into the model.
        '''
        if not mimedata.hasFormat( PipelineProjectModel.MIMEDATA ):
            return False
            
        item = cPickle.loads( str( mimedata.data( PipelineProjectModel.MIMEDATA ) ) )
        dropParent = self.getNode( parentIndex )
        
        # do not allow a folder to be dropped on an asset...
        if dropParent.typeInfo() == "ASSET":
            if item.typeInfo() == "NODE" or item.typeInfo() == "ASSET":
                return False
        
        if dropParent.typeInfo() == "ROOT":
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
        for i in range(self.rowCount(index)):
            data.append(self.index(i, 0, index))
            
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



class PipelineContentsModel(QtCore.QAbstractTableModel):
    
    MIMEDATA = 'application/x-qabstractitemmodeldatalist'
    
    def __init__(self, components = [], parent = None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.__components = components


    def headerData(self, section, orientation, role):

        if role == QtCore.Qt.DisplayRole:
            
            if orientation == QtCore.Qt.Horizontal:
                if section == 0:
                    return "Contents"
                if section == 1:
                    return "Info"
            else:
                return 

        if role == QtCore.Qt.DecorationRole:

            if orientation == QtCore.Qt.Horizontal:
                if section == 0:
                    return QtGui.QIcon(QtGui.QPixmap(cube_icon))
                if section == 1:
                    return QtGui.QIcon(QtGui.QPixmap(cube_icon))
            else:
                return 


    def rowCount(self, parent):
        return len(self.__components)

    def columnCount(self, parent):
        return 1
        
    def data(self, index, role):
        
        
        if role == QtCore.Qt.EditRole:
            return self.__components[index.row()].name
        
        
        if role == QtCore.Qt.DecorationRole:
            if index.column() == 0:
                resource = self.__components[index.row()].resource()
                return QtGui.QIcon(QtGui.QPixmap(resource))
              
        if role == QtCore.Qt.DisplayRole:
            
            row = index.row()
            if index.column() == 0:
                return self.__components[row].name
            if index.column() == 1:
                return "test test test test test test"

    def flags(self, index):
        
        if index.isValid():
        
            if self.getNode(index).typeInfo() == "DUMMY":
                return QtCore.Qt.NoItemFlags
        
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDropEnabled | QtCore.Qt.ItemIsDragEnabled
        
    """CUSTOM"""
    """INPUTS: QModelIndex"""
    def getNode(self, index):
        if index.isValid():
            return self.__components[index.row()]

        return None        
        
    def setData(self, index, value, role = QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            
            row = index.row()
            
            if role == QtCore.Qt.EditRole:
                self.__components[row].name = value 
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

    def supportedDropActions( self ):

        return QtCore.Qt.MoveAction | QtCore.Qt.CopyAction

    #def mimeTypes( self ):
    #    '''The MimeType for the encoded data.'''
    #    types =  'application/x-qabstractitemmodeldatalist' 
    #    return types
        
    def mimeData( self, indices ):
        '''Encode serialized data from the item at the given index into a QMimeData object.'''
        
        data = ''
        item = self.getNode( indices[0] )

        try:
            data += cPickle.dumps( item )

        except:
            pass

        mimedata = QtCore.QMimeData()
        mimedata.setData( PipelineContentsModel.MIMEDATA , data ) 


        return mimedata

    '''
    def dropMimeData( self, mimedata, action, row, column, parentIndex ):
        #print mimedata, action, row, column, parentIndex
        print self.getNode(parentIndex).name
        return

        if not mimedata.hasFormat( PipelineProjectModel.MIMEDATA ):
            return False
            
        
        
        
        item = cPickle.loads( str( mimedata.data( PipelineProjectModel.MIMEDATA ) ) )
        dropParent = self.getNode( parentIndex )
        
        # do not allow a folder to be dropped on an asset...
        if dropParent.typeInfo() == "ASSET":
            if item.typeInfo() == "NODE" or item.typeInfo() == "ASSET":
                return False
        
        if dropParent.typeInfo() == "ROOT":
            return False
            
               
        #dropParent.addChild( item )
        self.insertRows( dropParent.childCount(), 1, parent = parentIndex )
            
        self.dataChanged.emit( parentIndex, parentIndex )
         
        return True '''

        
class PipelineProjectProxyModel(QtGui.QSortFilterProxyModel):
    def __init__(self,parent = None):
        
        super(PipelineProjectProxyModel, self).__init__(parent)
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

        if super(PipelineProjectProxyModel,self).filterAcceptsRow(sourceRow,sourceParent): 
            
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
             
        super(PipelineProjectProxyModel, self).setFilterRegExp(exp)
        if self.treeView:
            if len(exp)>0:  
                #self.treeView._ignoreSelections = True
                      
                self.treeView._ignoreExpentions = True
                self.treeView.expandAll()
                self.treeView._ignoreExpentions = False
            else:
                self.treeView._ignoreExpentions = True
                self.treeView.restoreState()          
                self.treeView._ignoreExpentions = False         

        