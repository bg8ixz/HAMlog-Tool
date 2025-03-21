# main.py
import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QAction
from PyQt5.QtCore import QTimer, QDateTime, QUrl
from PyQt5.QtGui import QDesktopServices
# 引入一堆窗口
from rx_log import Ui_rx_log
from changeop import Ui_opchange__Form # 引入opchange.py中的窗口类
from changeop import ChangeOpWindow  # 引入opchange.py中自定义的关于窗口类
from del_log_pwd import Ui_del_pwd_set_Form # 引入opchange.py中的窗口类
from del_log_pwd import DelPwdSetWindow  # 引入opchange.py中自定义的关于窗口类
from about import Ui_about__Form  # 引入about.py中的窗口类
from about import AboutWindow  # 引入about.py中自定义的关于窗口类
from contact import Ui_contact_Form  # 引入about.py中的窗口类
from contact import ContactWindow  # 引入about.py中自定义的关于窗口类
import webbrowser


#时间更新显示
class MainWindow(QMainWindow, Ui_rx_log):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        # 从数据库获取label_2的内容
        label_2_content = get_config_from_db()
        self.label_2.setText(label_2_content)

        #这是时间实时显示
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # 每秒更新一次

        #这是更换操作员的设置按钮
        self.op_set_action.triggered.connect(self.open_change_op_window)

        #这是更换删除密码的设置按钮
        self.delpwd_action.triggered.connect(self.open_delpwd_window)

        #self.change_op_window_operator_changed_signal = ChangeOpWindow.operator_changed_signal
        #self.change_op_window_operator_changed_signal.connect(self.update_config_in_db)

        # 这是点击关于按钮的操作
        self.aubot_action = self.findChild(QAction, 'aubot_action')  # 假设其objectName为'aubot_action'
        assert self.aubot_action is not None, "Failed to find the aubot_action in UI"
        # 连接关于按钮动作到槽函数
        self.aubot_action.triggered.connect(self.open_about_window)

        # 这是点击联系按钮的操作
        self.contact_action = self.findChild(QAction, 'contact_action')  # 假设其objectName为'aubot_action'
        assert self.contact_action is not None, "Failed to find the contact_action in UI"
        # 连接联系按钮动作到槽函数
        self.contact_action.triggered.connect(self.open_contact_window)

        # 反馈按钮的操作
        self.feedback_action = self.findChild(QAction, 'feedback_action') # 查找名为 feedback_action 的 QAction
        assert self.feedback_action is not None, "Failed to find the feedback_action in UI"
        self.feedback_action.triggered.connect(self.open_feedback_page) # 连接槽函数
    
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

        # 更新label_2的内容（如果需要在这里实时更新的话）
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