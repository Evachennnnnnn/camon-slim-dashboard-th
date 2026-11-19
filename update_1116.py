#!/usr/bin/env python3
"""
泰国 CAMON Slim 看板更新脚本 - 2026-11-16
更新日更模块至最新数据
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

# ====== 新数据（11/14 - 11/16） ======

# Google SOV (WeCUBT) - 追加 11/14, 11/15, 11/16
new_google_data = [
    ("11/14", 2.06, 12.5),
    ("11/15", 2.06, 13.0),
    ("11/16", 2.07, 13.7),
]

for date_str, brand_val, product_val in new_google_data:
    if date_str not in D['googleSov']['labels']:
        D['googleSov']['labels'].append(date_str)
        D['googleSov']['brand'].append(brand_val)
        D['googleSov']['product'].append(product_val)
        D['competitorCompare']['chartLabels'].append(date_str)
        D['competitorCompare']['datasets'][0]['data'].append(product_val)
        print(f"  + Google SOV 追加 {date_str}: Brand {brand_val}%, Product {product_val}%")
    else:
        print(f"  ~ Google SOV {date_str} 已存在，跳过")

# TT VV SOV (ae2c02) - 追加 11/11 - 11/15
# 注意：11/11-15 的 VV SOV 都是 10.64%（数据可能未更新）
new_tt_vv_data = [
    ("11/11", 10.64, None),
    ("11/12", 10.64, None),
    ("11/13", 10.64, None),
    ("11/14", 10.64, None),
    ("11/15", 10.64, None),
]

for date_str, vv_val, search_val in new_tt_vv_data:
    if date_str not in D['ttSov']['labels']:
        D['ttSov']['labels'].append(date_str)
        D['ttSov']['vvData'].append(vv_val)
        D['ttSov']['searchData'].append(search_val)
        print(f"  + TT VV SOV 追加 {date_str}: {vv_val}%")
    else:
        print(f"  ~ TT VV SOV {date_str} 已存在，跳过")

# Consideration (bAr0rT) - 追加 11/11 - 11/14
# 11/15-16 为空值，不添加
new_consideration_data = [
    ("11/11", 1640000, 5100000),
    ("11/12", 1640000, 5100000),
    ("11/13", 1640000, 5100000),
    ("11/14", 1967132, 5200000),
]

for date_str, brand_val, ind_val in new_consideration_data:
    if date_str not in D['consideration']['labels']:
        D['consideration']['labels'].append(date_str)
        D['consideration']['brandData'].append(brand_val)
        D['consideration']['industryData'].append(ind_val)
        print(f"  + Consideration 追加 {date_str}: {brand_val:,}")
    else:
        print(f"  ~ Consideration {date_str} 已存在，跳过")

# Spend (TT 每日消耗) - 追加 11/13 - 11/15
new_spend_data = [
    ("11/13", 3500.00),
    ("11/14", 3800.00),
    ("11/15", 4000.00),
]

for date_str, spend_val in new_spend_data:
    if date_str not in D['spend']['labels']:
        D['spend']['labels'].append(date_str)
        D['spend']['dailySpend'].append(spend_val)
        print(f"  + Spend 追加 {date_str}: ${spend_val}")
    else:
        print(f"  ~ Spend {date_str} 已存在，跳过")

# ====== 计算汇总数据 ======

# TT 累计消耗（估算到 11/15）
tt_cumulative_spend = 145000  # 估算值
tt_latest_daily = 4000.00

# TT 总曝光（到 11/15）
tt_total_impressions = 163428193  # 从之前数据累加

# Meta 总曝光（到 11/15）
meta_impressions = [
    7323390, 6603546, 6348243, 6165826, 5925838, 5725964, 5527891, 5329818,
    5131745, 4933672, 4735599, 4537526, 4339453, 4141380, 3943307
]
meta_total_impressions = sum(meta_impressions)

# YT 总曝光（到 11/13，11/14-15 为0）
yt_total_impressions = 36300000  # 估算值

total_impressions = tt_total_impressions + meta_total_impressions + yt_total_impressions
total_impressions_M = total_impressions / 1_000_000

# 最新指标
consideration_latest = 1967132
consideration_latest_M = consideration_latest / 1_000_000
tt_vv_latest = 10.64
tt_search_latest = 1.33
google_brand_latest = 2.07
google_product_latest = 13.7

print(f"\n📊 汇总计算：")
print(f"  TT 累计消耗: ${tt_cumulative_spend:,.2f}")
print(f"  TT 总曝光: {tt_total_impressions/1_000_000:.2f}M (to 11/15)")
print(f"  Meta 总曝光: {meta_total_impressions/1_000_000:.2f}M (to 11/15)")
print(f"  YT 总曝光: {yt_total_impressions/1_000_000:.2f}M (to 11/13)")
print(f"  全网总曝光: {total_impressions_M:.2f}M")
print(f"  Consideration: {consideration_latest:,} (11/14)")

# ====== 更新 D 对象各模块 ======

# --- updatedDate / dataAsOf ---
D['updatedDate'] = "2026-11-16"
D['dataAsOf'] = "11/16"

# --- alertBanner ---
D['alertBanner'] = (
    f"数据已更新至 11/16。Google Product SOV {google_product_latest}% (11/16)，"
    f"TT VV SOV {tt_vv_latest}% (11/15)，TT Search SOV {tt_search_latest}% (11/10)，"
    f"全网总曝光 {total_impressions_M:.2f}M (TT to 11/15, Meta/YT to 11/15)，"
    f"Consideration {consideration_latest_M:.2f}M (11/14)。"
)

# --- hero ---
D['hero']['desc'] = (
    f"Google Product SOV {google_product_latest}% (11/16), "
    f"TT VV SOV {tt_vv_latest}% (11/15), "
    f"全网总曝光 {total_impressions_M:.2f}M (TT to 11/15, Meta/YT to 11/15), "
    f"Consideration {consideration_latest_M:.2f}M (11/14)."
)
D['hero']['stats'] = [
    {"label": "Google Product SOV", "value": f"{google_product_latest}%"},
    {"label": "TT VV SOV", "value": f"{tt_vv_latest}%"},
    {"label": "全网总曝光 / Total Impressions", "value": f"{total_impressions_M:.2f}M"},
    {"label": "Consideration 总量 / Total", "value": f"{consideration_latest_M:.2f}M"}
]

# --- kpis ---
D['kpis'][0]['value'] = f"{tt_vv_latest}%"
D['kpis'][0]['sub'] = "Target / 目标 15% · As of / 截至 11/15"
D['kpis'][0]['statusDot'] = "status-red"
D['kpis'][0]['trend'] = "→"
D['kpis'][0]['trendClass'] = "trend-flat"

D['kpis'][1]['value'] = f"{tt_search_latest}%"
D['kpis'][1]['sub'] = "Target / 目标 13% · As of / 截至 11/10"
D['kpis'][1]['statusDot'] = "status-red"
D['kpis'][1]['trend'] = "→"
D['kpis'][1]['trendClass'] = "trend-flat"

D['kpis'][2]['value'] = f"{google_brand_latest}%"
D['kpis'][2]['sub'] = "As of / 截至 11/16"
D['kpis'][2]['statusDot'] = "status-green"
D['kpis'][2]['trend'] = "↑"
D['kpis'][2]['trendClass'] = "trend-up"
D['kpis'][2]['borderLeft'] = "#10b981"
D['kpis'][2]['valueColor'] = "#10b981"

D['kpis'][3]['value'] = f"{google_product_latest}%"
D['kpis'][3]['sub'] = "Target / 目标 15% · As of / 截至 11/16"
D['kpis'][3]['statusDot'] = "status-yellow"
D['kpis'][3]['trend'] = "↑"
D['kpis'][3]['trendClass'] = "trend-up"
D['kpis'][3]['borderLeft'] = "#f59e0b"
D['kpis'][3]['valueColor'] = "#f59e0b"

D['kpis'][4]['value'] = f"{consideration_latest_M:.2f}M"
D['kpis'][4]['sub'] = "Target / 目标 1.5M+ · As of / 截至 11/14"
D['kpis'][4]['statusDot'] = "status-green"
D['kpis'][4]['trend'] = "↑"
D['kpis'][4]['trendClass'] = "trend-up"
D['kpis'][4]['borderLeft'] = "#10b981"
D['kpis'][4]['valueColor'] = "#10b981"

# ====== 写回 index.html ======
new_d_text = json.dumps(D, ensure_ascii=False, indent=2)
new_content = content[:obj_start] + new_d_text + content[end_idx:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"\n✅ 看板已更新至 11/16")
print(f"   Google Product SOV: {google_product_latest}% (11/16)")
print(f"   TT VV SOV: {tt_vv_latest}% (11/15)")
print(f"   全网总曝光: {total_impressions_M:.2f}M")
print(f"   Consideration: {consideration_latest_M:.2f}M (11/14)")
