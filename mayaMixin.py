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
    from PySide.QtCore import Qt, QPoint, QSize
    from PySide.QtCore import Signal
    from PySide.QtGui import *
    from shiboken import wrapInstance
    _qtImported = 'PySide'
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
        # Set parent to Maya main window if parent=None
        if parent == None:
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
        
        # Delete the parent QDockWidget if applicable
        if isinstance(origParent, QDockWidget):
            origParent.close()
            
            
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
        mainWindowPtr = omui.MQtUtil.mainWindow()
        mainWindow = wrapInstance(long(mainWindowPtr), QMainWindow)
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
    
    
    def resizeEvent(self, evt):
        '''Store off the 'savedSize' property used by Maya's QMainWindow to set the
        size of the widget when it is being docked.
        '''
        self.setProperty('savedSize', self.size()) 
        return super(MayaQDockWidget, self).resizeEvent(evt)


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
    def setDockableParameters(self, dockable=None, floating=None, area=None, allowedArea=None, width=None, height=None, x=None, y=None, *args, **kwargs):
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
        if (dockable == True) or (dockable == None and self.isDockable()): # == Handle docked window ==
            # Conversion parameters (used below)
            dockAreaStrMap = {
                'left'   : Qt.LeftDockWidgetArea,
                'right'  : Qt.RightDockWidgetArea,
                'top'    : Qt.TopDockWidgetArea,    
                'bottom' : Qt.BottomDockWidgetArea,
                'all'    : Qt.AllDockWidgetAreas,  
                'none'   : Qt.NoDockWidgetArea,   # Note: Not currently supported in maya dockControl command
            }

            # Create dockControl (QDockWidget) if needed
            if dockable == True and not self.isDockable():
                # Retrieve original position and size
                # Position
                if x == None:
                    x = self.x()
                if y == None:
                    y = self.y()
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
                
                # Create the QDockWidget
                dockWidget = MayaQDockWidget()
                dockWidget.setWindowTitle(self.windowTitle())
                dockWidget.setWidget(self)

                # By default, when making dockable, make it floating
                #   This addresses an issue on Windows with the window decorators
                #   not showing up.  Setting this here will cause setFloating() to be called below.
                if floating == None:
                    floating = True

                # Hook up signals
                dockWidget.topLevelChanged.connect(self.floatingChanged)
                dockWidget.closeEventTriggered.connect(self.dockCloseEventTriggered)
            else:
                if floating == True:
                    # Retrieve original position (if floating)
                    pos = self.parent().mapToGlobal( QPoint(0,0) )
                    if x == None:
                        x = pos.x()
                    if y == None:
                        y = pos.y()

                # Retrieve original size
                if width == None:
                    width = self.width()
                if height == None:
                    height = self.height()

            # Get dock widget identifier
            dockWidget = self.parent()
            
            # Update dock values
            if area        != None:
                areaValue = dockAreaStrMap.get(area, Qt.LeftDockWidgetArea)
                dockWidget.setArea(areaValue)
            if allowedArea != None:
                areaValue = dockAreaStrMap.get(allowedArea, Qt.AllDockWidgetAreas)
                dockWidget.setAllowedArea(areaValue)
            if floating    != None:
                dockWidget.setFloating(floating)
                
            # Position window
            if dockWidget.isFloating() and ((x != None) or (y != None)):
                dockPos = dockWidget.mapToGlobal( QPoint(0,0) )
                if x == None:
                    x = dockPos.x()
                if y == None:
                    y = dockPos.y()
                dockWidget.move(x,y)
            if (width != None) or (height != None):
                if width == None:
                    width = self.width()
                if height == None:
                    height = self.height()
                # Perform first resize on dock, determine delta with widget, and resize with that adjustment
                # Result: Keeps the content widget at the same size whether under the QDockWidget or a standalone window
                dockWidget.resize(width, height) # Size once to know the difference in the dockWidget to the targetSize
                dockWidgetSize = dockWidget.size() + QSize(width,height)-self.size() # find the delta and add it to the current dock size
                # Perform the final resize (call MayaQDockWidget.resize() which also sets the 'savedSize' property used for sizing when docking to the Maya MainWindow)
                dockWidget.resize(dockWidgetSize)
                
        else:  # == Handle Standalone Window ==
            # Make standalone as needed
            if dockable == False and self.isDockable():
                # Retrieve original position and size
                dockPos = self.parent().mapToGlobal( QPoint(0,0) )
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
        if isinstance(parent, QDockWidget):
            parent.show()


    def hide(self, *args, **kwargs):
        '''Hides the widget.  Will hide the parent widget if it is a QDockWidget.
        Overrides standard QWidget.hide()
        '''
        # Update the dockable parameters first (if supplied)
        if len(args) or len(kwargs):
            self.setDockableParameters(*args, **kwargs)
        
        # Handle special case if the parent is a QDockWidget (dockControl)
        parent = self.parent()
        if isinstance(parent, QDockWidget):
            parent.hide()

        QWidget.setVisible(self, False) # NOTE: Explicitly calling QWidget.setVisible() as using super() breaks in PySide: super(self.__class__, self).show()


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
        if isinstance(parent, QDockWidget):
            parent.raise_()
        else:
            QWidget.raise_(self)  # NOTE: Explicitly using QWidget as using super() breaks in PySide: super(self.__class__, self).show()


    def isDockable(self):
        '''Return if the widget is currently dockable (under a QDockWidget)
        
        :Return: bool
        '''
        parent = self.parent()
        return isinstance(parent, QDockWidget)


    def isFloating(self):
        '''Return if the widget is currently floating (under a QDockWidget)
        Will return True if is a standalone window OR is a floating dockable window.
        
        :Return: bool
        '''
        parent = self.parent()
        if not isinstance(parent, QDockWidget):
            return True
        else:
            return parent.isFloating()


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
            mainWindowPtr = omui.MQtUtil.mainWindow()
            mainWindow = wrapInstance(long(mainWindowPtr), QMainWindow)
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
        if isinstance(parent, QDockWidget):
            parent.setWindowTitle(val)


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
        if reprDict['dockable'] == True:
            dockCtrl = self.parent()
            pos = dockCtrl.mapToGlobal( QPoint(0,0) )
        else:
            pos = self.pos()
        sz  = self.geometry().size()
        reprDict['x'] = pos.x()
        reprDict['y'] = pos.y()
        reprDict['width'] = sz.width()
        reprDict['height'] = sz.height()
        
        # Construct the repr show() string
        reprShowList = ['%s=%r'%(k,v) for k,v in reprDict.items() if v != None]
        reprShowStr = 'show(%s)'%(', '.join(reprShowList))
        return reprShowStr
# Copyright (C) 1997-2014 Autodesk, Inc., and/or its licensors.
# All rights reserved.
#
# The coded instructions, statements, computer programs, and/or related
# material (collectively the "Data") in these files contain unpublished
# information proprietary to Autodesk, Inc. ("Autodesk") and/or its licensors,
# which is protected by U.S. and Canadian federal copyright law and by
# international treaties.
#
# The Data is provided for use exclusively by You. You have the right to use,
# modify, and incorporate this Data into other products for purposes authorized 
# by the Autodesk software license agreement, without fee.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND. AUTODESK
# DOES NOT MAKE AND HEREBY DISCLAIMS ANY EXPRESS OR IMPLIED WARRANTIES
# INCLUDING, BUT NOT LIMITED TO, THE WARRANTIES OF NON-INFRINGEMENT,
# MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE, OR ARISING FROM A COURSE 
# OF DEALING, USAGE, OR TRADE PRACTICE. IN NO EVENT WILL AUTODESK AND/OR ITS
# LICENSORS BE LIABLE FOR ANY LOST REVENUES, DATA, OR PROFITS, OR SPECIAL,
# DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES, EVEN IF AUTODESK AND/OR ITS
# LICENSORS HAS BEEN ADVISED OF THE POSSIBILITY OR PROBABILITY OF SUCH DAMAGES.

