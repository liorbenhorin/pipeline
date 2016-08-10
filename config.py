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
_standard_ = "standard"
_super_ = "super"


localIconPath = os.path.join(os.path.dirname(__file__), 'icons/treeview/')
# if os.path.exists(localIconPath):

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
master_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "save_master"))
creation_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "creation"))
new_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "new"))
client_icon = os.path.join(localIconPath, "%s.svg" % "client")
add_cube_icon = os.path.join(localIconPath, "%s.svg" % "add_cube")
dummy_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "braces"))
collapse_icon = os.path.join(localIconPath, "%s.svg" % "unfold-less")
expend_icon = os.path.join(localIconPath, "%s.svg" % "unfold-more")
offline_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "offline"))
catagory_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "catagory"))
asset_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "asset"))
component_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "component"))
delete_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "delete"))
load_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "load"))
unload_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "unload"))
project_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "project"))
users_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "users"))
settings_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "settings"))
set_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "set"))
yes_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "yes"))
no_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "no"))
search_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "search"))
edit_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "edit"))
new_folder_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "new_folder"))
open_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "open"))
save_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "save"))
save_master_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "save_master"))
down_arrow_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "down_arrow"))
import_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "import"))
export_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "export"))
help_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "help"))
anim_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "anim"))
asset_mode_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "asset_mode"))
reload_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "reload"))
shutter_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "shutter"))
camrea_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "camera"))
play_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "play"))
large_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "large"))
small_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "small"))

large_image_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "large_image"))
large_image_icon_dark = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "large_image_dark"))
large_image_icon_click = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "large_image_click"))
large_image_icon_click_dark = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "large_image_click_dark"))

wide_image_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "wide_image"))
wide_image_icon_click = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "wide_image_click"))
wide_image_icon_dark = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "wide_image_dark"))
wide_image_icon_click_dark = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "wide_image_click_dark"))

warning_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "critical"))
simple_warning_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "warning"))
massage_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "massage"))
archive_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "archive"))
logo = QtGui.QPixmap(os.path.join(localIconPath, "%s.png" % "pipeline_logo"))
time_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "time"))
buffer_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "buffer"))
counter_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "counter"))
text_icon = QtGui.QPixmap(os.path.join(localIconPath, "%s.svg" % "cursor-text"))