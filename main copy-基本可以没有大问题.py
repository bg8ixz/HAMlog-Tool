# main.py
APP_VERSION = "1.0.0.Alpha"
import os, re, sys, sqlite3
import webbrowser
from datetime import datetime
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QRadioButton,QAction, QLineEdit, QStyledItemDelegate, QListWidget, QTableView, QHeaderView, QLabel, QComboBox, QVBoxLayout, QCompleter, QMessageBox
from PyQt5.QtCore import QTimer, QDateTime, QUrl, QObject, Qt, QVariant, QSignalBlocker, QStringListModel, QSortFilterProxyModel, QRegExp
from PyQt5.QtGui import QDesktopServices, QIcon,QStandardItem, QStandardItemModel, QRegExpValidator
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

        current_dir = os.getcwd()   # 获取当前运行目录
        icon_file_path = os.path.join(current_dir, 'favicon.ico')   # 指定图标文件相对于运行目录的相对路径
        app_icon = QIcon(icon_file_path)    # 加载图标
        self.setWindowIcon(app_icon)    # 设置窗口图标

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
        print("fo:",for_info)
        
        # 操作员的来源
        op = self.label_2.text()
        #rx_callsign_text = self.rx_callsign.text().upper()
        qth_index = self.qth_comboBox.currentIndex()
        rig_index = self.rig_comboBox.currentIndex()
        power_index = self.power_comboBox.currentIndex()
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
    #---------------------------------------------------下面是添加通联数据实现结束----------------------------------------------------------

    #---------------------------------------------------下面是自动序号实现开始
    def update_rx_num_auto(self):
        # 获取当前日期
        current_date = datetime.now().strftime('%Y-%m-%d')
        print(current_date)

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