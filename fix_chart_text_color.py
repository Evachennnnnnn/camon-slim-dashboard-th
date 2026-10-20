import re

# 读取文件
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 把图表内的文字颜色改回深色（因为图表容器现在是白色背景）
# 1. ticks 文字颜色
content = content.replace("ticks:{color:'#e5e5e5'", "ticks:{color:'#64748b'")

# 2. legend 标签颜色
content = content.replace("labels:{color:'#e5e5e5'", "labels:{color:'#475569'")

# 3. title 颜色
content = content.replace("title:{display:true,color:'#e5e5e5',text:", "title:{display:true,text:")

# 4. 特定的 title 颜色
content = content.replace("color:'#ec4899'}", "color:'#475569'}")
content = content.replace("color:'#f472b6'}", "color:'#475569'}")

# 5. 修复 font 颜色
content = content.replace("font:{size:11,color:'#e5e5e5'}", "font:{size:11}")

# 写回文件
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Chart text colors fixed for white background!")
