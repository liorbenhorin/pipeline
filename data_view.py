
from PySide import QtCore, QtGui, QtXml
import cPickle
import os
import functools

import data as dt
reload(dt)

import data_model as dtm
reload(dtm)

import modules.files as files
reload(files)

import dialogue as dlg
reload(dlg)


global _node_
global _root_
global  _stage_
global _asset_
global _folder_
global _dummy_
global _version_
global _new_
global _catagory_

_catagory_ = "catagory"
_new_ = "new"
_version_ = "version"
_node_ = "node"
_root_ = "root"
_stage_ = "stage"
_asset_ = "asset"
_folder_ = "folder" 
_dummy_ = "dummy"


# def set_icons():
#     global localIconPath
#
#     localIconPath = os.path.join(os.path.dirname(__file__), 'icons')
#     if not os.path.exists(localIconPath):
#         log.info("icons folder not found: %s"%localIconPath)
#         return
#
#
#     global offline_icon
#     global catagory_icon
#     global asset_icon
#     global component_icon
#     global new_icon
#     global delete_icon
#     global load_icon
#     global unload_icon
#     global project_icon
#     global users_icon
#     global settings_icon
#     global set_icon
#     global yes_icon
#     global no_icon
#     global search_icon
#     global edit_icon
#     global delete_folder_icon
#     global new_folder_icon
#     global open_icon
#     global save_icon
#     global save_master_icon
#     global add_icon
#     global down_arrow_icon
#     global import_icon
#     global export_icon
#     global help_icon
#     global anim_icon
#     global asset_mode_icon
#     global reload_icon
#     global shutter_icon
#     global camrea_icon
#     global play_icon
#     global comment_icon
#     global large_icon
#     global small_icon
#
#     global large_image_icon
#     global large_image_icon_dark
#     global large_image_icon_click
#     global large_image_icon_click_dark
#     global wide_image_icon
#     global wide_image_icon_click
#     global wide_image_icon_dark
#     global wide_image_icon_click_dark
#
#
#     offline_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"offline"))
#     catagory_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"catagory"))
#     asset_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"asset"))
#     component_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"component"))
#     new_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"new"))
#     delete_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"delete"))
#     load_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"load"))
#     unload_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"unload"))
#     project_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"project"))
#     users_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"users"))
#     settings_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"settings"))
#     set_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"set"))
#     yes_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"yes"))
#     no_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"no"))
#     search_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"search"))
#     edit_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"edit"))
#     delete_folder_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"delete_folder"))
#     new_folder_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"new_folder"))
#     open_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"open"))
#     save_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"save"))
#     save_master_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"save_master"))
#     add_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"add"))
#     down_arrow_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"down_arrow"))
#     import_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"import"))
#     export_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"export"))
#     help_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"help"))
#     anim_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"anim"))
#     asset_mode_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"asset_mode"))
#     reload_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"reload"))
#     shutter_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"shutter"))
#     camrea_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"camera"))
#     play_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"play"))
#     comment_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"comment"))
#
#     large_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"large"))
#     small_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"small"))
#
#
#     large_image_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"large_image"))
#     large_image_icon_dark = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"large_image_dark"))
#     large_image_icon_click = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"large_image_click"))
#     large_image_icon_click_dark = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"large_image_click_dark"))
#
#     wide_image_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"wide_image"))
#     wide_image_icon_click = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"wide_image_click"))
#     wide_image_icon_dark = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"wide_image_dark"))
#     wide_image_icon_click_dark = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"wide_image_click_dark"))
#
#
# # declare all the global icons  variables
# set_icons()


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


    localIconPath = os.path.join(os.path.dirname(__file__), 'icons/')
    if not os.path.exists(localIconPath):
        return

    global large_icon
    global small_icon
    global reload_icon
    global load_icon
    global open_icon
    global new_icon
    global set_icon
    global edit_icon

    edit_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "edit"))
    set_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "set"))
    reload_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "reload"))
    load_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "load"))
    large_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"large"))
    small_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"small"))
    open_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "openFolder"))
    new_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "new"))
    
set_icons()


def setComboValue(QComboBox, String):
    index = QComboBox.findText(String, QtCore.Qt.MatchFixedString)
    if index >= 0:
        QComboBox.setCurrentIndex(index)
        return True
    return False


# class ColorDelegate: public QItemDelegate
# {
# public:
# 	ColorDelegate(QObject *parent = 0) : QItemDelegate(parent) {}
#
# public:
# 	virtual void paint(QPainter *painter, const QStyleOptionViewItem &option, const QModelIndex &index) const
# 	{
# 		drawBackground(painter, option, index);
# 		QItemDelegate::paint(painter, option, index);
# 	}
#
# protected:
# 	virtual void drawBackground(QPainter *painter, const QStyleOptionViewItem &option, const QModelIndex &index) const
# 	{
# 		Q_UNUSED(index);
# 		painter->fillRect(option.rect, QColor(qrand()%255, qrand()%255, qrand()%255));
# 	}
# };
#
# class rowBackgroundColorDelegate(QtGui.QItemDelegate):
#
#     def __init__(self, parent):
#         QtGui.QItemDelegate.__init__(self, parent)
#
#     def paint(self, painter, option, index):
#         hoverd = False
#         if option.state == QtGui.QStyle.State_MouseOver:
#             hoverd = True
#             print "Y"
#         else:
#             print "A"
#             if self.parent():
#                 print "Z"
#                 t = self.parent()
#                 hover = t.indexAt(t.viewport().mapToGlobal(QtGui.QCursor.pos()))
#
#                 if hover.row() == index.row():
#                     print "x"
#                     hoverd = True
#                     t.update(hover)
#
#         #if hoverd:
#         print "YY"
#         bg = QtGui.QBrush(option.palette.highlight())
#         bgColor = QtGui.QColor(option.palette.highlight().color())
#         bgColor.setAlpha(100)
#         bg.setColor(bgColor)
#
#         painter.fillRect(option.rect, bg)
#         painter.setPen(option.palette.text().color())
#
#
#         #self.drawBackground(painter, option, index)
#         #QItemDelegate::paint(painter, option, index)
#
#     def drawBackground(self, painter, option, index):
#
#
#         painter.fillRect(option.rect, QtGui.QColor(10,10,10))


class EditProjectButtonDelegate(QtGui.QItemDelegate):

    def __init__(self, parent):
        QtGui.QItemDelegate.__init__(self, parent)

    def paint(self, painter, option, index):

        if not self.parent().indexWidget(index):


            label = "Edit"
            icon = edit_icon


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
            icon = set_icon


            button = QtGui.QPushButton(
                label,
                index.data(),
                self.parent(),
                clicked=self.parent().setProject
            )

            button.setIconSize(QtCore.QSize(20, 20))
            button.setIcon(QtGui.QIcon(icon))
            self.parent().setIndexWidget(index, button)

class PipelineProjectsView(QtGui.QTableView):
    def __init__(self, parentWidget = None, parent = None):
        super(PipelineProjectsView, self).__init__(parent)

        self.parent = parent
        self.parentWidget = parentWidget

        self.setAlternatingRowColors(True)
        self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.setWordWrap(True)
        #elf.setShowGrid(False)
        self.verticalHeader().setResizeMode(QtGui.QHeaderView.Fixed)
        #self.icons_size(32)
        #self.setMinimumWidth(250)
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        #self.setSortingEnabled(True)
        #self.horizontalHeader().setOffset(10)
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
        #self.horizontalHeader().setDefaultSectionSize(int)
        #self.verticalHeader().setDefaultSectionSize(int)
        #self.horizontalHeader().resizeSection(0, int)
        #self.horizontalHeader().setResizeMode(0, QtGui.QHeaderView.Fixed)
        self.update()

    def clearModel(self):
        self.setModel(None)
        if self._proxyModel:
            self._proxyModel.setSourceModel(None)
            self._proxyModel = None


    def setModel_(self, model = None):
        self.clearModel()
        if model:


            self._proxyModel = dtm.PipelineVersionsProxyModel()
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
        if self.model().sourceModel().items[0].typeInfo() == _new_:
            self.model().sourceModel().items[0].parent().initialVersion()
        else:
            self.model().sourceModel().getNode(index).edit()
            self.setCurrentIndex(index)

    def setProject(self):

        button = self.sender()
        index = self.indexAt(button.pos())
        index = self.model().mapToSource(index)
        if self.model().sourceModel().items[0].typeInfo() == _new_:
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
            if self.parent().model().sourceModel().getNode(soure_index).typeInfo() == _new_:
                label = ""
                icon = new_icon
            else:
                label = ""
                icon = open_icon

            button = QtGui.QPushButton(
                label,
                self.parent(),
                clicked=self.parent().MultiButtonClicked
            )

            button.setIconSize(QtCore.QSize(20, 20))

            button.setIcon(QtGui.QIcon(icon))

            self.parent().setIndexWidget(index, button)


class HeaderViewFilter2(QtCore.QObject):
    def __init__(self, parent = None,  *args):
        super(HeaderViewFilter2, self).__init__(parent, *args)

    def eventFilter(self, object, event):
        if event.type() == QtCore.QEvent.MouseMove:
            print "*"
            logicalIndex = object.indexAt(event.pos())
            #print logicalIndex, "*"
            return True


class PipelineVersionsView(QtGui.QTreeView):
    def __init__(self, parentWidget = None, parent = None):
        super(PipelineVersionsView, self).__init__(parent)

        self.parent = parent
        self.parentWidget = parentWidget

        self.setAlternatingRowColors(True)
        self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.setWordWrap(True)

        #self.setShowGrid(False)


        #>>>self.verticalHeader().setResizeMode(QtGui.QHeaderView.Fixed)
        #self.icons_size(32)       
        #self.setMinimumWidth(250)


        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)


        #self.setSortingEnabled(True)
        #self.horizontalHeader().setOffset(10)
        #>>>self.horizontalHeader().hide()
        self.setSortingEnabled(True)

        self.setMouseTracking(True)
        #self.filter = HeaderViewFilter2(self)
        #self.installEventFilter(self.filter)

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

    # def mouseMoveEvent(self, event):
    #     print event, "<<<"
    #     print self.indexAt(event.pos()), "<<<"

    # def mouseMoveEvent(self, e):
    #
    #     i = self.indexAt(e.pos())
    #
    #
    #     self.setItemDelegateForRow(i.row(), rowBackgroundColorDelegate(self))

    def addSlider(self):

        self._slider = IconScaleSlider(self)
        self.parentWidget.layout().addWidget(self._slider)
        self._slider.listSlider.sliderMoved.connect(self.icons_size)
        self.icons_size(32)


    def icons_size(self, int):
        self.setIconSize(QtCore.QSize(int, int))
        #self.horizontalHeader().setDefaultSectionSize(int)
        #>>>self.verticalHeader().setDefaultSectionSize(int)
        #>>>self.horizontalHeader().resizeSection(0, int)
        #>>>self.horizontalHeader().setResizeMode(0, QtGui.QHeaderView.Fixed)
        self.header().resizeSection(0, int)
        self.header().setResizeMode(0, QtGui.QHeaderView.Fixed)
        try:
            self.model().sourceModel()._rowHeight = int
        except:
            print "no model"
        self.update()

    def clearModel(self):
        self.setModel(None)
        if self._proxyModel:
            self._proxyModel.setSourceModel(None)
            self._proxyModel = None


    def setModel_(self, model = None):
        self.clearModel()
        if model:


            self._proxyModel = dtm.PipelineVersionsProxyModel()
            self._proxyModel.setSourceModel(model)

            self._proxyModel.setDynamicSortFilter(True)
            #self._proxyModel.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
            self._proxyModel.setSortRole(dtm.PipelineVersionsModel2.sortRole)
            #self._proxyModel.setFilterRole(0)
            #self._proxyModel.setFilterKeyColumn(2)

            #self._proxyModel.invalidateFilter()
            self.setModel(self._proxyModel)

            self.setIndentation(0)



            #self.header().setResizeMode(QtGui.QHeaderView.Stretch)






            self.header().resizeSection(0, 32)
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
            #>>>self.horizontalHeader().resizeSection(4,40)
            #>>>self.horizontalHeader().setResizeMode(4,QtGui.QHeaderView.Fixed)
            # size the load button column
            #>>>self.horizontalHeader().resizeSection(3,32)
            #>>>self.horizontalHeader().setResizeMode(3,QtGui.QHeaderView.Fixed)
            # size the note button column
            #self.horizontalHeader().resizeSection(2,25)
            #self.horizontalHeader().setResizeMode(2,QtGui.QHeaderView.Fixed)

            #>>>self.horizontalHeader().resizeSection(0, self._slider.listSlider.value())
            #>>>self.horizontalHeader().setResizeMode(0, QtGui.QHeaderView.Fixed)

            #self.horizontalHeader().setResizeMode(0,QtGui.QHeaderView.Stretch)
            #>>>self.horizontalHeader().setResizeMode(1,QtGui.QHeaderView.Stretch)
            #>>>self.horizontalHeader().setResizeMode(2, QtGui.QHeaderView.Stretch)
            
            # setup the buttons for loading and more options with delegates
            self.setItemDelegateForColumn(5,  loadButtonDelegate(self))
            #self.setItemDelegateForColumn(4,  OptionsButtonDelegate(self))

            #self.setCurrentIndex(self.model().sourceModel().index(0, 0, None))

            self.sortByColumn(1, QtCore.Qt.DescendingOrder)
            #self.model().sort(0,QtCore.Qt.DescendingOrder)

            self.update()



            #self.setCurrentIndex(self.model().index(0,0, None))

    
    '''
    def setModel(self,model):
        
        super(PipelineVersionsView,self).setModel(model)
        # size the options button column
    '''

    #@QtCore.Slot()
    def MultiButtonClicked(self):
        # This slot will be called when our button is clicked. 
        # self.sender() returns a refence to the QPushButton created
        # by the delegate, not the delegate itself.
        button = self.sender()
        index = self.indexAt(button.pos())
        index = self.model().mapToSource(index)
        if self.model().sourceModel().getNode(index).typeInfo() == _new_:
            self.model().sourceModel().getNode(index).parent().initialVersion()
        else:
            self.model().sourceModel().getNode(index).load()
            self.parent.set_thumbnail(self.model().sourceModel().getNode(index).resource)
            self.parent.version = self.model().sourceModel().getNode(index)
            self.setCurrentIndex(self.model().mapFromSource(index))


    #@QtCore.Slot()
    def deletActionClicked(self):
        # This slot will be called when our button is clicked. 
        # self.sender() returns a refence to the QPushButton created
        # by the delegate, not the delegate itself.
        button = self.sender().parent()
        index = self.indexAt(button.pos())
        index = self.model().mapToSource(index)
        self.model().sourceModel().getNode(index).delete_me()


    # def delete(self):
    #     # This slot will be called when our button is clicked.
    #     # self.sender() returns a refence to the QPushButton created
    #     # by the delegate, not the delegate itself.
    #     button = self.sender().parent()
    #     index = self.indexAt(button.pos())
    #     index = self.model().mapToSource(index)
    #     self.model().sourceModel().getNode(index).delete_me()
    #
    #     node = self.asModelNode(index)
    #     parentIndex = self.sourceModel.parent(index)
    #     self.sourceModel.removeRows(node.row(), 1, parentIndex, kill=True)
    #     self._proxyModel.invalidate()
    #
    # def contextMenuEvent(self, event):
    #
    #     handled = True
    #     node = None
    #     index = self.indexAt(event.pos())
    #     menu = QtGui.QMenu()
    #     actions = []
    #     append_defult_options = True
    #
    #     if index.isValid():
    #
    #         tableModelNode = self.model().getNode(index)
    #         src = self.model().mapToSource(index)
    #         node = self.model().sourceModel().getNode(src)
    #
    #     if node:
    #
    #
    #         actions.append(QtGui.QAction("Explore", menu, triggered=functools.partial(self.explore, src)))
    #         actions.append(QtGui.QAction("Delete", menu, triggered=functools.partial(self.delete, src)))
    #
    #
    #
    #     menu.addActions(actions)
    #
    #     # if handled:
    #
    #     menu.exec_(event.globalPos())
    #     # TELL QT IVE HANDLED THIS THING
    #
    #     # else:
    #     # event.ignore() #GIVE SOMEONE ELSE A CHANCE TO HANDLE IT
    #
    #     event.accept()
    #     return

class IconScaleSlider(QtGui.QWidget):
    def __init__(self, parent):
        super(IconScaleSlider, self).__init__(parent)


        self.large_lable = QtGui.QLabel()
        self.large_lable.setMaximumSize(QtCore.QSize(16, 16))
        self.large_lable.setPixmap(large_icon)
        self.small_lable = QtGui.QLabel()
        self.small_lable.setMaximumSize(QtCore.QSize(16, 16))
        self.small_lable.setPixmap(small_icon)
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
        #self.listSlider.valueChanged.connect(self.list.icons_size)

        self.slideLayout.addWidget(self.small_lable)
        self.slideLayout.addWidget(self.listSlider)
        self.slideLayout.addWidget(self.large_lable)

        self.setMinimumHeight(25)
        self.setLayout(self.slideLayout)


        #h_layout.addWidget(slideWidget)




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
        print "CLICK>>>"
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
                self.versionsView.setModel_(versionModel)
            else:
                try:
                    del versionModel
                except:
                    pass
                self.versionsView.setModel_(None)
                   
class pipelineTreeView(QtGui.QTreeView):

    update = QtCore.Signal()

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
                           }''')
    

        self.changed = False
        self.update.connect(self.model_changed)

    def model_changed(self):
        if not self.changed:
            self.changed = True


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
        return modelRootIndex
        # get the first childe of the model's root                                   
        #return self.sourceModel.index(0,0,modelRootIndex)
      
    
    def mouseReleaseEvent(self, event):
        
        super(pipelineTreeView, self).mouseReleaseEvent(event)
        self.saveSelection()
        #self.tableView.update(self.selectionModel().selection())
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

            elif node.typeInfo() == _stage_:
                actions.append(QtGui.QAction("Delete", menu, triggered = functools.partial(self.delete, src) ))

        else:
            actions.append(QtGui.QAction("Create new %s"%(_folder_), menu, triggered = functools.partial(self.create_new_folder, self.projectRootIndex()) ))
            actions.append(QtGui.QAction("Create new %s"%(_asset_), menu, triggered = functools.partial(self.create_new_asset, self.projectRootIndex()) ))

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
        #self.tableView.update(QtGui.QItemSelection())
        
        node = self.asModelNode(index)
        parentIndex = self.sourceModel.parent(index)
        self.sourceModel.removeRows(node.row(),1,parentIndex, kill=True)
        self._proxyModel.invalidate()

        self.updateTable( self.fromProxyIndex(parentIndex))
        self.update.emit()
        return True

    def create_new_folder(self, parent):
        parent_node = self.sourceModel.getNode(parent)

        folder_name, ok = QtGui.QInputDialog.getText(self, 'New Folder', 'Enter Folder name:')

        if ok:
            path = os.path.join(parent_node.path, folder_name)
            node = dt.FolderNode(folder_name, path=path, parent=parent_node, virtual = True)
            #if node is not False:
            self.sourceModel.insertRows(0, 0, parent=parent, node=node)
            self._proxyModel.invalidate()
            self.updateTable(self.fromProxyIndex(parent))
            self.update.emit()
        
    # def create_new_folder(self, parent):
    #     parent_node = self.sourceModel.getNode(parent)
    #
    #     folder_name, ok = QtGui.QInputDialog.getText(self, 'New Folder', 'Enter Folder name:')
    #
    #     if ok:
    #         path = os.path.join(parent_node.path, folder_name)
    #         node = dt.FolderNode(folder_name, parent = parent_node).create( path = path)
    #         if node is not False:
    #             self.sourceModel.insertRows( 0, 0, parent = parent , node = node)
    #             self._proxyModel.invalidate()
    #             self.updateTable( self.fromProxyIndex(parent))
    #             self.update.emit()
        
    def create_new_asset(self, parent):
        parent_node = self.sourceModel.getNode(parent)
        
        folder_name, ok = QtGui.QInputDialog.getText(self, 'New Asset', 'Enter Asset name:')
        
        if ok:
            path = os.path.join(parent_node.path, folder_name)
            node = dt.AssetNode(folder_name, parent = parent_node).create( path = path)
            if node is not False: 
                self._sourceModel.insertRows( 0, 0, parent = parent , node = node)
                self._proxyModel.invalidate()
                self.updateTable( self.fromProxyIndex(parent))
                self.update.emit()
        
    def create_new_stage(self, parent):
        parent_node = self.sourceModel.getNode(parent)
 
        stages = self.pipelineUI.project.stages["asset"] + self.pipelineUI.project.stages["animation"]
        stageDlg = dlg.newStage(stages = stages)
        result = stageDlg.exec_()
        stage_name  = stageDlg.result()
        if result == QtGui.QDialog.Accepted:

            path = os.path.join(parent_node.path, stage_name)
            node = dt.StageNode(stage_name, parent = parent_node).create( path = path)
            if node is not False:

                self._sourceModel.insertRows( 0, 0, parent = parent , node = node)
                self._proxyModel.invalidate()
                self.updateTable( self.fromProxyIndex(parent))
                self.update.emit()

    def updateTable(self, index):
        selection = QtGui.QItemSelection(index, index)        
        #self.tableView.update(selection)

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
            #self.tableView.clearModel()
            
            model = dtm.PipelineContentsModel(self.tree_as_flat_list)
            #self.tableView.populateTable(model)
            

    def commit(self):
        print "commit tree:"
        self.sourceModel.rootNode.commit()

class PipelineStagesView(QtGui.QListView):
    def __init__(self,parent = None):
        super(PipelineStagesView, self).__init__(parent)
        
        #display options
        
        self.setViewMode(QtGui.QListView.IconMode)
        self.setUniformItemSizes(True)
        self.setResizeMode(QtGui.QListView.Adjust)
        self.setFlow(QtGui.QListView.LeftToRight)
        self.setWrapping(True)
        self.setTextElideMode(QtCore.Qt.ElideRight)
        
        w = 48
        grid_w = w + 5
        grid_h = w + 30
        size = QtCore.QSize(w,w)
        size2 = QtCore.QSize(grid_w, grid_h)
        self.setIconSize(size)
        self.setGridSize(size2)
        
        #list = []
        #[list.append(dt.StageNode("<Stage>")) for i in range(6)]
        #self.setModel(dtm.PipelineListModel(list))
        
        #self.setSpacing(5)
        self.setWordWrap(True)
        '''
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
        self.verticalHeader().hide()'''
        
        #self.setSortingEnabled(True)

class ComboWidget(QtGui.QWidget):
    def __init__(self,
                 parent_layout = None,
                 parent = None):
        
        super(ComboWidget, self).__init__(parent)
        #self.parent = parent
        
        #self._parent = parent_box
        self._parent_layout = parent_layout  

        # UI
        self.setMaximumHeight(30)  
        self.layout = QtGui.QVBoxLayout(self)
        self.layout.setAlignment(QtCore.Qt.AlignLeft)
        self.comboBox = QtGui.QComboBox(self)
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

    def createModel(self):
        
        list = [dt.CatagoryNode("stage")]
        
        [list.append(dt.DummyNode(i)) for i in self._items]
        
        RemoveOption = False
        
        if list:
            RemoveOption = True
        
        list.append(dt.AddNode("Add..."))
        
        if RemoveOption:
            list.append(dt.AddNode("Remove..."))
        
        self._model = dtm.PipelineListModel(list) 
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
        
        
        # Init calls
        self.createModel()              
                    
        # connections                
        self.comboBox.currentIndexChanged.connect(self.update)

    def listDirectory(self):
        dir = self._path
        dirs = files.list_dir_folders(dir)   

              
        if dirs:
            
            self._subdirectories = dirs
            
            relative_path = os.path.relpath(dir, self.parent.project.path)
            depth = relative_path.count(os.sep)
            
            if self._stage in self._project.stages["asset"]:
                options = self._project.levels["asset"]

                if len(options) >  depth:
                    self._level = options[depth]
                
                    return
                
            if self._stage in self._project.stages["animation"]:
                options = self._project.levels["animation"]
                if len(options) > depth:
                    self._level = options[depth]
                
                    return
          
        self._level = "n/a"
                

    def createModel(self):
        
        list = [dt.CatagoryNode(self._level)]

        if self._level != "n/a":
            if self._subdirectories:
                for i in range(len(self._subdirectories)):
                    n = os.path.split(self._subdirectories[i])[1]
                    list.append(dt.FolderNode(n))
        
        RemoveOption = False
        
        if list:
            RemoveOption = True
        
        list.append(dt.AddNode("Add..."))
        
        if RemoveOption:
            list.append(dt.AddNode("Remove..."))
        
        self._model = dtm.PipelineListModel(list) 
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
                                      settings=self._settings, pipelineUI=self.parent)

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
                                     settings=self._settings, pipelineUI= self.parent)

                        self.parent.stageNode(stage)
                        self.parent.updateVersionsTable()
                        return True

                    #self.parent.stageNode(None)
                    #self.parent.updateVersionsTable()
                    #return True

            self.parent.stageNode(None)
            self.parent.updateVersionsTable()
            return True


        if self._parent_box:
            self._node = dt.FolderNode(os.path.split(path)[1], parent=self._parent_box._node, path=path, project=self._project,
                                   settings=self._settings, pipelineUI=self.parent)
        else:
            self._node = dt.FolderNode(os.path.split(path)[1], parent=None, path=path, project=self._project,
                                       settings=self._settings, pipelineUI=self.parent)

        self.parent.stageNode(None)
        self.parent.updateVersionsTable()
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
        

    
    
            