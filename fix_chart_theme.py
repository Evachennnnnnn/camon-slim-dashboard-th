import re

# 读取文件
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 修复图表配色 - 适配深色背景
# 1. 文字颜色：深色 → 浅色
content = content.replace("ticks:{color:'#64748b'}", "ticks:{color:'#e5e5e5'}")
content = content.replace("color:'#475569'", "color:'#e5e5e5'")

# 2. 网格线：浅色 → 深色半透明
content = content.replace("grid:{color:'#eef2f7'}", "grid:{color:'rgba(255,255,255,0.1)'}")

# 3. 标题颜色
content = content.replace("title:{display:true,text:'Brand SOV %'}", "title:{display:true,text:'Brand SOV %',color:'#e5e5e5'}")
content = content.replace("title:{display:true,text:'Product SOV %'}", "title:{display:true,text:'Product SOV %',color:'#e5e5e5'}")
content = content.replace("title:{display:true,text:'VV SOV %',color:'#7c3aed'}", "title:{display:true,text:'VV SOV %',color:'#ec4899'}")
content = content.replace("title:{display:true,text:'Search SOV %',color:'#ea580c'}", "title:{display:true,text:'Search SOV %',color:'#f472b6'}")
content = content.replace("title:{display:true,text:'Consideration',color:'#059669'}", "title:{display:true,text:'Consideration',color:'#ec4899'}")
content = content.replace("title:{display:true,text:'Progress % / 进度 %',color:'#f59e0b'}", "title:{display:true,text:'Progress % / 进度 %',color:'#ec4899'}")
content = content.replace("title:{display:true,text:'Spend $ / 消耗 $',color:'#fbbf24'}", "title:{display:true,text:'Spend $ / 消耗 $',color:'#f472b6'}")

# 4. Y轴标签颜色
content = content.replace("ticks:{color:'#7c3aed',callback:v=>v+'%'}", "ticks:{color:'#ec4899',callback:v=>v+'%'}")
content = content.replace("ticks:{color:'#ea580c',callback:v=>v+'%'}", "ticks:{color:'#f472b6',callback:v=>v+'%'}")
content = content.replace("ticks:{color:'#f59e0b',callback:v=>v+'%'}", "ticks:{color:'#ec4899',callback:v=>v+'%'}")
content = content.replace("ticks:{color:'#fbbf24',callback:v=>'$'+v}", "ticks:{color:'#f472b6',callback:v=>'$'+v}")

# 写回文件
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Chart theme fixed for dark background!")
