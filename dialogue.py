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
import base64
# from PySide import QtCore, QtGui
from PySide2 import QtGui, QtWidgets, QtCore

# from PySide2.QtGui import *
# from PySide2.QtWidgets import *
import os
import ast

import modules.data as data
reload(data)


def set_icons():
    localIconPath = os.path.join(os.path.dirname(__file__), 'icons')
    if not os.path.exists(localIconPath):
        return 
    
    global warning_icon
    global simple_warning_icon
    global massage_icon
    global users_icon
    global archive_icon
    global new_icon
    global edit_icon
    global logo
    global comment_icon
    
    warning_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"critical"))
    simple_warning_icon =  QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"warning"))
    massage_icon =  QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"massage"))
    users_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"users"))
    archive_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"archive"))
    new_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"new"))
    logo = QtGui.QPixmap(os.path.join(localIconPath, "%s.png"%"pipeline_logo"))
    edit_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"edit"))
    comment_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg"%"comment"))
        
def warning(icon, title, message ):
    
    if icon == "critical":
        dlg_icon = warning_icon
    elif icon == "warning":
        dlg_icon = simple_warning_icon
    else:
        dlg_icon = warning_icon            
    
    reply = QtWidgets.QMessageBox()
    reply.setIconPixmap(dlg_icon)

    reply.setText(message)
    #reply.setInformativeText("This is additional information")
    reply.setWindowTitle(title)
    #reply.setDetailedText("The details are as follows:")
    reply.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
    
    result = reply.exec_()
    if result == QtWidgets.QMessageBox.Yes:
        return True
    else:
        return False      
        
def massage(icon, title, message ):
    
    reply = QtWidgets.QMessageBox()
    
    if icon == "critical":
        reply.setIconPixmap(warning_icon)

    elif icon == "warning":
        reply.setIconPixmap(simple_warning_icon)

    elif icon == "massage":
        reply.setIconPixmap(massage_icon)
   
    reply.setText(message)
    reply.setWindowTitle(title)
    reply.setStandardButtons(QtWidgets.QMessageBox.Close)
    
    result = reply.exec_()
 
        
set_icons()


class about(QtWidgets.QDialog):
    def __init__(self, parent = None, title = None):
        super(about, self).__init__(parent)                    

        self.setMaximumWidth(330) 
        self.setMinimumWidth(330)        
        self.setMaximumHeight(300) 

        layout = QtWidgets.QVBoxLayout(self)

        self.logo_label = QtWidgets.QLabel()
        self.logo_label.setPixmap(logo.scaled(250,56))         
        self.logo_label.setAlignment(QtCore.Qt.AlignCenter)

        self.version_label = QtWidgets.QLabel("<b>V 1.0.2</b>")
        self.version_label.setAlignment(QtCore.Qt.AlignCenter)
        
        self.title_label = QtWidgets.QLabel("<b>A SIMPLE PROJECTS MANAGER FOR MAYA</b>")
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        
        self.info_label = QtWidgets.QLabel("<a href='http://pipeline.nnl.tv'><font color='white'>http://pipeline.nnl.tv</font></a><br><br>All rights reserved to Lior Ben Horin 2016")
        self.info_label.setAlignment(QtCore.Qt.AlignCenter)
        

        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok,
            QtCore.Qt.Horizontal, self)
        
        buttons.setCenterButtons(True)
        buttons.accepted.connect(self.accept)
        
        layout.addWidget(self.logo_label)
        layout.addWidget(self.version_label)  
        layout.addWidget(HLine())
        layout.addWidget(self.title_label)
        layout.addWidget(self.info_label)
        layout.addWidget(buttons)


class Create_from_selection(QtWidgets.QDialog):
    def __init__(self, parent = None, title = None):
        super(Create_from_selection, self).__init__(parent)
        
        
        
        self.setMaximumWidth(200) 
        self.setMinimumWidth(200)        
        self.setMaximumHeight(50) 

        self.label = QtWidgets.QLabel()
        self.label.setPixmap(new_icon)

        layout = QtWidgets.QVBoxLayout(self)
        self.item_name = QtWidgets.QLabel(title)
        self.text_input = QtWidgets.QLineEdit()
        self.include_radio = QtWidgets.QRadioButton("Include all connections")
        self.include_radio.setChecked(True)
        self.exclude_radio = QtWidgets.QRadioButton("Include only textures")
        
        

        layout.addWidget(self.item_name)
        layout.addWidget(self.text_input)
        layout.addWidget(self.include_radio)
        layout.addWidget(self.exclude_radio)

        
        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
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
        
class collect_component_options(QtWidgets.QDialog):
    def __init__(self, parent = None, title = None):
        super(collect_component_options, self).__init__(parent)
        
    
        self.setMaximumWidth(200) 
        self.setMinimumWidth(200)        
        self.setMaximumHeight(50) 

        #self.label = QtWidgets.QLabel()
        #self.label.setPixmap(archive_icon)

        layout = QtWidgets.QVBoxLayout(self)
        self.item_name = QtWidgets.QLabel(title)

        self.include_reference = QtWidgets.QCheckBox("Include referenced files")
        self.include_reference.setChecked(True)
        self.include_textures = QtWidgets.QCheckBox("Include textures")
        self.include_textures.setChecked(True)
        
        
        #layout.addWidget(self.label)
        #layout.addStretch()
        layout.addWidget(self.item_name)

        layout.addWidget(HLine())
        layout.addWidget(self.include_reference)
        layout.addWidget(self.include_textures)
        
        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def options(self):
        references = False
        textures = False
               
        if self.include_reference.isChecked():
            references = True
        if self.include_textures.isChecked():
            textures = True 
            
        return references, textures  


    def result(self):
        return self.options()        


    
class Login(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)

        self.setMaximumWidth(200) 
        self.setMinimumWidth(200)        
        self.setMaximumHeight(50) 
        
        self.label = QtWidgets.QLabel()
        self.label.setPixmap(users_icon)
        
        self.label_user = QtWidgets.QLabel("Username:")
        self.label_password = QtWidgets.QLabel("Password:")
        
        self.textName = QtWidgets.QLineEdit(self)
        self.textName.setMinimumSize(QtCore.QSize(0, 30))
        self.textPass = QtWidgets.QLineEdit(self)
        self.textPass.setMinimumSize(QtCore.QSize(0, 30))

        self.textPass.setInputMethodHints(QtCore.Qt.ImhHiddenText|QtCore.Qt.ImhNoAutoUppercase|QtCore.Qt.ImhNoPredictiveText)
        self.textPass.setEchoMode(QtWidgets.QLineEdit.Password)
    
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.label)
        layout.addWidget(HLine())
        layout.addWidget(self.label_user)
        layout.addWidget(self.textName)
        layout.addWidget(self.label_password)
        layout.addWidget(self.textPass)
        
        log = QtWidgets.QPushButton("Login")
        log.setDefault(True)
        
        canc = QtWidgets.QPushButton("Cancel")
        
       
        buttons = QtWidgets.QDialogButtonBox(QtCore.Qt.Horizontal)
        buttons.addButton(log, QtWidgets.QDialogButtonBox.AcceptRole)
        buttons.addButton(canc, QtWidgets.QDialogButtonBox.RejectRole)

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        

    def result(self):
        return self.textName.text(), self.textPass.text()


class Note(QtWidgets.QDialog):
    def __init__(self, parent=None, plainText=None):
        super(Note, self).__init__(parent)

        self.setMaximumWidth(400) 
        self.setMinimumWidth(400)        
        self.setMaximumHeight(200) 
        
        self.label = QtWidgets.QLabel()
        self.label.setPixmap(edit_icon)
        
        self.label_Note = QtWidgets.QLabel("Take note:")
        self.textNote = QtWidgets.QTextEdit(self)
    
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(HLine())
        layout.addWidget(self.label_Note)
        layout.addWidget(self.textNote)

        
        ok = QtWidgets.QPushButton("OK")
        ok.setDefault(True)
        
        canc = QtWidgets.QPushButton("Cancel")
        
       
        buttons = QtWidgets.QDialogButtonBox(QtCore.Qt.Horizontal)
        buttons.addButton(ok, QtWidgets.QDialogButtonBox.AcceptRole)
        buttons.addButton(canc, QtWidgets.QDialogButtonBox.RejectRole)

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
        self.textNote.setPlainText(plainText)

    def result(self):
        if self.textNote.toPlainText() == "":
            return "No notes"
        return self.textNote.toPlainText()

class ErrorReport(QtWidgets.QDialog):
    def __init__(self, parent=None, plainText=None):
        super(ErrorReport, self).__init__(parent)

        self.setMaximumWidth(600) 
        self.setMinimumWidth(600)        
        self.setMaximumHeight(800) 
        
        self.label = QtWidgets.QLabel()
        self.label.setPixmap(warning_icon)
        
        self.label_Note = QtWidgets.QLabel("Somthing is wrong here.<br>Considre sending this bug report for inspection.")
        self.textNote = QtWidgets.QTextEdit(self)
        self.label_what = QtWidgets.QLabel("Please describe what is going on: (optional)")
        self.textMore = QtWidgets.QTextEdit(self)
        
        self.dont_ask = QtWidgets.QCheckBox("Don't ask me this again")
        
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(HLine())
        layout.addWidget(self.label_Note)
        layout.addWidget(self.textNote)
        layout.addWidget(self.label_what)
        layout.addWidget(self.textMore)
        layout.addWidget(self.dont_ask)
        
        ok = QtWidgets.QPushButton("Email report")
        ok.setDefault(True)
        
        canc = QtWidgets.QPushButton("Dismiss")
        
       
        buttons = QtWidgets.QDialogButtonBox(QtCore.Qt.Horizontal)
        buttons.addButton(ok, QtWidgets.QDialogButtonBox.AcceptRole)
        buttons.addButton(canc, QtWidgets.QDialogButtonBox.RejectRole)

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
        self.textNote.setPlainText(plainText)

    def result(self):
        if self.dont_ask.isChecked():
            dont_ask = True
        else:
            dont_ask = False
            
        return self.textNote.toPlainText(), self.textMore.toPlainText(), dont_ask

        
class playblast_options(QtWidgets.QDialog):
    def __init__(self, parent = None, title = None, hud = True, offscreen = True, formats = None, format = "movie", compressions = None, compression = "H.264", scale = 50):
        super(playblast_options, self).__init__(parent)
        
    
        self.setMaximumWidth(200) 
        self.setMinimumWidth(200)        
        self.setMaximumHeight(50) 


        layout = QtWidgets.QVBoxLayout(self)
        self.item_name = QtWidgets.QLabel(title)

        self.include_hud = QtWidgets.QCheckBox("Record HUD")
        self.include_hud.setChecked(hud)
        
        self.render_offscreen = QtWidgets.QCheckBox("Record Offscreen")
        self.render_offscreen.setChecked(offscreen)

        
        self.scaleLayout = QtWidgets.QHBoxLayout(self)
        
        self.scale_label = QtWidgets.QLabel("Scale:")
        
        self.scaleSlider = QtWidgets.QSlider()
        self.scaleSlider.setOrientation(QtCore.Qt.Horizontal)
        self.scaleSlider.setMinimum(10)
        self.scaleSlider.setMaximum(100)
        self.scaleSlider.setValue(scale)       
        
        self.scaleSpinbox = QtWidgets.QSpinBox()
        self.scaleSpinbox.setMinimum(10)
        self.scaleSpinbox.setMaximum(100)
        self.scaleSpinbox.setValue(scale)
        
        self.scaleSlider.valueChanged.connect(self.sacle_spinbox_value)
        self.scaleSpinbox.valueChanged.connect(self.sacle_slider_value)

        
        self.scaleLayout.addWidget(self.scaleSpinbox)
        self.scaleLayout.addWidget(self.scaleSlider)
        
        self.format_label = QtWidgets.QLabel("Format:")
            
        self.format_combo = QtWidgets.QComboBox()
        self.format_combo.setEditable(False)
        if formats:
            self.format_combo.addItems(formats)
        else:
            self.format_combo.addItems([format])
                  
        i = self.format_combo.findText(format, QtCore.Qt.MatchFixedString)
        if i >= 0:
            self.format_combo.setCurrentIndex(i)

        self.compression_label = QtWidgets.QLabel("Compression:")

        self.compression_combo = QtWidgets.QComboBox()
        self.compression_combo.setEditable(False)
        if formats:
            self.compression_combo.addItems(compressions)
        else:
            self.compression_combo.addItems([compression])
                  
        i = self.compression_combo.findText(compression, QtCore.Qt.MatchFixedString)
        if i >= 0:
            self.compression_combo.setCurrentIndex(i)

        
        layout.addWidget(self.item_name)

        layout.addWidget(HLine())
        layout.addWidget(self.include_hud)
        layout.addWidget(self.render_offscreen)
        layout.addWidget(self.scale_label)
        layout.addLayout(self.scaleLayout)
        layout.addWidget(self.format_label)
        layout.addWidget(self.format_combo)
        layout.addWidget(self.compression_label)
        layout.addWidget(self.compression_combo)
                
        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def sacle_spinbox_value(self,value):
        self.scaleSpinbox.setValue(value)

    def sacle_slider_value(self,value):
        self.scaleSlider.setValue(value)
    
    def options(self):
        options = {}
        hud = False
        offscreen = False
        
        if self.include_hud.isChecked():
            hud = True
        if self.render_offscreen.isChecked():
            offscreen = False
        
        options["hud"] = hud
        options["offscreen"] = offscreen
        options["format"] = self.format_combo.currentText() 
        options["compression"] = self.compression_combo.currentText()
        options["scale"] = self.scaleSpinbox.value()
            
        return options
        
    def result(self):
        return self.options()   


def encode64(string):
    return base64.b64encode(string)

def decode64(string):
    return  base64.b64decode(string)


def HLine():
    toto = QtWidgets.QFrame()
    toto.setFrameShape(QtWidgets.QFrame.HLine)
    toto.setFrameShadow(QtWidgets.QFrame.Sunken)
    return toto    
    
def crop_text(text,lines,crop_sign):   
    if len(text.split('\n')) > lines:
        crop_text  = text.rsplit('\n',len(text.split('\n'))-lines)[0]
        crop_text = crop_text + crop_sign
        return crop_text    
    else:
        return text

def _decode_strings():
    strings = []
    strings.append(decode64(data.encoded_strings()[0]))
    strings.append(decode64(data.encoded_strings()[1]))
    strings.append(decode64(data.encoded_strings()[2]))
    strings.append(decode64(data.encoded_strings()[3]))
    strings.append(decode64(data.encoded_strings()[5]))
    strings.append(ast.literal_eval(decode64(data.encoded_strings()[7])))                                                      
    return strings
    
