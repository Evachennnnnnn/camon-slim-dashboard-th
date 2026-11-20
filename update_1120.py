#!/usr/bin/env python3
"""
泰国 CAMON Slim 看板更新脚本 - 2026-11-20
更新日更模块至最新数据，保留周更模块不动
"""
import json
import sys
import subprocess

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

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
D = json.loads(d_text)
print(f"✅ 成功解析 D 对象，当前 updatedDate: {D['updatedDate']}")

# 保存周更模块
saved_audience = json.loads(json.dumps(D.get('audience', {})))
saved_keywords = json.loads(json.dumps(D.get('keywords', {})))
saved_paidComments = json.loads(json.dumps(D.get('paidComments', {})))

# ====== 新增数据 ======

# --- Google SOV: 追加 11/20 ---
if '11/20' not in D['googleSov']['labels']:
    D['googleSov']['labels'].append('11/20')
    D['googleSov']['brand'].append(2.11)
    D['googleSov']['product'].append(11.23)
    D['competitorCompare']['chartLabels'].append('11/20')
    D['competitorCompare']['datasets'][0]['data'].append(11.23)
    print(f"  + Google SOV 追加 11/20: Brand 2.11%, Product 11.23%")

# --- TT VV SOV: 更新 11/17 (null → 7.81/1.43)，追加 11/19 ---
idx_1117 = D['ttSov']['labels'].index('11/17') if '11/17' in D['ttSov']['labels'] else -1
if idx_1117 >= 0 and D['ttSov']['vvData'][idx_1117] is None:
    D['ttSov']['vvData'][idx_1117] = 7.81
    D['ttSov']['searchData'][idx_1117] = 1.43
    print(f"  ~ TT SOV 11/17 更新: VV 7.81%, Search 1.43%")

# 11/18 已有 label 但 null，检查是否需要更新（源表 11/18 曝光为空但有 search SOV 1.44%）
idx_1118 = D['ttSov']['labels'].index('11/18') if '11/18' in D['ttSov']['labels'] else -1
if idx_1118 >= 0:
    # 11/18 VV SOV 源表空，但 Search SOV = 1.44%
    D['ttSov']['searchData'][idx_1118] = 1.44
    print(f"  ~ TT SOV 11/18 更新: Search 1.44% (VV 仍空)")

if '11/19' not in D['ttSov']['labels']:
    D['ttSov']['labels'].append('11/19')
    D['ttSov']['vvData'].append(None)
    D['ttSov']['searchData'].append(None)
    print(f"  + TT SOV 追加 11/19 (null)")

# --- Consideration: 追加 11/17 ---
if '11/17' not in D['consideration']['labels']:
    D['consideration']['labels'].append('11/17')
    D['consideration']['brandData'].append(1956325)
    D['consideration']['industryData'].append(5357421)
    # Rate = 1956325 / 6650049 * 100 = 29.42%
    rate_1117 = round(1956325 / 6650049 * 100, 2)
    D['consideration']['rateData'].append(rate_1117)
    D['consideration']['rateLabels'].append('11/17')
    D['consideration']['latestRate'] = rate_1117
    print(f"  + Consideration 追加 11/17: {1956325:,}, Rate {rate_1117}%")

# --- Spend: 追加 11/19 ---
if '11/19' not in D['spend']['labels']:
    D['spend']['labels'].append('11/19')
    D['spend']['dailySpend'].append(4171.66)
    D['spend']['spendProgress'].append(0.954260658682635)
    D['spend']['exposureProgress'].append(None)
    print(f"  + Spend 追加 11/19: $4,171.66")

# ====== 计算汇总 ======

# TT 累计消耗
tt_cumulative_spend = sum(D['spend']['dailySpend'])

# TT 总曝光（to 11/17）
tt_daily_impressions = [
    417245, 512731, 1058612, 1980509, 2304924, 4160130, 4104540, 5142215,
    4945262, 4493444, 6665384, 8508983, 7978743, 5313511, 7226108, 10589341,
    16758489, 10552314, 19134836, 23463392, 45831076, 18704152, 16891273,
    10283289, 12229637, 13019465, 16368239, 18172809, 18165959, 13596202,
    4778124, 6650049
]
tt_total_impressions = sum(tt_daily_impressions)

# Meta 总曝光（to 11/19）
meta_daily_impressions = [
    389920, 1324958, 1615904, 2791710, 2432241, 3800623, 4061030, 4418270,
    3907302, 3967229, 4332156, 4024103, 5026959, 3616780, 6556499, 7312020,
    8654870, 16037402, 4933802, 5375550, 5602967, 2470857, 3465317, 4437635,
    5746827, 7219537, 7447018, 7323390, 4828489, 5179382, 2942154, 2826615
]
meta_total_impressions = sum(meta_daily_impressions)

meta_daily_spend = [
    97.75, 356.71, 452.02, 825.58, 734.54, 1182.44, 1270.40, 1308.64,
    1130.95, 1163.58, 1345.65, 1332.71, 1706.00, 1027.78, 2621.93,
    1957.93, 2430.58, 4965.62, 1538.29, 1785.03, 1851.15, 897.50,
    1521.91, 2016.61, 2454.91, 2786.62, 2845.16, 2738.24, 1723.95,
    2194.13, 1422.44, 1427.91
]
meta_cumulative_spend = sum(meta_daily_spend)

# YT 总曝光（to 11/19）
yt_daily_impressions = [
    0, 0, 0, 0, 0, 0, 0, 0, 0,
    67031, 1454760, 1763049, 1670956, 1713798, 1573422,
    0, 1303401, 5173269, 5780003, 5292973, 5367570, 5122405,
    14572, 85893, 112207, 111709, 113383, 0, 0, 0,
    60787, 135490, 127894
]
yt_total_impressions = sum(yt_daily_impressions)

yt_daily_spend = [
    0, 0, 0, 0, 0, 0, 0, 0, 0,
    19.04, 562.88, 727.83, 726.62, 731.30, 728.40,
    0, 308.96, 1156.25, 1154.06, 1146.32, 1164.67, 1165.35,
    13.82, 46.57, 46.61, 46.44, 46.57, 0, 0, 0,
    84.97, 143.74, 147.72
]
yt_cumulative_spend = sum(yt_daily_spend)

total_impressions = tt_total_impressions + meta_total_impressions + yt_total_impressions
total_impressions_M = total_impressions / 1_000_000

# 最新指标
google_brand_latest = 2.11
google_product_latest = 11.23
tt_vv_latest = 7.81   # 11/17
tt_search_latest = 1.44  # 11/18
consideration_latest = 1956325
consideration_latest_M = consideration_latest / 1_000_000
consideration_rate_latest = round(1956325 / 6650049 * 100, 2)

print(f"\n📊 汇总计算：")
print(f"  TT 累计消耗: ${tt_cumulative_spend:,.2f}")
print(f"  TT 总曝光: {tt_total_impressions/1_000_000:.2f}M (to 11/17)")
print(f"  Meta 累计消耗: ${meta_cumulative_spend:,.2f}")
print(f"  Meta 总曝光: {meta_total_impressions/1_000_000:.2f}M (to 11/19)")
print(f"  YT 累计消耗: ${yt_cumulative_spend:,.2f}")
print(f"  YT 总曝光: {yt_total_impressions/1_000_000:.2f}M (to 11/19)")
print(f"  全网总曝光: {total_impressions_M:.2f}M")
print(f"  Consideration: {consideration_latest:,} (11/17)")
print(f"  Consideration Rate: {consideration_rate_latest}%")

# ====== 更新 D 对象 ======

D['updatedDate'] = "2026-11-20"
D['dataAsOf'] = "11/20"

D['alertBanner'] = (
    f"数据更新至 11/20：Google Product SOV {google_product_latest}% (11/20)，"
    f"TT VV SOV {tt_vv_latest}% (11/17)，TT Search SOV {tt_search_latest}% (11/18)，"
    f"全网总曝光 {total_impressions_M:.2f}M，"
    f"Consideration {consideration_latest_M:.2f}M (11/17)，"
    f"挑战赛 14天 3,624 视频已超 POVA 8 Benchmark。"
)

D['hero']['desc'] = (
    f"Google Product SOV {google_product_latest}% (11/20), "
    f"TT VV SOV {tt_vv_latest}% (11/17), "
    f"全网总曝光 {total_impressions_M:.2f}M, "
    f"Consideration {consideration_latest_M:.2f}M (11/17)."
)
D['hero']['stats'] = [
    {"label": "Google Product SOV", "value": f"{google_product_latest}%"},
    {"label": "TikTok VV SOV", "value": f"{tt_vv_latest}%"},
    {"label": "TikTok Search SOV", "value": f"{tt_search_latest}%"},
    {"label": "Consideration", "value": f"{consideration_latest_M:.2f}M"}
]

# KPIs
D['kpis'][0]['value'] = f"{tt_vv_latest}%"
D['kpis'][0]['sub'] = "Target / 目标 15% · As of / 截至 11/17"
D['kpis'][0]['statusDot'] = "status-red"
D['kpis'][0]['trend'] = "↓"
D['kpis'][0]['trendClass'] = "trend-down"

D['kpis'][1]['value'] = f"{consideration_rate_latest}%"
D['kpis'][1]['sub'] = f"Consideration / TECNO曝光 · As of / 截至 11/17"
D['kpis'][1]['statusDot'] = "status-green"
D['kpis'][1]['trend'] = "→"
D['kpis'][1]['trendClass'] = "trend-flat"
D['kpis'][1]['borderLeft'] = "#10b981"
D['kpis'][1]['valueColor'] = "#10b981"

D['kpis'][2]['value'] = f"{total_impressions_M:.2f}M"
D['kpis'][2]['sub'] = f"TT {tt_total_impressions/1_000_000:.2f}M + Meta {meta_total_impressions/1_000_000:.2f}M + YT {yt_total_impressions/1_000_000:.2f}M"
D['kpis'][2]['statusDot'] = "status-green"
D['kpis'][2]['trend'] = "↑"
D['kpis'][2]['trendClass'] = "trend-up"
D['kpis'][2]['borderLeft'] = "#10b981"
D['kpis'][2]['valueColor'] = "#10b981"

D['kpis'][3]['value'] = "12.1M"
D['kpis'][3]['sub'] = "14天 · 超 POVA 8 Benchmark 5.8M"
D['kpis'][3]['statusDot'] = "status-green"
D['kpis'][3]['trend'] = "↑"
D['kpis'][3]['trendClass'] = "trend-up"
D['kpis'][3]['borderLeft'] = "#10b981"
D['kpis'][3]['valueColor'] = "#10b981"

# Challenge: 14天
D['challenge']['camonSlim']['period'] = "14天 / 14 Days"
D['challenge']['camonSlim']['videos'] = "3,624"
D['challenge']['camonSlim']['creators'] = "2,226"
D['challenge']['camonSlim']['views'] = "12.1M"
D['challenge']['camonSlim']['engagementRate'] = 0.0514
D['challenge']['camonSlim']['likes'] = "490.8K"
D['challenge']['camonSlim']['comments'] = "16.2K"
D['challenge']['camonSlim']['shares'] = "80.3K"
D['challenge']['camonSlim']['filters'] = "19.4K"

D['challenge']['stats'][0]['value'] = "3,624"
D['challenge']['stats'][1]['value'] = "19.4K"
D['challenge']['stats'][2]['value'] = "12.1M"
D['challenge']['stats'][3]['value'] = "5.14%"

D['challenge']['insights'][0]['items'] = [
    'CAMON Slim 14天 = POVA 8 14天，同周期直接对比',
    '视频提交量 3,624 vs 2,220（+63%），参与达人 2,226 vs 1,452（+53%）',
    '总播放 12.1M vs 5.8M（+109%），互动率 5.14% vs 3.34%（+54%）'
]
D['challenge']['insights'][1]['items'] = [
    '日均视频：259/天 vs 159/天（1.63倍）',
    '日均播放：0.86M/天 vs 0.41M/天（2.1倍）',
    '滤镜使用 19.4K vs 17K，同周期已超 POVA 8'
]

# Overview
D['overview'][0]['current'] = f"{google_brand_latest}%"
D['overview'][0]['date'] = "11/20"
D['overview'][1]['current'] = f"{google_product_latest}%"
D['overview'][1]['date'] = "11/20"
D['overview'][2]['current'] = f"{tt_vv_latest}%"
D['overview'][2]['date'] = "11/17"
D['overview'][3]['current'] = f"{tt_search_latest}%"
D['overview'][3]['date'] = "11/18"
D['overview'][4]['current'] = f"${tt_cumulative_spend:,.2f} cumulative"
D['overview'][4]['date'] = "11/19"
D['overview'][5]['current'] = f"${meta_cumulative_spend:,.2f} cumulative"
D['overview'][5]['date'] = "11/19"
D['overview'][6]['current'] = f"{meta_total_impressions/1e6:.2f}M cumulative"
D['overview'][6]['date'] = "11/19"
D['overview'][7]['current'] = f"{consideration_latest_M:.2f}M"
D['overview'][7]['date'] = "11/17"
D['overview'][8]['current'] = f"{consideration_rate_latest}%"
D['overview'][8]['date'] = "11/17"

# Notes
D['googleSov']['brandNote'] = f'Brand SOV latest {google_brand_latest}% (11/20) / 品牌 SOV 最新 {google_brand_latest}%（11/20）'
D['googleSov']['productNote'] = f'Product SOV latest {google_product_latest}% (11/20) / 产品 SOV 最新 {google_product_latest}%（11/20）'

D['competitorCompare']['note'] = f'Google Trends 对比关键词 / Comparison: CAMON Slim vs OPPO Reno 16 F, VIVO V80 Lite, Redmi Note 17 Pro · 截至 11/20'
prev_product = 13.09  # 11/19
trend_dir = "↑" if google_product_latest > prev_product else "↓"
trend_class = "trend-up" if google_product_latest > prev_product else "trend-down"
D['competitorCompare']['table'][0]['sov'] = f'{google_product_latest}%'
D['competitorCompare']['table'][0]['trend'] = trend_dir
D['competitorCompare']['table'][0]['trendClass'] = trend_class
D['competitorCompare']['insight'] = f'💡 竞品对比组合：CAMON Slim vs OPPO Reno 16 F / VIVO V80 Lite / Redmi Note 17 Pro。CAMON Slim 产品 SOV 最新 {google_product_latest}%（11/20），较昨日 {prev_product}% {trend_dir}。竞品数据来自 Google Trends 相对搜索热度。/ Product SOV latest {google_product_latest}% (11/20).'

D['ttSov']['note'] = f'VV SOV latest {tt_vv_latest}% (11/17); Search SOV latest {tt_search_latest}% (11/18). / TikTok声量最新数据 VV 到11/17，Search 到11/18'

D['consideration']['note'] = f'Brand Consideration latest {consideration_latest_M:.2f}M (11/17). / 本品牌 Consideration 最新 {consideration_latest_M:.2f}M（11/17）。'
D['consideration']['rateNote'] = f'Consideration Rate = Consideration / TECNO总曝光，最新 {consideration_rate_latest}% (11/17)'

# 恢复周更模块
D['audience'] = saved_audience
D['keywords'] = saved_keywords
D['paidComments'] = saved_paidComments

# ====== 验证 ======
print("\n--- Array Validation ---")
print(f"Google SOV: labels={len(D['googleSov']['labels'])}, brand={len(D['googleSov']['brand'])}, product={len(D['googleSov']['product'])}")
assert len(D['googleSov']['labels']) == len(D['googleSov']['brand']) == len(D['googleSov']['product']), "Google SOV mismatch!"

print(f"Competitor: labels={len(D['competitorCompare']['chartLabels'])}, data={len(D['competitorCompare']['datasets'][0]['data'])}")
assert len(D['competitorCompare']['chartLabels']) == len(D['competitorCompare']['datasets'][0]['data']), "Competitor mismatch!"

print(f"TT SOV: labels={len(D['ttSov']['labels'])}, vv={len(D['ttSov']['vvData'])}, search={len(D['ttSov']['searchData'])}")
assert len(D['ttSov']['labels']) == len(D['ttSov']['vvData']) == len(D['ttSov']['searchData']), "TT SOV mismatch!"

print(f"Spend: labels={len(D['spend']['labels'])}, daily={len(D['spend']['dailySpend'])}, progress={len(D['spend']['spendProgress'])}, exposure={len(D['spend']['exposureProgress'])}")
assert len(D['spend']['labels']) == len(D['spend']['dailySpend']) == len(D['spend']['spendProgress']) == len(D['spend']['exposureProgress']), "Spend mismatch!"

print(f"Consideration: labels={len(D['consideration']['labels'])}, brand={len(D['consideration']['brandData'])}, industry={len(D['consideration']['industryData'])}")
assert len(D['consideration']['labels']) == len(D['consideration']['brandData']) == len(D['consideration']['industryData']), "Consideration mismatch!"

print(f"Consideration Rate: labels={len(D['consideration']['rateLabels'])}, data={len(D['consideration']['rateData'])}")
assert len(D['consideration']['rateLabels']) == len(D['consideration']['rateData']), "Consideration Rate mismatch!"

print("✅ All array lengths match!")

# 写回
new_d_text = json.dumps(D, ensure_ascii=False, indent=2)
new_content = content[:obj_start] + new_d_text + content[end_idx:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"\n✅ Dashboard updated to 11/20")
print(f"   Google Product SOV: {google_product_latest}% (11/20)")
print(f"   TT VV SOV: {tt_vv_latest}% (11/17)")
print(f"   TT Search SOV: {tt_search_latest}% (11/18)")
print(f"   全网总曝光: {total_impressions_M:.2f}M")
print(f"   Consideration: {consideration_latest_M:.2f}M (11/17)")
print(f"   Challenge: 14天, {D['challenge']['camonSlim']['videos']} videos, {D['challenge']['camonSlim']['views']} views")

# JS VALIDATION
validate_js = '''
const fs = require("fs");
const html = fs.readFileSync("index.html", "utf8");
const m = html.match(/const D = (\\{[\\s\\S]*?\\n\\})\\n/);
if(!m) { console.log("ERROR: no D match"); process.exit(1); }
try {
    const D = JSON.parse(m[1]);
    console.log("✅ JS parse OK: " + Object.keys(D).length + " keys");
    console.log("   googleSov: " + D.googleSov.labels.length + " dates");
    console.log("   ttSov: " + D.ttSov.labels.length + " dates");
    console.log("   spend: " + D.spend.labels.length + " dates");
    console.log("   competitor: " + D.competitorCompare.chartLabels.length + " dates");
    console.log("   consideration: " + D.consideration.labels.length + " dates");
    console.log("   challenge videos: " + D.challenge.camonSlim.videos);
    console.log("   challenge views: " + D.challenge.camonSlim.views);
    console.log("   kpis: " + D.kpis.length + " items");
    console.log("   overview: " + D.overview.length + " rows");
    console.log("   audience: " + (D.audience ? "present" : "MISSING"));
    console.log("   keywords: " + (D.keywords ? "present" : "MISSING"));
    console.log("   paidComments: " + (D.paidComments ? "present" : "MISSING"));
    console.log("\\n🎉 All validations passed!");
} catch(e) {
    console.log("❌ PARSE ERROR: " + e.message);
    process.exit(1);
}
'''

result = subprocess.run(['node', '-e', validate_js], capture_output=True, text=True)
print(f"\n--- Final JS Validation ---")
print(result.stdout)
if result.returncode != 0:
    print("STDERR:", result.stderr)
    sys.exit(1)
