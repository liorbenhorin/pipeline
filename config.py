""" GLOBAL VARIABLES """
import os
from PySide import QtGui

_master_ = "master"
_admin_ = "admin"
_assets_ = "asset"
_animation_ = "animation"
_catagory_ = "catagory"
_new_ = "new"
_node_ = "node"
_root_ = "root"
_stage_ = "stage"
_asset_ = "asset"
_folder_ = "folder"
_dummy_ = "dummy"
_version_ = "version"

localIconPath = os.path.join(os.path.dirname(__file__), 'icons/treeview/')
if os.path.exists(localIconPath):

    branch_more = os.path.join(localIconPath, "branch-more.svg")
    branch_closed = os.path.join(localIconPath, "branch-closed.svg")
    branch_open = os.path.join(localIconPath, "branch-open.svg")
    branch_end = os.path.join(localIconPath, "branch-end.svg")
    vline = os.path.join(localIconPath, "vline.svg")
    localIconPath = os.path.join(os.path.dirname(__file__), 'icons/')
    folder_icon = os.path.join(localIconPath, "%s.svg" % "folder")
    cube_icon = os.path.join(localIconPath, "%s.svg" % "cube")
    cube_icon_full = os.path.join(localIconPath, "%s.svg" % "cube-fill")


    delete_folder_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "delete_folder"))
    comment_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "comment"))
    comment_full_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "comment_full"))
    add_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "add"))
    large_image_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "large_image"))