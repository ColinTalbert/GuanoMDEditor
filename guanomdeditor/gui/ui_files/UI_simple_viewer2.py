# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SimpleViewer2.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(937, 645)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(10, -1, -1, -1)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.file_name = QtWidgets.QLineEdit(Form)
        self.file_name.setObjectName("file_name")
        self.horizontalLayout.addWidget(self.file_name)
        self.btn_browse = QtWidgets.QPushButton(Form)
        self.btn_browse.setObjectName("btn_browse")
        self.horizontalLayout.addWidget(self.btn_browse)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.scrollArea = QtWidgets.QScrollArea(Form)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 917, 563))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.header_layout = QtWidgets.QHBoxLayout()
        self.header_layout.setObjectName("header_layout")
        self.label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_2.setObjectName("label_2")
        self.header_layout.addWidget(self.label_2)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.header_layout.addItem(spacerItem)
        self.lbl_namespaces = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_namespaces.sizePolicy().hasHeightForWidth())
        self.lbl_namespaces.setSizePolicy(sizePolicy)
        self.lbl_namespaces.setObjectName("lbl_namespaces")
        self.header_layout.addWidget(self.lbl_namespaces)
        self.verticalLayout.addLayout(self.header_layout)
        self.namespace_list = QtWidgets.QScrollArea(self.scrollAreaWidgetContents)
        self.namespace_list.setWidgetResizable(True)
        self.namespace_list.setObjectName("namespace_list")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 897, 515))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        spacerItem1 = QtWidgets.QSpacerItem(20, 494, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.namespace_list.setWidget(self.scrollAreaWidgetContents_2)
        self.verticalLayout.addWidget(self.namespace_list)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_2.addWidget(self.scrollArea)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.btn_save = QtWidgets.QPushButton(Form)
        self.btn_save.setObjectName("btn_save")
        self.horizontalLayout_2.addWidget(self.btn_save)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "File:"))
        self.btn_browse.setText(_translate("Form", "browse"))
        self.label_2.setText(_translate("Form", "Guano Metadata:"))
        self.lbl_namespaces.setText(_translate("Form", "Namespaces:"))
        self.btn_save.setText(_translate("Form", "Save"))

