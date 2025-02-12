## 展示如何去引用tool.py中的工具
#檔案層級

# project
# |-tools(package)
#     |-__init__.py
#     |-tool.py
# |-tool_demo.py

from tools import tool
print(tool.sum_num(1, 2, 3))