# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FileRenamer.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1093, 465)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.d_browse_frame = QtWidgets.QFrame(Form)
        self.d_browse_frame.setObjectName("d_browse_frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.d_browse_frame)
        self.horizontalLayout.setContentsMargins(10, -1, -1, -1)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.d_browse_frame)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.directory_name = QtWidgets.QLineEdit(self.d_browse_frame)
        self.directory_name.setObjectName("directory_name")
        self.horizontalLayout.addWidget(self.directory_name)
        self.btn_browse = QtWidgets.QPushButton(self.d_browse_frame)
        self.btn_browse.setObjectName("btn_browse")
        self.horizontalLayout.addWidget(self.btn_browse)
        self.verticalLayout_3.addWidget(self.d_browse_frame)
        self.chk_auto_rename = QtWidgets.QCheckBox(Form)
        self.chk_auto_rename.setObjectName("chk_auto_rename")
        self.verticalLayout_3.addWidget(self.chk_auto_rename)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.chk_replace = QtWidgets.QCheckBox(Form)
        self.chk_replace.setObjectName("chk_replace")
        self.horizontalLayout_2.addWidget(self.chk_replace)
        self.replace_from = QtWidgets.QLineEdit(Form)
        self.replace_from.setObjectName("replace_from")
        self.horizontalLayout_2.addWidget(self.replace_from)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.replace_to = QtWidgets.QLineEdit(Form)
        self.replace_to.setObjectName("replace_to")
        self.horizontalLayout_2.addWidget(self.replace_to)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.treeview_original = QtWidgets.QTreeView(self.groupBox)
        self.treeview_original.setObjectName("treeview_original")
        self.verticalLayout.addWidget(self.treeview_original)
        self.horizontalLayout_3.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.treeview_changed = QtWidgets.QTreeView(self.groupBox_2)
        self.treeview_changed.setObjectName("treeview_changed")
        self.verticalLayout_2.addWidget(self.treeview_changed)
        self.horizontalLayout_3.addWidget(self.groupBox_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.progressBar = QtWidgets.QProgressBar(Form)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout_4.addWidget(self.progressBar)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.btn_save = QtWidgets.QPushButton(Form)
        self.btn_save.setObjectName("btn_save")
        self.horizontalLayout_4.addWidget(self.btn_save)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Root Directory:"))
        self.btn_browse.setText(_translate("Form", "browse"))
        self.chk_auto_rename.setText(_translate("Form", "NABat Auto Correct"))
        self.chk_replace.setText(_translate("Form", "Replace"))
        self.label_2.setText(_translate("Form", "with"))
        self.groupBox.setTitle(_translate("Form", "Original"))
        self.groupBox_2.setTitle(_translate("Form", "Renamed"))
        self.btn_save.setText(_translate("Form", "Rename Files"))
