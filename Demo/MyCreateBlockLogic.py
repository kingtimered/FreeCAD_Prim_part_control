# -*- coding: utf-8 -*-
# MyCreateBlockLogic.py
# 逻辑分离：用于增强MyCreateBlock.py的UI逻辑，支持Box的创建与旋转

import FreeCAD, FreeCADGui
from PySide6.QtCore import QObject
from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Qt

class BoxController(QObject):
    def __init__(self, ui, mainwindow):
        super().__init__()
        self.ui = ui
        self.mainwindow = mainwindow
        self.box_obj = None
        self.doc = FreeCAD.ActiveDocument
        self._connect_signals()
        self._reset_sliders()
        self._rot_x = 0
        self._rot_y = 0
        self._rot_z = 0

    def _connect_signals(self):
        self.ui.pushButton.clicked.connect(self.create_box)
        self.ui.horizontalSlider.valueChanged.connect(self.rotate_z)
        self.ui.horizontalSlider_2.valueChanged.connect(self.rotate_x)
        self.ui.horizontalSlider_3.valueChanged.connect(self.rotate_y)

    def _reset_sliders(self):
        self.ui.horizontalSlider.setValue(0)
        self.ui.horizontalSlider_2.setValue(0)
        self.ui.horizontalSlider_3.setValue(0)

    def create_box(self):
        # 获取输入
        try:
            length = float(self.ui.lineEdit.text())
            width = float(self.ui.lineEdit_2.text())
            height = float(self.ui.lineEdit_3.text())
        except Exception:
            FreeCAD.Console.PrintError("参数输入有误\n")
            return
        # 创建Box
        self.doc = FreeCAD.ActiveDocument
        if not self.doc:
            self.doc = FreeCAD.newDocument()
        box = self.doc.addObject("Part::Box", "Box")
        # 目前操作对象不能更改，只能操作新创建的BOX 
        box.Length = length
        box.Width = width
        box.Height = height
        self.doc.recompute()
        FreeCADGui.ActiveDocument.ActiveView.fitAll()
        self.box_obj = box
        self._reset_sliders()
        self._rot_x = 0
        self._rot_y = 0
        self._rot_z = 0

    def _update_box_rotation(self):
        if not self.box_obj:
            return
        from FreeCAD import Rotation, Vector
        rot = Rotation(Vector(1,0,0), self._rot_x)
        rot = rot.multiply(Rotation(Vector(0,1,0), self._rot_y))
        rot = rot.multiply(Rotation(Vector(0,0,1), self._rot_z))
        self.box_obj.Placement.Rotation = rot
        self.doc.recompute()
        FreeCADGui.ActiveDocument.ActiveView.update()

    def rotate_x(self, value):
        self._rot_x = value
        self._update_box_rotation()

    def rotate_y(self, value):
        self._rot_y = value
        self._update_box_rotation()

    def rotate_z(self, value):
        self._rot_z = value
        self._update_box_rotation()
