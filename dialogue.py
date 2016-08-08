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
from PySide import QtCore, QtGui
import os
import ast

import modules.data as data
reload(data)
#
# import data_model as dtm
# reload(dtm)
# #


global preset
preset = {}
preset["project_name"] = "puppies"
preset["prefix"] = "pdt"
preset["padding"] = 2


global _admin_
_admin_ = "admin"

import data_view as dtv
import data_model as dtm
import data as dt


# reload(dt)
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


    global buffer_icon
    global counter_icon
    global text_icon
    global time_icon

    time_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "time"))

    buffer_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "buffer"))
    counter_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "counter"))
    text_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "cursor-text"))

        
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


class about(QtGui.QDialog):
    def __init__(self, parent = None, title = None):
        super(about, self).__init__(parent)                    

        self.setMaximumWidth(330) 
        self.setMinimumWidth(330)        
        self.setMaximumHeight(300) 

        layout = QtGui.QVBoxLayout(self)

        self.logo_label = QtGui.QLabel()
        self.logo_label.setPixmap(logo.scaled(250,56))         
        self.logo_label.setAlignment(QtCore.Qt.AlignCenter)

        self.version_label = QtGui.QLabel("<b>V 1.0</b>")
        self.version_label.setAlignment(QtCore.Qt.AlignCenter)
        
        self.title_label = QtGui.QLabel("<b>A SIMPLE PROJECTS MANAGER FOR MAYA</b>")
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        
        self.info_label = QtGui.QLabel("<a href='http://pipeline.nnl.tv'><font color='white'>http://pipeline.nnl.tv</font></a><br><br>All rights reserved to Lior Ben Horin 2016")
        self.info_label.setAlignment(QtCore.Qt.AlignCenter)
        

        buttons = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok,
            QtCore.Qt.Horizontal, self)
        
        buttons.setCenterButtons(True)
        buttons.accepted.connect(self.accept)
        
        layout.addWidget(self.logo_label)
        layout.addWidget(self.version_label)  
        layout.addWidget(HLine())
        layout.addWidget(self.title_label)
        layout.addWidget(self.info_label)
        layout.addWidget(buttons)


class Create_from_selection(QtGui.QDialog):
    def __init__(self, parent = None, title = None):
        super(Create_from_selection, self).__init__(parent)
        
        
        
        self.setMaximumWidth(200) 
        self.setMinimumWidth(200)        
        self.setMaximumHeight(50) 

        self.label = QtGui.QLabel()
        self.label.setPixmap(new_icon)

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
        
class collect_component_options(QtGui.QDialog):
    def __init__(self, parent = None, title = None):
        super(collect_component_options, self).__init__(parent)
        
    
        self.setMaximumWidth(200) 
        self.setMinimumWidth(200)        
        self.setMaximumHeight(50) 

        #self.label = QtGui.QLabel()
        #self.label.setPixmap(archive_icon)

        layout = QtGui.QVBoxLayout(self)
        self.item_name = QtGui.QLabel(title)

        self.include_reference = QtGui.QCheckBox("Include referenced files")
        self.include_reference.setChecked(True)
        self.include_textures = QtGui.QCheckBox("Include textures")
        self.include_textures.setChecked(True)
        
        
        #layout.addWidget(self.label)
        #layout.addStretch()
        layout.addWidget(self.item_name)

        layout.addWidget(HLine())
        layout.addWidget(self.include_reference)
        layout.addWidget(self.include_textures)
        
        buttons = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel,
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
        layout.addWidget(self.label)
        layout.addWidget(HLine())
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


class Note(QtGui.QDialog):
    def __init__(self, parent=None, plainText=None):
        super(Note, self).__init__(parent)

        self.setMaximumWidth(400) 
        self.setMinimumWidth(400)        
        self.setMaximumHeight(200) 
        
        self.label = QtGui.QLabel()
        self.label.setPixmap(edit_icon)
        
        self.label_Note = QtGui.QLabel("Take note:")       
        self.textNote = QtGui.QTextEdit(self)
    
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(HLine())
        layout.addWidget(self.label_Note)
        layout.addWidget(self.textNote)

        
        ok = QtGui.QPushButton("OK")
        ok.setDefault(True)
        
        canc = QtGui.QPushButton("Cancel")
        
       
        buttons = QtGui.QDialogButtonBox(QtCore.Qt.Horizontal)
        buttons.addButton(ok, QtGui.QDialogButtonBox.AcceptRole)
        buttons.addButton(canc, QtGui.QDialogButtonBox.RejectRole)

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
        self.textNote.setPlainText(plainText)

    def result(self):
        if self.textNote.toPlainText() == "":
            return "No notes"
        return self.textNote.toPlainText()

class ErrorReport(QtGui.QDialog):
    def __init__(self, parent=None, plainText=None):
        super(ErrorReport, self).__init__(parent)

        self.setMaximumWidth(600) 
        self.setMinimumWidth(600)        
        self.setMaximumHeight(800) 
        
        self.label = QtGui.QLabel()
        self.label.setPixmap(warning_icon)
        
        self.label_Note = QtGui.QLabel("Somthing is wrong here.<br>Considre sending this bug report for inspection.")
        self.textNote = QtGui.QTextEdit(self)
        self.label_what = QtGui.QLabel("Please describe what is going on: (optional)")
        self.textMore = QtGui.QTextEdit(self)
        
        self.dont_ask = QtGui.QCheckBox("Don't ask me this again")
        
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(HLine())
        layout.addWidget(self.label_Note)
        layout.addWidget(self.textNote)
        layout.addWidget(self.label_what)
        layout.addWidget(self.textMore)
        layout.addWidget(self.dont_ask)
        
        ok = QtGui.QPushButton("Email report")
        ok.setDefault(True)
        
        canc = QtGui.QPushButton("Dismiss")
        
       
        buttons = QtGui.QDialogButtonBox(QtCore.Qt.Horizontal)
        buttons.addButton(ok, QtGui.QDialogButtonBox.AcceptRole)
        buttons.addButton(canc, QtGui.QDialogButtonBox.RejectRole)

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

        
class playblast_options(QtGui.QDialog):
    def __init__(self, parent = None, title = None, hud = True, offscreen = True, formats = None, format = "movie", compressions = None, compression = "H.264", scale = 50):
        super(playblast_options, self).__init__(parent)
        
    
        self.setMaximumWidth(200) 
        self.setMinimumWidth(200)        
        self.setMaximumHeight(50) 


        layout = QtGui.QVBoxLayout(self)
        self.item_name = QtGui.QLabel(title)

        self.include_hud = QtGui.QCheckBox("Record HUD")
        self.include_hud.setChecked(hud)
        
        self.render_offscreen = QtGui.QCheckBox("Record Offscreen")
        self.render_offscreen.setChecked(offscreen)

        
        self.scaleLayout = QtGui.QHBoxLayout(self)
        
        self.scale_label = QtGui.QLabel("Scale:")
        
        self.scaleSlider = QtGui.QSlider()
        self.scaleSlider.setOrientation(QtCore.Qt.Horizontal)
        self.scaleSlider.setMinimum(10)
        self.scaleSlider.setMaximum(100)
        self.scaleSlider.setValue(scale)       
        
        self.scaleSpinbox = QtGui.QSpinBox()
        self.scaleSpinbox.setMinimum(10)
        self.scaleSpinbox.setMaximum(100)
        self.scaleSpinbox.setValue(scale)
        
        self.scaleSlider.valueChanged.connect(self.sacle_spinbox_value)
        self.scaleSpinbox.valueChanged.connect(self.sacle_slider_value)

        
        self.scaleLayout.addWidget(self.scaleSpinbox)
        self.scaleLayout.addWidget(self.scaleSlider)
        
        self.format_label = QtGui.QLabel("Format:")    
            
        self.format_combo = QtGui.QComboBox()
        self.format_combo.setEditable(False)
        if formats:
            self.format_combo.addItems(formats)
        else:
            self.format_combo.addItems([format])
                  
        i = self.format_combo.findText(format, QtCore.Qt.MatchFixedString)
        if i >= 0:
            self.format_combo.setCurrentIndex(i)

        self.compression_label = QtGui.QLabel("Compression:")  

        self.compression_combo = QtGui.QComboBox()
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
                
        buttons = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel,
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
    toto = QtGui.QFrame()
    toto.setFrameShape(QtGui.QFrame.HLine)
    toto.setFrameShadow(QtGui.QFrame.Sunken)
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




class newStage(QtGui.QDialog):
    def __init__(self, parent = None, title = None, stages = []):
        super(newStage, self).__init__(parent)
        
    
        self.setMaximumWidth(200) 
        self.setMinimumWidth(200)        
        self.setMaximumHeight(50) 


        layout = QtGui.QVBoxLayout(self)
        self.stage_name = QtGui.QLabel("Stage type:")

        self.stage_combo = QtGui.QComboBox()
        self.stage_combo.setEditable(False)
        if stages:
            self.stage_combo.addItems(stages)
        else:
            self.stage_combo.addItems([stages])
                  
     
        layout.addWidget(self.stage_name)
        layout.addWidget(self.stage_combo)

                
        buttons = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

       
    def result(self):
        return self.stage_combo.currentText()



class newNodeDialog(QtGui.QDialog):
    def __init__(self, parent=None, string = "", name_label_string = "", title = ""):
        super(newNodeDialog, self).__init__(parent)



        self.setMaximumWidth(400)
        self.setMinimumWidth(400)
        self.setMaximumHeight(50)

        self.layout = QtGui.QVBoxLayout(self)




        self.input_widget = QtGui.QWidget(self)
        self.input_layout = QtGui.QVBoxLayout(self.input_widget)

        self.name_widget = groupInput(self, label=name_label_string, inputWidget=QtGui.QLineEdit(self),  ic=text_icon)

        self.name_input = self.name_widget.input
        self.name_input.setText(string)


        self.create_title = Title(self, label=title)
        self.input_layout.addWidget(self.create_title)

        self.input_layout.addWidget(self.name_widget)

        self.layout.addWidget(self.input_widget)

        self.input_layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setContentsMargins(5, 5, 5, 10)

        buttons = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        self.layout.addWidget(buttons)



class newFolderDialog(newNodeDialog):
    def __init__(self, parent =  None, string = "", name_label_sting = "Name", title = "Create new folder"):
        super(newFolderDialog, self).__init__(parent, string, name_label_sting, title)



        self.input_quantity_widget = groupInput(self, label = "Quantity", inputWidget=QtGui.QSpinBox(self), ic= buffer_icon)

        self.quantity_slider = self.input_quantity_widget.input
        self.quantity_slider.setMinimum(1)
        self.quantity_slider.setMaximum(1000)
        self.quantity_slider.setValue(1)


        self.input_padding_widget = groupInput(self, label="Padding", inputWidget=QtGui.QSpinBox(self), ic=counter_icon)

        self.padding_slider = self.input_padding_widget.input
        self.padding_slider.setMinimum(0)
        self.padding_slider.setMaximum(6)
        self.padding_slider.setValue(3)

        self.input_layout.addWidget(self.input_quantity_widget)
        self.input_layout.addWidget(self.input_padding_widget)


    def result(self):
        res = {}
        res["name"] = self.name_input.text()
        res["quantity"] = self.quantity_slider.value()
        res["padding"] = self.padding_slider.value()
        return res






class newAssetDialog(newFolderDialog):
    def __init__(self, parent =  None, string = "", name_label_sting = "Name", title = "Create new asset", stages = [], ancestors = None, project = None):
        super(newAssetDialog, self).__init__(parent, string, name_label_sting, title)

        self.create_stages_title = Title(self, label = "Add stages:")
        self.input_layout.addWidget(self.create_stages_title)
        self.project = project

        self.stages_options = {}
        for stage in stages:
            widget = QtGui.QWidget(self)
            layout = QtGui.QVBoxLayout(widget)
            layout.setContentsMargins(5, 2, 5, 2)
            layout.setAlignment(QtCore.Qt.AlignLeft)
            checkbox = QtGui.QCheckBox(stage)
            self.stages_options[stage] = checkbox
            layout.addWidget(checkbox)
            self.input_layout.addWidget(widget)

        ancestors_names = []
        [ancestors_names.append("<{}>".format(node.name)) for node in ancestors]

        self.name_format_widget = NameFormatWidget( self, name_input=self.name_input, ancestors=ancestors_names, project = self.project)
        self.input_layout.addWidget(self.name_format_widget)
        self.name_input.textChanged.connect(self.name_format_widget.preview_format)



    def result(self):
        res = {}
        res["name"] = self.name_input.text()
        res["quantity"] = self.quantity_slider.value()
        res["padding"] = self.padding_slider.value()
        stages = {}
        for option in self.stages_options:
            stages[option] = self.stages_options[option].isChecked() # {stage: bool}
        res["stages"] = stages
        res["name_format"] = self.name_format_widget.depth_slider.value()
        return res



class newStageDialog(newNodeDialog):
    def __init__(self, parent =  None, string = "", parent_name = None, name_label_sting = "Name", title = "Create new stage", stages = [], ancestors = None, project = None):
        super(newStageDialog, self).__init__(parent, string, name_label_sting, title)

        self.project = project
        self.name_widget.setParent(None)
        self.name_widget.deleteLater()


        #self.create_stages_title = Title(self, label = "Add stages:")
        #self.input_layout.addWidget(self.create_stages_title)

        self.stages_options = {}
        for stage in stages:
            widget = QtGui.QWidget(self)
            layout = QtGui.QVBoxLayout(widget)
            layout.setContentsMargins(5, 2, 5, 2)
            layout.setAlignment(QtCore.Qt.AlignLeft)
            checkbox = QtGui.QCheckBox(stage)
            self.stages_options[stage] = checkbox
            layout.addWidget(checkbox)
            self.input_layout.addWidget(widget)

        ancestors_names = []
        [ancestors_names.append("<{}>".format(node.name)) for node in ancestors]

        self.name_format_widget = NameFormatWidget( self, parent_name=parent_name, ancestors=ancestors_names, project = self.project)
        self.input_layout.addWidget(self.name_format_widget)
        #self.name_input.textChanged.connect(self.name_format_widget.preview_format)



    def result(self):
        res = {}
        stages = {}
        for option in self.stages_options:
            stages[option] = self.stages_options[option].isChecked() # {stage: bool}
        res["stages"] = stages
        res["name_format"] = self.name_format_widget.depth_slider.value()
        return res



class newTreeDialog(newFolderDialog):
    def __init__(self, parent =  None, string = "", name_label_sting = "Name", title = "Create new tree", stages = [], project = None, section = None):
        super(newTreeDialog, self).__init__(parent, string, name_label_sting, title)
        self.project = project
        self.levels_names = self.project.levels[section]
        self.levels = []
        self.name_widget.label.setText("{} name".format(self.levels_names[0]))
        self.name_input.setText(self.levels_names[0])
        self.levels.append([self.levels_names[0], self.name_input, self.quantity_slider, self.padding_slider])
        names = []
        for i in range(1,len(self.levels_names)-1):
            names.append(self.levels_names[i])



        for level in names:
            name_widget = groupInput(self, label=level, inputWidget=QtGui.QLineEdit(self),
                                          ic=text_icon)
            name_widget.label.setText("{} name".format(level))
            create_title = Title(self, label=level)
            name_input = name_widget.input
            name_input.setText(level)
            self.input_layout.addWidget(create_title)
            self.input_layout.addWidget(name_widget)

            input_quantity_widget = groupInput(self, label="Quantity", inputWidget=QtGui.QSpinBox(self),
                                                    ic=buffer_icon)

            quantity_slider = input_quantity_widget.input
            quantity_slider.setMinimum(1)
            quantity_slider.setMaximum(1000)
            quantity_slider.setValue(1)
            self.input_layout.addWidget(input_quantity_widget)
            input_padding_widget = groupInput(self, label="Padding", inputWidget=QtGui.QSpinBox(self),
                                                   ic=counter_icon)

            padding_slider = input_padding_widget.input
            padding_slider.setMinimum(0)
            padding_slider.setMaximum(6)
            padding_slider.setValue(3)
            self.input_layout.addWidget(input_padding_widget)
            self.levels.append([level, name_input, quantity_slider, padding_slider])


        self.create_stages_title = Title(self, label = "Add stages:")
        self.input_layout.addWidget(self.create_stages_title)
        self.project = project
        stages = self.project.stages[section]

        self.stages_options = {}
        for stage in stages:
            widget = QtGui.QWidget(self)
            layout = QtGui.QVBoxLayout(widget)
            layout.setContentsMargins(5, 2, 5, 2)
            layout.setAlignment(QtCore.Qt.AlignLeft)
            checkbox = QtGui.QCheckBox(stage)
            self.stages_options[stage] = checkbox
            layout.addWidget(checkbox)
            self.input_layout.addWidget(widget)

        ancestors = list(self.project.levels[section])
        ancestors = ancestors[:-1]


        self.name_format_widget = NameFormatWidget( self,  multi_inputs = self.levels, ancestors=ancestors, project = self.project)
        self.input_layout.addWidget(self.name_format_widget)
        for l in self.levels:
            l[1].textChanged.connect(self.name_format_widget.preview_format)
            l[3].valueChanged.connect(self.name_format_widget.preview_format)


    def result(self):
        res = {}



        levels = []
        for level in self.levels:
            levels.append([level[0],level[1].text(),level[2].value(),level[3].value()])
        res["levels"] = levels
        '''
        res["levels"] is a list with instruction for tree creation:
        [ [level_name, folder_name, padding, quantitiy] , ... for each level ]
        '''

        stages = {}
        for option in self.stages_options:
            stages[option] = self.stages_options[option].isChecked() # {stage: bool}
        res["stages"] = stages
        res["name_format"] = self.name_format_widget.depth_slider.value()
        return res



class NameFormatWidget(QtGui.QWidget):
    def __init__(self, parent = None, parent_name = None, name_input = None, multi_inputs = None, ancestors = None, project = None):
        super(NameFormatWidget, self).__init__(parent)

        self.project = project

        self.name_input = name_input
        self.multi_inputs = multi_inputs
        self.ancestors = ancestors
        self.parent_name = parent_name

        self.ancestors_names = ancestors

        if not multi_inputs:
            self.ancestors_names.reverse()
            self.ancestors_names.pop(0)

        self.max_depth = len(self.ancestors_names)

        self.layout = QtGui.QVBoxLayout(self)
        self.layout.setContentsMargins(5, 2, 5, 2)
        self.layout.setAlignment(QtCore.Qt.AlignLeft)

        self.file_name_title = Title(self, label="File name format:")
        self.layout.addWidget(self.file_name_title)

        self.input_format_widget = groupInput(self, label="Format Depth", inputWidget=QtGui.QSpinBox(self), ic=counter_icon)

        self.depth_slider = self.input_format_widget.input
        self.depth_slider.setMinimum(0)
        self.depth_slider.setMaximum(self.max_depth)
        self.depth_slider.setValue(self.max_depth)

        self.format_preview_widget = groupInput(self, inputWidget=QtGui.QLineEdit(self))
        self.format_preview = self.format_preview_widget.input
        self.format_preview.setEnabled(False)
        self.preview_format()

        self.layout.addWidget(self.input_format_widget)
        self.layout.addWidget(self.format_preview_widget)

        self.depth_slider.valueChanged.connect(self.preview_format)


    def pad_proxy(self, val):
        pad = ""
        for i in range(val):
            pad += "#"
        return pad

    def preview_format(self):
        levels = self.ancestors_names[-self.depth_slider.value():] if self.depth_slider.value() > 0 else []
        if self.name_input:
            new_name = "<{}>".format(self.name_input.text()) if self.name_input.text() else "<{}>".format("asset_name")
            levels.append(new_name)



        if self.multi_inputs:
            levels = []
            if self.depth_slider.value() > 0:
                for input in self.multi_inputs[-self.depth_slider.value():]:
                    text = input[1]
                    pad = input[3]
                    new_name = "<{}>".format(text.text()) if text.text() else "<{}>".format(self.pad_proxy(pad.value()))
                    levels.append(new_name)
            else:
                input = self.multi_inputs[-1]
                text = input[1]
                pad = input[3]
                new_name = "<{}>".format(text.text()) if text.text() else "<{}>".format(self.pad_proxy(pad.value()))
                levels.append(new_name)

        levels.append("<stage>")

        string = "_".join(levels)

        pad = self.pad_proxy(self.project.project_padding)

        final = "{0}_{1}_{2}{3}.{4}".format(self.project.prefix, string, "v", pad,"ma") if self.project.prefix else "{0}_{1}{2}.{3}".format( string, "v", pad,"ma")
        self.format_preview.setText(final)

class Title(QtGui.QWidget):
    def __init__(self, parent, label="Input"):
        super(Title, self).__init__(parent)

        self.layout = QtGui.QVBoxLayout(self)
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.layout.setAlignment(QtCore.Qt.AlignLeft)

        self.label = QtGui.QLabel(label)
        self.label.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.label.setMinimumSize(QtCore.QSize(60, 20))

        self.layout.addWidget(self.label)

        self.layout.addWidget(HLine())
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)



class groupInput(QtGui.QWidget):
    def __init__(self, parent, label = None, inputWidget = None, ic = None):
        super(groupInput, self).__init__(parent)

        self.layout = QtGui.QHBoxLayout(self)
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.layout.setAlignment(QtCore.Qt.AlignLeft)


        if ic:
            self.icon = QtGui.QLabel()
            self.icon.setPixmap(ic)
            self.icon.setMinimumSize(QtCore.QSize(24, 24))
            self.layout.addWidget(self.icon)


        if label:
            self.label = QtGui.QLabel(label)
            self.label.setMinimumSize(QtCore.QSize(100, 30))
            self.layout.addWidget(self.label)

        if inputWidget:
            self.input = inputWidget
            self.input.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding )
            self.input.setMinimumSize(QtCore.QSize(0, 30))
            self.layout.addWidget(self.input)






class projectDialog(QtGui.QDialog):
    def __init__(self, parent=None, **kwargs):
        super(projectDialog, self).__init__(parent)



        self.layout = QtGui.QVBoxLayout(self)


        self.input_widget = QtGui.QWidget(self)
        self.input_layout = QtGui.QVBoxLayout(self.input_widget)

        self.title = Title(self, label= "New project")
        self.input_layout.addWidget(self.title)


        self.name_widget = groupInput(self, label="Project name", inputWidget=QtGui.QLineEdit(self), ic=text_icon)
        self.name_input = self.name_widget.input
        self.input_layout.addWidget(self.name_widget)


        self.input_padding_widget = groupInput(self, label="Padding", inputWidget=QtGui.QSpinBox(self), ic=counter_icon)

        self.padding_slider = self.input_padding_widget.input
        self.padding_slider.setMinimum(0)
        self.padding_slider.setMaximum(6)
        self.padding_slider.setValue(3)
        self.input_layout.addWidget(self.input_padding_widget)


        self.input_fps_widget = groupInput(self, label="Default fps", inputWidget=QtGui.QComboBox(self), ic=time_icon)
        self.fps_input = self.input_fps_widget.input
        self.fps_input.setEditable(False)
        rates = ["PAL (25fps)", "Film (24fps)", "NTSC (30fps)"]
        self.fps_input.addItems(rates)
        self.input_layout.addWidget(self.input_fps_widget)
        i = self.fps_input.findText(rates[0], QtCore.Qt.MatchFixedString)
        if i >= 0:
            self.fps_input.setCurrentIndex(i)


        self.prefix_widget = groupInput(self, label="Project prefix", inputWidget=QtGui.QLineEdit(self), ic=text_icon)
        self.prefix_input = self.prefix_widget.input
        self.input_layout.addWidget(self.prefix_widget)

        self.suffix_widget = groupInput(self, label="Project suffix", inputWidget=QtGui.QLineEdit(self), ic=text_icon)
        self.suffix_input = self.suffix_widget.input
        self.input_layout.addWidget(self.suffix_widget)

        self.var_title = Title(self, label= "Project variables")
        self.input_layout.addWidget(self.var_title)

        self.variable_tabs = Tabs(self)
        self.input_layout.addWidget(self.variable_tabs)


        self.levels_widget = QtGui.QWidget()
        self.level_layout = QtGui.QVBoxLayout(self.levels_widget)
        self.levels_widget.setMinimumHeight(200)
        self.levels_widget.setMinimumWidth(450)
        self.variable_tabs.tab_widget.addTab(self.levels_widget, "Levels")
        self.levels_tree = dtv.PipelineLevelsView(self.levels_widget)
        self.level_layout.addWidget(self.levels_tree)
        self.levels_tree.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)

        self.stages_widget = QtGui.QWidget()
        self.stages_layout = QtGui.QVBoxLayout(self.stages_widget)
        self.stages_widget.setMinimumHeight(200)
        self.stages_widget.setMinimumWidth(450)
        self.variable_tabs.tab_widget.addTab(self.stages_widget, "Stages")
        self.stages_tree = dtv.PipelineLevelsView(self.stages_widget)
        self.stages_layout.addWidget(self.stages_tree)
        self.stages_tree.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)

        self.users_widget = QtGui.QWidget()
        self.users_layout = QtGui.QVBoxLayout(self.users_widget)
        self.users_widget.setMinimumHeight(200)
        self.users_widget.setMinimumWidth(450)
        self.variable_tabs.tab_widget.addTab(self.users_widget, "Users")
        self.users_tree = dtv.PipelineUsersView(self.users_widget)
        self.users_layout.addWidget(self.users_tree)
        self.users_tree.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)


        self.layout.addWidget(self.input_widget)
        self.input_layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setContentsMargins(5, 5, 5, 10)


        self.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)

        buttons = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal, self)

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        self.layout.addWidget(buttons)

        self.populated_variables()

        self.name_input.setText(preset["project_name"])
        self.padding_slider.setValue(preset["padding"])
        self.prefix_input.setText(preset["prefix"])


    def populated_variables(self):


        level1 = dt.LevelsNode("animation")
        level1.setLevels(["ep","seq","sc","stage"])
        level2 = dt.LevelsNode("asset")
        level2.setLevels(["ep","type","asset","stage"])

        self.levels_model = dtm.PipelineLevelsModel([level1,level2])
        self.levels_tree.setModel(self.levels_model)


        stages1 = dt.LevelsNode("animation")
        stages1.setLevels([ "layout","anim","lightning"])
        stages2 = dt.LevelsNode("asset")
        stages2.setLevels(["model", "rig", "clip","shading"])

        self.stages_model = dtm.PipelineStagesModel([stages1, stages2])
        self.stages_tree.setModel(self.stages_model)


        user1 = dt.UserNode("root", "1234", _admin_)
        self.users_model = dtm.PipelineUsersModel([user1])
        self.users_tree.setModel(self.users_model)


    def exctract_stages_levels_data(self, model):
        if model:
             levels = {}
             for index, root in enumerate(model.items):
                 levels[root.name] = filter(lambda a: a != "", root._levels)

             return levels

    def exctract_users_data(self, model):
        if model:
            users = {}
            for index, user in enumerate(model.items):
                users[index] = [user.name, user._password, user._role]

            return users


    def result(self):
        res = {}
        res["name"] = self.name_input.text()
        res["fps"] = self.fps_input.currentText()
        res["padding"] = self.padding_slider.value()
        res["prefix"] = self.prefix_input.text()
        res["suffix"] = self.suffix_input.text()
        res["levels"] = self.exctract_stages_levels_data(self.levels_model)
        res["stages"] = self.exctract_stages_levels_data(self.stages_model)
        res["users"] = self.exctract_users_data(self.users_tree.model())
        return res

class WidgetLayout(QtGui.QWidget):
    def __init__(self, parent=None, layout = None):
        super(WidgetLayout, self).__init__(parent)

        self.layout = layout
        self.layout.setContentsMargins(5, 5, 5, 5)
        #self.layout.setAlignment(QtCore.Qt.AlignLeft)


class Tabs(QtGui.QWidget):
    def __init__(self, parent = None):
        super(Tabs, self).__init__(parent)

        self.layout = QtGui.QVBoxLayout(self)
        self.tab_widget = QtGui.QTabWidget(self)
        self.layout.addWidget(self.tab_widget)
        self.layout.setContentsMargins(5, 5, 5, 10)
        #self.tab_widget.setIconSize(QtCore.QSize(16,16))




class test(QtGui.QDialog):
    def __init__(self, parent = None, title = None):
        super(test, self).__init__(parent)

        layout =  QtGui.QVBoxLayout(self)
        scrollArea = QtGui.QScrollArea()

        scrollArea.setWidgetResizable(True)
        scrollAreaWidgetContents = QtGui.QWidget()
        scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 488, 208))

        horizontalLayout = QtGui.QHBoxLayout(scrollAreaWidgetContents)

        self.splitter = QtGui.QSplitter(scrollAreaWidgetContents)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setHandleWidth(10)
        self.splitter.setChildrenCollapsible(False)

        self._columns = []

        self.add_column_at_end(self.splitter)

        horizontalLayout.addWidget(self.splitter)
        scrollArea.setWidget(scrollAreaWidgetContents)

        layout.addWidget(scrollArea)


        widget = QtGui.QWidget()
        horizontalLayout_2 = QtGui.QHBoxLayout(widget)

        pushButton_2 = QtGui.QPushButton(widget)
        pushButton_2.setText("+")

        pushButton = QtGui.QPushButton(widget)
        pushButton.setText("-")

        pushButton_3 = QtGui.QPushButton(widget)
        pushButton_3.setText("reset")

        horizontalLayout_2.addWidget(pushButton_3)
        horizontalLayout_2.addWidget(pushButton_2)
        horizontalLayout_2.addWidget(pushButton)

        layout.addWidget(widget)

        pushButton_2.clicked.connect(self.add)
        pushButton.clicked.connect(self.remove)
        pushButton_3.clicked.connect(self.del_all_columns)

        import json
        print json.dumps(virtual_tree(),indent=2)

    def add(self):
        self.add_column_at_end(self.splitter)

    def remove(self):
        self.del_column_from_end()

    def add_column_at_end(self,splitter):
        self._columns.append(self.table_column(splitter))

    def del_column_from_end(self):
        if len(self._columns)>1:
            self._columns[-1].setParent(None)
            self._columns[-1].deleteLater()
            del self._columns[-1]
            return True
        return False

    def del_all_columns(self):
        while self.del_column_from_end():
            continue

    def table_column(self,splitter):
        tableWidget = QtGui.QTableWidget(splitter)
        tableWidget.setMinimumSize(QtCore.QSize(100, 100))
        splitter.addWidget(tableWidget)
        return tableWidget


def virtual_tree():
    tree = {}
    tree["root"] = {
                    "level_1":{
                               "level_1_2": None
                               }
                    ,"level_2":{"level_2_2":{
                                             "level_3_1":None
                                             }
                                }
                    }
    return tree



class test2(QtGui.QDialog):
    def __init__(self, parent = None, title = None):
        super(test2, self).__init__(parent)

        layout =  QtGui.QVBoxLayout(self)
        self.input_layout.addWidget(self.quantity_label)
        self.input_layout.addWidget(self.quantity_slider)

        self.treeWidget = QtGui.QTreeWidget(self);
        self.treeWidget.setAutoScrollMargin(16)
        self.treeWidget.setIndentation(30)
        self.treeWidget.setAnimated(False)
        self.treeWidget.setUniformRowHeights(True)

        font = QtGui.QFont()
        font.setPointSize(14)
        self.treeWidget.setFont(font)

        layout.addWidget(self.treeWidget)

        self.fill_widget(self.treeWidget, virtual_data())

    def fill_item(self,item, value):
        item.setExpanded(True)
        if type(value) is dict:
            for key, val in sorted(value.iteritems()):
                child = QtGui.QTreeWidgetItem()
                child.setText(0, unicode(key))
                item.addChild(child)
                self.fill_item(child, val)

        elif type(value) is list:
            for val in value:
                child = QtGui.QTreeWidgetItem()
                item.addChild(child)
                if type(val) is dict:
                    child.setText(0, '[dict]')
                    self.fill_item(child, val)
                elif type(val) is list:
                    child.setText(0, '[list]')
                    self.fill_item(child, val)
                else:
                    child.setText(0, unicode(val))
                    child.setExpanded(True)
        else:
            child = QtGui.QTreeWidgetItem()
            child.setText(0, unicode(value))
            item.addChild(child)

    def fill_widget(self,widget, value):
      widget.clear()
      self.fill_item(widget.invisibleRootItem(), value)

def virtual_data():
    d = { 'key1': 'value1',
         'key2': 'value2',
         'key3': [1,2,3, { 1: 3, 7 : 9}],
         'key5': { 'another key1' : 'another value1','another key2' : 'another value2'} }

    return d


class treeview(QtGui.QDialog):
    def __init__(self, parent = None, model = None):
        super(treeview, self).__init__(parent)

        layout =  QtGui.QVBoxLayout(self)

        self.treeView = QtGui.QTreeView(self);
        #self.treeView.setAutoScrollMargin(16)
        #self.treeView.setIndentation(30)
        #self.treeView.setAnimated(False)
        #self.treeView.setUniformRowHeights(True)
        self.treeView.setSortingEnabled(True)
        #font = QtGui.QFont()
        #font.setPointSize(14)
        #self.treeView.setFont(font)
        self.model = model
        self.treeView.setModel(self.model)

        line = QtGui.QLineEdit()
        layout.addWidget(line)

        layout.addWidget(self.treeView)

        QtCore.QObject.connect(line, QtCore.SIGNAL("textChanged(QString)"), self.model.setFilterRegExp)

