# Menu

import Bladex
import Console
import Menu
import MenuText
import BUIx
import Raster
import MenuWidget
import ScorerWidgets
import BBLib
import BCopy
import Reference
import os
import sys
import shutil
import string
import Language
import MemPersistence

#
MenuFontSmall = Language.LetrasMenuSmall
MenuFontMed = Language.LetrasMenu
MenuFontBig = Language.LetrasMenuBig


#
def makedirs(name, mode=511):
    head, tail = os.path.split(name)
    if head and tail and not os.path.exists(head):
        makedirs(head, mode)
    os.mkdir(name, mode)


# 获取当前菜单的部件
def GetMenuWidget(name):
    CurrFrame = Menu._MainMenu.MenuStack.Top()
    for i in CurrFrame.MenuItems:
        if hasattr(i, "MenuDescr") and i.MenuDescr["Name"] == name:
            return i


#
KEY = "BOD_Reforged_1"  # 对于内存储存的变量名称
MOD_PATH = "../../BODLoader/Mods/BOD Reforged/"
SETTINGS_PATH = "../../Config/BLConfig/BOD Reforged/settings.py"
MENU_LOGO_FILE = (
    MOD_PATH + "Scripts/log_small.png",
    "Reforged_log_small",
)
_RESHADEFX = 0  # 标志更改ReshadeFX
_LOGFILE = os.path.join(MOD_PATH, ".log")
Bladex.ReadBitMap(MENU_LOGO_FILE[0], MENU_LOGO_FILE[1])


#
execfile(os.path.join(MOD_PATH, "Scripts/GetFiles.py"))

dirs = [
    "../../bin/bin/Preset",
    "../../bin/bin/reshade-shaders/Shaders",
    "../../bin/bin/reshade-shaders/Shaders/FXShaders",
    "../../bin/bin/reshade-shaders/Shaders/qUINT",
    "../../bin/bin/reshade-shaders/Textures",
]

for i in dirs:
    if not os.path.exists(i):
        makedirs(i)


#
def WriteLog(arg):
    f = open(_LOGFILE, "at")
    f.write(arg)
    f.close()


def WriteMessage(*args):
    f = open(os.path.join(MOD_PATH, "Scripts/.message"), "w")
    for i in args:
        f.write(str(i) + "\n")
    f.close()


# 判断游戏状态/地图，调整Reshade效果
def CheckCurrentMap(time):
    global KEY
    if PRE_DATA["ReshadeFX"] == "Disabled":
        Bladex.RemoveAfterFrameFunc("CheckCurrentMap")
        WriteMessage("Disabled")
        MemPersistence.Delete(KEY)
        return

    v = MemPersistence.Get(KEY)
    if not v:
        curr_mode, curr_map = Bladex.GetAppMode(), Bladex.GetCurrentMap()
        MemPersistence.Store(KEY, [curr_mode, curr_map])
        WriteMessage(curr_mode, curr_map)
    else:
        pre_mode, pre_map = v
        curr_mode, curr_map = Bladex.GetAppMode(), Bladex.GetCurrentMap()
        changed = 0

        if (curr_mode != pre_mode) or (curr_map != pre_map):
            changed = 1

        #
        Scorer = sys.modules.get("Scorer")
        if curr_mode == "Game" and curr_map == "Casa" and Scorer:
            widget = Scorer.wFrame.GetWidget("AreYouSure")
            if widget.this != "NULL":
                mode = ["Game", "Menu"]
                curr_mode = mode[widget.GetVisible()]
                changed = curr_mode != pre_mode

        if changed:
            WriteMessage(curr_mode, curr_map)
            MemPersistence.Store(KEY, [curr_mode, curr_map])


def MoveFile(src, dst, src_descr, dst_descr):
    if os.path.exists(src):
        if not os.path.exists(dst):
            os.rename(src, dst)
            return 1
        else:
            WriteLog("BOD Reforged: <%s> %s file already exist\n" % (dst, dst_descr))
    else:
        WriteLog("BOD Reforged: <%s> %s file does not exist\n" % (src, src_descr))
    return 0


#
def ProcessFile(root, args, mode="move"):
    # 处理多种2K人物纹理之间的切换
    if type(args) == type(()):
        Textures = GetFiles("Texture")
        pre_files = GetFiles(args[0])
        # 当前游戏文件移动到暂存区
        for i in pre_files:
            cur_f = os.path.join("../../", i)
            cur_f2stage = os.path.join(root[0], i)
            MoveFile(cur_f, cur_f2stage, "current", "stage")
        # 新文件移动到游戏目录里
        for i in GetFiles(args[1]):
            cur_f = os.path.join("../../", i)
            new_f = os.path.join(root[1], i)

            ret = 1
            if i not in pre_files:
                if i in Textures:
                    reforged_f = os.path.join(MOD_PATH, "Reforged/", i)
                    ret = MoveFile(cur_f, reforged_f, "current", "reforged")
                else:
                    original_f = os.path.join(MOD_PATH, "Original/", i)
                    ret = MoveFile(cur_f, original_f, "current", "original")
            else:
                pre_files.remove(i)
            if ret:
                MoveFile(new_f, cur_f, "new", "current")
        # 文件数量少于上一种纹理，使用默认2K纹理
        for i in pre_files:
            cur_f = os.path.join("../../", i)
            reforged_f = os.path.join(MOD_PATH, "Reforged/", i)
            MoveFile(reforged_f, cur_f, "reforged", "current")
        return

    #
    for i in GetFiles(args):
        cur_f = os.path.join("../../", i)
        cur_f2stage = os.path.join(root[0], i)
        new_f = os.path.join(root[1], i)

        if mode == "overwrite":
            if not os.path.exists(cur_f2stage):
                if os.path.exists(cur_f):
                    os.rename(cur_f, cur_f2stage)
                else:
                    WriteLog("BOD Reforged: <%s> current file does not exist\n" % cur_f)
            if os.path.exists(new_f):
                shutil.copy(new_f, cur_f)
            else:
                WriteLog("BOD Reforged: <%s> new file does not exist\n" % new_f)
            continue

        # if mode == "move":
        ret = MoveFile(cur_f, cur_f2stage, "current", "stage")
        if not ret and string.find(args, "Char 2K") != -1:
            cur_f2stage = os.path.join(MOD_PATH, "Reforged/", i)
            ret = MoveFile(cur_f, cur_f2stage, "current", "stage")
        if ret:
            MoveFile(new_f, cur_f, "new", "current")

        # if os.path.exists(cur_f):
        #     if not os.path.exists(cur_f2stage):
        #         if os.path.exists(new_f):
        #             os.rename(cur_f, cur_f2stage)
        #             os.rename(new_f, cur_f)
        #         else:
        #             WriteLog("BOD Reforged: <%s> new file does not exist\n" % new_f)
        #     else:
        #         WriteLog("BOD Reforged: <%s> stage file already exist\n" % cur_f2stage)
        # else:
        #     WriteLog("BOD Reforged: <%s> current file does not exist\n" % cur_f)


def SetReshade(val):
    global KEY
    if val == "Enabled":
        for i in GetFiles("Reshade"):
            src, dst = os.path.join(MOD_PATH, "Reforged/", i), os.path.join("../../", i)
            shutil.copy(src, dst)
            if os.path.exists("../../bin/bin/dxgi.dll"):
                Bladex.SetAfterFrameFunc("CheckCurrentMap", CheckCurrentMap)
            else:
                Reference.debugprint("BOD Reforged: ReShade Not Installed.")
    else:
        for i in GetFiles("Reshade"):
            path = os.path.join("../../", i)
            if os.path.exists(path):
                os.remove(path)


def SaveSettings():
    s = str(DATA)
    s = string.replace(s, "{", "{\n    ")
    s = string.replace(s, ",", ",\n   ")
    s = string.replace(s, "}", "\n}")

    f = open(SETTINGS_PATH, "w")
    f.write("# DO NOT EDIT\n" "DATA = ")
    f.write(s)
    f.close()


def Install():
    # SetReshade(DATA["ReshadeFX"])
    # PRE_DATA["ReshadeFX"] = DATA["ReshadeFX"] = "Enabled"

    BLUnsFile = open(
        "../../BODLoader/Uns/BLUns_" + os.path.basename(MOD_PATH[:-1]) + ".py", "at"
    )
    BLUnsFile.write("%s\n" % ("import sys"))
    BLUnsFile.write("%s\n" % ("sys.modules['ReforgedMenu'].Uninstall()"))
    BLUnsFile.close()

    PRE_DATA["Installed"] = DATA["Installed"] = 1
    SaveSettings()
    Reference.debugprint("Reforged: Install")


def Uninstall():
    global DATA
    DATA = BCopy.deepcopy(DEF_DATA)
    ApplyCMD(None)
    Reference.debugprint("Reforged: Uninstall")


########


# 设置Apply选项是否可用
def OnChange():
    status = 0
    for i in DATA.keys():
        if DATA[i] != PRE_DATA[i]:
            if i != "CharTexture":
                status = 1
            # 人物纹理选项已改变，且选项可用
            elif GetMenuWidget(
                MenuText.GetMenuText("character textures") + ": "
            ).focusable:
                status = 1
            if status:
                break
    GetMenuWidget(MenuText.GetMenuText("Apply")).focusable = status


def IsFocusableReshadeFX(target):
    target.focusable = os.path.exists("../../bin/bin/dxgi.dll")


def SetReshadeFX(option):
    DATA["ReshadeFX"] = option
    OnChange()


def GetReshadeFX():
    return _DATA["ReshadeFX"].index(DATA["ReshadeFX"])


def InitLabelReshadeFX(target):
    MenuDescr = target.MenuDescr
    if os.path.exists("../../bin/bin/dxgi.dll"):
        MenuDescr["Text"] = "[Reshade: Installed]"
        MenuDescr["Color"] = 0, 200, 0
    else:
        MenuDescr["Text"] = "[Reshade: Uninstalled]"
        MenuDescr["Color"] = 200, 0, 0


def SetTexture(option, target):
    DATA["Texture"] = option
    v = GetTexture()
    GetMenuWidget(MenuText.GetMenuText("character textures") + ": ").focusable = v
    # if not v:
    #     GetMenuWidget(MenuText.GetMenuText("character textures") + ": ").SetSelOption(0)
    #     SetCharTexture(_DATA["CharTexture"][0])
    OnChange()


def GetTexture():
    return _DATA["Texture"].index(DATA["Texture"])


def SetCharTexture(option):
    DATA["CharTexture"] = option
    OnChange()


def GetCharTexture():
    return _DATA["CharTexture"].index(DATA["CharTexture"])


def IsFocusableCharTexture(target):
    target.focusable = GetTexture()


def SetHUD(option):
    DATA["HUD"] = option
    OnChange()


def GetHUD():
    return _DATA["HUD"].index(DATA["HUD"])


def SetGamePlayEnhancements(option):
    DATA["GamePlay Enhancements"] = option
    OnChange()


def GetGamePlayEnhancements():
    return _DATA["GamePlay Enhancements"].index(DATA["GamePlay Enhancements"])


def ApplyCMD(target):
    global DATA, PRE_DATA, _RESHADEFX
    # Empty Log
    if target:
        open(_LOGFILE, "w").close()

    # Reshade
    if DATA["ReshadeFX"] != PRE_DATA["ReshadeFX"]:
        SetReshade(DATA["ReshadeFX"])
        _RESHADEFX = 1
    else:
        _RESHADEFX = 0
    # Texture
    reset_CharTexture = 0
    if DATA["Texture"] != PRE_DATA["Texture"]:
        dir_name = {"Original": "Original", "2K": "Reforged"}
        root = (
            os.path.join(MOD_PATH, "%s/" % dir_name[PRE_DATA["Texture"]]),
            os.path.join(MOD_PATH, "%s/" % dir_name[DATA["Texture"]]),
        )
        ProcessFile(root, "Texture")
        if DATA["Texture"] == "Original":
            reset_CharTexture = 1

    # CharTexture
    Pre_CharTexture = (
        (PRE_DATA["Texture"] == "Original") and "Original" or PRE_DATA["CharTexture"]
    )
    CharTexture = (DATA["Texture"] == "Original") and "Original" or DATA["CharTexture"]
    if CharTexture != Pre_CharTexture:
        dir_name = {
            "Original": "Original",
            "2K": "Reforged/3DCHARS 2K",
            "2K Hybrid": "Reforged/3DCHARS 2K Hybrid",
            "2K Original": "Reforged/3DCHARS 2K Original",
        }
        root = (
            os.path.join(MOD_PATH, "%s/" % dir_name[Pre_CharTexture]),
            os.path.join(MOD_PATH, "%s/" % dir_name[CharTexture]),
        )
        if "Original" not in (Pre_CharTexture, CharTexture):
            args = (
                "Char " + Pre_CharTexture,
                "Char " + CharTexture,
            )
        else:
            args = (
                Pre_CharTexture == "Original"
                and ("Char " + CharTexture)
                or ("Char " + Pre_CharTexture)
            )
        ProcessFile(root, args)

    # HUD
    if DATA["HUD"] != PRE_DATA["HUD"]:
        dir_name = {"Original": "Original", "Updated": "Reforged/UPDATED_HUD"}
        root = (
            os.path.join(MOD_PATH, "%s/" % dir_name[PRE_DATA["HUD"]]),
            os.path.join(MOD_PATH, "%s/" % dir_name[DATA["HUD"]]),
        )
        ProcessFile(root, "HUD", "overwrite")

    # GamePlay Enhancements
    if DATA["GamePlay Enhancements"] != PRE_DATA["GamePlay Enhancements"]:
        dir_name = {"OFF": "Original", "ON": "Reforged"}
        root = (
            os.path.join(MOD_PATH, "%s/" % dir_name[PRE_DATA["GamePlay Enhancements"]]),
            os.path.join(MOD_PATH, "%s/" % dir_name[DATA["GamePlay Enhancements"]]),
        )
        ProcessFile(root, "GamePlay Enhancements", "overwrite")

    #
    if reset_CharTexture:
        GetMenuWidget(MenuText.GetMenuText("character textures") + ": ").SetSelOption(0)
        DATA["CharTexture"] = _DATA["CharTexture"][0]

    PRE_DATA = BCopy.deepcopy(DATA)
    # is not uninstall
    if target:
        SaveSettings()
        OnChange()


def InitRestartGame(target):
    import GameText

    global _RESHADEFX
    if _RESHADEFX:
        target.SetText(MenuText.GetMenuText("Restart Game"))
        target.MenuDescr["Command"] = RestartGame
    else:
        target.SetText(
            '%s "%s"'
            % (
                MenuText.GetMenuText("Restart"),
                GameText.MapDescriptor(Bladex.GetCurrentMap()),
            )
        )
        target.MenuDescr["Command"] = RestartLevel


# XXX Unable to know the rendering API
def RestartGame(target):
    cmd = os.path.join(MOD_PATH, "Scripts\\restart.bat")
    cmd = string.replace(cmd, "/", "\\")
    params = []
    if Console.ConsoleVisible():
        params.append("-console")
    os.system('start "" "%s" %s' % (cmd, string.join(params)))
    Bladex.Quit()


def RestartLevel(target):
    Bladex.LoadLevel(Bladex.GetCurrentMap())


########


class M_B_LogoWidget(BUIx.B_RectWidget):
    def __init__(self, Parent, MenuDescr, StackMenu):
        LogoFile = MenuDescr["LogoFile"]
        # self.Bitmap = {}

        logo = BBLib.B_BitMap24()
        logo.ReadFromFile(LogoFile[0])

        self.vidw, self.vidh = MenuDescr.get("Size", logo.GetDimension())
        GetScale = MenuDescr.get("Scale", 1.0)
        self.vidw, self.vidh = self.vidw * GetScale, self.vidh * GetScale
        BUIx.B_RectWidget.__init__(
            self, Parent, MenuDescr["Name"], self.vidw, self.vidh
        )
        # self.Selected = 0
        # self.Solid = 0
        # self.Border = 0
        # self.SetBorder(1)
        self.SetSolid(1)
        self.SetColor(255, 255, 255)
        self.SetAlpha(1)
        self.SetVisible(1)

        self.SetBitmap(LogoFile[1])
        # self.SetAutoScale(1)
        # self.SetDrawFunc(self.Draw)

    def Draw(self, x, y, time):
        Raster.SetPosition(x, y)
        Raster.DrawImage(self.vidw, self.vidh, "RGB", "Normal", self.Logobmp.GetData())
        self.DefDraw(x, y, time)

    def FinalRelease(self):
        BUIx.B_RectWidget.FinalRelease(self)

    def AcceptsFocus(self):
        return 0


class B_MenuItemLabelNoFXNoFocus(BUIx.B_TextWidget, MenuWidget.B_MenuTreeItem):
    def __init__(
        self, Parent, MenuDescr, StackMenu, font_server=ScorerWidgets.font_server
    ):
        font = MenuDescr.get("Font", Language.LetrasMenu)

        BUIx.B_TextWidget.__init__(
            self,
            Parent,
            "SubMenu" + MenuDescr["Name"],
            MenuDescr["Text"],
            font_server,
            font,
        )
        MenuWidget.B_MenuTreeItem.__init__(self, MenuDescr, StackMenu)

        self.SetDrawFunc(self.Draw)
        self.SetAlpha(MenuDescr.get("Alpha", 1.0))
        r, g, b = MenuDescr.get("Color", (210, 210, 0))
        self.SetColor(r, g, b)
        self.thisown = 1

        self.Pre_MenuDescr = BCopy.deepcopy(MenuDescr)
        MenuDescr.get("PostInitCommand", lambda x: 0)(self)

    def __del__(self):
        # print "B_MenuItemText.__del__()",self.Name()
        pass

    def __str__(self):
        # print "B_MenuItemTextNoFX widget with text",self.GetTextData()
        pass

    def Draw(self, x, y, time):
        if self.GetVisible() == 0:
            return

        if self.Pre_MenuDescr != self.MenuDescr:
            MenuDescr = self.MenuDescr
            self.SetText(MenuDescr["Text"])
            r, g, b = MenuDescr.get("Color", (210, 210, 0))
            self.SetAlpha(MenuDescr.get("Alpha", 1.0))
            self.SetColor(r, g, b)
            self.Pre_MenuDescr = BCopy.deepcopy(MenuDescr)

        self.DefDraw(x, y, time)

    def AcceptsFocus(self):
        return 0


class B_MenuItemOption(MenuWidget.B_MenuItemOption):
    def Draw(self, x, y, time):
        if self.GetVisible() == 0:
            return

        # print "MenuItemText",self.Name()
        foc = self.GetHasFocus()
        if foc:
            self.SetColor(252, 247, 167)
        elif not self.focusable:
            # self.SetColor(128, 128, 128)
            self.SetColor(207, 144, 49)
            self.SetAlpha(0.5)
        else:
            self.SetColor(207, 144, 49)

        self.DefDraw(x, y, time)
        self.SetAlpha(1.0)


class B_MenuItemTextNoFX(MenuWidget.B_MenuItemTextNoFX):
    def __init__(
        self, Parent, MenuDescr, StackMenu, font_server=ScorerWidgets.font_server
    ):
        MenuWidget.B_MenuItemTextNoFX.__init__(
            self, Parent, MenuDescr, StackMenu, font_server=ScorerWidgets.font_server
        )
        self.focusable = MenuDescr.get("Focusable", 1)
        MenuDescr.get("PostInitCommand", lambda x: 0)(self)

    def Draw(self, x, y, time):
        if self.GetVisible() == 0:
            return

        # print "MenuItemText",self.Name()
        foc = self.GetHasFocus()
        if foc:
            self.SetColor(252, 247, 167)
        elif not self.focusable:
            # self.SetColor(128, 128, 128)
            self.SetColor(207, 144, 49)
            self.SetAlpha(0.5)
        else:
            self.SetColor(207, 144, 49)

        self.DefDraw(x, y, time)
        self.SetAlpha(1.0)

    def ActivateItem(self, activate):
        if activate == 1:
            if not self.AcceptsFocus():
                return 0
            self.MenuDescr.get("Command_Force", lambda x: 0)(self)
            NewFrame = self.CreateFrame()
            if NewFrame:
                self.StackMenu.Push(NewFrame)
                return 1
            else:
                command = self.MenuDescr.get("Command")
                if command:
                    command(self)
                    return 1
                return 0
        elif activate == 0:
            w = self.StackMenu.Top()
            hasattr(w, "FinalRelease") and w.FinalRelease()
            self.StackMenu.Pop()

    def AcceptsFocus(self):
        return self.focusable


#

DEF_DATA = {
    "Installed": 0,
    "ReshadeFX": "Disabled",
    "Texture": "Original",
    "CharTexture": "2K",
    "HUD": "Original",
    "GamePlay Enhancements": "OFF",
}


class init(BUIx.B_RectWidget):
    def __init__(self, Parent, MenuDescr, StackMenu):
        self.thisown = 0
        ##########
        global _DATA, PRE_DATA, DATA
        _DATA = {
            "ReshadeFX": ["Enabled", "Disabled"],
            "Texture": ["Original", "2K"],
            "CharTexture": ["2K", "2K Hybrid", "2K Original"],
            "HUD": ["Original", "Updated"],
            "GamePlay Enhancements": ["OFF", "ON"],
        }
        DATA = {}
        execfile(SETTINGS_PATH, globals())
        PRE_DATA = BCopy.deepcopy(DATA)
        ##########

        if Parent:
            BUIx.B_RectWidget.__init__(self, Parent, MenuDescr["Name"], 1, 1)

    def FinalRelease(self):
        BUIx.B_RectWidget.FinalRelease(self)

    def AcceptsFocus(self):
        return 0


########################
init(None, None, None)
if not PRE_DATA["Installed"]:
    Install()
else:
    if PRE_DATA["ReshadeFX"] == "Enabled" and os.path.exists("../../bin/bin/dxgi.dll"):
        Bladex.SetAfterFrameFunc("CheckCurrentMap", CheckCurrentMap)
#

ModMenu = [
    {"Name": "init", "Kind": init},
    {
        "Name": "MENU_LOGO",
        "Kind": M_B_LogoWidget,
        "VSep": 10,  # 0
        "LogoFile": MENU_LOGO_FILE,
        "Scale": 0.45,
    },
    {
        "Name": MenuText.GetMenuText("Version 1.0"),
        # "VSep": 10,
        "Font": MenuFontMed,
        "Scale": 0.4,
        "Kind": MenuWidget.B_MenuItemTextNoFXNoFocus,
    },
    {
        "Name": MenuText.GetMenuText("Reshade FX") + ": ",
        "Font": MenuFontMed,
        "Kind": B_MenuItemOption,
        "VSep": 25,
        "Scale": 0.4,
        "Options": _DATA["ReshadeFX"],
        "SelOptionFunc": GetReshadeFX,
        "Command": SetReshadeFX,
        "PostInitCommand": IsFocusableReshadeFX,
    },
    {
        "Name": "LabelReshadeFX",
        "Text": "[Reshade: Uninstalled]",
        "Color": (200, 0, 0),
        "Font": MenuFontSmall,
        "Kind": B_MenuItemLabelNoFXNoFocus,
        "VSep": 0,
        "Scale": 0.3,
        "PostInitCommand": InitLabelReshadeFX,
    },
    {
        "Name": MenuText.GetMenuText("Textures") + ": ",
        "Font": MenuFontBig,
        "Kind": B_MenuItemOption,
        "VSep": 20,
        "Scale": 0.6,
        "Options": _DATA["Texture"],
        "SelOptionFunc": GetTexture,
        "Command2": SetTexture,
    },
    {
        "Name": MenuText.GetMenuText("character textures") + ": ",
        "Font": MenuFontMed,
        "Kind": B_MenuItemOption,
        # "VSep": 15,
        "Scale": 0.4,
        "Options": _DATA["CharTexture"],
        "SelOptionFunc": GetCharTexture,
        "Command": SetCharTexture,
        "PostInitCommand": IsFocusableCharTexture,
    },
    {
        "Name": MenuText.GetMenuText("HUD") + ": ",
        "Font": MenuFontMed,
        "Kind": B_MenuItemOption,
        "VSep": 20,
        "Scale": 0.4,
        "Options": _DATA["HUD"],
        "SelOptionFunc": GetHUD,
        "Command": SetHUD,
    },
    {
        "Name": MenuText.GetMenuText("GamePlay enhancements") + ": ",
        "Font": MenuFontMed,
        "Kind": B_MenuItemOption,
        "VSep": 20,
        "Scale": 0.4,
        "Options": _DATA["GamePlay Enhancements"],
        "SelOptionFunc": GetGamePlayEnhancements,
        "Command": SetGamePlayEnhancements,
    },
    {
        "Name": MenuText.GetMenuText("Apply"),
        "Kind": B_MenuItemTextNoFX,
        "VSep": 45,  # 20
        "Command_Force": ApplyCMD,
        "Focusable": 0,
        "ListDescr": [
            {
                "Name": "LabelApply1",
                "Text": MenuText.GetMenuText("Apply Successfully!\n"),
                "VSep": 120,
                "Font": MenuFontMed,
                "Scale": 0.45,
                "Kind": B_MenuItemLabelNoFXNoFocus,
            },
            {
                "Name": "LabelApply2",
                "Text": MenuText.GetMenuText(
                    "ReshadeFX changes require restarting the game\n"
                    "Other changes require restarting the level or reloading the save\n"
                ),
                "VSep": 1,
                "Font": MenuFontMed,
                "Scale": 0.45,
                "Color": (207, 144, 49),
                "Alpha": 0.5,
                "Kind": B_MenuItemLabelNoFXNoFocus,
            },
            {
                "Name": MenuText.GetMenuText("Restart Game"),
                "VSep": 20,
                "Font": MenuFontMed,
                "Scale": 0.4,
                "Kind": B_MenuItemTextNoFX,
                "Command": RestartGame,
                "PostInitCommand": InitRestartGame,
            },
            {
                "Name": MenuText.GetMenuText("No"),
                "VSep": 5,
                "Font": MenuFontMed,
                "Scale": 0.4,
                "Command": Menu.BackMenu,
            },
            {"Name": "Back", "Kind": MenuWidget.B_BackBlank},
        ],
    },
    {
        "Name": MenuText.GetMenuText("BACK"),
        "VSep": 15,
        "Command": Menu.BackMenu,
    },
    {"Name": "Back", "Kind": MenuWidget.B_BackBlank},
]
