# main.py
APP_VERSION = "1.0.0.Alpha"
import os, re, sys, sqlite3, base64
import webbrowser
from datetime import datetime
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QRadioButton,QAction, QLineEdit, QStyledItemDelegate, QListWidget, QTableView, QHeaderView, QLabel, QComboBox, QVBoxLayout, QCompleter, QMessageBox
from PyQt5.QtCore import QByteArray, QTimer, QDateTime, QUrl, QObject, Qt, QVariant, QSignalBlocker, QStringListModel, QSortFilterProxyModel, QRegExp
from PyQt5.QtGui import QDesktopServices, QIcon, QPixmap, QImage, QStandardItem, QStandardItemModel, QRegExpValidator, QIntValidator
from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel, QSqlTableModel, QSqlQuery
# 引入一堆窗口
from rx_log import Ui_rx_log
from rx_log import Rx_logWindow
from changeop import Ui_opchange__Form # 引入opchange.py中的窗口类
from changeop import ChangeOpWindow  # 引入opchange.py中自定义的关于窗口类
from del_log_pwd import Ui_del_pwd_set_Form # 引入opchange.py中的窗口类
from del_log_pwd import DelPwdSetWindow  # 引入opchange.py中自定义的关于窗口类
from about import Ui_about__Form  # 引入about.py中的窗口类
from about import AboutWindow  # 引入about.py中自定义的关于窗口类
from contact import Ui_contact_Form  # 引入contact.py中的窗口类
from contact import ContactWindow  # 引入contact.py中自定义的联系窗口类
from looklog import Ui_looklog_Form  # 引入looklog.py中的窗口类
from looklog import LooklogWindow  # 引入looklog.py中自定义的关于窗口类


# 定义了一个名为RxLogModel的类，它继承自QObject，用于与SQLite数据库交互，特别是查询存储在rx_log.db数据库中的rx_log表中rx_callsign列的数据。
'''说人话就是 查呼号就靠这一段'''
class RxLogModel(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.conn = sqlite3.connect('rx_log.db')
        self.cursor = self.conn.cursor()

    def search_callsign_latest(self, pattern):   # 传入参数有两种prefix（前缀匹配）、pattern（模糊匹配）
        '''     WHERE rx_callsign LIKE '{prefix}%'      # 匹配呼号前缀
                WHERE rx_callsign LIKE '%{pattern}%'    # 模糊匹配呼号
        '''
        query = f"""
            SELECT rx_callsign
            FROM (
                SELECT rx_callsign, 
                       datetime(date || ' ' || time, 'yyyy-MM-dd HH:mm:ss') AS datetime_value
                FROM rx_log
                WHERE rx_callsign LIKE '%{pattern}%'
                ORDER BY datetime_value DESC
            )
            GROUP BY rx_callsign
        """
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        return [item[0] for item in results]    # 返回包含匹配呼号的列表


class CenterAlignedItemDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        option.displayAlignment = Qt.AlignCenter

#时间更新显示
class MainWindow(QMainWindow, Ui_rx_log):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        '''
        current_dir = os.getcwd()   # 获取当前运行目录
        icon_file_path = os.path.join(current_dir, 'favicon.ico')   # 指定图标文件相对于运行目录的相对路径
        app_icon = QIcon(icon_file_path)    # 加载图标
        self.setWindowIcon(app_icon)    # 设置窗口图标
        '''
        # 把ICO转为base64编码的字符串来引入到窗口
        icon_data = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAASwAAAEsCAIAAAD2HxkiAAAACXBIWXMAAAsTAAALEwEAmpwYAAAK+mlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4gPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iQWRvYmUgWE1QIENvcmUgNi4wLWMwMDYgNzkuZGFiYWNiYiwgMjAyMS8wNC8xNC0wMDozOTo0NCAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczpkYz0iaHR0cDovL3B1cmwub3JnL2RjL2VsZW1lbnRzLzEuMS8iIHhtbG5zOnhtcE1NPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvbW0vIiB4bWxuczpzdEV2dD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL3NUeXBlL1Jlc291cmNlRXZlbnQjIiB4bWxuczpzdFJlZj0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL3NUeXBlL1Jlc291cmNlUmVmIyIgeG1sbnM6cGhvdG9zaG9wPSJodHRwOi8vbnMuYWRvYmUuY29tL3Bob3Rvc2hvcC8xLjAvIiB4bWxuczp0aWZmPSJodHRwOi8vbnMuYWRvYmUuY29tL3RpZmYvMS4wLyIgeG1sbnM6ZXhpZj0iaHR0cDovL25zLmFkb2JlLmNvbS9leGlmLzEuMC8iIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIDIyLjQgKFdpbmRvd3MpIiB4bXA6Q3JlYXRlRGF0ZT0iMjAyNC0wNC0wMlQxMjoxNjoxNSswODowMCIgeG1wOk1ldGFkYXRhRGF0ZT0iMjAyNC0wNC0wMlQxMjoyOToyMSswODowMCIgeG1wOk1vZGlmeURhdGU9IjIwMjQtMDQtMDJUMTI6Mjk6MjErMDg6MDAiIGRjOmZvcm1hdD0iaW1hZ2UvcG5nIiB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOjQ3ZjM3Zjc4LTFiODctYmY0OC1iNDdkLWM5NjgzNmQ0OTQ0YSIgeG1wTU06RG9jdW1lbnRJRD0iYWRvYmU6ZG9jaWQ6cGhvdG9zaG9wOjU3ODgwNjA0LTE2OTEtZDg0My05OGU0LTc4MTU4Yjc5MzY0OCIgeG1wTU06T3JpZ2luYWxEb2N1bWVudElEPSJ4bXAuZGlkOjFlYmE2ZWRkLWFlMTYtMDQ0OS05ZWZlLWI2ZDc3NTQzOTVlYyIgcGhvdG9zaG9wOkNvbG9yTW9kZT0iMyIgdGlmZjpPcmllbnRhdGlvbj0iMSIgdGlmZjpYUmVzb2x1dGlvbj0iNzIwMDAwLzEwMDAwIiB0aWZmOllSZXNvbHV0aW9uPSI3MjAwMDAvMTAwMDAiIHRpZmY6UmVzb2x1dGlvblVuaXQ9IjIiIGV4aWY6Q29sb3JTcGFjZT0iNjU1MzUiIGV4aWY6UGl4ZWxYRGltZW5zaW9uPSIzMDAiIGV4aWY6UGl4ZWxZRGltZW5zaW9uPSIzMDAiPiA8eG1wTU06SGlzdG9yeT4gPHJkZjpTZXE+IDxyZGY6bGkgc3RFdnQ6YWN0aW9uPSJjcmVhdGVkIiBzdEV2dDppbnN0YW5jZUlEPSJ4bXAuaWlkOjFlYmE2ZWRkLWFlMTYtMDQ0OS05ZWZlLWI2ZDc3NTQzOTVlYyIgc3RFdnQ6d2hlbj0iMjAyNC0wNC0wMlQxMjoxNjoxNSswODowMCIgc3RFdnQ6c29mdHdhcmVBZ2VudD0iQWRvYmUgUGhvdG9zaG9wIDIyLjQgKFdpbmRvd3MpIi8+IDxyZGY6bGkgc3RFdnQ6YWN0aW9uPSJzYXZlZCIgc3RFdnQ6aW5zdGFuY2VJRD0ieG1wLmlpZDozNDFiZDM5ZC1kNWU3LTYxNGMtYTYxNy01YWZjODVhMDVlMjciIHN0RXZ0OndoZW49IjIwMjQtMDQtMDJUMTI6MjE6MjMrMDg6MDAiIHN0RXZ0OnNvZnR3YXJlQWdlbnQ9IkFkb2JlIFBob3Rvc2hvcCAyMi40IChXaW5kb3dzKSIgc3RFdnQ6Y2hhbmdlZD0iLyIvPiA8cmRmOmxpIHN0RXZ0OmFjdGlvbj0ic2F2ZWQiIHN0RXZ0Omluc3RhbmNlSUQ9InhtcC5paWQ6MmVlNzY2ZTAtOGUzNC01NDQ2LWE0YzgtY2Y2OWRiZjZmMzczIiBzdEV2dDp3aGVuPSIyMDI0LTA0LTAyVDEyOjI5OjIxKzA4OjAwIiBzdEV2dDpzb2Z0d2FyZUFnZW50PSJBZG9iZSBQaG90b3Nob3AgMjIuNCAoV2luZG93cykiIHN0RXZ0OmNoYW5nZWQ9Ii8iLz4gPHJkZjpsaSBzdEV2dDphY3Rpb249ImNvbnZlcnRlZCIgc3RFdnQ6cGFyYW1ldGVycz0iZnJvbSBhcHBsaWNhdGlvbi92bmQuYWRvYmUucGhvdG9zaG9wIHRvIGltYWdlL3BuZyIvPiA8cmRmOmxpIHN0RXZ0OmFjdGlvbj0iZGVyaXZlZCIgc3RFdnQ6cGFyYW1ldGVycz0iY29udmVydGVkIGZyb20gYXBwbGljYXRpb24vdm5kLmFkb2JlLnBob3Rvc2hvcCB0byBpbWFnZS9wbmciLz4gPHJkZjpsaSBzdEV2dDphY3Rpb249InNhdmVkIiBzdEV2dDppbnN0YW5jZUlEPSJ4bXAuaWlkOjQ3ZjM3Zjc4LTFiODctYmY0OC1iNDdkLWM5NjgzNmQ0OTQ0YSIgc3RFdnQ6d2hlbj0iMjAyNC0wNC0wMlQxMjoyOToyMSswODowMCIgc3RFdnQ6c29mdHdhcmVBZ2VudD0iQWRvYmUgUGhvdG9zaG9wIDIyLjQgKFdpbmRvd3MpIiBzdEV2dDpjaGFuZ2VkPSIvIi8+IDwvcmRmOlNlcT4gPC94bXBNTTpIaXN0b3J5PiA8eG1wTU06RGVyaXZlZEZyb20gc3RSZWY6aW5zdGFuY2VJRD0ieG1wLmlpZDoyZWU3NjZlMC04ZTM0LTU0NDYtYTRjOC1jZjY5ZGJmNmYzNzMiIHN0UmVmOmRvY3VtZW50SUQ9ImFkb2JlOmRvY2lkOnBob3Rvc2hvcDo0ZmVmZmIwNS0xMTg1LTBlNGYtYWQxNS0xNmIyZDFiN2NkMTQiIHN0UmVmOm9yaWdpbmFsRG9jdW1lbnRJRD0ieG1wLmRpZDoxZWJhNmVkZC1hZTE2LTA0NDktOWVmZS1iNmQ3NzU0Mzk1ZWMiLz4gPHBob3Rvc2hvcDpUZXh0TGF5ZXJzPiA8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"
        icon_data = icon_data.split(",")[1]     # 移除前缀，得到纯Base64编码数据
        jiema_icon_data = base64.b64decode(icon_data)   # 解码base64字符串为字节数据
        icon = QIcon()      # 使用字节数据创建一个QIcon对象
        icon.addPixmap(QPixmap.fromImage(QImage.fromData(jiema_icon_data)))    #在PyQt5.QtGui引入QPixmap、QImage，PyQt5.QtCore引入QByteArray
        self.setWindowIcon(icon)    # 设置窗口图标
        

        self.db_connection = sqlite3.connect('rx_log.db')   # 假设数据库文件名为database.db
        self.cursor = self.db_connection.cursor()
        self.rx_callsign_new.setVisible(False)  # 设置为不可见
        self.rx_callsign.textChanged.connect(self.handle_rx_callsign_text_changed)  # 信号和槽的连接,选择或取消选择项时，此信号会被发射
        self.callsign_xuanze_listWidget.itemSelectionChanged.connect(self.update_selected_details)

        # 这是一个查询机制，为了在快速选择里面选择呼号
        self.rx_callsign = self.findChild(QLineEdit, 'rx_callsign')  # 获取QLineEdit组件
        self.callsign_xuanze_listWidget = self.findChild(QListWidget, 'callsign_xuanze_listWidget')
        self.model = RxLogModel()   # 调用最前面的模糊匹配呼号
        
        # 创建一个定时器用于延迟执行查询操作
        self.debounce_timer = QTimer()
        self.debounce_timer.setSingleShot(True)  # 设置定时器为单次模式
        self.debounce_timer.timeout.connect(self.update_callsign_list_debounced)  # 当定时器超时时触发更新函数
        
        # 连接文本变化信号到调度更新函数
        self.rx_callsign.textChanged.connect(self.schedule_update)

        # 从数据库获取操作员的内容
        label_2_content = get_config_from_db()
        self.label_2.setText(label_2_content)

        #这是时间实时显示
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # 每秒更新一次
        
        self.op_set_action.triggered.connect(self.open_change_op_window)      #这是更换操作员的设置按钮  
        self.delpwd_action.triggered.connect(self.open_delpwd_window)   #这是更换删除密码的设置按钮

        # 这是点击关于按钮的操作
        self.aubot_action = self.findChild(QAction, 'aubot_action')  # 假设其objectName为'aubot_action'
        assert self.aubot_action is not None, "Failed to find the aubot_action in UI"        
        self.aubot_action.triggered.connect(self.open_about_window) # 连接关于按钮动作到槽函数

        # 这是点击联系按钮的操作
        self.contact_action = self.findChild(QAction, 'contact_action')  # 假设其objectName为'aubot_action'
        assert self.contact_action is not None, "Failed to find the contact_action in UI"   # 添加断言，确保aubot_action在UI中被正确找到
        self.contact_action.triggered.connect(self.open_contact_window)  # 连接联系按钮动作到槽函数

        # 反馈按钮的操作
        self.feedback_action = self.findChild(QAction, 'feedback_action') # 查找名为 feedback_action 的 QAction
        assert self.feedback_action is not None, "Failed to find the feedback_action in UI" # 添加断言，确保feedback_action在UI中被正确找到
        self.feedback_action.triggered.connect(self.open_feedback_page)    # 连接反馈按钮动作到槽函数

        # 创建打开日志Open Log菜单项（假定已在UI设计工具中设置了相应的action）
        self.open_log_action = self.findChild(QAction, "open_log_action")  # 替换为实际对象名
        assert self.open_log_action is not None, "Failed to find the open_log_action in UI" # 添加断言，确保open_log_action在UI中被正确找到
        self.open_log_action.triggered.connect(self.open_log_window)    # 为open_log_action的triggered信号绑定槽函数

        # 连接清空QTH按钮、清空设备按钮的信号与槽
        self.clear_qth_pushButton.clicked.connect(self.on_clear_qth_pushButton_clicked)
        self.clear_rig_pushButton.clicked.connect(self.on_clear_rig_pushButton_clicked)
        self.initial_load = True
        self.qth_comboBox.lineEdit().textChanged.connect(self.update_search_results)  # 监听QTH选择框里面的文本变化事件
        # 设置定时器，每x秒触发一次最近通联数据
        self.refresh_timer = QtCore.QTimer(interval=3000, timeout=self.update_table_view)
        self.refresh_timer.start()  # 启动定时器


    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++在QTH框子加载默认城市开始++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # 初始化QComboBox控件
        #self.qth_comboBox = QComboBox()
        # 使用 findChild 方法找到 rx_log.py 中已有的 QComboBox 实例
        #self.qth_comboBox = self.findChild(QComboBox, 'qth_comboBox')  # 实际 objectName
        #assert self.qth_comboBox is not None, "Failed to find the qth_comboBox in UI" # 判断qth_comboBox是否被找到
        self.populate_city_list()   # 继续对找到的 QComboBox 实例进行操作
        # 初始化表格视图 - 最新通联信息
        self.initialize_table_view()

        #-------------------------------------------------------------------------测试可编辑序号开始
        #限制sn_lineEdit只能输入数字
        sn_lineEdit_reg_exp = QRegExp("[0-9]*")
        sn_lineEdit_validator = QRegExpValidator(sn_lineEdit_reg_exp)
        self.sn_lineEdit.setValidator(sn_lineEdit_validator)
        # 获取QLabel和QLineEdit对象
        self.rx_num_auto = self.rx_num_auto  # 假设rx_num_auto是QLabel对象的objectName
        self.sn_lineEdit = self.sn_lineEdit  # 假设sn_lineEdit是QLineEdit对象的objectName

        # 默认隐藏QLineEdit
        self.sn_lineEdit.setVisible(False)
        # 在构造函数中设置双击事件处理器
        self.rx_num_auto.mouseDoubleClickEvent = self.handle_double_click
        #编辑序号结束
        #下面是来源信息其他 编辑框联动
        # 假设您已加载UI并获得了QLineEdit和QRadioButton实例
        self.other_lineEdit = self.findChild(QLineEdit, 'other_lineEdit')
        self.laiyuan_qita = self.findChild(QRadioButton, 'laiyuan_qita')
        self.other_lineEdit.setDisabled(True) #初始化其他编辑框不允许使用
        # 连接QRadioButton的toggled信号与槽函数
        self.laiyuan_qita.toggled.connect(self.handle_laiyuan_qita_toggled)
        # 上面是来源信息其他 编辑框联动

        #--------------------------------------------------------------------------开始插入新通联数据了
        # 限制rx_callsign只能输入大小写字母、数字和一条斜杠
        rx_callsign_reg_exp = QRegExp("[A-Za-z0-9\/]*")
        rx_callsign_validator = QRegExpValidator(rx_callsign_reg_exp)
        self.rx_callsign.setValidator(rx_callsign_validator)
        # 绑定下一个next_rx_Button的clicked信号到handle_next_rx_button_clicked槽函数
        self.next_rx_Button.clicked.connect(self.handle_next_rx_button_clicked)
        # 获取所有的laiyuan_* RadioButton
        # 为每个RadioButton的toggled信号绑定同一个槽函数
        for radio_button in [self.laiyuan_redian, self.laiyuan_zhongji, self.laiyuan_shouji, self.laiyuan_qita]:
            radio_button.toggled.connect(self.radio_button_toggled)
        self.laiyuan_radio_buttons = self.findChildren(QRadioButton, 'laiyuan_*')
        #self.laiyuan_radio_buttons = self.findChildren(QRadioButton, 'laiyuan_redian')
        #self.laiyuan_radio_buttons = self.findChildren(QRadioButton, 'laiyuan_zhongji')
        #self.laiyuan_radio_buttons = self.findChildren(QRadioButton, 'laiyuan_shouji')
        #self.laiyuan_radio_buttons = self.findChildren(QRadioButton, 'laiyuan_qita')
        # 初始化当前选中的RadioButton为None
        self.currently_selected_radio_button = None
        #---------------------------------------------------下面是自动序号实现开始
        # 获取UI界面上的rx_num_auto控件实例
        self.rx_num_auto = self.findChild(QLabel, 'rx_num_auto')

        # 在适当位置（如程序启动时）执行查询并设置rx_num_auto文本 说人话就是查最新的序号是多少
        self.update_rx_num_auto()
        #---------------------------------------------------上面是自动序号实现结束
        # 为rx_signal_input和tx_signal_input添加QIntValidator，限制输入范围为0到59
        signal_validator = QIntValidator(0, 59, self)
        self.rx_signal_input.setValidator(signal_validator)
        self.tx_signal_input.setValidator(signal_validator)
        # 连接文本变化信号到自定义槽函数，检查输入值并给出提示
        self.rx_signal_input.textChanged.connect(self.check_signal_input)
        self.tx_signal_input.textChanged.connect(self.check_signal_input)


        # 连接rx_callsign的文本变化信号到自定义槽函数，查询匹配项数量并更新rx_callsign_new
        self.rx_callsign.textChanged.connect(self.update_rx_callsign_new)

    def update_rx_callsign_new(self):
        rx_callsign_text = self.rx_callsign.text().upper()

        # 如果rx_callsign为空，清空rx_callsign_new并返回
        if not rx_callsign_text:
            self.rx_callsign_new.clear()
            return

        # 构建查询语句，查询与rx_callsign匹配的记录数量
        query = f"SELECT COUNT(*) FROM rx_log WHERE rx_callsign LIKE '%{rx_callsign_text}%';"

        self.cursor.execute(query)
        match_count = self.cursor.fetchone()[0]

        # 根据匹配项数量更新rx_callsign_new的文本
        if match_count == 0:
            self.rx_callsign_new.setVisible(True)  # 设置为不可见
            self.rx_callsign_new.setText("活捉新友台！")
        else:
            self.rx_callsign_new.setVisible(True) 
            self.rx_callsign_new.setText(f"累计通联{match_count}次")
        # 强制刷新rx_callsign_new控件
        self.rx_callsign_new.update()
    def check_signal_input(self):
        text = self.sender().text()
        if text.isdigit() and int(text) > 59:
            QMessageBox.warning(self, "敬告友台", "　　信号报告没有超过59的说法，\n请输入0到59之间的数值。")
            self.sender().clear()  # 清除输入，恢复到有效范围内的值
    #---------------------------------------------------下面是添加通联数据实现开始----------------------------------------------------------
    def radio_button_toggled(self, checked):
        # 当RadioButton的选中状态发生变化时，记录选中的RadioButton
        if checked:
            self.currently_selected_radio_button = self.sender()

    def handle_next_rx_button_clicked(self):
        
        # 获取当前日期时间和日期时间格式化字符串
        current_datetime = datetime.now()
        date_time_str = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
        date_str = current_datetime.strftime('%Y-%m-%d')
        time_str = current_datetime.strftime('%H:%M:%S')

        # 获取其他控件的值
        sn = self.rx_num_auto.text()
        rx_callsign = self.rx_callsign.text().upper()
        rx_signal = self.rx_signal_input.text()
        tx_signal = self.tx_signal_input.text()
        qth = self.qth_comboBox.currentText()
        rig = self.rig_comboBox.currentText()
        power = self.power_comboBox.currentText()

        # 判断哪个RadioButton被选中，获取对应的for_info
        for_info = ""
        # 获取当前选中的RadioButton（可能为None）
        selected_button = self.currently_selected_radio_button
        if selected_button == self.laiyuan_redian:
            for_info = "热点"
        elif selected_button == self.laiyuan_zhongji:
            for_info = "中继"
        elif selected_button == self.laiyuan_shouji:
            for_info = "智能终端"
        elif selected_button == self.laiyuan_qita:
            for_info = self.other_lineEdit.text()
        print("for:",for_info)
            # 获取对方信号（若未输入，则默认为59）
        rx_signal = self.rx_signal_input.text()
        if not rx_signal:
            rx_signal = "59"

        # 获取我方信号（若未输入，则默认为59）
        tx_signal = self.tx_signal_input.text()
        if not tx_signal:
            tx_signal = "59"
        # 操作员的来源
        op = self.label_2.text()
        #rx_callsign_text = self.rx_callsign.text().upper()
        #qth_index = self.qth_comboBox.currentIndex()
        #rig_index = self.rig_comboBox.currentIndex()
        #power_index = self.power_comboBox.currentIndex()
        other_text = self.other_lineEdit.text()

        # 非空检查
        if not rx_callsign or qth== -1 or rig == -1 or power == -1:
            QMessageBox.warning(self, "警告", "请输入或选择完整的通联参数！")
            return

        if self.currently_selected_radio_button == self.laiyuan_qita and not other_text:
            QMessageBox.warning(self, "警告", "选择“其他”时，请填写方式或频率！")
            return
        # 插入数据到rx_log表
        insert_query = f"""
            INSERT INTO rx_log (
                date_time,
                date,
                time,
                sn,
                rx_callsign,
                rx_signal,
                tx_signal,
                qth,
                rig,
                power,
                for_info,
                op
            ) VALUES (
                '{date_time_str}',
                '{date_str}',
                '{time_str}',
                '{sn}',
                '{rx_callsign}',
                '{rx_signal}',
                '{tx_signal}',
                '{qth}',
                '{rig}',
                '{power}',
                '{for_info}',
                '{op}'
            );
        """
        self.cursor.execute(insert_query)
        self.db_connection.commit()

        # 更新rx_num_auto文本内容
        self.update_rx_num_auto()
        # 清空输入控件
        self.rx_callsign.clear()
        self.rx_signal_input.clear()
        self.tx_signal_input.clear()

        # 将组合框设置为初始值
        self.qth_comboBox.setCurrentIndex(-1)
        self.rig_comboBox.setCurrentIndex(-1)
        self.power_comboBox.setCurrentIndex(-1)
        # 取消所有QRadioButton的选中状态，遍历所有需要取消选中的QRadioButton列表，对每个按钮调用setChecked(False)
        for radio_button in [self.laiyuan_redian, self.laiyuan_zhongji, self.laiyuan_shouji, self.laiyuan_qita]:
            radio_button.setChecked(False)
        # 取消所有QRadioButton的选中状态
        #self.laiyuan_redian.setChecked(False)
        self.laiyuan_zhongji.setChecked(True)
        #self.laiyuan_shouji.setChecked(False)
        #self.laiyuan_qita.setChecked(False)
        #self.other_lineEdit.setDisabled(True)   # 把其他来源编辑框设置成不能编辑

        # 清空other_lineEdit（若有内容）
        if self.other_lineEdit.text():
            self.other_lineEdit.clear()
        # 判断当前的新友台提示是不是显示了    
        if self.rx_callsign_new.setVisible(True) :
            self.rx_callsign_new.setVisible(False) 
        else:
            pass   


    #---------------------------------------------------下面是添加通联数据实现结束----------------------------------------------------------

    #---------------------------------------------------下面是自动序号实现开始
    def update_rx_num_auto(self):
        current_datetime = datetime.now()   # 获取当前日期和时间
        # 检查是否已过当天凌晨00:00:00
        if current_datetime.hour == 0 and current_datetime.minute == 0 and current_datetime.second == 0:
            next_sn = 1
        else:
            # 获取当前日期
            current_date = current_datetime.strftime('%Y-%m-%d')

            # 查询当天最大序号
            query = f"SELECT MAX(sn) FROM rx_log WHERE date = '{current_date}';"
            self.cursor.execute(query)
            max_sn_today = self.cursor.fetchone()[0]

            # 计算并设置下一个可用序号
            if max_sn_today is None or max_sn_today == "":
                next_sn = 1
            else:
                next_sn = max_sn_today + 1

        self.rx_num_auto.setText(str(next_sn))
    #---------------------------------------------------上面是自动序号实现结束

        # 下面是来源信息其他 编辑框联动 的槽函数
    # 定义槽函数
    def handle_laiyuan_qita_toggled(self, checked: bool):
        self.other_lineEdit.setDisabled(not checked)  # 当checked为False时，禁用other_lineEdit；否则启用
    # 上面是来源信息其他 编辑框联动 的槽函数
    # 可编辑序号的功能开始
    def handle_double_click(self, event):
        if not self.sn_lineEdit.isVisible():
            # 显示QLineEdit，隐藏QLabel
            self.rx_num_auto.setVisible(False)
            self.sn_lineEdit.setVisible(True)
            self.sn_lineEdit.setFocus()  # 聚焦QLineEdit，准备编辑

            # 连接editingFinished信号到update_label_text槽
            self.sn_lineEdit.editingFinished.connect(self.update_label_text)

    def update_label_text(self):
        # 获取QLineEdit的文本，更新QLabel
        text = self.sn_lineEdit.text()
        self.rx_num_auto.setText(text)

        # 隐藏QLineEdit，显示QLabel
        self.sn_lineEdit.setVisible(False)
        self.rx_num_auto.setVisible(True)

        # 尝试断开editingFinished信号连接，忽略可能的TypeError异常
        try:
            self.sn_lineEdit.editingFinished.disconnect(self.update_label_text)
        except TypeError:
            pass


        #----------------------------------------------------------------------测试可编辑序号借宿
    def populate_city_list(self):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT city_name FROM city")
        cities = [row[0] for row in cursor.fetchall()]
        # print(f"Database query result: {cities}")  # 打印查询结果以确认其正确性
        self.qth_comboBox.clear()  # 清空现有内容，确保每次启动时重新填充
        self.qth_comboBox.addItems(cities)
        self.qth_comboBox.setCurrentIndex(-1)  # 默认不选中任何项
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++在QTH框子加载默认城市结束++++++++++++++继续QTH匹配项开始++++++++++++++++++++++++++++++++++++++++
    def initialize_table_view(self):
        # 初始化数据模型
        model = QStandardItemModel()

        # 定义表头映射
        header_mapping = {
            'date': '日期',
            'time': '时间',
            'sn': '序号',
            'rx_callsign': '呼号',
            'qth': 'QTH',
        }

        # 设置表头
        new_header_labels = [header_mapping[col] for col in ['date', 'time', 'sn', 'rx_callsign', 'qth']]
        model.setHorizontalHeaderLabels(new_header_labels)

        # 将数据模型绑定到表格视图
        self.newlog_tableView.setModel(model)

        # 查询并填充数据
        self.update_table_view()
        # 创建一个居中对齐的代理
        center_delegate = CenterAlignedItemDelegate()
        # 为表格视图中的所有列设置居中对齐的代理
        for column in range(model.columnCount()):
            self.newlog_tableView.setItemDelegateForColumn(column, center_delegate)

    def update_table_view(self):
        # 查询所有数据
        #query = "SELECT date, time, sn, rx_callsign, qth FROM rx_log ORDER BY date DESC, time DESC, sn DESC"
        query = """
            SELECT date, time, sn, rx_callsign, qth
            FROM rx_log
            ORDER BY date DESC, time DESC, sn DESC
            LIMIT 9
        """
        # 使用传入的查询语句执行查询
        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        # 获取已绑定的数据模型
        model = self.newlog_tableView.model()

        # 清空模型现有数据
        model.removeRows(0, model.rowCount())

        # 将查询结果转换为模型项并添加到模型中
        for row in rows:
            items = [QStandardItem(str(v)) for v in row]
            model.appendRow(items)

        # 设置表格视图的列宽自适应
        self.newlog_tableView.resizeColumnsToContents()
        # 调整列宽，使每列比自适应宽度大5像素
        for column in range(model.columnCount()):
            width = self.newlog_tableView.columnWidth(column) + 20
            self.newlog_tableView.setColumnWidth(column, width)
    # -------------------------------------------到这里
    def update_search_results(self, search_text):
        if self.initial_load:
            self.initial_load = False
            return

        cursor = self.db_connection.cursor()
        search_pattern = f"%{search_text}%"

        # 使用 LIKE 操作符进行模糊查询
        query = """
            SELECT city_name 
            FROM city 
            WHERE city_sx LIKE ? OR city_name LIKE ?
        """
        cursor.execute(query, (search_pattern, search_pattern))

        cities = [row[0] for row in cursor.fetchall()]
        # 不清除原有内容，仅添加匹配项到下拉列表
        existing_items = [item.text() for item in self.qth_comboBox.model().findItems("", Qt.MatchContains)]
        for city in cities:
            if city not in existing_items:
                self.qth_comboBox.addItem(city)


        # 如果有匹配结果，自动展开下拉列表
        if cities:
            self.qth_comboBox.showPopup()

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++在QTH框子匹配输入结束++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++清空QTH和设备内容开始++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def on_clear_qth_pushButton_clicked(self):
        self.qth_comboBox.setCurrentIndex(-1)  # 清空QTH选择当前选中的项，保留下拉列表内容
        
    def on_clear_rig_pushButton_clicked(self):
        self.rig_comboBox.setCurrentIndex(-1)  # 清空设备选择当前选中的项，保留下拉列表内容
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++清空QTH和设备内容结束++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # 根据呼号框内是否有内容判定是否清除所有的输入内容
    def handle_rx_callsign_text_changed(self, text):
        if not text:  # 当输入框内容为空时
            self.rx_signal_input.clear()  # 清空 rx_signal_input
            self.tx_signal_input.clear()  # 清空 tx_signal_input            
            self.qth_comboBox.setCurrentIndex(-1)  # 清空 qth_combobox 选择
            self.rig_comboBox.setCurrentIndex(-1)   # 清空 rig_combobox 选择
            self.power_comboBox.setCurrentIndex(-1) # 清空 power_combobox 选择
        

    # 这是自动填选中呼号信息的代码
    def update_selected_details(self):
        selected_item = self.callsign_xuanze_listWidget.selectedItems()
        if selected_item:
            selected_callsign = selected_item[0].text()

            # 安全地构造SQL查询（使用参数化查询避免SQL注入）
            query = """
                SELECT rx_signal, tx_signal, qth, rig, power
                FROM rx_log
                WHERE rx_callsign = ?
            """
            self.cursor.execute(query, (selected_callsign,))
            result = self.cursor.fetchone()

            if result:
                self.rx_signal_input.setText(str(result[0]))  # rx_signal
                self.tx_signal_input.setText(str(result[1]))  # tx_signal

                # 对于QComboBox，先检查item是否存在，再设置或添加
                qth_index = self.qth_comboBox.findText(result[2], Qt.MatchFixedString)
                if qth_index == -1:
                    self.qth_comboBox.addItem(result[2])
                    qth_index = self.qth_comboBox.findText(result[2], Qt.MatchFixedString)
                self.qth_comboBox.setCurrentIndex(qth_index)

                rig_index = self.rig_comboBox.findText(result[3], Qt.MatchFixedString)
                if rig_index == -1:
                    self.rig_comboBox.addItem(result[3])
                    rig_index = self.rig_comboBox.findText(result[3], Qt.MatchFixedString)
                self.rig_comboBox.setCurrentIndex(rig_index)

                power_index = self.power_comboBox.findText(result[4], Qt.MatchFixedString)
                if power_index == -1:
                    self.power_comboBox.addItem(result[4])
                    power_index = self.power_comboBox.findText(result[4], Qt.MatchFixedString)
                self.power_comboBox.setCurrentIndex(power_index)

    # 这是查询 快速选择呼号的代码
    def schedule_update(self):
        """当rx_callsign文本发生变化时,停止当前的定时器并重新启动一个新的定时器"""
        self.debounce_timer.stop()  # 停止当前的定时器
        self.debounce_timer.start(300)  # 开启一个新的定时器，300毫秒后执行update_callsign_list_debounced

    def update_callsign_list_debounced(self):
        """这个函数会在debounce_timer超时后执行,此时再进行查询和更新操作"""
        current_text = self.rx_callsign.text()  # 获取当前输入的文字
        # 当输入框为空时，清空列表并返回
        if not current_text:
            self.callsign_xuanze_listWidget.clear()
            return

        self.update_callsign_list(current_text)  # 调用原本的更新函数

    def update_callsign_list(self, text):
        self.callsign_xuanze_listWidget.clear()  # 清空原有的列表内容
        matching_callsigns = self.model.search_callsign_latest(text)  # 查询数据库 这个方法名需要与最前面的一致
        for callsign in matching_callsigns:
            self.callsign_xuanze_listWidget.addItem(callsign)  # 添加匹配项到列表中

        # 当在列表中选择一个项目时，更新rx_callsign的内容
        self.callsign_xuanze_listWidget.itemSelectionChanged.connect(self.update_rx_callsign)

    def update_rx_callsign(self):
        selected_items = self.callsign_xuanze_listWidget.selectedItems()

        if selected_items:
            # 至少有一个项目被选中，获取并处理第一个选中项
            selected_item = selected_items[0]
            self.rx_callsign.setText(selected_item.text())
        else:
            # 没有项目被选中，忽略此次操作
            pass

    # 这是打开关于窗口
    def open_about_window(self):
        self.about_window = AboutWindow()  # 创建about窗口实例
        self.about_window.show()  # 显示about窗口

    # 这是打开联系窗口
    def open_contact_window(self):
        self.contact_window = ContactWindow()  # 创建contact窗口实例
        self.contact_window.show()  # 显示contact窗口

    # 这是打开反馈页面
    def open_feedback_page(self):
        url = "https://support.qq.com/products/642622/"  # 目标网页 URL
        QDesktopServices.openUrl(QUrl(url))  # 使用 QDesktopServices 打开 URL

    # 这是打开查看日志窗口
    def open_log_window(self):
        self.log_window = LooklogWindow()  # 假设looklog.py中定义的窗口类名为LooklogWindow
        self.log_window.show()

    def update_time(self):
        current_time = QDateTime.currentDateTime()
        time_str = current_time.toString("yyyy-MM-dd HH:mm:ss dddd")

        # 设置now_time_label的文字颜色为红色（#ff0000）
        self.now_time_label.setStyleSheet("color: #ff0000;")
        self.now_time_label.setText(time_str)

    #打开更改操作员界面
    def open_change_op_window(self):
        self.change_op_window = ChangeOpWindow(self)
        self.change_op_window.operator_changed_signal.connect(self.update_config_in_db)  # 在这里连接信号与槽
        self.change_op_window.show()

    def update_config_in_db(self, new_callsign):
        # 确保提交到数据库的是大写字符
        new_callsign = new_callsign.upper()
        conn = sqlite3.connect('rx_log.db')
        cursor = conn.cursor()

        query = "UPDATE config SET content = ? WHERE name = '操作员'"
        cursor.execute(query, (new_callsign,))
        conn.commit()
        conn.close()

        # 更新界面上操作员OP的内容（如果需要在这里实时更新的话）
        self.label_2.setText(new_callsign)

    # 添加打开更改删除日志密码界面的方法
    def open_delpwd_window(self):
        self.del_pwd_window = DelPwdSetWindow(self)
        # 连接更改密码窗口的信号与槽，更改信号连接，使用DelPwdSetWindow类中定义的正确信号名
        self.del_pwd_window.password_changed_signal.connect(self.update_delpwd_in_db)
        self.del_pwd_window.show()

    # 添加更新删除日志密码到数据库的方法
    def update_delpwd_in_db(self, new_password):
        conn = sqlite3.connect('rx_log.db')
        cursor = conn.cursor()
        query = "UPDATE config SET content = ? WHERE name = '日志删除密码'"
        cursor.execute(query, (new_password,))
        conn.commit()
        conn.close()

        # 如果需要在此处更新相关界面元素，可以添加代码

    def closeEvent(self, event):
        self.db_connection.close()  # 在关闭窗口时关闭数据库连接
        super(MainWindow, self).closeEvent(event)

#从数据库获取当前操作员
# 定义获取数据库内容的函数
def get_config_from_db(db_name='rx_log.db', table='config', name='操作员'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
        
    query = f"SELECT content FROM {table} WHERE name = ?"
    cursor.execute(query, (name,))
    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]
    else:
        return ""

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())