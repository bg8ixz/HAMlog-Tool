import sqlite3
import os

# 获取脚本所在目录的绝对路径
script_dir = os.path.dirname(os.path.abspath(__file__))

# 数据库文件名（位于脚本所在目录下）
db_file = os.path.join(script_dir, 'rx_log.db')

# 连接到SQLite数据库（如果数据库不存在，则创建）
def create_connection():
    conn = sqlite3.connect(db_file)
    conn.execute("PRAGMA foreign_keys = ON")  # 如果有外键约束，启用外键检查
    return conn

# 创建rig表，假设rig_name列具有唯一性约束
def create_rig_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rig (
            id INTEGER PRIMARY KEY,
            rig_sx TEXT,
            rig_name TEXT UNIQUE
        )
    """)
    conn.commit()

# 检查rig_name是否已存在
def rig_name_exists(conn, rig_name):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM rig WHERE rig_name=?", (rig_name,))
    count = cursor.fetchone()[0]
    return count > 0

# 批量插入数据，避免重复rig_name
def insert_unique_rigs(conn, rigs_data):
    unique_to_insert = [(abbreviation, position) for abbreviation, position in rigs_data if not rig_name_exists(conn, position)]

    if unique_to_insert:
        cursor = conn.cursor()
        # 使用INSERT OR IGNORE避免因唯一性约束冲突而抛出错误
        cursor.executemany("INSERT OR IGNORE INTO rig (rig_sx, rig_name) VALUES (?, ?)", unique_to_insert)
        conn.commit()

# 主函数
def main():
    conn = create_connection()

    # 创建rig表
    create_rig_table(conn)

    # 准备要插入的数据
    rigs_data = [
        ("bf1701", "宝峰 DM-17011pyu"),
        ("bf1702", "宝峰 DM-1702"),
        ("bf1801", "宝峰 DM-1801"),
        ("qsk5", "泉盛 K5"),
        ("qsk6", "泉盛 K6"),
        ("shks8600", "森海克斯8600"),
        ("qyt8900", "泉益通 KT-8900"),
        ("wn6600", "威诺 VR-6600PRO"),
        # ... 更多记录
        ("wnn7500", "威诺 VR-N7500"),
    ]

    # 插入数据（避免重复rig_name）
    insert_unique_rigs(conn, rigs_data)

    # 关闭连接
    conn.close()

# 运行主函数
if __name__ == "__main__":
    main()