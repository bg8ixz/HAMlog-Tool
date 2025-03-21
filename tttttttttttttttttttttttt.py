import apsw

# 可选：进一步调用APSW的某个函数或类以验证其功能
conn = apsw.Connection(":memory:")
cursor = conn.cursor()
cursor.execute("CREATE TABLE test (id INTEGER PRIMARY KEY)")
print("APSW installed and working correctly.")