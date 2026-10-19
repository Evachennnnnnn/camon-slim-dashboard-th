import json
import re

# 从飞书表格读取的最新泰国数据
D = {
    "updatedDate": "2026-10-19",
    "dataAsOf": "10/19",
    
    "alertBanner": "数据已更新至 10/19。Google Brand SOV 1.63%，Product SOV 8.82%，TT VV SOV 0.42%，TT Search SOV 1.05%，Consideration 448K。/ Data updated to 10/19. Google Brand SOV 1.63%, Product SOV 8.82%, TT VV SOV 0.42%, TT Search SOV 1.05%, Consideration 448K.",
    
    "hero": {
        "desc": "Google Product SOV 8.82% (10/19), Consideration 448K (10/17), TT VV SOV 0.42% (10/17), TT Search SOV 1.05% (10/17). / Google 产品 SOV 8.82%，Consideration 总量 448K，TT VV SOV 0.42%，TT Search SOV 1.05%。",
        "stats": [
            {"label": "Google 产品 SOV / Product SOV", "value": "8.82%"},
            {"label": "Consideration 总量 / Total", "value": "448K"},
            {"label": "TT VV SOV", "value": "0.42%"},
            {"label": "TT Search SOV", "value": "1.05%"}
        ]
    },
    
    "kpis": [
        {"label": "TikTok Video View SOV", "statusDot": "status-red", "value": "0.42%", "trend": "↓", "trendClass": "trend-down", "sub": "Target / 目标 20% · As of / 截至 10/17", "borderLeft": None, "valueColor": None},
        {"label": "TikTok Search SOV", "statusDot": "status-red", "value": "1.05%", "trend": "↓", "trendClass": "trend-down", "sub": "Target / 目标 13% · As of / 截至 10/17", "borderLeft": None, "valueColor": None},
        {"label": "Google Brand SOV", "statusDot": "status-red", "value": "1.63%", "trend": "→", "trendClass": "trend-flat", "sub": "As of / 截至 10/19", "borderLeft": "#f472b6", "valueColor": "#f472b6"},
        {"label": "Google Product SOV", "statusDot": "status-red", "value": "8.82%", "trend": "↓", "trendClass": "trend-down", "sub": "As of / 截至 10/19", "borderLeft": "#ef4444", "valueColor": "#ef4444"},
        {"label": "Consideration", "statusDot": "status-red", "value": "448K", "trend": "↓", "trendClass": "trend-down", "sub": "Industry avg / 行业均值 4.23M · As of / 截至 10/17", "borderLeft": "#a855f7", "valueColor": "#a855f7"},
        {"label": "互动量 / Engagement", "statusDot": "status-red", "value": "78.6K", "trend": "↓", "trendClass": "trend-down", "sub": "Industry rank / 行业排名 #18 · As of / 截至 10/17", "borderLeft": "#ec4899", "valueColor": "#ec4899"}
    ],
    
    "overview": [
        {"status": "red", "metric": "Google 品牌 SOV / Brand SOV", "current": "1.63%", "target": "—", "date": "10/19"},
        {"status": "red", "metric": "Google 产品 SOV / Product SOV", "current": "8.82%", "target": "—", "date": "10/19"},
        {"status": "red", "metric": "TikTok VV SOV", "current": "0.42%", "target": "20%", "date": "10/17"},
        {"status": "red", "metric": "TikTok Search SOV", "current": "1.05%", "target": "13%", "date": "10/17"},
        {"status": "red", "metric": "互动量行业排名 / Engagement Rank", "current": "#18", "target": "Top 3", "date": "10/17"},
        {"status": "red", "metric": "Consideration 总量 / Total", "current": "448K", "target": "—", "date": "10/17"}
    ],
    
    "topVideos": [],
    "kolVideos": [],
    
    "googleSov": {
        "labels": ["10/19"],
        "brand": [1.63],
        "product": [8.82],
        "brandNote": "Brand SOV latest 1.63% (10/19) / 品牌 SOV 最新 1.63%（10/19）",
        "productNote": "Product SOV latest 8.82% (10/19) / 产品 SOV 最新 8.82%（10/19）"
    },
    
    "competitorCompare": {
        "note": "Google Trends 对比关键词 / Comparison: CAMON Slim vs OPPO Reno 16 F, VIVO V80 Lite, Redmi Note 17 Pro · 截至 10/19",
        "trendLink": "https://trends.google.com/trends/explore?date=today%201-m&geo=TH&q=CAMON%20Slim,OPPO%20Reno%2016%20F,VIVO%20V80%20Lite,Redmi%20Note%2017%20Pro&hl=en",
        "dailyLinks": [],
        "chartLabels": ["10/19"],
        "datasets": [
            {"label": "CAMON Slim (TECNO)", "data": [8.82], "borderColor": "#10b981", "bg": "rgba(16,185,129,.15)", "fill": True, "dash": None, "width": 3, "pointRadius": 5},
            {"label": "OPPO Reno 16 F", "data": [], "borderColor": "#a855f7", "bg": "rgba(168,85,247,.05)", "fill": False, "dash": [4,2], "width": None, "pointRadius": 3},
            {"label": "VIVO V80 Lite", "data": [], "borderColor": "#2563eb", "bg": "rgba(37,99,235,.05)", "fill": False, "dash": [4,2], "width": None, "pointRadius": 3},
            {"label": "Redmi Note 17 Pro", "data": [], "borderColor": "#ea580c", "bg": "rgba(234,88,12,.05)", "fill": False, "dash": [4,2], "width": None, "pointRadius": 3}
        ],
        "table": [
            {"product": "CAMON Slim", "brand": "TECNO", "brandBold": True, "brandColor": "#10b981", "sov": "8.82%", "sovColor": "#ef4444", "sovBold": True, "sovSize": "16px", "trend": "↓", "trendClass": "trend-down", "highlight": True},
            {"product": "OPPO Reno 16 F", "brand": "OPPO", "brandBold": False, "brandColor": None, "sov": "—", "sovColor": "#6b7280", "sovBold": False, "sovSize": None, "trend": "→", "trendClass": "trend-flat", "highlight": False},
            {"product": "VIVO V80 Lite", "brand": "vivo", "brandBold": False, "brandColor": None, "sov": "—", "sovColor": "#6b7280", "sovBold": False, "sovSize": None, "trend": "→", "trendClass": "trend-flat", "highlight": False},
            {"product": "Redmi Note 17 Pro", "brand": "Xiaomi", "brandBold": False, "brandColor": None, "sov": "—", "sovColor": "#6b7280", "sovBold": False, "sovSize": None, "trend": "→", "trendClass": "trend-flat", "highlight": False}
        ],
        "insight": "💡 竞品对比组合：CAMON Slim vs OPPO Reno 16 F / VIVO V80 Lite / Redmi Note 17 Pro。CAMON Slim 产品 SOV 最新 8.82%（10/19）。竞品数据来自 Google Trends 相对搜索热度，反映搜索声量占比。/ Competitor set: CAMON Slim vs OPPO Reno 16 F / VIVO V80 Lite / Redmi Note 17 Pro. Product SOV latest 8.82% (10/19). Competitor data from Google Trends relative search interest."
    },
    
    "ttSov": {
        "labels": ["10/17"],
        "vvData": [0.42],
        "searchData": [1.05],
        "note": "VV SOV latest 0.42% (10/17); Search SOV latest 1.05% (10/17) / VV SOV 最新 0.42%（10/17）；Search SOV 最新 1.05%（10/17）"
    },
    
    "consideration": {
        "labels": ["10/17"],
        "brandData": [448555],
        "industryData": [4225531],
        "note": "Brand Consideration latest 448K (10/17). / 本品牌 Consideration 最新 448K（10/17）。"
    },
    
    "spend": {
        "labels": ["10/17"],
        "dailySpend": [0],
        "spendProgress": [0],
        "exposureProgress": [0.06]
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

print("✅ SOV data updated!")
print(f"Google Brand SOV: {D['googleSov']['brand'][0]}%")
print(f"Google Product SOV: {D['googleSov']['product'][0]}%")
