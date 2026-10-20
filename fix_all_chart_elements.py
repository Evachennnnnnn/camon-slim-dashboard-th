import re

# 读取文件
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 修复所有图表元素 - 白色背景需要深色文字
# 1. 修复 title 颜色（从浅色改成深色）
content = content.replace("title:{display:true,text:'Brand SOV %',color:'#e5e5e5'}", "title:{display:true,text:'Brand SOV %',color:'#475569'}")
content = content.replace("title:{display:true,text:'Product SOV %',color:'#e5e5e5'}", "title:{display:true,text:'Product SOV %',color:'#475569'}")
content = content.replace("title:{display:true,text:'VV SOV %',color:'#e5e5e5'}", "title:{display:true,text:'VV SOV %',color:'#475569'}")
content = content.replace("title:{display:true,text:'Search SOV %',color:'#e5e5e5'}", "title:{display:true,text:'Search SOV %',color:'#475569'}")
content = content.replace("title:{display:true,text:'Consideration',color:'#e5e5e5'}", "title:{display:true,text:'Consideration',color:'#475569'}")
content = content.replace("title:{display:true,text:'Progress % / 进度 %',color:'#e5e5e5'}", "title:{display:true,text:'Progress % / 进度 %',color:'#475569'}")
content = content.replace("title:{display:true,text:'Spend $ / 消耗 $',color:'#e5e5e5'}", "title:{display:true,text:'Spend $ / 消耗 $',color:'#475569'}")

# 2. 修复 Y 轴标签颜色
content = content.replace("ticks:{color:'#ec4899',callback:v=>v+'%'}", "ticks:{color:'#64748b',callback:v=>v+'%'}")
content = content.replace("ticks:{color:'#f472b6',callback:v=>v+'%'}", "ticks:{color:'#64748b',callback:v=>v+'%'}")

# 3. 修复 title 的 color 属性（如果有重复的 color）
content = re.sub(r"title:\{display:true,color:'#e5e5e5',text:", "title:{display:true,text:", content)

# 写回文件
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ All chart elements fixed for white background!")
