from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QLineEdit, QPushButton, QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSignal, QRegularExpression
from PyQt5.QtGui import QRegularExpressionValidator

class Ui_opchange__Form(object):
    def setupUi(self, opchange__Form):
        opchange__Form.setObjectName("opchange__Form")
        opchange__Form.resize(318, 118)
        font = QtGui.QFont()
        font.setFamily("阿里巴巴普惠体 2.0 55 Regular")
        font.setPointSize(13)
        opchange__Form.setFont(font)
        self.changeop_callsign = QtWidgets.QLineEdit(opchange__Form)
        self.changeop_callsign.setGeometry(QtCore.QRect(146, 17, 160, 30))
        self.changeop_callsign.setObjectName("changeop_callsign")
        self.label = QtWidgets.QLabel(opchange__Form)
        self.label.setGeometry(QtCore.QRect(10, 20, 140, 31))
        font = QtGui.QFont()
        font.setFamily("阿里巴巴普惠体 2.0 55 Regular")
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.changeop_ok_Button = QtWidgets.QPushButton(opchange__Form)
        self.changeop_ok_Button.setGeometry(QtCore.QRect(110, 80, 90, 30))
        font = QtGui.QFont()
        font.setFamily("阿里巴巴普惠体 2.0 55 Regular")
        font.setPointSize(13)
        self.changeop_ok_Button.setFont(font)
        self.changeop_ok_Button.setObjectName("changeop_ok_Button")
        self.changeop_redme_label = QtWidgets.QLabel(opchange__Form)
        self.changeop_redme_label.setGeometry(QtCore.QRect(10, 50, 301, 30))
        font = QtGui.QFont()
        font.setFamily("阿里巴巴普惠体 2.0 45 Light")
        font.setPointSize(9)
        self.changeop_redme_label.setFont(font)
        self.changeop_redme_label.setAlignment(QtCore.Qt.AlignCenter)
        self.changeop_redme_label.setWordWrap(False)
        self.changeop_redme_label.setObjectName("changeop_redme_label")

        self.retranslateUi(opchange__Form)
        QtCore.QMetaObject.connectSlotsByName(opchange__Form)

    def retranslateUi(self, opchange__Form):
        _translate = QtCore.QCoreApplication.translate
        opchange__Form.setWindowTitle(_translate("opchange__Form", "变更操作员"))
        self.changeop_callsign.setPlaceholderText(_translate("opchange__Form", "请输入操作员呼号"))
        self.label.setText(_translate("opchange__Form", "操作员（OP）："))
        self.changeop_ok_Button.setText(_translate("opchange__Form", "确认变更"))
        self.changeop_redme_label.setText(_translate("opchange__Form", "呼号不分大小写，可以输入BG8LAK或B1/BG8LAK）"))

class ChangeOpWindow(QMainWindow, Ui_opchange__Form):
    operator_changed_signal = pyqtSignal(str) #  新增信号，用于通知操作员变更

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # 设置最大字符数限制为8（不包括斜杠）
        self.changeop_callsign.setMaxLength(9)  # 考虑到可能会有一个斜杠，所以这里设为9

        # 设置验证器，只允许输入字母、数字和至多一个斜杠
        regex = QRegularExpression(r'^[A-Za-z0-9]*/?[A-Za-z0-9]*$')  # 正则表达式匹配一个可选的斜杠，两侧是字母或数字
        validator = QRegularExpressionValidator(regex, self.changeop_callsign)
        self.changeop_callsign.setValidator(validator)

        # 文本改变事件，将字母转为大写（此处仅在提交时转为大写，以便用户能看见小写输入）
        self.changeop_ok_Button.clicked.connect(self.update_and_emit_operator)

    def update_and_emit_operator(self):
        # 先将输入转换为大写，同时去掉两端的空格
        new_callsign = self.changeop_callsign.text().strip().upper()
        # 检查是否包含至多一个斜杠，且除了斜杠外其余部分都是字母和数字
        parts = new_callsign.split('/')
        if len(parts) <= 2 and all(part.isalnum() for part in parts):
            self.operator_changed_signal.emit(new_callsign)
            self.close() 

        new_callsign = self.changeop_callsign.text()
        if new_callsign:
            self.operator_changed_signal.emit(new_callsign)  # 发射信号
            self.close()