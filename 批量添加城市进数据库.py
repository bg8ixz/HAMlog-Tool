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

# 创建city表，假设city_name列具有唯一性约束
def create_city_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS city (
            id INTEGER PRIMARY KEY,
            city_sx TEXT,
            city_name TEXT UNIQUE
        )
    """)
    conn.commit()

# 检查city_name是否已存在
def city_name_exists(conn, city_name):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM city WHERE city_name=?", (city_name,))
    count = cursor.fetchone()[0]
    return count > 0

# 批量插入数据，避免重复city_name
def insert_unique_cities(conn, cities_data):
    unique_to_insert = [(abbreviation, position) for abbreviation, position in cities_data if not city_name_exists(conn, position)]

    if unique_to_insert:
        cursor = conn.cursor()
        # 使用INSERT OR IGNORE避免因唯一性约束冲突而抛出错误
        cursor.executemany("INSERT OR IGNORE INTO city (city_sx, city_name) VALUES (?, ?)", unique_to_insert)
        conn.commit()

# 主函数
def main():
    conn = create_connection()

    # 创建city表
    create_city_table(conn)

    # 准备要插入的数据
    cities_data = [
        ("cqsybq", "重庆市区"),
        ("cqsbnq", "重庆市南区"),
        ("cqsbbq", "重庆市北区"),
        ("cqscsq", "重庆长寿区"),
        ("cqswzq", "重庆市万区"),
        ("cqscsq", "重庆市长寿区"),
        ("cqsyzq", "重庆市渝中区"),
        ("cqsbsq", "重庆市璧山区"),
        # ... 更多记录
        ("cqsjjq", "重庆市江津区"),
    ]

    # 插入数据（避免重复city_name）
    insert_unique_cities(conn, cities_data)

    # 关闭连接
    conn.close()

# 运行主函数
if __name__ == "__main__":
    main()
