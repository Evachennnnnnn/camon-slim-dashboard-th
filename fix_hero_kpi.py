import json
import re

# 读取文件
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 提取D对象
pattern = r'const D = (\{[\s\S]*?\n\});'
match = re.search(pattern, content)

if match:
    D = json.loads(match.group(1))
    
    # 修改Hero为菲律宾结构（不要消耗）
    D['hero'] = {
        "desc": "Google Product SOV 8.82% (10/19), Consideration 448K (10/17), TT曝光 417K (10/17), 互动量 78.6K (10/17). / Google 产品 SOV 8.82%，Consideration 总量 448K，TT曝光 417K，互动量 78.6K。",
        "stats": [
            {"label": "Google 产品 SOV / Product SOV", "value": "8.82%"},
            {"label": "Consideration 总量 / Total", "value": "448K"},
            {"label": "全网总曝光 / Total Impressions", "value": "417K"},
            {"label": "互动量 / Engagement", "value": "78.6K"}
        ]
    }
    
    # 修改KPI为菲律宾结构（不要消耗）
    D['kpis'] = [
        {"label": "TikTok Video View SOV", "statusDot": "status-red", "value": "0.42%", "trend": "↓", "trendClass": "trend-down", "sub": "Target / 目标 20% · As of / 截至 10/17", "borderLeft": None, "valueColor": None},
        {"label": "TikTok Search SOV", "statusDot": "status-red", "value": "1.02%", "trend": "↓", "trendClass": "trend-down", "sub": "Target / 目标 13% · As of / 截至 10/17", "borderLeft": None, "valueColor": None},
        {"label": "TikTok曝光量 / TikTok Impressions", "statusDot": "status-red", "value": "417K", "trend": "→", "trendClass": "trend-flat", "sub": "As of / 截至 10/17", "borderLeft": "#ec4899", "valueColor": "#ec4899"},
        {"label": "Meta曝光量 / Meta Impressions", "statusDot": "status-green", "value": "389K", "trend": "↑", "trendClass": "trend-up", "sub": "As of / 截至 10/19", "borderLeft": "#f472b6", "valueColor": "#f472b6"},
        {"label": "YouTube曝光量 / YouTube Impressions", "statusDot": "status-red", "value": "0", "trend": "→", "trendClass": "trend-flat", "sub": "As of / 截至 10/19", "borderLeft": "#a855f7", "valueColor": "#a855f7"},
        {"label": "互动量 / Engagement", "statusDot": "status-red", "value": "78.6K", "trend": "↓", "trendClass": "trend-down", "sub": "Industry share / 行业占比：0.62% · Rank / 排名 #18 · As of / 截至 10/17", "borderLeft": "#ec4899", "valueColor": "#ec4899"}
    ]
    
    # 替换D对象
    new_d = f'const D = {json.dumps(D, ensure_ascii=False, indent=2)};'
    content = re.sub(pattern, new_d, content)

# 写回文件
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Hero and KPI updated to PH structure!")
