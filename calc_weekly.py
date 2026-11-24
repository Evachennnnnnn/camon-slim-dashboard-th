import json

# ============================================================
# 1. AUDIENCE INSIGHT - 从飞书 QozPbw 精确数据
# ============================================================
# 平台总计（从飞书数据提取）
audience = {
    "platformMetrics": [
        {"label": "TikTok 消耗", "value": "$169,684", "bg": "rgba(0,242,234,.12)", "border": "#00c4be", "color": "#0f766e"},
        {"label": "TikTok CPM", "value": "$0.57", "bg": "rgba(0,242,234,.12)", "border": "#00c4be", "color": "#0f766e"},
        {"label": "Meta 消耗", "value": "$58,303", "bg": "rgba(24,119,242,.12)", "border": "#1565c0", "color": "#1565c0"},
        {"label": "Meta CPM", "value": "$0.35", "bg": "rgba(24,119,242,.12)", "border": "#1565c0", "color": "#1565c0"},
        {"label": "Line 消耗", "value": "$55,285", "bg": "rgba(255,152,0,.12)", "border": "#f57c00", "color": "#e65100"},
        {"label": "Line CPM", "value": "$0.25", "bg": "rgba(255,152,0,.12)", "border": "#f57c00", "color": "#e65100"},
        {"label": "Google 消耗", "value": "$14,291", "bg": "rgba(234,67,53,.12)", "border": "#c5221f", "color": "#c5221f"},
        {"label": "Google CPM", "value": "$0.20", "bg": "rgba(234,67,53,.12)", "border": "#c5221f", "color": "#c5221f"},
        {"label": "Grand Total", "value": "$297,562", "bg": "rgba(16,185,129,.12)", "border": "#059669", "color": "#059669"},
        {"label": "Avg CPM", "value": "$0.39", "bg": "rgba(16,185,129,.12)", "border": "#059669", "color": "#059669"}
    ],
    "ttAudience": [
        {"name": "Social & Lifestyle", "cost": "$34,675", "cpm": "$0.35", "cpe": "$0.16", "vtr": "97.3%"},
        {"name": "Rational Buyer", "cost": "$8,668", "cpm": "$0.35", "cpe": "$0.15", "vtr": "97.4%"},
        {"name": "Side Hustle / Ambitious", "cost": "$8,422", "cpm": "$0.36", "cpe": "$0.16", "vtr": "97.2%"},
        {"name": "RMKT & Lookalike", "cost": "$7,628", "cpm": "$0.36", "cpe": "$0.14", "vtr": "95.6%"},
        {"name": "Tech Upgrade", "cost": "$5,545", "cpm": "$0.37", "cpe": "$0.13", "vtr": "95.2%"},
        {"name": "Urban Social Upgraders", "cost": "$4,816", "cpm": "$0.36", "cpe": "$0.15", "vtr": "96.8%"},
        {"name": "Competitor", "cost": "$4,095", "cpm": "$0.48", "cpe": "$0.13", "vtr": "96.1%"}
    ],
    "fbigAudience": [
        {"name": "Tech Upgrade", "cost": "$11,765", "cpm": "$0.31", "cpe": "$0.01", "vtr": "3.1%"},
        {"name": "Social & Lifestyle", "cost": "$8,892", "cpm": "$0.32", "cpe": "$0.01", "vtr": "3.6%"},
        {"name": "Broad", "cost": "$5,482", "cpm": "$0.31", "cpe": "$0.09", "vtr": "0.3%"},
        {"name": "Rational Buyer", "cost": "$5,420", "cpm": "$0.31", "cpe": "$0.01", "vtr": "3.0%"},
        {"name": "Side Hustle / Ambitious", "cost": "$5,360", "cpm": "$0.31", "cpe": "$0.01", "vtr": "3.6%"},
        {"name": "Competitor", "cost": "$5,014", "cpm": "$0.31", "cpe": "$0.01", "vtr": "2.7%"},
        {"name": "RMKT & Lookalike", "cost": "$3,619", "cpm": "$0.30", "cpe": "$0.01", "vtr": "2.8%"},
        {"name": "Urban Social Upgraders", "cost": "$1,661", "cpm": "$0.31", "cpe": "$0.01", "vtr": "4.0%"}
    ]
}

print("✅ Audience Insight 精确数据准备完成")
print(f"   Grand Total: $297,562")
print(f"   TT: $169,684 | Meta: $58,303 | Line: $55,285 | Google: $14,291")

# 输出 JSON 供 JS 使用
with open('/tmp/weekly_audience.json', 'w') as f:
    json.dump(audience, f)

print("\n✅ 已写入 /tmp/weekly_audience.json")
