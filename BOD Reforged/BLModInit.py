####################################################################################
## BODLoader Mod Init File
####################################################################################

# Mod imports

import Bladex
import Reference
import GameText

# Translations

import Language
import MenuText

import sys

#
sys.path.append("../../BODLoader/Mods/BOD Reforged/Scripts")

#####################
if sys.modules.get("ReforgedMenu"):
    ReforgedMenu = reload(sys.modules["ReforgedMenu"])
else:
    import ReforgedMenu

global ModMenu
ModMenu = ReforgedMenu.ModMenu
#####################

sys.path.remove("../../BODLoader/Mods/BOD Reforged/Scripts")
