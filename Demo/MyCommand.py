import FreeCAD, FreeCADGui
import FreeCAD
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QDialog,QMdiArea,QMdiSubWindow
import MyCreateBlock
from PySide6 import QtWidgets


class MyCommand4Part:
    def GetResources(self):
        return {'Pixmap': 'Draft_2DShapeView', 'MenuText': '创建块', 'ToolTip': '输入参数,创建块'}

    def Activated(self): #点击按钮执行的动作
        """Do something here"""
        toplevel = QtWidgets.QApplication.topLevelWidgets()
        for i in toplevel:
            if i.metaObject().className() == "Gui::MainWindow":
                ui = MyCreateBlock.Ui_MainWindow()
                my_mw = QtWidgets.QMainWindow(i)
                ui.setupUi(my_mw)
                my_mw.show()
                return None
        raise Exception("No main window found")

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return True
FreeCADGui.addCommand('MyCommand4Part', MyCommand4Part())
