#!/usr/bin/env python
"""
Maya mixin classes to add common functionality for custom PyQt/PySide widgets in Maya.

* MayaQWidgetBaseMixin      Mixin that should be applied to all custom QWidgets created for Maya
                            to automatically handle setting the objectName and parenting

* MayaQWidgetDockableMixin  Mixin that adds dockable capabilities within Maya controlled with
                            the show() function
"""


import uuid

from maya import cmds
from maya import mel
from maya import OpenMayaUI as omui

# Import available PySide or PyQt package, as it will work with both
try:
    from PySide2.QtCore import Qt, QPoint, QSize
    from PySide2.QtCore import Signal
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    from shiboken2 import wrapInstance
    _qtImported = 'PySide2'
except ImportError, e1:
    try:
        from PyQt4.QtCore import Qt, QPoint, QSize
        from PyQt4.QtCore import pyqtSignal as Signal
        from PyQt4.QtGui import *
        from sip import wrapinstance as wrapInstance
        _qtImported = 'PyQt4'
    except ImportError, e2:
        raise ImportError, '%s, %s'%(e1,e2)


class MayaQWidgetBaseMixin(object):
    '''
    Handle common actions for Maya Qt widgets during initialization:
        * auto-naming a Widget so it can be looked up as a string through
          maya.OpenMayaUI.MQtUtil.findControl()
        * parenting the widget under the main maya window if no parent is explicitly
          specified so not to have the Window disappear when the instance variable
          goes out of scope

    Integration Notes:
        Inheritance ordering: This class must be placed *BEFORE* the Qt class for proper execution
        This is needed to workaround a bug where PyQt/PySide does not call super() in its own __init__ functions

    Example:
        class MyQWidget(MayaQWidgetBaseMixin, QPushButton):
            def __init__(self, parent=None):
                super(MyQWidget, self).__init__(parent=parent)
                self.setText('Push Me')
        myWidget = MyQWidget()
        myWidget.show()
        print myWidget.objectName()
    '''
    def __init__(self, parent=None, *args, **kwargs):
        super(MayaQWidgetBaseMixin, self).__init__(parent=parent, *args, **kwargs) # Init all baseclasses (including QWidget) of the main class
        self._initForMaya(parent=parent)


    def _initForMaya(self, parent=None, *args, **kwargs):
        '''
        Handle the auto-parenting and auto-naming.

        :Parameters:
            parent (string)
                Explicitly specify the QWidget parent.  If 'None', then automatically
                parent under the main Maya window
        '''

        # If the input parent happens to be a Native window (such as the main Maya
        # window) then when we are parented to it, we also become a Native window.
        # Being a Native window is okay, but we don't want our ancestors to be
        # switched to Native, such as when we are docked inside a tabWidget.
        self.setAttribute(Qt.WA_DontCreateNativeAncestors)

        # Set parent to Maya main window if parent=None
        if parent is None:
            self._makeMayaStandaloneWindow()

        # Set a unique object name string so Maya can easily look it up
        if self.objectName() == '':
            self.setObjectName('%s_%s'%(self.__class__.__name__, uuid.uuid4()))


    def _makeMayaStandaloneWindow(self):
        '''Make a standalone window, though parented under Maya's mainWindow.
        The parenting under Maya's mainWindow is done so that the QWidget will not
        auto-destroy itself when the instance variable goes out of scope.
        '''
        origParent = self.parent()

        # Parent under the main Maya window
        mainWindowPtr = omui.MQtUtil.mainWindow()
        mainWindow = wrapInstance(long(mainWindowPtr), QMainWindow)
        self.setParent(mainWindow)

        # Make this widget appear as a standalone window even though it is parented
        if isinstance(self, QDockWidget):
            self.setWindowFlags(Qt.Dialog|Qt.FramelessWindowHint)
        else:
            self.setWindowFlags(Qt.Window)

        # Delete the parent workspace control if applicable
        if origParent:
            parentName = origParent.objectName()
            if parentName and len(parentName) and cmds.workspaceControl(parentName, q=True, exists=True):
                cmds.deleteUI(parentName, control=True)


class MayaQDockWidget(MayaQWidgetBaseMixin,QDockWidget):
    '''QDockWidget tailored for use with Maya.
    Mimics the behavior performed by Maya's internal QMayaDockWidget class and the dockControl command

    :Signals:
        closeEventTriggered: emitted when a closeEvent occurs

    :Known Issues:
        * Manually dragging the DockWidget to dock in the Main MayaWindow will have it resize to the 'sizeHint' size
          of the child widget() instead of preserving its existing size.
    '''
    # Custom Signals
    closeEventTriggered = Signal()   # Qt Signal triggered when closeEvent occurs
    windowStateChanged = Signal()  # Qt Signal triggered when the window is moved or resized.

    def __init__(self, parent=None, *args, **kwargs):
        super(MayaQDockWidget, self).__init__(parent=parent, *args, **kwargs) # Init all baseclasses (including QWidget) of the main class

        # == Mimic operations performed by Maya internal QmayaDockWidget ==
        self.setAttribute(Qt.WA_MacAlwaysShowToolWindow)

        # WORKAROUND: The mainWindow.handleDockWidgetVisChange may not be present on some PyQt and PySide systems.
        #             Handle case if it fails to connect to the attr.
        mainWindowPtr = omui.MQtUtil.mainWindow()
        mainWindow = wrapInstance(long(mainWindowPtr), QMainWindow)
        try:
            self.visibilityChanged.connect(mainWindow.handleDockWidgetVisChange)
        except AttributeError, e:
            # Error connecting visibilityChanged trigger to mainWindow.handleDockWidgetVisChange.
            # Falling back to using MEL command directly.
            mel.eval('evalDeferred("updateEditorToggleCheckboxes()")')  # Currently mainWindow.handleDockWidgetVisChange only makes this updateEditorToggleCheckboxes call


    def setArea(self, area):
        '''Set the docking area
        '''
        # Skip setting the area if no area value passed in
        if area == Qt.NoDockWidgetArea:
            return

        # Mimic operations performed by Maya dockControl command
        mainWindow = self.parent()  if isinstance(self.parent(), QMainWindow) else wrapInstance(long(omui.MQtUtil.mainWindow()), QMainWindow)

        childrenList = mainWindow.children()
        foundDockWidgetToTab = False
        for child in childrenList:
            # Create Tabbed dock if a QDockWidget already at that area
            if (child != self) and (isinstance(child, QDockWidget)):
                if  not child.isHidden() and  not child.isFloating():
                    if mainWindow.dockWidgetArea(child) == area:
                        mainWindow.tabifyDockWidget(child, self)
                        self.raise_()
                        foundDockWidgetToTab = True
                        break
        # If no other QDockWidget at that area, then just add it
        if not foundDockWidgetToTab:
            mainWindow.addDockWidget(area, self)

    def resizeEvent(self, event):
        super(MayaQDockWidget, self).resizeEvent(event)
        if event.isAccepted():
            self.windowStateChanged.emit()

    def moveEvent(self, event):
        super(MayaQDockWidget, self).moveEvent(event)
        if event.isAccepted():
            self.windowStateChanged.emit()

    def closeEvent(self, evt):
        '''Hide the QDockWidget and trigger the closeEventTriggered signal
        '''
        # Handle the standard closeEvent()
        super(MayaQDockWidget, self).closeEvent(evt)

        if evt.isAccepted():
            # Force visibility to False
            self.setVisible(False) # since this does not seem to have happened already

            # Emit that a close event is occurring
            self.closeEventTriggered.emit()


class MayaQWidgetDockableMixin(MayaQWidgetBaseMixin):
    '''
    Handle Maya dockable actions controlled with the show() function.

    Integration Notes:
        Inheritance ordering: This class must be placed *BEFORE* the Qt class for proper execution
        This is needed to workaround a bug where PyQt/PySide does not call super() in its own __init__ functions

    Example:
        class MyQWidget(MayaQWidgetDockableMixin, QPushButton):
            def __init__(self, parent=None):
                super(MyQWidget, self).__init__(parent=parent)
                self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred )
                self.setText('Push Me')
        myWidget = MyQWidget()
        myWidget.show(dockable=True)
        myWidget.show(dockable=False)
        print myWidget.showRepr()
    '''

    # Custom Signals
    closeEventTriggered = Signal()   # Qt Signal triggered when closeEvent occurs
    windowStateChanged = Signal()  # Qt Signal triggered when the window is moved or resized.

    def setDockableParameters(self, dockable=None, floating=None, area=None, allowedArea=None, width=None, height=None, x=None, y=None, retain=True, plugins=None, controls=None, uiScript=None, closeCallback=None, *args, **kwargs):
        '''
        Set the dockable parameters.

        :Parameters:
            dockable (bool)
                Specify if the window is dockable (default=False)
            floating (bool)
                Should the window be floating or docked (default=True)
            area (string)
                Default area to dock into (default='left')
                Options: 'top', 'left', 'right', 'bottom'
            allowedArea (string)
                Allowed dock areas (default='all')
                Options: 'top', 'left', 'right', 'bottom', 'all'
            width (int)
                Width of the window
            height (int)
                Height of the window
            x (int)
                left edge of the window
            y (int)
                top edge of the window

        :See: show(), hide(), and setVisible()
        '''
        if ((dockable == True) or (dockable == None and self.isDockable())): # == Handle docked window ==
            # By default, when making dockable, make it floating
            #   This addresses an issue on Windows with the window decorators not showing up.
            if floating == None and area == None:
                floating = True

            # Create workspaceControl if needed
            if dockable == True and not self.isDockable():
                # Retrieve original position and size
                # Position
                if x == None:
                    x = self.x()
                    # Give suitable default value if null
                    if x == 0:
                        x = 250
                if y == None:
                    y = self.y()
                    # Give suitable default value if null
                    if y == 0:
                        y = 200
                # Size
                unininitializedSize = QSize(640,480)  # Hardcode: (640,480) is the default size for a QWidget
                if self.size() == unininitializedSize:
                    # Get size from widget sizeHint if size not yet initialized (before the first show())
                    widgetSizeHint = self.sizeHint()
                else:
                    widgetSizeHint = self.size() # use the current size of the widget
                if width == None:
                    width = widgetSizeHint.width()
                if height == None:
                    height = widgetSizeHint.height()

                if controls is None:
                    controls = []
                if plugins is None:
                    plugins = []

                workspaceControlName = self.objectName() + 'WorkspaceControl'
                # Set to floating if requested or if no docking area given
                if floating == True or area == None:
                    workspaceControlName = cmds.workspaceControl(workspaceControlName, label=self.windowTitle(), retain=retain, loadImmediately=True, floating=True, initialWidth=width, initialHeight=height, requiredPlugin=plugins, requiredControl=controls)
                else:
                    if self.parent() is None or self.parent().objectName() == "MayaWindow":#omui.MQtUtil.mainWindow():
                        # If parented to the Maya main window or nothing, dock into the Maya main window
                        workspaceControlName = cmds.workspaceControl(workspaceControlName, label=self.windowTitle(), retain=retain, loadImmediately=True, dockToMainWindow=(area, True), initialWidth=width, initialHeight=height, requiredPlugin=plugins, requiredControl=controls)
                    else:
                        # Otherwise, the parent should be within a workspace control - need to go up the hierarchy to find it
                        foundParentWorkspaceControl = False
                        parent = self.parent()
                        while parent is not None:
                            dockToWorkspaceControlName = parent.objectName()
                            if cmds.workspaceControl(dockToWorkspaceControlName, q=True, exists=True):
                                workspaceControlName = cmds.workspaceControl(workspaceControlName, label=self.windowTitle(), retain=retain, loadImmediately=True, dockToControl=(dockToWorkspaceControlName, area), initialWidth=width, initialHeight=height, requiredPlugin=plugins, requiredControl=controls)
                                foundParentWorkspaceControl = True
                                break
                            else:
                                parent = parent.parent()

                        if foundParentWorkspaceControl == False:
                            # If parent workspace control cannot be found, just make the workspace control a floating window
                            workspaceControlName = cmds.workspaceControl(workspaceControlName, label=self.windowTitle(), retain=retain, loadImmediately=True, floating=True, initialWidth=width, initialHeight=height, requiredPlugin=plugins, requiredControl=controls)

                parent = omui.MQtUtil.getCurrentParent()
                mixinPtr = omui.MQtUtil.findControl(self.objectName())
                omui.MQtUtil.addWidgetToMayaLayout(long(mixinPtr), long(parent))

                if uiScript is not None and len(uiScript):
                    cmds.workspaceControl(workspaceControlName, e=True, uiScript=uiScript)

                if closeCallback is not None:
                    cmds.workspaceControl(workspaceControlName, e=True, closeCommand=closeCallback)

                # Hook up signals
                #dockWidget.topLevelChanged.connect(self.floatingChanged)
                #dockWidget.closeEventTriggered.connect(self.dockCloseEventTriggered)

        else:  # == Handle Standalone Window ==
            # Make standalone as needed
            if not dockable and self.isDockable():
                # Retrieve original position and size
                dockPos = self.parent().pos()
                if x == None:
                    x = dockPos.x()
                if y == None:
                    y = dockPos.y()
                if width == None:
                    width = self.width()
                if height == None:
                    height = self.height()
                # Turn into a standalone window and reposition
                currentVisibility = self.isVisible()
                self._makeMayaStandaloneWindow() # Set the parent back to Maya and remove the parent dock widget
                self.setVisible(currentVisibility)

            # Handle position and sizing
            if (width != None) or (height != None):
                if width == None:
                    width = self.width()
                if height == None:
                    height = self.height()
                self.resize(width, height)
            if (x != None) or (y != None):
                if x == None:
                    x = self.x()
                if y == None:
                    y = self.y()
                self.move(x,y)

    def setSizeHint(self, size):
        '''
        Virtual method used to pass the user settable width and height down to the widget whose
        size policy controls the actual size most of the time.
        '''
        pass

    def show(self, *args, **kwargs):
        '''
        Show the QWidget window.  Overrides standard QWidget.show()

        :See: setDockableParameters() for a list of parameters
        '''
        # Update the dockable parameters first (if supplied)
        if len(args) or len(kwargs):
            self.setDockableParameters(*args, **kwargs)

        # Handle the standard setVisible() operation of show()
        QWidget.setVisible(self, True) # NOTE: Explicitly calling QWidget.setVisible() as using super() breaks in PySide: super(self.__class__, self).show()

        # Handle special case if the parent is a QDockWidget (dockControl)
        parent = self.parent()
        if parent:
            parentName = parent.objectName()
            if parentName and len(parentName) and cmds.workspaceControl(parentName, q=True, exists=True):
                if cmds.workspaceControl(parentName, q=True, visible=True):
                    cmds.workspaceControl(parentName, e=True, r=True)
                else:
                    cmds.workspaceControl(parentName, e=True, visible=True)


    def hide(self, *args, **kwargs):
        '''Hides the widget.  Will hide the parent widget if it is a QDockWidget.
        Overrides standard QWidget.hide()
        '''
        # Handle special case if the parent is a QDockWidget (dockControl)
        parent = self.parent()
        if parent:
            parentName = parent.objectName()
            if parentName and len(parentName) and cmds.workspaceControl(parentName, q=True, exists=True):
                cmds.workspaceControl(parentName, e=True, visible=False)
            else:
                QWidget.setVisible(self, False) # NOTE: Explicitly calling QWidget.setVisible() as using super() breaks in PySide: super(self.__class__, self).show()

    def close(self):
        '''Closes the widget. Overrides standard QWidget.close()
        '''
        parent = self.parent()
        if parent:
            parentName = parent.objectName()
            if parentName and len(parentName) and cmds.workspaceControl(parentName, q=True, exists=True):
                cmds.workspaceControl(parentName, e=True, close=True)
            else:
                QWidget.close(self)

    def isVisible(self):
        '''Return if the widget is currently visible. Overrides standard QWidget.isVisible()

        :Return: bool
        '''
        parent = self.parent()
        if parent:
            parentName = parent.objectName()
            if parentName and len(parentName) and cmds.workspaceControl(parentName, q=True, exists=True):
                return cmds.workspaceControl(parentName, q=True, visible=True)
        return QWidget.isVisible(self)

    def setVisible(self, makeVisible, *args, **kwargs):
        '''
        Show/hide the QWidget window.  Overrides standard QWidget.setVisible() to pass along additional arguments

        :See: show() and hide()
        '''
        if (makeVisible == True):
            return self.show(*args, **kwargs)
        else:
            return self.hide(*args, **kwargs)


    def raise_(self):
        '''Raises the widget to the top.  Will raise the parent widget if it is a QDockWidget.
        Overrides standard QWidget.raise_()
        '''
        # Handle special case if the parent is a QDockWidget (dockControl)
        parent = self.parent()
        if parent:
            parentName = parent.objectName()
            if parentName and len(parentName) and cmds.workspaceControl(parentName, q=True, exists=True):
                # Raise the workspace control
                cmds.workspaceControl(parentName, e=True, r=True)
            else:
                QWidget.raise_(self)  # NOTE: Explicitly using QWidget as using super() breaks in PySide: super(self.__class__, self).show()


    def isDockable(self):
        '''Return if the widget is currently dockable (under a QDockWidget)

        :Return: bool
        '''
        parent = self.parent()
        if parent:
            parentName = parent.objectName()
            if parentName and len(parentName):
                return cmds.workspaceControl(parentName, q=True, exists=True)
            else:
                return False
        return False


    def isFloating(self):
        '''Return if the widget is currently floating (under a QDockWidget)
        Will return True if is a standalone window OR is a floating dockable window.

        :Return: bool
        '''
        parent = self.parent()
        if parent:
            parentName = parent.objectName()
            if parentName and len(parentName) and cmds.workspaceControl(parentName, q=True, exists=True):
                return cmds.workspaceControl(parentName, q=True, floating=True)
            else:
                return True
        return True


    def floatingChanged(self, isFloating):
        '''Triggered when QDockWidget.topLevelChanged() signal is triggered.
        Stub function.  Override to perform actions when this happens.
        '''
        pass


    def dockCloseEventTriggered(self):
        '''Triggered when QDockWidget.closeEventTriggered() signal is triggered.
        Stub function.  Override to perform actions when this happens.
        '''
        pass


    def dockArea(self):
        '''Return area if the widget is currently docked to the Maya MainWindow
        Will return None if not dockable

        :Return: str
        '''
        dockControlQt = self.parent()

        if not isinstance(dockControlQt, QDockWidget):
            return None
        else:
            mainWindow = self.parent().parent() if isinstance(self.parent().parent(), QMainWindow) \
                else wrapInstance(long(omui.MQtUtil.mainWindow()), QMainWindow)

            dockAreaMap = {
                Qt.LeftDockWidgetArea   : 'left',
                Qt.RightDockWidgetArea  : 'right',
                Qt.TopDockWidgetArea    : 'top',
                Qt.BottomDockWidgetArea : 'bottom',
                Qt.AllDockWidgetAreas   : 'all',
                Qt.NoDockWidgetArea     : 'none',   # Note: 'none' not supported in maya dockControl command
            }
            dockWidgetAreaBitmap = mainWindow.dockWidgetArea(dockControlQt)
            return dockAreaMap[dockWidgetAreaBitmap]


    def setWindowTitle(self, val):
        '''Sets the QWidget's title and also it's parent QDockWidget's title if dockable.

        :Return: None
        '''
        # Handle the standard setVisible() operation of show()
        QWidget.setWindowTitle(self, val) # NOTE: Explicitly calling QWidget.setWindowTitle() as using super() breaks in PySide: super(self.__class__, self).show()

        # Handle special case if the parent is a QDockWidget (dockControl)
        parent = self.parent()
        if parent:
            parentName = parent.objectName()
            if parentName and len(parentName) and cmds.workspaceControl(parentName, q=True, exists=True):
                cmds.workspaceControl(parentName, e=True, label=val)

    def showRepr(self):
        '''Present a string of the parameters used to reproduce the current state of the
        widget used in the show() command.

        :Return: str
        '''
        reprDict = {}
        reprDict['dockable'] = self.isDockable()
        reprDict['floating'] = self.isFloating()
        reprDict['area']     = self.dockArea()
        #reprDict['allowedArea'] = ??
        if reprDict['floating']:
            if reprDict['dockable']:
                pos = self.parent().pos()
            else:
                pos = self.pos()
            reprDict['x'] = pos.x()
            reprDict['y'] = pos.y()

        sz  = self.geometry().size()
        reprDict['width'] = sz.width()
        reprDict['height'] = sz.height()

        # Construct the repr show() string
        reprShowList = ['%s=%r'%(k,v) for k,v in reprDict.items() if v != None]
        reprShowStr = 'show(%s)'%(', '.join(reprShowList))
        return reprShowStr# ===========================================================================
# Copyright 2016 Autodesk, Inc. All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
# ===========================================================================
