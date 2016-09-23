# PIPELINE
Projects manager for Maya

[http://pipeline.nnl.tv](http://pipeline.nnl.tv)

#Features

Pipeline is a simple and straight forward tool for managing maya projects,
from student shorts to meduim teams working on commercial projects.
It was inspired by the wonderful OpenPipline script, which appears to be discontinued.

**Simple**

Pipeline takes care of versions, nameing convention and folder structure, and nothing gets lost.
Asset bank for quick referecing into animation scenes.
Published assets with versions for easy recoveries.

**Collaborative**

Work on projects via file sharing services like Dropbox.
Users with premissions keep assets safe from less-technical animators.
OSX / Windows support.

**Straight forward**

Embeded nativly into Maya's interface.
Manage all you projects without leaving Maya.


#Version history

**TBA - 1.0.0 - First stable version**

**Version - 1.0.3 - Beta**

* Pipeline is compatible with Maya 2017 Win/OSX

**Version - 1.0.2 - Beta**

*New features*

* Rename anything (catagories, assets, components, sequences and shots).
* Toggle component masters from showing in the assets bank in the scenes mode (helps keep things clean).
* Record playblasts from shots, and Pipeline orgenise them in versions, too.
* Store playblasts inside the project folder or in a sister directory (useful when sharing projects to not slow down sync times).
* Improved notes module.
* file open is now writeing to maya's recently opened.
* the pipeline settings file is now stored inside the maya prefs directory.

*Fixed the following issues*

* Frame range and settings are not being loaded on file open.
* Project is not being right set after creation, on some cases.
* You cannot load a project, and need to restart Pipeline.
* Many function to fail when setting a version padding numbr other then 3.
* Showing an empty column when no users set to project
* Not setting the project correctly in some cases on a windows machines.


**8.6.16 - 1.0.0 - BETA - Free for educational and non commercial use!**

Like any program, it can have some bugs and glitchs,
so it's always a good idea to backup your work.
During the Beta stage Pipeline is collecting usage statistics.


#Compatibility

OSX / Windows
Maya 2015, 2016, 2016 Ext 2, 2017
Earlier Versions have not been tested.

#Installation

Place the pipeline folder in your maya scripts folder.
Run the following lines in a python tab in the script editor:
```
from pipeline import pipeline
pipeline.show()
```

#Feedback

Send feedback, bugreports and feature requests to liorbenhorin [at] gmail [dot] com

Enjoy!
