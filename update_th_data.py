import json
import re

# 从飞书表格读取的最新泰国数据（截至10/21）
D = {
    "updatedDate": "2026-10-21",
    "dataAsOf": "10/21",
    
    "alertBanner": "数据已更新至 10/21。Google Brand SOV 1.64%，TT Search SOV 1.11%，Meta 曝光 1.32M，Consideration 452K。/ Data updated to 10/21. Google Brand SOV 1.64%, TT Search SOV 1.11%, Meta Impressions 1.32M, Consideration 452K.",
    
    "hero": {
        "desc": "Google Brand SOV 1.64% (10/21), TT Search SOV 1.11% (10/18), Meta Impressions 1.32M (10/20), Consideration 452K (10/18). / Google 品牌 SOV 1.64%，TT Search SOV 1.11%，Meta 曝光 1.32M，Consideration 452K。",
        "stats": [
            {"label": "Google Brand SOV", "value": "1.64%"},
            {"label": "TT Search SOV", "value": "1.11%"},
            {"label": "Meta 曝光 / Meta Impressions", "value": "1.32M"},
            {"label": "Consideration 总量 / Total", "value": "452K"}
        ]
    },
    
    "kpis": [
        {"label": "TikTok Video View SOV", "statusDot": "status-red", "value": "0.42%", "trend": "→", "trendClass": "trend-flat", "sub": "Target / 目标 20% · As of / 截至 10/17", "borderLeft": None, "valueColor": None},
        {"label": "TikTok Search SOV", "statusDot": "status-red", "value": "1.11%", "trend": "↑", "trendClass": "trend-up", "sub": "Target / 目标 13% · As of / 截至 10/18", "borderLeft": None, "valueColor": None},
        {"label": "Google Brand SOV", "statusDot": "status-red", "value": "1.64%", "trend": "→", "trendClass": "trend-flat", "sub": "As of / 截至 10/21", "borderLeft": "#f472b6", "valueColor": "#f472b6"},
        {"label": "Google Product SOV", "statusDot": "status-red", "value": "0%", "trend": "↓", "trendClass": "trend-down", "sub": "As of / 截至 10/21", "borderLeft": "#ef4444", "valueColor": "#ef4444"},
        {"label": "Meta 曝光 / Meta Impressions", "statusDot": "status-green", "value": "1.32M", "trend": "↑", "trendClass": "trend-up", "sub": "Meta Spend 356.71 (10/20) · As of / 截至 10/20", "borderLeft": "#10b981", "valueColor": "#10b981"},
        {"label": "Consideration", "statusDot": "status-red", "value": "452K", "trend": "↑", "trendClass": "trend-up", "sub": "Industry avg / 行业均值 4.22M · As of / 截至 10/18", "borderLeft": "#a855f7", "valueColor": "#a855f7"}
    ],
    
    "overview": [
        {"status": "red", "metric": "Google 品牌 SOV / Brand SOV", "current": "1.64%", "target": "—", "date": "10/21"},
        {"status": "red", "metric": "Google 产品 SOV / Product SOV", "current": "0%", "target": "—", "date": "10/21"},
        {"status": "red", "metric": "TikTok VV SOV", "current": "0.42%", "target": "20%", "date": "10/17"},
        {"status": "red", "metric": "TikTok Search SOV", "current": "1.11%", "target": "13%", "date": "10/18"},
        {"status": "green", "metric": "Meta 曝光 / Meta Impressions", "current": "1.32M", "target": "—", "date": "10/20"},
        {"status": "green", "metric": "Meta 消耗 / Meta Spend", "current": "356.71", "target": "—", "date": "10/20"},
        {"status": "red", "metric": "Consideration 总量 / Total", "current": "452K", "target": "—", "date": "10/18"},
        {"status": "red", "metric": "互动量行业排名 / Engagement Rank", "current": "#18", "target": "Top 3", "date": "10/17"},
        {"status": "red", "metric": "TT 累计消耗 / TT Cumulative Spend", "current": "633.89", "target": "—", "date": "10/20"}
    ],
    
    "topVideos": [],
    "kolVideos": [],
    
    "googleSov": {
        "labels": ["10/19", "10/20", "10/21"],
        "brand": [1.63, 1.64, 1.64],
        "product": [8.82, 0, 0],
        "brandNote": "Brand SOV latest 1.64% (10/21) / 品牌 SOV 最新 1.64%（10/21）",
        "productNote": "Product SOV latest 0% (10/21) / 产品 SOV 最新 0%（10/21）"
    },
    
    "competitorCompare": {
        "note": "Google Trends 对比关键词 / Comparison: CAMON Slim vs OPPO Reno 16 F, VIVO V80 Lite, Redmi Note 17 Pro · 截至 10/21",
        "trendLink": "https://trends.google.com/trends/explore?date=today%201-m&geo=TH&q=CAMON%20Slim,OPPO%20Reno%2016%20F,VIVO%20V80%20Lite,Redmi%20Note%2017%20Pro&hl=en",
        "dailyLinks": [],
        "chartLabels": ["10/19", "10/20", "10/21"],
        "datasets": [
            {"label": "CAMON Slim (TECNO)", "data": [8.82, 0, 0], "borderColor": "#10b981", "bg": "rgba(16,185,129,.15)", "fill": True, "dash": None, "width": 3, "pointRadius": 5},
            {"label": "OPPO Reno 16 F", "data": [], "borderColor": "#a855f7", "bg": "rgba(168,85,247,.05)", "fill": False, "dash": [4,2], "width": None, "pointRadius": 3},
            {"label": "VIVO V80 Lite", "data": [], "borderColor": "#2563eb", "bg": "rgba(37,99,235,.05)", "fill": False, "dash": [4,2], "width": None, "pointRadius": 3},
            {"label": "Redmi Note 17 Pro", "data": [], "borderColor": "#ea580c", "bg": "rgba(234,88,12,.05)", "fill": False, "dash": [4,2], "width": None, "pointRadius": 3}
        ],
        "table": [
            {"product": "CAMON Slim", "brand": "TECNO", "brandBold": True, "brandColor": "#10b981", "sov": "0%", "sovColor": "#ef4444", "sovBold": True, "sovSize": "16px", "trend": "↓", "trendClass": "trend-down", "highlight": True},
            {"product": "OPPO Reno 16 F", "brand": "OPPO", "brandBold": False, "brandColor": None, "sov": "—", "sovColor": "#6b7280", "sovBold": False, "sovSize": None, "trend": "→", "trendClass": "trend-flat", "highlight": False},
            {"product": "VIVO V80 Lite", "brand": "vivo", "brandBold": False, "brandColor": None, "sov": "—", "sovColor": "#6b7280", "sovBold": False, "sovSize": None, "trend": "→", "trendClass": "trend-flat", "highlight": False},
            {"product": "Redmi Note 17 Pro", "brand": "Xiaomi", "brandBold": False, "brandColor": None, "sov": "—", "sovColor": "#6b7280", "sovBold": False, "sovSize": None, "trend": "→", "trendClass": "trend-flat", "highlight": False}
        ],
        "insight": "💡 竞品对比组合：CAMON Slim vs OPPO Reno 16 F / VIVO V80 Lite / Redmi Note 17 Pro。CAMON Slim 产品 SOV 从 10/19 的 8.82% 跌至 0%，搜索热度严重不足。/ Competitor set: CAMON Slim vs OPPO Reno 16 F / VIVO V80 Lite / Redmi Note 17 Pro. Product SOV dropped from 8.82% to 0%, search volume critically low."
    },
    
    "ttSov": {
        "labels": ["10/17", "10/18"],
        "vvData": [0.42, None],
        "searchData": [1.02, 1.11],
        "note": "VV SOV latest 0.42% (10/17, 10/18-21 exposure data pending); Search SOV latest 1.11% (10/18) / VV SOV 最新 0.42%（10/17，10/18-21曝光数据待补录）；Search SOV 最新 1.11%（10/18）"
    },
    
    "consideration": {
        "labels": ["10/17", "10/18"],
        "brandData": [448555, 451538],
        "industryData": [4225531, 4219704],
        "note": "Brand Consideration latest 452K (10/18). / 本品牌 Consideration 最新 452K（10/18）。"
    },
    
    "spend": {
        "labels": ["10/19", "10/20"],
        "dailySpend": [308.32, 780.03],
        "spendProgress": [0.18, 0.54],
        "exposureProgress": [0.06, 0.06],
        "metaSpend": [97.75, 356.71],
        "metaImpressions": [389920, 1324958],
        "ttSpend": [210.57, 423.32],
        "ytSpend": [0, 0]
    },
    
    "audience": {
        "platformMetrics": [],
        "ttAudience": [],
        "fbigAudience": []
    },
    
    "keywords": {
        "window": "Data window / 时间窗: 待更新 · Brand / 品牌: Tecno · Source: TikTok Keyword Analysis",
        "stats": [],
        "breakdown": [],
        "topVideos": [],
        "insights": []
    },
    
    "paidComments": {
        "window": "Data window / 时间窗: 待更新 · Source: TikTok Paid Comment export",
        "stats": [],
        "audience": [],
        "materials": [],
        "insights": []
    }
}

# 读取index.html
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 替换D对象
pattern = r'const D = \{[\s\S]*?\n\};'
new_d = f'const D = {json.dumps(D, ensure_ascii=False, indent=2)};'
content = re.sub(pattern, new_d, content)

# 写回文件
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Dashboard updated to 10/21!")
print(f"Google Brand SOV: {D['googleSov']['brand'][-1]}%")
print(f"Google Product SOV: {D['googleSov']['product'][-1]}%")
print(f"TT VV SOV: 0.42% (10/17)")
print(f"TT Search SOV: 1.11% (10/18)")
print(f"Meta Impressions: 1.32M (10/20)")
print(f"Consideration: 452K (10/18)")
