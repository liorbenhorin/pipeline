'''

PIPELINE 

BETA 1.0.0

Project manager for Maya

Ahutor: Lior Ben Horin
All rights reserved (c) 2016 
    
liorbenhorin.ghost.io
liorbenhorin@gmail.com

---------------------------------------------------------------------------------------------

install:

Place the pipeline folder in your maya scripts folder. Run these lines in a python tab in the script editor:
 
from pipeline import pipeline
reload(pipeline)
pipeline.show()

---------------------------------------------------------------------------------------------

You are using PIPELINE on you own risk. 
Things can allways go wrong, and under no circumstances the author
would be responsible for any damages cuesed from the use of this software.
When using this beta program you hearby agree to allow this program to collect 
and send usage data to the author.

---------------------------------------------------------------------------------------------  

The coded instructions, statements, computer programs, and/or related
material (collectively the "Data") in these files are subject to the terms 
and conditions defined by
Creative Commons Attribution-NonCommercial-NoDerivs 4.0 Unported License:
   http://creativecommons.org/licenses/by-nc-nd/4.0/
   http://creativecommons.org/licenses/by-nc-nd/4.0/legalcode
   http://creativecommons.org/licenses/by-nc-nd/4.0/legalcode.txt

---------------------------------------------------------------------------------------------  

'''


from PySide import QtCore, QtGui
import os

def set_icons():
    localIconPath = os.path.join(os.path.dirname(__file__), 'icons')
    if not os.path.exists(localIconPath):
        return 
    
    global warning_icon
    global simple_warning_icon
    global massage_icon
    global users_icon
    warning_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"critical")) 
    simple_warning_icon =  QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"warning"))
    massage_icon =  QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"massage"))
    users_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"users"))
    
def warning(icon, title, message ):
    
    if icon == "critical":
        dlg_icon = warning_icon
    elif icon == "warning":
        dlg_icon = simple_warning_icon
    else:
        dlg_icon = warning_icon            
    
    reply = QtGui.QMessageBox()
    reply.setIconPixmap(dlg_icon)

    reply.setText(message)
    #reply.setInformativeText("This is additional information")
    reply.setWindowTitle(title)
    #reply.setDetailedText("The details are as follows:")
    reply.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
    
    result = reply.exec_()
    if result == QtGui.QMessageBox.Yes:
        return True
    else:
        return False      
        
def massage(icon, title, message ):
    
    reply = QtGui.QMessageBox()
    
    if icon == "critical":
        reply.setIconPixmap(warning_icon)

    elif icon == "warning":
        reply.setIconPixmap(simple_warning_icon)

    elif icon == "massage":
        reply.setIconPixmap(massage_icon)
   
    reply.setText(message)
    reply.setWindowTitle(title)
    reply.setStandardButtons(QtGui.QMessageBox.Close)
    
    result = reply.exec_()
 
        
set_icons()



class Create_from_selection(QtGui.QDialog):
    def __init__(self, parent = None, title = None):
        super(Create_from_selection, self).__init__(parent)
        
        
        
        self.setMaximumWidth(200) 
        self.setMinimumWidth(200)        
        self.setMaximumHeight(50) 

        layout = QtGui.QVBoxLayout(self)
        self.item_name = QtGui.QLabel(title)
        self.text_input = QtGui.QLineEdit()
        self.include_radio = QtGui.QRadioButton("Include all connections")
        self.include_radio.setChecked(True)
        self.exclude_radio = QtGui.QRadioButton("Include only textures")
        
        
        layout.addWidget(self.item_name)
        layout.addWidget(self.text_input)
        layout.addWidget(self.include_radio)
        layout.addWidget(self.exclude_radio)
        
        buttons = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def radio_selection(self):
        if self.include_radio.isChecked():
            return "include"
        else:
            return "exclude"

    def result(self):
        return self.text_input.text(), self.radio_selection()
        
        
    
class Login(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)

        self.setMaximumWidth(200) 
        self.setMinimumWidth(200)        
        self.setMaximumHeight(50) 
        
        self.label = QtGui.QLabel()
        self.label.setPixmap(users_icon)
        
        self.label_user = QtGui.QLabel("Username:")
        self.label_password = QtGui.QLabel("Password:")
        
        self.textName = QtGui.QLineEdit(self)
        self.textName.setMinimumSize(QtCore.QSize(0, 30))
        self.textPass = QtGui.QLineEdit(self)
        self.textPass.setMinimumSize(QtCore.QSize(0, 30))

        self.textPass.setInputMethodHints(QtCore.Qt.ImhHiddenText|QtCore.Qt.ImhNoAutoUppercase|QtCore.Qt.ImhNoPredictiveText)
        self.textPass.setEchoMode(QtGui.QLineEdit.Password)
    
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.HLine())
        layout.addWidget(self.label_user)
        layout.addWidget(self.textName)
        layout.addWidget(self.label_password)
        layout.addWidget(self.textPass)
        
        log = QtGui.QPushButton("Login")
        log.setDefault(True)
        
        canc = QtGui.QPushButton("Cancel")
        
       
        buttons = QtGui.QDialogButtonBox(QtCore.Qt.Horizontal)
        buttons.addButton(log, QtGui.QDialogButtonBox.AcceptRole)
        buttons.addButton(canc, QtGui.QDialogButtonBox.RejectRole)

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        

    def result(self):
        return self.textName.text(), self.textPass.text()


    def HLine(self):
        toto = QtGui.QFrame()
        toto.setFrameShape(QtGui.QFrame.HLine)
        toto.setFrameShadow(QtGui.QFrame.Sunken)
        return toto    