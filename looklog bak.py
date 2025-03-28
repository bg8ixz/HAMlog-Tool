# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'looklog.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import os
import sqlite3
from datetime import datetime, timedelta
from PyQt5.QtCore import Qt, QTimer, QDate, QTime, QDateTime, QLocale, QRegExp
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QMainWindow, QMessageBox, QFileDialog, QStyledItemDelegate, QRadioButton, QTableView
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QValidator

class Ui_looklog_Form(object):
    def setupUi(self, looklog_Form):
        looklog_Form.setObjectName("looklog_Form")
        looklog_Form.resize(1298, 538)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(10)
        looklog_Form.setFont(font)
        self.suoyoulog_tableView = QtWidgets.QTableView(looklog_Form)
        self.suoyoulog_tableView.setGeometry(QtCore.QRect(20, 100, 1261, 421))
        self.suoyoulog_tableView.setObjectName("suoyoulog_tableView")
        self.groupBox = QtWidgets.QGroupBox(looklog_Form)
        self.groupBox.setGeometry(QtCore.QRect(20, 10, 451, 80))
        self.groupBox.setObjectName("groupBox")
        self.today_xuanze_Button = QtWidgets.QRadioButton(self.groupBox)
        self.today_xuanze_Button.setGeometry(QtCore.QRect(75, 20, 65, 16))
        self.today_xuanze_Button.setObjectName("today_xuanze_Button")
        self.day3_xuanze_Button = QtWidgets.QRadioButton(self.groupBox)
        self.day3_xuanze_Button.setGeometry(QtCore.QRect(140, 20, 65, 16))
        self.day3_xuanze_Button.setObjectName("day3_xuanze_Button")
        self.day7_xuanze_Button = QtWidgets.QRadioButton(self.groupBox)
        self.day7_xuanze_Button.setGeometry(QtCore.QRect(210, 20, 65, 16))
        self.day7_xuanze_Button.setObjectName("day7_xuanze_Button")
        self.day30_xuanze_Button = QtWidgets.QRadioButton(self.groupBox)
        self.day30_xuanze_Button.setGeometry(QtCore.QRect(282, 20, 65, 16))
        self.day30_xuanze_Button.setObjectName("day30_xuanze_Button")
        self.zidingyi_xuanze_Button = QtWidgets.QRadioButton(self.groupBox)
        self.zidingyi_xuanze_Button.setGeometry(QtCore.QRect(10, 52, 70, 16))
        self.zidingyi_xuanze_Button.setObjectName("zidingyi_xuanze_Button")
        self.kaishi_dateTimeEdit = QtWidgets.QDateTimeEdit(self.groupBox)
        self.kaishi_dateTimeEdit.setGeometry(QtCore.QRect(80, 46, 160, 22))
        self.kaishi_dateTimeEdit.setCalendarPopup(True)
        self.kaishi_dateTimeEdit.setTimeSpec(QtCore.Qt.LocalTime)
        self.kaishi_dateTimeEdit.setObjectName("kaishi_dateTimeEdit")
        self.lianjiefu_label = QtWidgets.QLabel(self.groupBox)
        self.lianjiefu_label.setGeometry(QtCore.QRect(246, 42, 16, 30))
        self.lianjiefu_label.setObjectName("lianjiefu_label")
        self.jiezhi_dateTimeEdit = QtWidgets.QDateTimeEdit(self.groupBox)
        self.jiezhi_dateTimeEdit.setGeometry(QtCore.QRect(260, 46, 160, 22))
        self.jiezhi_dateTimeEdit.setCalendarPopup(True)
        self.jiezhi_dateTimeEdit.setTimeSpec(QtCore.Qt.LocalTime)
        self.jiezhi_dateTimeEdit.setObjectName("jiezhi_dateTimeEdit")
        self.day90_xuanze_Button = QtWidgets.QRadioButton(self.groupBox)
        self.day90_xuanze_Button.setGeometry(QtCore.QRect(360, 20, 65, 16))
        self.day90_xuanze_Button.setObjectName("day90_xuanze_Button")
        self.all_xuanze_Button = QtWidgets.QRadioButton(self.groupBox)
        self.all_xuanze_Button.setGeometry(QtCore.QRect(10, 20, 51, 16))
        self.all_xuanze_Button.setObjectName("all_xuanze_Button")
        self.groupBox_2 = QtWidgets.QGroupBox(looklog_Form)
        self.groupBox_2.setGeometry(QtCore.QRect(970, 10, 191, 80))
        self.groupBox_2.setObjectName("groupBox_2")
        self.clearlog_pushButton = QtWidgets.QPushButton(self.groupBox_2)
        self.clearlog_pushButton.setGeometry(QtCore.QRect(15, 29, 75, 30))
        self.clearlog_pushButton.setObjectName("clearlog_pushButton")
        self.tolog_pushButton = QtWidgets.QPushButton(self.groupBox_2)
        self.tolog_pushButton.setGeometry(QtCore.QRect(103, 29, 75, 30))
        self.tolog_pushButton.setObjectName("tolog_pushButton")
        self.groupBox_3 = QtWidgets.QGroupBox(looklog_Form)
        self.groupBox_3.setGeometry(QtCore.QRect(480, 10, 261, 80))
        self.groupBox_3.setObjectName("groupBox_3")
        self.label_2 = QtWidgets.QLabel(self.groupBox_3)
        self.label_2.setGeometry(QtCore.QRect(10, 40, 81, 30))
        self.label_2.setObjectName("label_2")
        self.hejitonglian_label = QtWidgets.QLabel(self.groupBox_3)
        self.hejitonglian_label.setGeometry(QtCore.QRect(92, 27, 91, 41))
        font = QtGui.QFont()
        font.setPointSize(28)
        self.hejitonglian_label.setFont(font)
        self.hejitonglian_label.setAlignment(QtCore.Qt.AlignCenter)
        self.hejitonglian_label.setObjectName("hejitonglian_label")
        self.label_3 = QtWidgets.QLabel(self.groupBox_3)
        self.label_3.setGeometry(QtCore.QRect(190, 40, 54, 30))
        self.label_3.setObjectName("label_3")
        self.groupBox_4 = QtWidgets.QGroupBox(looklog_Form)
        self.groupBox_4.setGeometry(QtCore.QRect(750, 10, 211, 80))
        self.groupBox_4.setObjectName("groupBox_4")
        self.search_callsign_lineEdit = QtWidgets.QLineEdit(self.groupBox_4)
        self.search_callsign_lineEdit.setGeometry(QtCore.QRect(80, 20, 121, 22))
        self.search_callsign_lineEdit.setObjectName("search_callsign_lineEdit")
        self.label_4 = QtWidgets.QLabel(self.groupBox_4)
        self.label_4.setGeometry(QtCore.QRect(10, 20, 61, 30))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.groupBox_4)
        self.label_5.setGeometry(QtCore.QRect(30, 50, 61, 30))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.groupBox_4)
        self.label_6.setGeometry(QtCore.QRect(160, 50, 31, 30))
        self.label_6.setObjectName("label_6")
        self.hejitonglian_label_2 = QtWidgets.QLabel(self.groupBox_4)
        self.hejitonglian_label_2.setGeometry(QtCore.QRect(95, 46, 60, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.hejitonglian_label_2.setFont(font)
        self.hejitonglian_label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.hejitonglian_label_2.setObjectName("zonggongtonglian_label")

        self.retranslateUi(looklog_Form)
        QtCore.QMetaObject.connectSlotsByName(looklog_Form)

    def retranslateUi(self, looklog_Form):
        _translate = QtCore.QCoreApplication.translate
        looklog_Form.setWindowTitle(_translate("looklog_Form", "通联日志记录"))
        self.groupBox.setTitle(_translate("looklog_Form", "时间范围"))
        self.today_xuanze_Button.setText(_translate("looklog_Form", "今天"))
        self.day3_xuanze_Button.setText(_translate("looklog_Form", "近3天"))
        self.day7_xuanze_Button.setText(_translate("looklog_Form", "近7天"))
        self.day30_xuanze_Button.setText(_translate("looklog_Form", "近30天"))
        self.zidingyi_xuanze_Button.setText(_translate("looklog_Form", "自定义"))
        self.kaishi_dateTimeEdit.setDisplayFormat(_translate("looklog_Form", "yyyy-M-d HH:mm:ss"))
        self.lianjiefu_label.setText(_translate("looklog_Form", "-"))
        self.jiezhi_dateTimeEdit.setDisplayFormat(_translate("looklog_Form", "yyyy-M-d HH:mm:ss"))
        self.day90_xuanze_Button.setText(_translate("looklog_Form", "近90天"))
        self.all_xuanze_Button.setText(_translate("looklog_Form", "全部"))
        self.groupBox_2.setTitle(_translate("looklog_Form", "控制台"))
        self.clearlog_pushButton.setText(_translate("looklog_Form", "清空日志"))
        self.tolog_pushButton.setText(_translate("looklog_Form", "导出日志"))
        self.groupBox_3.setTitle(_translate("looklog_Form", "统计信息"))
        self.label_2.setText(_translate("looklog_Form", "已累计通联："))
        self.hejitonglian_label.setText(_translate("looklog_Form", "0"))
        self.label_3.setText(_translate("looklog_Form", "位友台"))
        self.groupBox_4.setTitle(_translate("looklog_Form", "通联查询"))
        self.search_callsign_lineEdit.setPlaceholderText(_translate("looklog_Form", "输入要查询的呼号"))
        self.label_4.setText(_translate("looklog_Form", "查询呼号："))
        self.label_5.setText(_translate("looklog_Form", "总计通联："))
        self.label_6.setText(_translate("looklog_Form", "次"))
        self.hejitonglian_label_2.setText(_translate("looklog_Form", "0"))

class DateRangeValidator(QValidator):
    def __init__(self, max_date):
        super().__init__()
        self.max_date = max_date

    def validate(self, input_str, pos):
        try:
            date_time = QDateTime.fromString(input_str, "yyyy-MM-dd HH-mm-ss")
            if date_time.isValid() and date_time <= self.max_date:
                return QValidator.Acceptable, pos
            else:
                return QValidator.Intermediate, pos
        except ValueError:
            return QValidator.Invalid, pos

    def fixup(self, input_str):
        pass

class CenterAlignedItemDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        option.displayAlignment = Qt.AlignCenter

class LooklogWindow(QMainWindow):
    def __init__(self):
        super(LooklogWindow, self).__init__()
        self.ui = Ui_looklog_Form()
        self.ui.setupUi(self)
        # 可能的其他初始化代码...
# ------------------------------------------------------------------------- 连接到数据库
        # 获取当前程序路径（推荐使用os.path.abspath(__file__)）
        script_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(script_dir, 'rx_log.db')

        # 连接到SQLite数据库
        self.conn = sqlite3.connect(db_path)  # 使用获取到的数据库路径

        # 获取游标对象
        self.cursor = self.conn.cursor()
# -------------------------------------------------------------------自定义时间范围开始
        # 初始化时禁用自定义日期时间范围的编辑器
        self.ui.kaishi_dateTimeEdit.setReadOnly(True)
        self.ui.jiezhi_dateTimeEdit.setReadOnly(True)
        # 初始化时设置自定义日期时间范围的编辑器文字为灰色
        self.ui.kaishi_dateTimeEdit.setStyleSheet("color: gray;")
        self.ui.jiezhi_dateTimeEdit.setStyleSheet("color: gray;")

        # 设置自定义日期时间范围的编辑器显示格式
        display_format = "yyyy-MM-dd HH:mm:ss"
        self.ui.kaishi_dateTimeEdit.setDisplayFormat(display_format)  # 设置开始日期时间编辑器的显示格式
        self.ui.jiezhi_dateTimeEdit.setDisplayFormat(display_format)  # 设置结束日期时间编辑器的显示格式

        # 设置自定义日期时间范围的编辑器默认显示今天的日期
        today = datetime.now()
        # today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)  # 获取当前日期，时分秒设为0
        # self.ui.kaishi_dateTimeEdit.setDateTime(today)  # 设置开始日期时间编辑器的日期时间为今天
        self.ui.kaishi_dateTimeEdit.setDateTime(today.replace(hour=0, minute=0, second=0, microsecond=0))  # 设置开始日期时间编辑器为今天凌晨
        self.ui.jiezhi_dateTimeEdit.setDateTime(today)  # 设置结束日期时间编辑器的日期时间为今天

        # 设置自定义日期时间范围的编辑器禁止选择今天之后的日期
        self.ui.kaishi_dateTimeEdit.setMaximumDateTime(today)  # 设置最大可选日期为今天
        self.ui.jiezhi_dateTimeEdit.setMaximumDateTime(today)

        # 为自定义时间范围按钮的切换状态连接处理槽
        self.ui.zidingyi_xuanze_Button.toggled.connect(self.toggle_custom_date_time_editors)
# -------------------------------------------------------------------自定义时间范围结束
        

# --------------------------------------------------------------------按钮显示日志功能开始

        # 关联QRadioButton的toggled信号到处理函数
        self.ui.all_xuanze_Button.toggled.connect(self.handle_time_range_selection)
        self.ui.today_xuanze_Button.toggled.connect(self.handle_time_range_selection)
        self.ui.day3_xuanze_Button.toggled.connect(self.handle_time_range_selection)
        self.ui.day7_xuanze_Button.toggled.connect(self.handle_time_range_selection)
        self.ui.day30_xuanze_Button.toggled.connect(self.handle_time_range_selection)
        self.ui.day90_xuanze_Button.toggled.connect(self.handle_time_range_selection)
        self.ui.zidingyi_xuanze_Button.toggled.connect(self.handle_time_range_selection)

        # 默认选中all_xuanze_Button 这一行不注释掉打不开窗口
        # self.ui.all_xuanze_Button.setChecked(True)

# --------------------------------------------------------------------实现按钮选择显示功能结束


        # 查询数据库表rx_log的实际列名
        self.cursor.execute("PRAGMA table_info(rx_log)")
        self.columns = [row[1] for row in self.cursor.fetchall()]

        # 初始化数据模型(为了后面绑定表头)
        model = QStandardItemModel()
        # 定义期望的表头映射
        header_mapping = {
            'date': '日期',
            'time': '时间',
            'sn': '通联序号',
            'rx_callsign': '呼号',
            'rx_signal': '对方信号',
            'tx_signal': '我方信号',
            'qth': 'QTH',
            'rig': '使用设备',
            'power': '功率',
            'for_info': '通联方式(频率)',
            'op': '操作员',
        }

        # 根据实际列名和映射关系生成新的表头
        new_header_labels = [header_mapping.get(col, col) for col in self.columns]
        model.setHorizontalHeaderLabels(new_header_labels)

        # 将数据模型绑定到表格视图
        self.ui.suoyoulog_tableView.setModel(model)

        # 查询所有日志数据 （与下面一个重复 但是这个没有按最新的排序）
        # self.cursor.execute(f"SELECT {','.join(columns)} FROM rx_log")
        # rows = self.cursor.fetchall()

        # 查询所有日志数据，按date_time字段降序排序
        self.cursor.execute(f"SELECT {','.join(self.columns)} FROM rx_log ORDER BY date_time DESC")
        rows = self.cursor.fetchall()

        # 创建新的QStandardItemModel，用于填充表格视图
        model = QStandardItemModel(self.ui.suoyoulog_tableView)

        # 设置新的表头
        model.setHorizontalHeaderLabels(new_header_labels)

        # 将查询结果转换为模型项并添加到模型中
        for row in rows:
            items = [QtGui.QStandardItem(str(v)) for v in row]
            model.appendRow(items)

        # 设置表格视图的模型
        self.ui.suoyoulog_tableView.setModel(model)

        # 隐藏指定列
        hidden_columns = [self.columns.index('id'), self.columns.index('date_time')]  # 需要隐藏的列索引（对应id和date_time列）
        for column_index in hidden_columns:
            self.ui.suoyoulog_tableView.setColumnHidden(column_index, True)

        # 设置表格视图的列宽自适应
        self.ui.suoyoulog_tableView.resizeColumnsToContents()

        # 调整列宽，使每列比自适应宽度大5像素
        for column in range(model.columnCount()):
            width = self.ui.suoyoulog_tableView.columnWidth(column) + 20
            self.ui.suoyoulog_tableView.setColumnWidth(column, width)

        # 创建一个居中对齐的代理
        # center_delegate = QStyledItemDelegate()
        # center_delegate.setAlignment(Qt.AlignCenter)
        center_delegate = CenterAlignedItemDelegate()

        # 为表格视图中的所有列设置居中对齐的代理
        for column in range(model.columnCount()):
            self.ui.suoyoulog_tableView.setItemDelegateForColumn(column, center_delegate)

        # ----------------------------------------------下面是统计功能-----------------------------
        # 统计rx_callsign非空的记录数量
        self.cursor.execute("SELECT COUNT(*) FROM rx_log WHERE rx_callsign IS NOT NULL")
        total_callsigns = self.cursor.fetchone()[0]  # 获取计数结果

        # 设置hejitonglian_label的文本为统计结果
        self.ui.hejitonglian_label.setText(f"{total_callsigns}")


        #------------------------定时更新开始
        # 创建定时器，每隔5秒查询一次数据库
        self.is_manual_time_range_selected = False  # 用于标记是否用户手动选择了时间范围
        self.refresh_timer = QTimer(self)
        self.refresh_timer.setInterval(5000)
        self.refresh_timer.timeout.connect(self.update_data_and_stats)
        self.refresh_timer.start()
        #------------------------------定时更新结束

        # ------------------------------------------------下面不要动------------------锁定窗口---
        # 设置窗口固定大小，不允许调整
        self.setFixedSize(self.size())  # 或者指定固定的宽度和高度，例如：self.setFixedSize(400, 300)

    def update_data_and_stats(self):
        # 查询最新日志数据
        self.cursor.execute(f"SELECT {','.join(self.columns)} FROM rx_log ORDER BY date_time DESC")  # 使用self.columns
        rows = self.cursor.fetchall()

        # 更新表格视图的模型数据
        model = self.ui.suoyoulog_tableView.model()
        model.removeRows(0, model.rowCount())  # 清空现有数据
        for row in rows:
            items = [QtGui.QStandardItem(str(v)) for v in row]
            model.appendRow(items)

        # 更新统计信息
        self.cursor.execute("SELECT COUNT(*) FROM rx_log WHERE rx_callsign IS NOT NULL")
        total_callsigns = self.cursor.fetchone()[0]
        self.ui.hejitonglian_label.setText(f"{total_callsigns}")

    def toggle_custom_date_time_editors(self, checked):
        """
        处理自定义时间范围按钮的切换状态，根据按钮是否被选中，决定日期时间编辑器的可编辑状态。
        """
        editable = checked  # 当按钮被选中时，编辑器应变为可编辑状态

        self.ui.kaishi_dateTimeEdit.setReadOnly(not editable)
        self.ui.jiezhi_dateTimeEdit.setReadOnly(not editable)
        """
        处理自定义时间范围按钮的切换状态，根据按钮是否被选中，决定日期时间编辑器的文本颜色。
        """
        if checked:
            self.ui.kaishi_dateTimeEdit.setStyleSheet("")  # 清除样式表，恢复默认颜色
            self.ui.jiezhi_dateTimeEdit.setStyleSheet("")
        else:
            self.ui.kaishi_dateTimeEdit.setStyleSheet("color: gray;")
            self.ui.jiezhi_dateTimeEdit.setStyleSheet("color: gray;")

#---------------------------------------------------------------------

    def handle_time_range_selection(self):

        current_button = self.sender()

        # 查询数据库表rx_log的实际列名
        self.cursor.execute("PRAGMA table_info(rx_log)")
        self.columns = [row[1] for row in self.cursor.fetchall()]

        # 如果需要更新表头，重新计算new_header_labels并设置
        header_mapping = {
            'date': '日期',
            'time': '时间',
            'sn': '通联序号',
            'rx_callsign': '呼号',
            'rx_signal': '对方信号',
            'tx_signal': '我方信号',
            'qth': 'QTH',
            'rig': '使用设备',
            'power': '功率',
            'for_info': '通联方式(频率)',
            'op': '操作员',
        }
        new_header_labels = [header_mapping.get(col, col) for col in self.columns]

        model = self.ui.suoyoulog_tableView.model()
        model.setHorizontalHeaderLabels(new_header_labels)

        self.is_manual_time_range_selected = True  # 用户手动选择了时间范围
        self.refresh_timer.stop()  # 停止定时器刷新

        if current_button == self.ui.all_xuanze_Button:
            time_condition = ""

        elif current_button == self.ui.today_xuanze_Button:
            today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            time_condition = f"date(date_time) = '{today}'"

        elif current_button == self.ui.day3_xuanze_Button:
            three_days_ago = datetime.now() - timedelta(days=3)
            three_days_ago_str = three_days_ago.strftime('%Y-%m-%d %H:%M:%S')
            today_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            time_condition = f"date(date_time) BETWEEN '{three_days_ago_str}' AND '{today_str}'"

        elif current_button == self.ui.day7_xuanze_Button:
            seven_days_ago = datetime.now() - timedelta(days=7)
            seven_days_ago_str = seven_days_ago.strftime('%Y-%m-%d %H:%M:%S')
            time_condition = f"date(date_time) BETWEEN '{seven_days_ago_str}' AND '{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}'"
        elif current_button == self.ui.day30_xuanze_Button:
            thirty_days_ago = datetime.now() - timedelta(days=30)
            thirty_days_ago_str = thirty_days_ago.strftime('%Y-%m-%d %H:%M:%S')
            time_condition = f"date(date_time) BETWEEN '{thirty_days_ago_str}' AND '{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}'"
        elif current_button == self.ui.day90_xuanze_Button:
            ninety_days_ago = datetime.now() - timedelta(days=90)
            ninety_days_ago_str = ninety_days_ago.strftime('%Y-%m-%d %H:%M:%S')
            time_condition = f"date(date_time) BETWEEN '{ninety_days_ago_str}' AND '{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}'"
        elif current_button == self.ui.zidingyi_xuanze_Button:
            start_date = self.ui.kaishi_dateTimeEdit.dateTime().toPyDateTime().date()
            end_date = self.ui.jiezhi_dateTimeEdit.dateTime().toPyDateTime().date()
            time_condition = f"date(date_time) BETWEEN '{start_date}' AND '{end_date}'"
        else:
            return  # 如果是未处理的按钮，不做任何操作
        
        model = self.ui.suoyoulog_tableView.model()  # 获取表格视图关联的数据模型
        # query = f"SELECT * FROM rx_log WHERE {time_condition}"
        query = f"SELECT * FROM rx_log WHERE {time_condition} ORDER BY date_time DESC"
        # rows = self.execute_query(query)
        rows = self.cursor.execute(query)  # 使用self.cursor而不是self.db_cursor


        # 清空并重新填充表格视图

        # model = self.ui.suoyoulog_tableView.model()
        model.clear()
        for row in rows:
            items = [QStandardItem(str(v)) for v in row]
            model.appendRow(items)

    def execute_query(self, query):
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return rows

#---------------------------------------------------------------------


    def closeEvent(self, event):
        # 在窗口关闭时确保数据库连接关闭
        self.conn.close()
        super().closeEvent(event)


# 确保这个类被正确导出
__all__ = ['LooklogWindow']