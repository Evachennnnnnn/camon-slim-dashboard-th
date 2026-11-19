#!/usr/bin/env python3
"""
泰国 CAMON Slim 看板更新脚本 - 2026-11-13
只更新日更模块，不动周更模块（audience/keywords/paidComments）
不动 challenge/topVideos/kolVideos（无新数据）
"""
import json
import re
import sys

# ====== 读取 index.html ======
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ====== 提取 D 对象（括号匹配） ======
start_marker = 'const D = '
start_idx = content.find(start_marker)
if start_idx == -1:
    print("❌ 找不到 const D =")
    sys.exit(1)

obj_start = start_idx + len(start_marker)
depth = 0
end_idx = None
for i in range(obj_start, len(content)):
    if content[i] == '{':
        depth += 1
    elif content[i] == '}':
        depth -= 1
        if depth == 0:
            end_idx = i + 1
            break

if end_idx is None:
    print("❌ D 对象括号不匹配")
    sys.exit(1)

d_text = content[obj_start:end_idx]
if d_text.rstrip().endswith(';'):
    d_text = d_text.rstrip()[:-1]

D = json.loads(d_text)
print(f"✅ 成功解析 D 对象，当前 updatedDate: {D['updatedDate']}")
print(f"   spend keys: {list(D.get('spend', {}).keys())}")

# ====== 保存原始周更/静态模块（防御性备份） ======
backups = {}
for key in ['audience', 'keywords', 'paidComments', 'challenge', 'topVideos', 'kolVideos']:
    backups[key] = json.dumps(D.get(key, {} if key != 'topVideos' and key != 'kolVideos' else []))

# ====== 新数据 ======

# --- Google SOV (WeCUBT) 追加 11/13 ---
new_google_date = "11/13"
new_google_brand = 2.06
new_google_product = 11.83

if new_google_date not in D['googleSov']['labels']:
    D['googleSov']['labels'].append(new_google_date)
    D['googleSov']['brand'].append(new_google_brand)
    D['googleSov']['product'].append(new_google_product)
    D['competitorCompare']['chartLabels'].append(new_google_date)
    D['competitorCompare']['datasets'][0]['data'].append(new_google_product)
    print(f"  + Google SOV 追加 {new_google_date}: Brand {new_google_brand}%, Product {new_google_product}%")
else:
    print(f"  ~ Google SOV {new_google_date} 已存在，跳过")

# --- TT VV SOV (ae2c02) 追加 11/10 ---
new_tt_vv_date = "11/10"
new_tt_vv = 10.64

if new_tt_vv_date not in D['ttSov']['labels']:
    D['ttSov']['labels'].append(new_tt_vv_date)
    D['ttSov']['vvData'].append(new_tt_vv)
    D['ttSov']['searchData'].append(None)
    print(f"  + TT VV SOV 追加 {new_tt_vv_date}: {new_tt_vv}%")
else:
    print(f"  ~ TT VV SOV {new_tt_vv_date} 已存在，跳过")

# --- Consideration (bAr0rT) 追加 11/9, 11/10 ---
for date_str, brand_val, ind_val in [
    ("11/9", 1587930, 4946837),
    ("11/10", 1641503, 5113146),
]:
    if date_str not in D['consideration']['labels']:
        D['consideration']['labels'].append(date_str)
        D['consideration']['brandData'].append(brand_val)
        D['consideration']['industryData'].append(ind_val)
        print(f"  + Consideration 追加 {date_str}: {brand_val:,}")
    else:
        print(f"  ~ Consideration {date_str} 已存在，跳过")

# --- Spend 追加 11/12 ---
# spend 模块只有 labels, dailySpend, spendProgress, exposureProgress
# dailySpend = TT 每日消耗
new_spend_date = "11/12"
new_tt_daily_spend = 4727.76

if new_spend_date not in D['spend']['labels']:
    D['spend']['labels'].append(new_spend_date)
    D['spend']['dailySpend'].append(new_tt_daily_spend)
    print(f"  + Spend 追加 {new_spend_date}: TT ${new_tt_daily_spend}")
else:
    print(f"  ~ Spend {new_spend_date} 已存在，跳过")

# ====== 计算汇总数据 ======

# TT 累计消耗（10/17 到 11/12）
tt_spend_all = [
    0, 0, 96.36, 423.32, 466.19, 1005.47, 1071.55, 1350.02, 1405.59, 1050.79,
    1820.94, 2830.39, 3060.28, 1961.25, 2387.24, 2164.64, 32707.54, 2766.45,
    5071.73, 6810.92, 35925.39, 4641.47, 4451.61, 2323.39, 3496.49, 4211.01, 4727.76
]
tt_cumulative_spend = sum(tt_spend_all)
tt_latest_daily = 4727.76

# TT 总曝光（到 11/10，11/11-12 无曝光数据）
tt_impressions = [
    417245, 512731, 1058612, 1980509, 2304924, 4160130, 4104540, 5142215,
    4945262, 4493444, 6665384, 8508983, 7978743, 5313511, 7226108, 10589341,
    16758489, 10552314, 19134836, 23463392, 45831076, 18704152, 16891273,
    10283289, 12229637
]
tt_total_impressions = sum(tt_impressions)

# Meta 总曝光（到 11/12）
meta_impressions = [
    389920, 1324958, 1615904, 2791710, 2432241, 3800623, 4061030, 4418270,
    3907302, 3967229, 4332156, 4024103, 5026959, 3616780, 6556499, 7312020,
    8654870, 16037402, 4933802, 5375550, 5602967, 2470857, 3465317, 4437635, 5746827
]
meta_total_impressions = sum(meta_impressions)

# YT 总曝光（到 11/12）
yt_impressions = [
    0, 0, 0, 0, 0, 0, 0, 67031, 1454760, 1763049, 1670956, 1713798, 1573422,
    0, 1303401, 5173269, 5780003, 5292973, 5367570, 5122405, 14572, 85893,
    112207, 111709
]
yt_total_impressions = sum(yt_impressions)

total_impressions = tt_total_impressions + meta_total_impressions + yt_total_impressions
total_impressions_M = total_impressions / 1_000_000

# Meta 最新
meta_latest_daily = 2454.91
meta_latest_impressions = 5746827

# YT 最新
yt_latest_daily = 46.44
yt_latest_impressions = 111709

# Consideration 最新（11/10）
consideration_latest = 1641503
consideration_latest_M = consideration_latest / 1_000_000

# TT VV SOV 最新（11/10）
tt_vv_latest = 10.64
# TT Search SOV 最新（11/8）
tt_search_latest = 1.33

# Google SOV 最新（11/13）
google_brand_latest = 2.06
google_product_latest = 11.83

# 预算进度
budget_total = 450000

print(f"\n📊 汇总计算：")
print(f"  TT 累计消耗: ${tt_cumulative_spend:,.2f}")
print(f"  TT 总曝光: {tt_total_impressions/1_000_000:.2f}M (to 11/10)")
print(f"  Meta 总曝光: {meta_total_impressions/1_000_000:.2f}M (to 11/12)")
print(f"  YT 总曝光: {yt_total_impressions/1_000_000:.2f}M (to 11/12)")
print(f"  全网总曝光: {total_impressions_M:.2f}M")
print(f"  Consideration: {consideration_latest:,} (11/10)")

# ====== 更新 D 对象各模块 ======

# --- updatedDate / dataAsOf ---
D['updatedDate'] = "2026-11-13"
D['dataAsOf'] = "11/13"

# --- alertBanner ---
D['alertBanner'] = (
    f"数据已更新至 11/13。Google Product SOV {google_product_latest}% (11/13)，"
    f"TT VV SOV {tt_vv_latest}% (11/10)，TT Search SOV {tt_search_latest}% (11/8)，"
    f"全网总曝光 {total_impressions_M:.2f}M (TT to 11/10, Meta/YT to 11/12)，"
    f"Consideration {consideration_latest_M:.2f}M (11/10)。"
)

# --- hero ---
D['hero']['desc'] = (
    f"Google Product SOV {google_product_latest}% (11/13), "
    f"TT VV SOV {tt_vv_latest}% (11/10), "
    f"全网总曝光 {total_impressions_M:.2f}M (TT to 11/10, Meta/YT to 11/12), "
    f"Consideration {consideration_latest_M:.2f}M (11/10)."
)
D['hero']['stats'] = [
    {"label": "Google Product SOV", "value": f"{google_product_latest}%"},
    {"label": "TT VV SOV", "value": f"{tt_vv_latest}%"},
    {"label": "全网总曝光 / Total Impressions", "value": f"{total_impressions_M:.2f}M"},
    {"label": "Consideration 总量 / Total", "value": f"{consideration_latest_M:.2f}M"}
]

# --- kpis ---
prev_vv = 8.85
vv_trend = "↑" if tt_vv_latest > prev_vv else "↓" if tt_vv_latest < prev_vv else "→"
vv_trend_class = "trend-up" if tt_vv_latest > prev_vv else "trend-down" if tt_vv_latest < prev_vv else "trend-flat"

prev_brand = 2.05
brand_trend = "↑" if google_brand_latest > prev_brand else "↓" if google_brand_latest < prev_brand else "→"
brand_trend_class = "trend-up" if google_brand_latest > prev_brand else "trend-down" if google_brand_latest < prev_brand else "trend-flat"

prev_product = 10.1
product_trend = "↑" if google_product_latest > prev_product else "↓" if google_product_latest < prev_product else "→"
product_trend_class = "trend-up" if google_product_latest > prev_product else "trend-down" if google_product_latest < prev_product else "trend-flat"

D['kpis'] = [
    {
        "label": "TikTok Video View SOV",
        "statusDot": "status-red",
        "value": f"{tt_vv_latest}%",
        "trend": vv_trend,
        "trendClass": vv_trend_class,
        "sub": "Target / 目标 20% · As of / 截至 11/10",
        "borderLeft": None,
        "valueColor": None
    },
    {
        "label": "TikTok Search SOV",
        "statusDot": "status-red",
        "value": f"{tt_search_latest}%",
        "trend": "→",
        "trendClass": "trend-flat",
        "sub": "Target / 目标 13% · As of / 截至 11/8",
        "borderLeft": None,
        "valueColor": None
    },
    {
        "label": "Google Brand SOV",
        "statusDot": "status-green",
        "value": f"{google_brand_latest}%",
        "trend": brand_trend,
        "trendClass": brand_trend_class,
        "sub": "As of / 截至 11/13",
        "borderLeft": "#10b981",
        "valueColor": "#10b981"
    },
    {
        "label": "Google Product SOV",
        "statusDot": "status-green",
        "value": f"{google_product_latest}%",
        "trend": product_trend,
        "trendClass": product_trend_class,
        "sub": "As of / 截至 11/13",
        "borderLeft": "#10b981",
        "valueColor": "#10b981"
    },
    {
        "label": "TT 消耗 / TT Spend",
        "statusDot": "status-green",
        "value": f"{tt_latest_daily:,.2f}",
        "trend": "↑",
        "trendClass": "trend-up",
        "sub": f"累计 / Cumulative {tt_cumulative_spend:,.2f} · As of / 截至 11/12",
        "borderLeft": "#10b981",
        "valueColor": "#10b981"
    },
    {
        "label": "Meta 消耗 / Meta Spend",
        "statusDot": "status-green",
        "value": f"{meta_latest_daily:,.2f}",
        "trend": "↑",
        "trendClass": "trend-up",
        "sub": f"Meta Impressions {meta_latest_impressions/1_000_000:.2f}M · As of / 截至 11/12",
        "borderLeft": "#10b981",
        "valueColor": "#10b981"
    }
]

# --- overview ---
D['overview'] = [
    {"status": "green", "metric": "Google 品牌 SOV / Brand SOV", "current": f"{google_brand_latest}%", "target": "—", "date": "11/13"},
    {"status": "green", "metric": "Google 产品 SOV / Product SOV", "current": f"{google_product_latest}%", "target": "—", "date": "11/13"},
    {"status": "red", "metric": "TikTok VV SOV", "current": f"{tt_vv_latest}%", "target": "20%", "date": "11/10"},
    {"status": "red", "metric": "TikTok Search SOV", "current": f"{tt_search_latest}%", "target": "13%", "date": "11/8"},
    {"status": "green", "metric": "TT 消耗 / TT Spend", "current": f"{tt_latest_daily:,.2f}", "target": "—", "date": "11/12"},
    {"status": "green", "metric": "Meta 消耗 / Meta Spend", "current": f"{meta_latest_daily:,.2f}", "target": "—", "date": "11/12"},
    {"status": "green", "metric": "Meta 曝光 / Meta Impressions", "current": f"{meta_latest_impressions/1_000_000:.2f}M", "target": "—", "date": "11/12"},
    {"status": "green", "metric": "YouTube 消耗 / YT Spend", "current": f"{yt_latest_daily:,.2f}", "target": "—", "date": "11/12"},
    {"status": "green", "metric": "YouTube 曝光 / YT Impressions", "current": f"{yt_latest_impressions/1000:.0f}K", "target": "—", "date": "11/12"},
    {"status": "green", "metric": "Consideration 总量 / Total", "current": f"{consideration_latest_M:.2f}M", "target": "—", "date": "11/10"}
]

# --- googleSov notes ---
D['googleSov']['brandNote'] = f"Brand SOV latest {google_brand_latest}% (11/13) / 品牌 SOV 最新 {google_brand_latest}%（11/13）"
D['googleSov']['productNote'] = f"Product SOV latest {google_product_latest}% (11/13) / 产品 SOV 最新 {google_product_latest}%（11/13）"

# --- competitorCompare ---
D['competitorCompare']['note'] = (
    f"Google Trends 对比关键词 / Comparison: CAMON Slim vs OPPO Reno 16 F, VIVO V80 Lite, Redmi Note 17 Pro · 截至 11/13"
)
D['competitorCompare']['table'][0]['sov'] = f"{google_product_latest}%"
D['competitorCompare']['table'][0]['sovColor'] = "#10b981"
D['competitorCompare']['table'][0]['trend'] = product_trend
D['competitorCompare']['table'][0]['trendClass'] = product_trend_class
D['competitorCompare']['insight'] = (
    f"💡 竞品对比组合：CAMON Slim vs OPPO Reno 16 F / VIVO V80 Lite / Redmi Note 17 Pro。"
    f"CAMON Slim 产品 SOV 最新 {google_product_latest}%（11/13）。"
    f"竞品数据来自 Google Trends 相对搜索热度，反映搜索声量占比。/ "
    f"Competitor set: CAMON Slim vs OPPO Reno 16 F / VIVO V80 Lite / Redmi Note 17 Pro. "
    f"Product SOV latest {google_product_latest}% (11/13)."
)

# --- ttSov note ---
D['ttSov']['note'] = (
    f"VV SOV latest {tt_vv_latest}% (11/10); Search SOV latest {tt_search_latest}% (11/8) / "
    f"VV SOV 最新 {tt_vv_latest}%（11/10）；Search SOV 最新 {tt_search_latest}%（11/8）"
)

# --- consideration note ---
D['consideration']['note'] = (
    f"Brand Consideration latest {consideration_latest/1_000_000:.2f}M (11/10). / "
    f"本品牌 Consideration 最新 {consideration_latest/1_000_000:.2f}M（11/10）。"
)

# --- spend 重新计算进度 ---
tt_target_impressions = 167_000_000
spend_progress_list = []
exposure_progress_list = []
cumulative_spend = 0
cumulative_imp = 0

tt_daily_spend = [
    0, 0, 96.36, 423.32, 466.19, 1005.47, 1071.55, 1350.02, 1405.59, 1050.79,
    1820.94, 2830.39, 3060.28, 1961.25, 2387.24, 2164.64, 32707.54, 2766.45,
    5071.73, 6810.92, 35925.39, 4641.47, 4451.61, 2323.39, 3496.49, 4211.01, 4727.76
]
tt_daily_imp = [
    417245, 512731, 1058612, 1980509, 2304924, 4160130, 4104540, 5142215,
    4945262, 4493444, 6665384, 8508983, 7978743, 5313511, 7226108, 10589341,
    16758489, 10552314, 19134836, 23463392, 45831076, 18704152, 16891273,
    10283289, 12229637, None, None
]

for i in range(len(D['spend']['labels'])):
    if i < len(tt_daily_spend):
        cumulative_spend += tt_daily_spend[i]
    spend_progress_list.append(round(cumulative_spend / budget_total * 100, 4) if budget_total > 0 else 0)

    if i < len(tt_daily_imp) and tt_daily_imp[i] is not None:
        cumulative_imp += tt_daily_imp[i]
    exposure_progress_list.append(round(cumulative_imp / tt_target_impressions * 100, 4) if tt_target_impressions > 0 else 0)

D['spend']['spendProgress'] = spend_progress_list
D['spend']['exposureProgress'] = exposure_progress_list

# ====== 防御性检查：周更/静态模块未被修改 ======
for key in ['audience', 'keywords', 'paidComments', 'challenge', 'topVideos', 'kolVideos']:
    current = json.dumps(D.get(key, {} if key not in ['topVideos', 'kolVideos'] else []))
    assert current == backups[key], f"❌ {key} 被意外修改！"
print("\n✅ 周更模块和挑战赛/TopVideos/KOL 数据完整无损")

# ====== 数组长度一致性检查 ======
assert len(D['googleSov']['labels']) == len(D['googleSov']['brand']) == len(D['googleSov']['product']), \
    f"❌ googleSov 长度不匹配: labels={len(D['googleSov']['labels'])}, brand={len(D['googleSov']['brand'])}, product={len(D['googleSov']['product'])}"
assert len(D['competitorCompare']['chartLabels']) == len(D['competitorCompare']['datasets'][0]['data']), \
    f"❌ competitorCompare 长度不匹配"
assert len(D['ttSov']['labels']) == len(D['ttSov']['vvData']) == len(D['ttSov']['searchData']), \
    f"❌ ttSov 长度不匹配: labels={len(D['ttSov']['labels'])}, vv={len(D['ttSov']['vvData'])}, search={len(D['ttSov']['searchData'])}"
assert len(D['consideration']['labels']) == len(D['consideration']['brandData']) == len(D['consideration']['industryData']), \
    f"❌ consideration 长度不匹配"
assert len(D['spend']['labels']) == len(D['spend']['dailySpend']) == len(D['spend']['spendProgress']) == len(D['spend']['exposureProgress']), \
    f"❌ spend 长度不匹配: labels={len(D['spend']['labels'])}, daily={len(D['spend']['dailySpend'])}, progress={len(D['spend']['spendProgress'])}, exposure={len(D['spend']['exposureProgress'])}"
print("✅ 所有数组长度一致")

# ====== 生成新的 D 对象文本并替换 ======
new_d_text = json.dumps(D, ensure_ascii=False, indent=2)
new_content = content[:obj_start] + new_d_text + content[end_idx:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"\n✅ index.html 已更新！")
print(f"  updatedDate: {D['updatedDate']}")
print(f"  Google Brand SOV: {google_brand_latest}% (11/13)")
print(f"  Google Product SOV: {google_product_latest}% (11/13)")
print(f"  TT VV SOV: {tt_vv_latest}% (11/10)")
print(f"  TT Search SOV: {tt_search_latest}% (11/8)")
print(f"  Consideration: {consideration_latest_M:.2f}M (11/10)")
print(f"  全网总曝光: {total_impressions_M:.2f}M")
print(f"  TT 累计消耗: ${tt_cumulative_spend:,.2f}")
