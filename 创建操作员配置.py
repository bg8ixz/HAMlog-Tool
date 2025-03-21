import sqlite3
import os

# 获取脚本所在目录的绝对路径
script_dir = os.path.dirname(os.path.abspath(__file__))

# 连接到SQLite数据库（如果不存在则创建）
conn = sqlite3.connect('rx_log.db')

# 创建一个游标对象
c = conn.cursor()

# 定义表格结构，尽管SQLite不直接支持自增，但rowid会自动为每一行生成唯一整数
create_table_sql = """
CREATE TABLE IF NOT EXISTS config (
    id INTEGER PRIMARY KEY,
    name TEXT,
    content TEXT
);
"""

# 执行SQL命令以创建表
c.execute(create_table_sql)

# 插入示例数据，由于id是PRIMARY KEY，所以SQLite会自动为其分配rowid
insert_data_sql = """
INSERT INTO config (name, content)
VALUES ('操作员', 'BG8IXZ');
"""

# 执行插入数据的SQL命令
c.execute(insert_data_sql)

# 提交事务，确保更改被保存到数据库
conn.commit()

# 关闭连接
conn.close()