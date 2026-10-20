import re

# 读取文件
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 替换图表配色为黑粉主题
# Google Brand Chart: 蓝色 → 粉色
content = content.replace("borderColor:'#2563eb',backgroundColor:'rgba(37,99,235,.1)'", "borderColor:'#ec4899',backgroundColor:'rgba(236,72,153,.1)'")
content = content.replace("pointBackgroundColor:'#2563eb'", "pointBackgroundColor:'#ec4899'")

# Google Product Chart: 绿色 → 粉色
content = content.replace("borderColor:'#059669',backgroundColor:'rgba(5,150,105,.1)'", "borderColor:'#f472b6',backgroundColor:'rgba(244,114,182,.1)'")
content = content.replace("pointBackgroundColor:'#059669'", "pointBackgroundColor:'#f472b6'")

# TT SOV Chart: 紫色/橙色 → 粉色/黑色
content = content.replace("borderColor:'#7c3aed',backgroundColor:'rgba(124,58,237,.1)'", "borderColor:'#ec4899',backgroundColor:'rgba(236,72,153,.1)'")
content = content.replace("pointBackgroundColor:'#7c3aed'", "pointBackgroundColor:'#ec4899'")
content = content.replace("borderColor:'#ea580c',backgroundColor:'rgba(234,88,12,.1)'", "borderColor:'#111111',backgroundColor:'rgba(17,17,17,.1)'")
content = content.replace("pointBackgroundColor:'#ea580c'", "pointBackgroundColor:'#111111'")

# Consideration Chart: 绿色/灰色 → 粉色/黑色
content = content.replace("borderColor:'#059669',backgroundColor:'rgba(5,150,105,.12)'", "borderColor:'#ec4899',backgroundColor:'rgba(236,72,153,.12)'")
content = content.replace("pointBackgroundColor:'#059669'", "pointBackgroundColor:'#ec4899'")
content = content.replace("borderColor:'#94a3b8',backgroundColor:'rgba(148,163,184,.08)'", "borderColor:'#6b7280',backgroundColor:'rgba(107,114,128,.08)'")

# Spend Chart: 黄色/绿色 → 粉色/黑色
content = content.replace("backgroundColor:'rgba(251,191,36,.6)',borderColor:'#f59e0b'", "backgroundColor:'rgba(236,72,153,.6)',borderColor:'#ec4899'")
content = content.replace("pointBackgroundColor:'#f59e0b'", "pointBackgroundColor:'#ec4899'")
content = content.replace("borderColor:'#0f766e'", "borderColor:'#111111'")
content = content.replace("pointBackgroundColor:'#0f766e'", "pointBackgroundColor:'#111111'")

# Competitor Compare Chart: 更新配色
content = content.replace('"borderColor": "#10b981"', '"borderColor": "#ec4899"')
content = content.replace('"bg": "rgba(16,185,129,.15)"', '"bg": "rgba(236,72,153,.15)"')

# 写回文件
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Chart colors updated to black+pink theme!")
