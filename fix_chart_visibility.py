import re

# 读取文件
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 修复图表可见性问题
# 1. 把所有黑色线条改成白色或粉色（在深色背景上看不见）
content = content.replace("borderColor:'#111111'", "borderColor:'#ffffff'")
content = content.replace("pointBackgroundColor:'#111111'", "pointBackgroundColor:'#ffffff'")
content = content.replace("backgroundColor:'rgba(17,17,17,.1)'", "backgroundColor:'rgba(255,255,255,.1)'")

# 2. 增加线条粗细，让图表更明显
content = content.replace("borderWidth:1", "borderWidth:2")

# 3. 增加数据点大小
content = content.replace("pointRadius:5", "pointRadius:8")
content = content.replace("pointRadius:3", "pointRadius:6")
content = content.replace("pointRadius:2", "pointRadius:5")

# 4. 确保图表容器有最小高度
content = content.replace(".chart { position:relative; height:340px; }", ".chart { position:relative; height:340px; min-height:340px; background:rgba(255,255,255,0.02); border-radius:8px; }")

# 写回文件
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Chart visibility fixed!")
