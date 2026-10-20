import re

# 读取文件
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 彻底修复所有图表配色 - 把所有深色文字改成浅色
# 1. 所有 ticks 颜色
content = content.replace("ticks:{color:'#64748b'", "ticks:{color:'#e5e5e5'")
content = content.replace("ticks:{color:'#475569'", "ticks:{color:'#e5e5e5'")

# 2. 所有 legend 标签颜色
content = content.replace("labels:{color:'#475569'", "labels:{color:'#e5e5e5'")

# 3. 所有 title 颜色
content = content.replace("title:{display:true,text:", "title:{display:true,color:'#e5e5e5',text:")

# 4. 修复 Consideration 图表的 Y 轴
content = content.replace("ticks:{color:'#64748b',callback:v=>Math.round", "ticks:{color:'#e5e5e5',callback:v=>Math.round")

# 5. 修复 Competitor Compare 图表
content = content.replace("font:{size:11}", "font:{size:11,color:'#e5e5e5'}")

# 写回文件
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ All chart colors fixed for dark background!")
