####################################################################################
## BODLoader
####################################################################################

####################################################################################
# Global variables
####################################################################################

global ModName
global ModDesc
global ModVersion
global ModAuthor
global ModAuthorInfo
global ModArenaMode
global NewFiles
global RepFiles
global MakeDirs

####################################################################################
# Mod Info
####################################################################################

# Mod Name
ModName = "Blade of Darkness Reforged"
# Mod Description
ModDesc = (
    """Description line 1\n""" """Description line 2\n""" """Description line 3\n"""
)

# Multilanguage descriptions:

# if Language.Current == "Spanish":
#  ModDesc          = (
#                    """Spanish Description line 1\n"""
# 	            """Spanish Description line 2\n"""
# 	            """Spanish Description line 3\n"""
# 	             )
# else:
#  ModDesc          = (
#                    """Description line 1\n"""
# 	            """Description line 2\n"""
# 	            """Description line 3\n"""
# 	             )

# Mod Version
ModVersion = "1.0"
# Author name
ModAuthor = "sfb" ", " "sryml (mod program)"
# Author info: email, url,...
ModAuthorInfo = "e-mail/home page"

####################################################################################
# Mod Data
####################################################################################

# Base dir for all paths: BOD\Maps\Casa

# Make new directories

MakeDirs = ["../../Config/BLConfig/BOD Reforged"]

# New Files added by Mod and destination directory

# NewFiles[0] = {"File": "File1.py", "Dest": "..\MapName"}
NewFiles[0] = {
    "File": "Scripts/settings.py",
    "Dest": "../../Config/BLConfig/BOD Reforged",
}
# Replaced Files
# RepFiles[1] = {"File": "Blade.exe", "Dest": "..\..\bin"}

# Setup to 1 for enable this mod in Arena mode
ModArenaMode = 0
