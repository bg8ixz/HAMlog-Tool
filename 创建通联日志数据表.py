import sqlite3
import os
from datetime import datetime


# 这一句是删除数据表 DROP TABLE IF EXISTS rx_log;
# 获取脚本所在目录的绝对路径
script_dir = os.path.dirname(os.path.abspath(__file__))

# 连接到SQLite数据库或者创建新的数据库（如果不存在的话）
conn = sqlite3.connect('rx_log.db')

# 创建一个游标对象
c = conn.cursor()

# SQL语句：创建rx_log表，其中id字段仍作为自增主键，新增date和time字段，sn字段允许不唯一但不能为空
create_table_sql = """
CREATE TABLE IF NOT EXISTS rx_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date_time TEXT NOT NULL,
    date TEXT NOT NULL,
    time TEXT NOT NULL,
    sn INTEGER NOT NULL,
    rx_callsign TEXT NOT NULL,
    rx_signal INT,
    tx_signal INT,
    qth TEXT,
    rig TEXT,
    power TEXT,
    for_info TEXT,
    op TEXT NOT NULL
);
"""

# 执行SQL语句
c.execute(create_table_sql)

# 提交事务
conn.commit()

# 获取当前的日期和时间
current_datetime = datetime.now()

# 分离日期和时间
now_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
record_date = current_datetime.strftime('%Y-%m-%d')
record_time = current_datetime.strftime('%H:%M:%S')

# 准备要插入的多条数据，这里是一个元组列表，每个元组包含一个sn和一个rx_callsign
multiple_records = [
    (now_datetime, record_date, record_time, 23, 'BG7INI', 59, 39, '重庆市巴南区', '宝峰 DM-1801', '1', '中继', 'BG8LAK'),
    (now_datetime, record_date, record_time, 24, 'BA4RF', 56, 32, '重庆市垫江县', '宝峰 DM-1702', '5', '中继', 'BG8LAK'),
    # 添加更多记录...
]

# 参数化查询模板，使用问号（?）作为占位符
insert_data_sql = """
    INSERT INTO rx_log (date_time, date, time, sn, rx_callsign, rx_signal, tx_signal, qth, rig, power, for_info, op)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

# 为了演示如何插入数据，添加一行示例数据，自动填充当前日期和时间
c.executemany(insert_data_sql, multiple_records)
# insert_data_sql = f"INSERT INTO rx_log (date_time, date, time, sn, rx_callsign) VALUES ('{now_datetime}', '{record_date}', '{record_time}', 1, 'BG7INI')"
# c.execute(insert_data_sql)

# 提交插入数据的事务
conn.commit()

# 关闭连接
conn.close()