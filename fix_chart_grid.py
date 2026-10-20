import re

# 读取文件
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 修复网格线颜色 - 白色背景上需要深色网格
content = content.replace("grid:{color:'rgba(255,255,255,0.1)'}", "grid:{color:'#e5e7eb'}")

# 写回文件
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Chart grid colors fixed!")
