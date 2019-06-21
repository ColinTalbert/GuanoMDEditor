# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'key_value.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(459, 22)
        Form.setStyleSheet("QFrame:Hover {\n"
"    background-color:rgb(224,232,245);\n"
"}\n"
"")
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(3, 0, 3, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.key_label = QtWidgets.QLabel(self.frame)
        self.key_label.setMinimumSize(QtCore.QSize(150, 0))
        self.key_label.setObjectName("key_label")
        self.horizontalLayout.addWidget(self.key_label)
        self.value_edit = QtWidgets.QLineEdit(self.frame)
        self.value_edit.setStyleSheet("")
        self.value_edit.setFrame(False)
        self.value_edit.setClearButtonEnabled(False)
        self.value_edit.setObjectName("value_edit")
        self.horizontalLayout.addWidget(self.value_edit)
        self.verticalLayout.addWidget(self.frame)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.key_label.setToolTip(_translate("Form", "test"))
        self.key_label.setText(_translate("Form", "TextLabel"))

