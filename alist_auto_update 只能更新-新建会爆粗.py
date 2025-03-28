#!/usr/bin/env python3
import requests
import datetime
import subprocess
import os
import re
  
# GitHub API URL 用于获取最新版本  
API_URL = "https://api.github.com/repos/uubulb/alist-freebsd/releases/latest"  

# 执行 ./alist version 命令并获取输出
try:
    version_output = subprocess.check_output(['./alist', 'version'], text=True).strip()
except subprocess.CalledProcessError as e:
    print("警告：执行查询Alist版本号命令出错:", e)
    exit(1)

# 解析获取到的版本号
version_pattern = r"Version: v(\d+\.\d+\.\d+)-\d+-g[a-fA-F0-9]+"
match = re.search(version_pattern, version_output)
if match:
    get_version = match.group(1)
    current_version = f"v{get_version}"
    print(f"当前 Alist 版本: {current_version}")
else:
    print("未能从输出中找到正确的版本号。")
    exit(1)

# 从 API 获取最新版本的数据
try:
    response = requests.get(API_URL)
    response.raise_for_status()  # 如果请求返回了一个错误状态码，将抛出异常
except requests.exceptions.RequestException as e:
    print(f"从 GitHub 获取最新版本信息出错: {e}")
    exit(1)
release_data = response.json()

# 从获取到的json数据中找到版本号
alist_freebsd_version = release_data.get('name', None)
if not alist_freebsd_version:
    print("没有找到 Alist FreeBSD 版本号。")
    exit(1)
print(f"最新 Alist 版本: {alist_freebsd_version}")  # 打印最新版本号（测试用）

# 比较版本号
if current_version == alist_freebsd_version:    # 如果前面没做v字符，则需要使用alist_freebsd_version.lstrip('v')移除获取到的GitHub上版本号的'v'
    print("当前已经是最新版本，不需要更新！")
    exit(0)
else:
    print(f"发现新版本 {alist_freebsd_version}，当前版本为 v{current_version}，正在执行更新...\n")

# 查找名为 'alist' 的文件的下载链接  
for asset in release_data['assets']:  
    if 'alist' in asset['name'].lower():  
        DOWNLOAD_URL = asset['browser_download_url']          
        #DOWNLOAD_URL = DOWNLOAD_URL.replace("https://github.com", "https://download.nuaa.cf")       # 本地测试加速用，Serv00可能会文件下载不全
        break  
else:  
    print("在发布中未找到名为 'alist' 的文件。")  
    exit(1)  

# 检查 alist 文件是否存在
if os.path.exists('alist'):    
    current_datetime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')     # 获取当前日期和时间并格式化为 YYYYMMDDHHMMSS
    new_name = f"{current_datetime}_alist_bak"      # 重命名现有文件，格式为 YYYYMMDDHHMMSS_alist_bak
    if os.path.exists(new_name):        
        print(f"文件 '{new_name}' 已存在，尝试生成一个新的文件名...")       # 如果重命名后的文件名已存在，再次循环直到找到一个不存在的文件名
        new_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + "_alist_bak"
    os.rename('alist', new_name)
    print(f"温馨提醒：'alist' 文件已存在，以防万一已重命名为 '{new_name}'。\n")

# 下载文件  
print(f"正在从 {DOWNLOAD_URL} 下载最新 FreeBSD 版 Alist ,请稍后...\n\n")  
response = requests.get(DOWNLOAD_URL, stream=True)  
with open('alist', 'wb') as f:  
    for chunk in response.iter_content(chunk_size=32768):   # 从 HTTP 响应中读取数据块（chunks）的大小，8192（8KB）、32768（32KB）、65536（64KB），自己换！
        f.write(chunk)  
  
# 赋予 alist 文件可执行权限  
os.chmod('alist', 0o755)  
  
# 检查是否存在 config.json 文件  
if os.path.exists('./data/config.json'):  
    print("---------------------------------------------\n温馨提示：Alist-FreeBSD 最新版本已经下载并替换完成！\n---------------------------------------------\n")  
else:   
    subprocess.Popen(['./alist', 'server'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)   # 启动 alist 服务
    print("已下载最新版本的 Alist-FreeBSD ，并生成 config.json 文件。")   
  
    # 清除终端（可能不适用于所有环境）  
    try:  
        os.system('clear' if os.name == 'posix' else 'cls')  
    except:  
        pass  
  
    print("配置文件 config.json 已成功生成，路径：./data/config.json ，请自行修改端口！")  
    print("使用命令 cd 命令进入 data 路径下")  
    print("再使用文本编辑器编辑 config.json 文件，修改 port 字段为你放行的端口！")  
    print("例如，使用 vim: vim config.json")  
    print("修改完成后，使用命令 cd .. 回到上级目录")